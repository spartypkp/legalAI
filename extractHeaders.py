import os
import getPSQLConn
import psycopg2
import json

def main():
    header_dct = {}
    cleaned_text = {}
    conn = getPSQLConn.connect()
    rows = get_all_rows_with_headers(conn)
    conn.close()
    
    for row in rows:
        row_lst = list(row)
        try:
            newText = remove_all_addendums(row_lst[8])
        except Exception as e:
            print("Failed remove_all_addendums", e)
            print()
            print(row)
            exit(1)
        try:
            range_dict, newText = extract_section_ranges(newText)
        except Exception as e:
            print("Failed extract_section_ranges", e)
            print()
            print(row)
            exit(1)
        row_lst[9] = newText
        cleaned_text[row_lst[0]] = newText
        add_to_header_dictionary(header_dct, row_lst, range_dict)

        
    with open("cleanedRowsToUpdate.txt", "w") as clean_file:
        clean_file.write(json.dumps(cleaned_text))
    clean_file.close()
    with open("nestedHeaderDict.txt", "w") as header_file:
        header_file.write(json.dumps(header_dct))
    header_file.close()
        
    

def add_to_header_dictionary(header_dct, row, range_dict):
    code = row[1]
    division = row[2]
    title = row[3]
    part = row[4]
    chapter = row[5]
    article = row[6]
    #print("Code:{}, {}".format(code, row[9]))

    if code not in header_dct:
        header_dct[code] = [{}, None, None, None, [], "code"]
    # A default dict would be so much better here but I am stubborn
    if title not in header_dct[code][0]:
        header_dct[code][0][title] = [{}, None, None, None, [], "title"]
    if "title" in range_dict and header_dct[code][0][title][1] is None:
        header_dct[code][0][title][1] = range_dict["title"][0]
        header_dct[code][0][title][2] = range_dict["title"][1]
        header_dct[code][0][title][3] = range_dict["title"][2]
    
    if division not in header_dct[code][0][title][0]:
        header_dct[code][0][title][0][division] = [{}, None, None, None, [], "division"]
    if "division" in range_dict and header_dct[code][0][title][0][division][1] is None:
        header_dct[code][0][title][0][division][1] = range_dict["division"][0]
        header_dct[code][0][title][0][division][2] = range_dict["division"][1]
        header_dct[code][0][title][0][division][3] = range_dict["division"][2]

    if part not in header_dct[code][0][title][0][division][0]:
        header_dct[code][0][title][0][division][0][part] = [{}, None, None, None, [], "part"]
    if "part" in range_dict and header_dct[code][0][title][0][division][0][part][1] is None:
        header_dct[code][0][title][0][division][0][part][1] = range_dict["part"][0]
        header_dct[code][0][title][0][division][0][part][2] = range_dict["part"][1]
        header_dct[code][0][title][0][division][0][part][3] = range_dict["part"][2]
    # This is getting ridculous
    if chapter not in header_dct[code][0][title][0][division][0][part][0]:
        header_dct[code][0][title][0][division][0][part][0][chapter] = [{}, None, None, None, [], "chapter"]
    if "chapter" in range_dict and header_dct[code][0][title][0][division][0][part][0][chapter][1] is None:
        header_dct[code][0][title][0][division][0][part][0][chapter][1] = range_dict["chapter"][0]
        header_dct[code][0][title][0][division][0][part][0][chapter][2] = range_dict["chapter"][1]
        header_dct[code][0][title][0][division][0][part][0][chapter][3] = range_dict["chapter"][2]
    # Fuck my life
    if article not in header_dct[code][0][title][0][division][0][part][0][chapter][0]:
        header_dct[code][0][title][0][division][0][part][0][chapter][0][article] = [None, None, None, None, [], "article"]
    if "article" in range_dict and header_dct[code][0][title][0][division][0][part][0][chapter][0][article][1] is None:
        header_dct[code][0][title][0][division][0][part][0][chapter][0][article][1] = range_dict["article"][0]
        header_dct[code][0][title][0][division][0][part][0][chapter][0][article][2] = range_dict["article"][1]
        header_dct[code][0][title][0][division][0][part][0][chapter][0][article][3] = range_dict["article"][2]
    

def get_all_rows_with_headers(conn):
    sql_select = "SELECT id, code, division, title, part, chapter, article, section, content, addendum, link FROM ca_code WHERE section = 'Header' AND is_code_description = 'false' ORDER BY code, id;"
    cursor = conn.cursor()
    cursor.execute(sql_select)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def remove_all_addendums(text):
    first_index = text.find("(")
    indexes = []
    while first_index != -1:
        second_index = text.find(")", first_index)
        indexes.append((first_index, second_index))
        first_index = text.find("(", second_index)
    if indexes == []:
        return text
    new_text = ""
    start = 0
    for pair in indexes:
        new_text += text[start:pair[0]]
        start = pair[1]+1
    new_text += text[start:]
    return new_text

def extract_section_ranges(text):
    
    text = text.replace("[[","[")
    text = text.replace(".]", "")
    text = text.replace("- [", "- ")
    #print()
    #print(text)

    range_dict = {}
    start = 0
    indexes = []
    new_text = text
    
    first_index = text.find("[")
    second_index = len(text)
    while first_index != -1:
        if text.find("]", first_index) == -1:

            break
        key_search = text[start:first_index].lower()
        if "division" in key_search:
            key = "division"
        elif "part" in key_search:
            key = "part"
        elif "title" in key_search:
            key = "title"
        elif "chapter" in key_search:
            key = "chapter"
        else:
            key = "article"

        title_search = text[start:first_index].split(".")
        title = title_search[-1].strip()

        second_index = text.find("]", first_index)
        indexes.append((first_index, second_index))


        range_search = text[first_index+1: second_index]
        range_search = range_search.split("-")
        if len(range_search) == 1:
            start = second_index
            first_index = text.find("[", second_index)
            continue
        
        range_start = range_search[0]
        range_end = range_search[1]

        range_dict[key] = [title, range_start, range_end]
        start = second_index
        first_index = text.find("[", second_index)

    new_text = ""
    start = 0

    for pair in indexes:
        new_text += text[start:pair[0]]
        start = pair[1]+1
    new_text += text[start:]
    return range_dict, new_text


if __name__ == "__main__":
    main()