import json
import os
import psycopg2
import calculateTokens
import getPSQLConn

def main():

    '''
    rows = get_all_sections_for_article(conn)
    conn.close()
    print(len(rows))
    for row in rows:
        #print(row)
        exit(1)
    
    '''
    with open("nestedHeaderDict.txt") as header_file:
        text = header_file.read()
        header_dct = json.loads(text)
    
    all_headers = [header_dct, "ROOT", "0", "ALL", [], "ROOT"]
    final_lst = post_order_traverse(all_headers)
    
    
    final_str = str(sorted(final_lst))
    num_tokens = calculateTokens.num_tokens_from_string(final_str)
    print("Number of total tokens: ", num_tokens)
    #print(final_lst)
    with open("nested3.txt", "w") as out_file:
        
        out_file.write(final_str)
    out_file.close()
    

def test():
    with open("nested2.txt", "r") as in_file:
        text = in_file.read()
        header_dct = json.loads(text)
    in_file.close()
    print(len(header_dct["HSC"][4]))
    print(header_dct["HSC"][0]["0"][0]["10"][4])
    print()
    print(header_dct["HSC"][0]["0"][0]["10"][0]["0"][4])
    print()
    print(header_dct["HSC"][0]["0"][0]["10"][0]["0"][0]["6"][4])

def collect_headers_from_path(dct_list, keys, conn):
    path_type = dct_list[5]

    if path_type == "article":
        key_lst = keys.split("*")
        code, title, division, part, chapter, article = key_lst
        sql_select = "SELECT DISTINCT id, code, division, title, part, chapter, article, section, content, addendum FROM ca_code WHERE code = '{}' AND title = '{}' AND division = '{}' AND part = '{}' AND chapter = '{}' AND article = '{}' AND (\"section\" NOT ILIKE '%Header%' OR \"section\" IS NULL) ORDER BY id;".format(code, title, division, part, chapter, article)
        rows = get_all_sections_for_article(conn, sql_select)
        return
    

def post_order_traverse(dct_list):
    #print(dct_list[1])
    lst = []
    if dct_list[5] == "division" or dct_list[5] == "part":
        if dct_list[1] is None:
            return []
        lst.append(dct_list[1])
        return []
    
    
    for k,v in dct_list[0].items():
        #print("Current key: {}, Current value: {}".format(k, v[1:]))
        post_order_traverse(v)
    if dct_list[1] is not None:
        lst.append(dct_list[1])
    #print(dct_list)
    dct_list[4] = lst
    return lst

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