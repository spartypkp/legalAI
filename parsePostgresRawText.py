from utilityFunctions import num_tokens_from_string as calc
import json
import re
import sys, os
import utilityFunctions as util

def main():
    extract_all_definitions()
    update_header_content()
    update_header_definitions()


def extract_all_definitions():
    # List content embeddings to be redone
    sql_select = "SELECT id, str_key, content FROM ca_code WHERE content ILIKE '%following definitions%' AND section NOT ILIKE '%Header%' OR section IS NULL ORDER BY id;"
    conn = util.psql_connect()
    rows = util.select_and_fetch_rows(conn, sql_select)

    with open("nestedHeaderDict.txt", "r") as header_file:
        text = header_file.read()
        header_dct = json.loads(text)
    header_file.close()

    content_to_update = {}
    definitions_to_update = {}
    failed_to_extract = {}

    for row in rows:
        id = row[0]
        str_key = row[1]
        content = row[2]
        print("id:{}, str_key:{}".format(id, str_key))
        try:
            newText, definitions, category = remove_definitions_from_str(content)
            content_to_update[id] = newText
        except:
            print("FAILED EXTRACTION: ", str_key)
            failed_to_extract[id] = content
            continue
        code, division, title, part, chapter, article, section = str_key.split("#")
        if category == "title":
            header_dct[code][0][title][4].append(definitions)
        elif category == "division":
            header_dct[code][0][title][0][division][4].append(definitions)
        elif category == "part":
            header_dct[code][0][title][0][division][0][part][4].append(definitions)
        elif category == "chapter":
            header_dct[code][0][title][0][division][0][part][0][chapter][4].append(definitions)
        elif category == "article":
            header_dct[code][0][title][0][division][0][part][0][chapter][0][article][4].extend(definitions)
            header_dct[code][0][title][0][division][0][part][0][chapter][0][article][0] = str_key
        else:
            # Update section definitions
            definitions_to_update[id] = definitions

    with open("failedExtraction.txt", "w") as fail_file:
        fail_file.write(json.dumps(failed_to_extract))
    fail_file.close()
    with open("nestedHeaderDict.txt", "w") as header_file:
        header_file.write(json.dumps(header_dct))
    header_file.close()
    with open("contentUpdate.txt","w") as content_file:
        content_file.write(json.dumps(content_to_update))
    content_file.close()
    with open("definitionsUpdate.txt","w") as definition_file:
        definition_file.write(json.dumps(definitions_to_update))
    definition_file.close()

def update_header_definitions():
    conn = util.psql_connect()
    with open("definitionsUpdate.txt","r") as definition_file:
        text = definition_file.read()
        definitions_to_update = json.loads(text)
    definition_file.close()

    cursor = conn.cursor()
    for k,v in definitions_to_update.items():
        if "'" in v:
            v = v.replace("'", "''")
        sql = "UPDATE ca_code SET definitions='{}' WHERE id={};".format(v, int(k))
        cursor.execute(sql)
    conn.commit()
    conn.close()

def update_header_content():
    conn = util.psql_connect()
    with open("contentUpdate.txt","r") as content_file:
        text = content_file.read()
        content_to_update = json.loads(text)
    content_file.close()

    cursor = conn.cursor()
    for k,v in content_to_update.items():
        print("Key: {}, Value: {}".format(k, v))
        if v is None:
            v = ""
        if "'" in v:
            v = v.replace("'", "''")
        sql = "UPDATE ca_code SET content='{}' WHERE id={};".format(v, int(k))
        cursor.execute(sql)
    conn.commit()
    conn.close()

def remove_definitions_from_str(test_str):
    target = "following definitions"
    # 1. find start index of 'following definitions'
    i  = test_str.index(target)
    # 2. Set some initial values
    prev_section_index = 0
    next_subsection_index = test_str.index("(", i)
    category = None
    definitions = ""
    
    try:
        # Try and find the last subsection
        prev_section_index = test_str.rindex(")", 0, i)
        prev_id = test_str[prev_section_index-1]  #'h'
        prev_section_index -= 2

         # Find the next subsection using ord()+1
        next_id = chr(ord(prev_id)+1)
        
        end_of_definitions = "({})\xa0".format(next_id)
        end_definition_index = test_str.index(end_of_definitions, i, len(test_str))
        definitions = test_str[next_subsection_index:end_definition_index]

        newText = test_str[0:prev_section_index] + test_str[end_definition_index:]
    except:
        newText = None
        definitions = test_str
        
    text_to_search = test_str[prev_section_index:next_subsection_index]
    if "division" in text_to_search:
        category = "division"
    elif "title" in text_to_search:
        category = "title"
    elif "part" in text_to_search:
        category = "part"
    elif "chapter" in text_to_search:
        category = "chapter"
    elif "article" in text_to_search:
        category = "article"
    else:
        category = "section"

    return newText, definitions, category

# Extract all header data, previously extractHeaders.py
def extractHeaders():
    header_dct = {}
    cleaned_text = {}
    conn = util.psql_connect()
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
    code, division, title, part, chapter, article = row[1:7]
    # Range_dct: {Key: "division": [title, (range tup)]}
    # header_dct:  {Key "BPC": [{} Subtrees, Title, Tup:(Range start, range end), [definitions], "floor tag"]}
    if code not in header_dct:
        header_dct[code] = [{}, None, None, [], "code"]
    # A default dict would be so much better here but I am stubborn
    if title not in header_dct[code][0]:
        header_dct[code][0][title] = [{}, None, None, [], "title"]
    if "title" in range_dict and header_dct[code][0][title][1] is None:
        header_dct[code][0][title][1] = range_dict["title"][0]
        header_dct[code][0][title][2] = tuple(range_dict["title"][1][0],range_dict["title"][1][1])
    
    if division not in header_dct[code][0][title][0]:
        header_dct[code][0][title][0][division] = [{}, None, None, [], "division"]
    if "division" in range_dict and header_dct[code][0][title][0][division][1] is None:
        header_dct[code][0][title][0][division][1] = range_dict["division"][0]
        header_dct[code][0][title][0][division][2] = tuple(range_dict["division"][1][0],range_dict["division"][1][1])

    if part not in header_dct[code][0][title][0][division][0]:
        header_dct[code][0][title][0][division][0][part] = [{}, None, None, [], "part"]
    if "part" in range_dict and header_dct[code][0][title][0][division][0][part][1] is None:
        header_dct[code][0][title][0][division][0][part][1] = range_dict["part"][0]
        header_dct[code][0][title][0][division][0][part][2] = tuple(range_dict["part"][1][0],range_dict["part"][1][1])
    # This is getting ridculous
    if chapter not in header_dct[code][0][title][0][division][0][part][0]:
        header_dct[code][0][title][0][division][0][part][0][chapter] = [{}, None, None, [], "chapter"]
    if "chapter" in range_dict and header_dct[code][0][title][0][division][0][part][0][chapter][1] is None:
        header_dct[code][0][title][0][division][0][part][0][chapter][1] = range_dict["chapter"][0]
        header_dct[code][0][title][0][division][0][part][0][chapter][2] = tuple(range_dict["chapter"][1][0],range_dict["chapter"][1][1])
    # Fuck my life
    if article not in header_dct[code][0][title][0][division][0][part][0][chapter][0]:
        header_dct[code][0][title][0][division][0][part][0][chapter][0][article] = [None, None, [], "article"]
    if "article" in range_dict and header_dct[code][0][title][0][division][0][part][0][chapter][0][article][1] is None:
        header_dct[code][0][title][0][division][0][part][0][chapter][0][article][0] = range_dict["article"][0]
        header_dct[code][0][title][0][division][0][part][0][chapter][0][article][1] = tuple(range_dict["article"][1][0],range_dict["article"][1][1])

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

        range_dict[key] = [title, (range_start, range_end)]
        start = second_index
        first_index = text.find("[", second_index)

    new_text = ""
    start = 0

    for pair in indexes:
        new_text += text[start:pair[0]]
        start = pair[1]+1
    new_text += text[start:]
    return range_dict, new_text


# Traverse local header Tree dictionary, previously headerTreeTraversals.py
def headerTreeTraversals():
    
    with open("nestedHeaderDict.txt", "r") as header_file:
        text = header_file.read()
        header_dct = json.loads(text)
    header_file.close()
    
    all_headers = [header_dct, "ROOT", "0", "INF", "", "ROOT"]
    all_headers = header_dct["WIC"]
    #print(type(all_headers[0])==dict)
    traverse_titles_and_definitions("WIC", all_headers, "", "", "")

def traverse_titles_and_definitions(key, header_dct_values, def_str, path, titles):
    if header_dct_values[4] != "":
        def_str = def_str + ", " + header_dct_values[4]
    
    if header_dct_values[1] != "ROOT":
        currentPath = "{}='{}' AND ".format(header_dct_values[5], key)
        
        path += currentPath
        if header_dct_values[1] is not None:
            titles = titles + ", " + header_dct_values[1]
    
    if type(header_dct_values[0]) != dict or header_dct_values[5] == "article":
        path = path[0:len(path)-5]+";"
        updateAllSectionsForArticle(def_str, path, titles)
        return
    
    for k,v in header_dct_values[0].items():
        traverse_titles_and_definitions(k, v, def_str, path, titles)

def updateAllSectionsForArticle(def_str, path, titles):
    titles, def_str = titles.strip(","), def_str.strip(",")
    if "'" in titles:
        titles = titles.replace("'", "''")
    if "'" in def_str:
        def_str = def_str.replace("'", "''")
    conn = util.psql_connect()
    cursor = conn.cursor()
    sql_select = "SELECT id, definitions FROM ca_code WHERE {}".format(path)
    print(sql_select)
    rows = util.select_and_fetch_rows(conn, sql_select)
    for tup in rows:
        id = int(tup[0])
        old_def = tup[1]
        
        if def_str == "":
            def_str = " "
        if old_def is None or old_def == "":
            old_def = " "
        if "'" in old_def:
            old_def = old_def.replace("'","''")
        new_def = def_str + ", " + old_def
        new_def = new_def.strip(", ")
        sql_update = "UPDATE ca_code set title_path='{}', definitions='{}' WHERE id='{}';".format(titles, new_def, id)
        cursor.execute(sql_update)
    conn.commit()
    conn.close()

# Update all rows that have cleaned header text, previously analyzeHeders.py
def analyzeHeaders():
    update_all_header_content()

def get_all_sections_for_article(conn, sql_select):
    cursor = conn.cursor()
    cursor.execute(sql_select)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def update_all_header_content(conn):
    with open("cleanedRowsToUpdate.txt", "r") as cleaned_file:
        text = cleaned_file.read()
        clean_dict = json.loads(text)
    cleaned_file.close()
    cursor = conn.cursor()
    for k,v in clean_dict.items():
        print("Key: {}, Value: {}".format(k, v))
        if "'" in v:
            v = v.replace("'", "''")
            print(v)
        sql = "UPDATE ca_code SET content='{}' WHERE id={};".format(v, int(k))
        cursor.execute(sql)
    conn.commit()
    conn.close()



if __name__ == "__main__":
    main()