import getPSQLConn as psql
import json

def main():
    
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
    conn = psql.connect()
    cursor = conn.cursor()
    sql_select = "SELECT id, definitions FROM ca_code WHERE {}".format(path)
    print(sql_select)
    rows = psql.select_and_fetch_rows(conn, sql_select)
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

if __name__ == "__main__":
    main()