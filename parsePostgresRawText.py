from utilityFunctions import num_tokens_from_string as calc
import json
import re
import sys, os
import utilityFunctions as util
from interval import interval, inf, imath
import matplotlib.pyplot as plt
import promptStorage as prompts
import openai
CODES = ["CIV","BPC","CCP","COM","CONS","CORP","EDC","ELEC","EVID","FAC","FAM","FGC","FIN","GOV","HNC","HSC","INS","LAB","MVC","PCC","PEN","PRC","PROB","PUC","RTC","SHC","UIC","VEH","WAT","WIC"]
DIR = os.path.dirname(os.path.realpath(__file__))
COUNT = 0

def main():
    # 19,000 keywords found
    # row 9500: 21827 keywords, 34703 definitions
    # 30,000 unique definitions found
    test_remaining_tokens(firstPass=False)
    #test_remaining_tokens()
    #test_definition_dict()
    #reformat_definitions()
    

def reformat_definitions():
    

    with open("definitionWithRanges.txt", "r") as output_file:
        text = output_file.read()
        all_definitions = json.loads(text)
    output_file.close()

    with open("definitionFromSections.txt","r") as input_file:
        text = input_file.read()
        raw_sections = json.loads(text)
    input_file.close()

    with open("referenceDefinitions.txt", "r") as reference_file:
        text = reference_file.read()
        reference_definitions= json.loads(text)
    reference_file.close()

    with open("temporary.txt", "r") as temp_file:
        text = temp_file.read()
        temp = json.loads(text)
    temp_file.close()

    with open("{}/intermediateParsingDicts/nestedHeaderDict.txt".format(DIR), "r") as header_file:
        text = header_file.read()
        header_dct = json.loads(text)
    header_file.close()
    
    header_values= [header_dct, "ROOT", "0", "INF", "", "ROOT"]
    
    # raw_sections [[id, str_key, content, content_tokens]]
    # reference_definitions [keyword, definition, code, interval]
    # big sections [text, code, interval, tokens]
    # all_definitions {keyword: {definition: {code: interval}}}
    
    big_raw_sections = raw_sections[1]
    raw_sections = raw_sections[0]
    
    big_sections = temp[1]
    big_sections.extend(big_raw_sections)
    # index 3540
    count = 0
    for i in range(9000, len(raw_sections)):
        if count == 4:
            exit(1)
        section = raw_sections[i]     
        id = section[0]
        str_key = section[1]
        code = str_key.split("#")[0]
        content = section[2]
        content_tokens = section[3]

        print("Row Index: {}, ID: {}, Str_Key: {}, Tokens: {}".format(i, id, str_key, content_tokens))
        if i % 50 == 0 and i != 9500:
            with open("referenceDefinitions.txt","w") as write_file:
                write_file.write(json.dumps(reference_definitions))
            write_file.close
            with open("definitionWithRanges.txt","w") as write_file:
                write_file.write(json.dumps(all_definitions))
            write_file.close()
        rnge = find_key_scope(str_key, header_values)
        
        
        prompt = prompts.get_prompt_extract_definitions(content)
        used_model = "gpt-3.5-turbo-16k"
        chat_completion = openai.ChatCompletion.create(model=used_model,messages=prompt, temperature=0)
        definitions_str = chat_completion.choices[0].message.content
        definitions_lst = definitions_str[1:].split("*")
        print(definitions_lst)
        count += 1
        continue
        # index 3540
        
        for definition in definitions_lst:
            try:
                def_index = definition.index(":")
            except:
                print("Misclassified as definition! {}".format(definition[0:20]))
                continue
            
            keyWord = definition[0:def_index].strip()
            definition = definition[def_index+1:].strip()
            if "as defined in" in definition or "has the same meaning as" in definition:
                reference_definitions.append((keyWord, definition, code, rnge))
                continue
            
            # KeyWord already in all_definitions
            if keyWord in all_definitions:
                # Definition already in unique_definitions
                if definition in all_definitions[keyWord]:
                    # Definition already found in another code, range union
                    if code in all_definitions[keyWord][definition]:
                        #print("Definition already found, performing range union...")
                        all_definitions[keyWord][definition][code] = interval(all_definitions[keyWord][definition][code][0]) | rnge
                    # Definition found in new code, create new interval
                    else:
                        #print("Same definition in different code: {} with range: {}".format(code, rnge))
                        all_definitions[keyWord][definition][code] = rnge
                # New definition exists for keyword
                else:
                    all_definitions[keyWord][definition] = {code: rnge}
                    #print("New definition: {} exists for keyword: {}".format(definition, keyWord))
            # Brand new keyword
            else:
                all_definitions[keyWord] = {definition: {code: rnge}}
                #print("New keyword!  ", all_definitions[keyWord])

    with open("referenceDefinitions.txt","w") as write_file:
        write_file.write(json.dumps(reference_definitions))
    write_file.close
    with open("definitionWithRanges.txt","w") as write_file:
        write_file.write(json.dumps(all_definitions))
    write_file.close()
    with open("temporary.txt","w") as write_file:
        write_file.write(json.dumps(big_sections))
    write_file.close()
    

def remaining():
    small = []
    big = []
    with open("sendToGPT4.txt","r") as read_file:
        text = read_file.read()
        lst = json.loads(text)
    read_file.close()
    
    #print(len(lst))
    for text in lst:
        tokens = util.num_tokens_from_string(text)
        count = text.count('“')
        if count > 1 or count == 0:
            big.append(text)
        else:
            #print(text)
            # Start “
            # End ”
            firstIndex = text.index('“')
            secondIndex = text.index('”', firstIndex+1)
            text = text[firstIndex:secondIndex+1] + ":" + text[secondIndex+1:]
            small.append(text)
    print(len(big))
    print(len(small))
    small = sorted(small, key=len)
    big = sorted(big, key=len)
    with open("small.txt","w") as small_file:
        small_file.write(json.dumps(small))
    small_file.close()
    with open("big.txt", "w") as big_file:
        big_file.write(json.dumps(big))
    big_file.close()
    print(small[-1])
    #plt.hist(tokens,bins=12)
    #plt.show()


def test_remaining_tokens(firstPass=False):
    # Always open this
    with open("definitionFromSections.txt","r") as input_file:
        text = input_file.read()
        all_raw_sections = json.loads(text)
    input_file.close()

    # Always open this
    with open("{}/intermediateParsingDicts/nestedHeaderDict.txt".format(DIR), "r") as header_file:
        text = header_file.read()
        header_dct = json.loads(text)
    header_file.close()
    
    # Iterative saving implementation
    if firstPass:
        reference_definitions = []
        all_definitions = {}
        needs_gpt4 = []
    else:
        # Open only if already passed through some
        with open("referenceDefinitions.txt","r") as reference_file:
            temp = reference_file.read()
            reference_definitions = json.loads(temp)
        reference_file.close
        # Open only if already passed through some
        with open("definitionWithRanges.txt","r") as all_definitions_file:
            temp = all_definitions_file.read()
            all_definitions = json.loads(temp)
        all_definitions_file.close()

        with open("remaining.txt", "r") as remaining_file:
            temp = remaining_file.read()
            needs_gpt4 = json.loads(temp)
        remaining_file.close()

    
    raw_sections = all_raw_sections[0]
    total_new_tokens = 0
    header_values= [header_dct, "ROOT", "0", "INF", "", "ROOT"]
    
    # raw_sections [[id, str_key, content, content_tokens]]
    # reference_definitions [keyword, definition, code, interval]
    # big sections [text, code, interval, tokens]
    # all_definitions {keyword: {definition: {code: interval}}}

    # 13668 sections
    for i in range(6050, len(raw_sections)):
        # LOCAL lists
        needs_gpt = []
        already_done = []
        
        if i % 50 == 0 and i != 6050:
            with open("referenceDefinitions.txt","w") as write_file:
                write_file.write(json.dumps(reference_definitions))
            write_file.close
            with open("definitionWithRanges.txt","w") as write_file:
                write_file.write(json.dumps(all_definitions))
            write_file.close()
            with open("remaining.txt","w") as write_file:
                write_file.write(json.dumps(needs_gpt4))
            write_file.close()


        section = raw_sections[i] 
        id = section[0]   
        str_key = section[1]
        code = str_key.split("#")[0]
        content = section[2]
        content_tokens = section[3]
        
        print("Row Index: {}, ID: {}, Str_Key: {}, Tokens: {}".format(i, id, str_key, content_tokens))

        new_tokens = find_next_definition(content, needs_gpt, already_done)
        rnge = find_key_scope(str_key, header_values)

        for term in needs_gpt:
            count = term.count('“')
            if count > 1 or count == 0:
                needs_gpt4.append((id, str_key, code, term, rnge))
            else:
                firstIndex = term.index('“')
                secondIndex = term.index('”', firstIndex+1)
                term = term[firstIndex:secondIndex+1] + ":" + term[secondIndex+1:]
                prompt = prompts.get_prompt_extract_definitions(term)
                
                chat_completion =  util.create_chat_completion(used_model="gpt-3.5-turbo-16k",prompt_messages=prompt, temp=0, api_key_choice="will")
                result = chat_completion.choices[0].message.content
                #print("With GPT 3.5: ", result)
                add_to_dct(all_definitions, reference_definitions, code, rnge, result)
                
                
        # Add to dict
        for done_definition in already_done:
            #print("No GPT Needed: ", result)
            add_to_dct(all_definitions, reference_definitions, code, rnge, done_definition)
            
        total_new_tokens += new_tokens
        

    with open("referenceDefinitions.txt","w") as write_file:
        write_file.write(json.dumps(reference_definitions))
    write_file.close
    with open("definitionWithRanges.txt","w") as write_file:
        write_file.write(json.dumps(all_definitions))
    write_file.close()
    with open("remaining.txt","w") as write_file:
        write_file.write(json.dumps(needs_gpt4))
    write_file.close()

def add_to_dct(all_definitions, reference_definitions, code, rnge, result):
    if '“' not in result:
            result = result.replace("\"",'“',1)
            result = result.replace("\"",'”', 1)
    result = result.replace('”','”:', 1)
    #print(result)
    
    if ":" not in result[:len(result)-2]:
        #print("No Colon Case!")
        return
    colon_index = result.index(":")
    keyWord = result[0:colon_index].lower()
    definition = result[colon_index+1:]

    if "as defined in" in definition or "has the same meaning as" in definition:
        reference_definitions.append((keyWord, definition, code, rnge))
        return

    # KeyWord already in all_definitions
    if keyWord in all_definitions:
        # Definition already in unique_definitions
        if definition in all_definitions[keyWord]:
            # Definition already found in another code, range union
            if code in all_definitions[keyWord][definition]:
                #print("Definition already found, performing range union...")
                all_definitions[keyWord][definition][code] = interval(all_definitions[keyWord][definition][code][0]) | rnge
            # Definition found in new code, create new interval
            else:
                #print("Same definition in different code: {} with range: {}".format(code, rnge))
                all_definitions[keyWord][definition][code] = rnge
        # New definition exists for keyword
        else:
            all_definitions[keyWord][definition] = {code: rnge}
            #print("New definition: {} exists for keyword: {}".format(definition, keyWord))
    # Brand new keyword
    else:
        all_definitions[keyWord] = {definition: {code: rnge}}
        #print("New keyword!  ", all_definitions[keyWord])

def find_next_definition(text, needs_gpt4, already_done):
    indices = []
    text = text.replace('‛', '“')
    current = 0
    total_tokens = 0
    next_period_index = 0
    
    needs_gpt4_local = []
    already_done_local = []
    if text.count('“') % 2 != 0:
        new_tokens = util.num_tokens_from_string(text)
        needs_gpt4.append(text)
        return new_tokens
    try:
        while True:      
            first_index = text.index('“', current)
            if next_period_index > first_index:
                new_tokens = util.num_tokens_from_string(text)
                needs_gpt4.append(text)
                return new_tokens
            
            current = first_index+1
            second_index = text.index('“', first_index)
            next_period_index = text.index('.', first_index)
            current = second_index+1
            indices.append(first_index)
    except:
        #print(indices)
        if len(indices) == 0:
            new_tokens = util.num_tokens_from_string(text)
            needs_gpt4.append(text)
            return new_tokens
        try:
            working_index = 0
            for i in range(1, len(indices)):      
                last_index = indices[i-1]
                current_index = indices[i]
                working_index = i
                definition = text[last_index:current_index]
                index = definition.rindex('”')
                new_tokens = util.num_tokens_from_string(definition)
                keyWord = definition[0:index+1] + ":" + definition[index+1:]
                if len(keyWord) > 200:
                    needs_gpt4_local.append(keyWord)
                    total_tokens += new_tokens
                else:
                    already_done_local.append(keyWord)
            
            #print(indices)
            #print(text)
            definition = text[indices[-1]:]
            index = definition.rindex('”')
            #print(definition2)
            new_tokens = util.num_tokens_from_string(definition)
            keyWord = definition[0:index+1] + ":" + definition[index+1:]
            if len(keyWord) > 200:
                needs_gpt4_local.append(keyWord)
                total_tokens += new_tokens
            else:
                already_done_local.append(keyWord)
        except Exception as e:
            new_tokens = util.num_tokens_from_string(text)
            needs_gpt4.append(text)
            return new_tokens
    needs_gpt4.extend(needs_gpt4_local)
    already_done.extend(already_done_local)
    return total_tokens

def test_definition_dict():
    with open("definitionWithRanges.txt", "r") as output_file:
        text = output_file.read()
        all_definitions = json.loads(text)
    output_file.close()
    print(len(all_definitions))
    unique_definitions = 0
    for key in all_definitions.keys():
        unique_definitions += len(all_definitions[key].keys())
    print(unique_definitions)


def find_key_scope(str_key, header_values):
    #  0,   1,2,3,4,5,6
    # [HSC,10,0,0,4,1,11165.1]
    str_key_split = str_key.split("#")
    str_key_split[1], str_key_split[2] = str_key_split[2], str_key_split[1]
    for i in range(5, -1, -1):
        if str_key_split[i] != "0":
            stop = str_key_split[i]
    
    values = header_values
    for element in str_key_split:
        values = values[0][element]
        
        if element==stop:
            start = values[3]
            end = values[4]
            
            try:
                start = start.strip()
                end = end.strip()
                try:
                    rnge = interval[float(start), float(end)]
                except:
                    rnge = -1
            except:
                rnge = -1
            if rnge == -1 and values[4] != "code":
                try:
                    rnge = interval[float(str_key_split[-1]),float(str_key_split[-1])]
                except:
                    # Specific Section
                    rnge = interval[-2, -1]
            else:
                # code level
                rnge = interval[-4, -3]
            return rnge
    

def extract_definitions_from_sections():
    sql_select = "SELECT id, str_key, content, content_tokens FROM ca_code WHERE content ILIKE '%” means%' ORDER BY content_tokens;"
    conn = util.psql_connect()
    rows = util.select_and_fetch_rows(conn, sql_select)
    regular_rows = []
    big_rows = []
    for i, row in enumerate(rows):
        text = row[2]
        tokens = util.num_tokens_from_string(text)
        if tokens > 2000:
            big_rows.append(list(row))
            big_rows[-1][3] = tokens
        else:
            regular_rows.append(list(row))

    result = [regular_rows, big_rows]
    with open("definitionFromSections.txt","w") as write_file:
        write_file.write(json.dumps(result))
    write_file.close()
    conn.close()


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
    # header_dct:  {Key "BPC": [{} Subtrees, Title, Range start, range end, [definitions], "floor tag"]}
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

def traverse_definitions(key, header_dct_values, path, lst):
    
    
    #print("Traversing for key: ", key)
    
    if header_dct_values[4] != "":
        text = header_dct_values[4]
        
        try:
            start = header_dct_values[2].strip()
            end = header_dct_values[3].strip()
            start = float(start)
            end = float(end)
            rnge = interval[start, end]
            print(rnge)
        except:
            rnge = interval[-1,-1]
        code = path.split("*")[0]
        lst.append([text, code, rnge])
        

    if header_dct_values[1] != "ROOT":
        currentPath = "{}*".format(key)
        path += currentPath
        
    if type(header_dct_values[0]) != dict or header_dct_values[5] == "article":
        return
    
    for k,v in header_dct_values[0].items():
        traverse_definitions(k, v, path, lst)


def traverse_titles_and_definitions(key, header_dct_values, path, titles):
# Range_dct: {Key: "division": [title, (range tup)]}
    # header_dct:  {Key "BPC": [{} Subtrees, Title, Tup:(Range start, range end), [definitions], "floor tag"]}

    
    if header_dct_values[1] != "ROOT":
        currentPath = "{}='{}' AND ".format(header_dct_values[5], key)
        path += currentPath
        
    if type(header_dct_values[0]) != dict or header_dct_values[5] == "article":
        path = path[0:len(path)-5]+";"
        return
    
    for k,v in header_dct_values[0].items():
        traverse_titles_and_definitions(k, v, path, titles)

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