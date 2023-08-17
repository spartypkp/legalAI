import warnings
from bs4 import BeautifulSoup
import os
import urllib.request
import requests
import json
import re
import calculateTokens
import psycopg2

CODE_SELECTION = "https://leginfo.legislature.ca.gov/faces/codes.xhtml"
FULL_PATH =  "https://leginfo.legislature.ca.gov"


DIR = os.path.dirname(os.path.realpath(__file__))
GLOBAL_ID = 0

# Total tokens: 44,132,506
# $4.4 cost total
# 178, 580 unique IDs

def main():
    GLOBAL_ID = get_ID()
    html_scraper()

def html_scraper():
    
    sections = open("sections", "r")
    currentCode = None
    for line in sections:
        if line[0] == "#":
            split = line.split("-")
            currentCode = split[-1].strip()
            print("Starting to scrape all text from California Legal Code: {}".format(currentCode))
        else:
            # Temporary for scraping in chunks
            
            #if currentCode in DONE:
                #continue
            scrape(line, "{}".format(currentCode))

            print("Finishided scraping Code: {}. Started at ID {} , ended at ID {}".format(currentCode, get_ID(), GLOBAL_ID))
            set_ID(GLOBAL_ID)


def scrape(link, fileName):
    
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            dct = scrape_sections_per_code({}, link, fileName)
        with open('{}/scrapedData/{}.txt'.format(DIR, fileName), 'w') as convert_file:
            convert_file.write(json.dumps(dct))
        convert_file.close()
        # Temporary
    except Exception as exc:
        print("Could not scrape articles for code {}".format(fileName))
        print(exc)
        exit(1)


def getHTMLdocument(url):
    # request for HTML document of given url
    response = requests.get(url)
    # response will be provided in JSON format
    return response.text

def extract_article_text(link, code):
    soup = BeautifulSoup("".join(getHTMLdocument(link)), "lxml")
    text = soup.get_text()
    cutIndex = text.find("Code Text")
    newText = text[cutIndex+10:].strip()
    newText = newText[0:len(newText)-10]
    firstIndex = newText.find("- {}".format(code)) + len(code) + 2
    lastIndex = newText.rfind("{}".format(code), len(newText)-50)
    newText = newText[firstIndex:lastIndex]
    return newText

def scrape_sections_per_code(dct, current, code):

    soup = BeautifulSoup("".join(getHTMLdocument(current)), "lxml")
    # Key: Int - unique id, Value: List: sectionTags
    # [ID: 0, Code: 1, Division: 2, Title: 3, Part:4, Chapter: 5, Article: 6, Section: 7,
    #  isCodeDescription: 8, text: 9, addendum: 10, embedding: 11, link: 12]
    # 13 length
    sectionTags = ["", code, "", "", "", "", "", "", "", "", "", "", ""]
    for link in soup.find_all('a'):
        path = link.get('href')
        if path is None or "/faces" not in path:
            continue
        else:
            path = "{}{}".format(FULL_PATH, path)
            if "_displayText" in path:
                #print("Scraping path {} for code {}".format(path, code))
                # Get entirety of expanded text
                articleText = extract_article_text(path, code)

                isCodeDescription = get_tags_from_link(path, sectionTags)

                sectionTags[12] = path
                sectionTags[8] = isCodeDescription

                split_sections(dct, sectionTags, articleText)

    return dct

def split_sections(dct, sectionTags, text):
    # [ID: 0, Code: 1, Division: 2, Title: 3, Part:4, Chapter: 5, Article: 6, Section: 7,
    #  isCodeDescription: 8, text: 9, addendum: 10, embedding: 11, link: 12]
    global GLOBAL_ID

    indexes = [m.start() for m in re.finditer('\u00a0\u00a0', text)]
    left = 0
    sectionID = "Header"

    for i in range(1, len(indexes)):
        current_index = indexes[i]
        if text[current_index-1] != ".":
            continue
        else:
            # Find last ")"
            for i in range(current_index-2, 0, -1):
                if text[i] == ")":
                    if sectionID != "Header":
                        sectionText = "{} {}".format(sectionID, text[left:i+1]).strip()
                    else:
                        sectionText = text[left:i+1].strip()
                    left = current_index+2

                    # Find addendum if present
                    addendum_index = get_addendum_index(sectionText)

                    if addendum_index == -1:
                        addendum = ""
                    else:
                        addendum = sectionText[addendum_index:]
                        sectionText = sectionText[0:addendum_index]

                    local_id = GLOBAL_ID
                    localSectionTags = sectionTags.copy()
                    localSectionTags[7] = sectionID
                    localSectionTags[9] = sectionText
                    localSectionTags[10] = addendum
                    localSectionTags[11] = []

                    key = create_key(localSectionTags[1:8])

                    if key in dct.keys():
                        if sectionText == dct[key][9]:
                            return
                        else:
                            newKey = key + "(Cont.)"
                            file = open("duplicateKeys.txt","a")
                            file.write("({},{},{})\n".format(newKey, key, sectionTags[12]))
                            file.close()
                            key = newKey
                            
                    localSectionTags[0] = local_id
                    GLOBAL_ID += 1


                    dct[key] = localSectionTags
                    sectionID = text[i+1:current_index-1]
                    break

    sectionText = "{} {}".format(sectionID, text[left:]).strip()
    addendum_index = get_addendum_index(sectionText)

    if addendum_index == -1:
        addendum = ""
    else:
        addendum = sectionText[addendum_index:]
        sectionText = sectionText[0:addendum_index]

    local_id = GLOBAL_ID
    localSectionTags = sectionTags.copy()
    localSectionTags[7] = sectionID
    localSectionTags[9] = sectionText
    localSectionTags[10] = addendum
    localSectionTags[11] = []

    key = create_key(localSectionTags[1:8])
    
    
    if key in dct.keys():
        if sectionText == dct[key][9]:
            return
        else:
            newKey = key + "(Cont.)"
            file = open("duplicateKeys.txt","a")
            file.write("({},{},{})\n".format(newKey, key, sectionTags[12]))
            file.close()
            key = newKey

    localSectionTags[0] = local_id
    GLOBAL_ID += 1

    dct[key] = localSectionTags


def get_addendum_index(sectionText):
    if sectionText[-1] != ")":
        return -1

    stack = [")"]
    for i in range(len(sectionText)-2, 0, -1):
        if sectionText[i] == ")":
            stack.append(")")
        elif sectionText[i] == "(":
            stack.pop()
            if len(stack) == 0:
                return i
    return -1


def get_tags_from_link(path, sectionTags):
    # [ ID, CONS, Division, Title, Part, Chapter, Article, Section ]
    codeDescription = True
    sections = [x.strip(".") for x in path.split("&")]
    for i in range(2, 7):
        num = sections[i-1].split("=")[1]
        if num != "":
            codeDescription = False
            sectionTags[i] = num
        else:
            sectionTags[i] = "0"

    return codeDescription

def create_key(lst):
    return "{}#{}#{}#{}#{}#{}#{}".format(*lst)

def get_ID():
    with open("id.txt", "r") as get_file:
        ID = int(get_file.read())
    get_file.close()
    return ID

def set_ID(newID):
    with open("id.txt", "w") as set_file:
        set_file.write(str(newID))
    set_file.close()

if __name__ == '__main__':
    main()

