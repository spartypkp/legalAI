from calculateTokens import num_tokens_from_string as calc
import json
import re
import sys, os
import getPSQLConn as psql

def main():
    extract_all_definitions()
    update_header_content()
    update_header_definitions()


def extract_all_definitions():
    # List content embeddings to be redone
    sql_select = "SELECT id, str_key, content FROM ca_code WHERE content ILIKE '%following definitions%' AND section NOT ILIKE '%Header%' OR section IS NULL ORDER BY id;"
    conn = psql.connect()
    rows = psql.select_and_fetch_rows(conn, sql_select)

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
    conn = psql.connect()
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
    conn = psql.connect()
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



if __name__ == "__main__":
    main()