import getPSQLConn as psql
import os
import psycopg2
import json
import embedCodes

def main():
    conn = psql.connect()
    sql_select = "SELECT id, definitions, title_path, content_tokens FROM ca_code ORDER BY id;"
    rows = psql.select_and_fetch_rows(conn, sql_select)
    print(len(rows))
    conn.close()
    conn = psql.connect()
    get_all_row_embeddings(rows, conn)

def get_all_row_embeddings(rows, conn):
    titleDict = {}
    defDict = {}
    cursor = conn.cursor()
    for tup in rows:
        id = int(tup[0])
        
        definitions = tup[1]
        title_path = tup[2]
        content_tokens = tup[3]
        sql_update = "UPDATE ca_code SET "
        if definitions in defDict:
            print("Definition already in defDict for id: {}".format(id))
            def_embedding = defDict[definitions][0]
            def_tokens = defDict[definitions][1]
        else:
            try:
                def_embedding, def_tokens = embedCodes.get_embedding_and_token(definitions)
                print("New definition found for id: {}".format(id))
                defDict[definitions] = [def_embedding, def_tokens]
                sql_update += "definition_embedding='{}', ".format(def_embedding)
            except:
                def_tokens = 0
        if title_path in titleDict:
            title_embedding = titleDict[title_path][0]
            title_tokens = titleDict[title_path][1]
        else:
            try:
                title_embedding, title_tokens = embedCodes.get_embedding_and_token(title_path)
                titleDict[title_path] = [title_embedding, title_tokens]
                sql_update += "title_path_embedding='{}', ".format(title_embedding)
            except:
                title_tokens = 0
            
        total_tokens = content_tokens+def_tokens+title_tokens
        sql_update +=  " titles_tokens='{}', definition_tokens='{}', total_tokens='{}' WHERE id='{}';".format(title_tokens, def_tokens, total_tokens, id)
        cursor.execute(sql_update)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()