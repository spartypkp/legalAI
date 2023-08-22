import getPSQLConn as psql
import os
import psycopg2
import json
import embedCodes

def main():
    conn = psql.connect()
    sql_select = "SELECT id, definitions, title_path, content_tokens FROM ca_code ORDER BY id;"
    rows = psql.select_and_fetch_rows(conn, sql_select)
    conn.close()
    conn = psql.connect()
    get_all_row_embeddings(rows, conn)

def get_all_row_embeddings(rows, conn):
    cursor = conn.cursor()
    for tup in rows:
        id = int(tup[0])
        if id % 1000 == 0:
            print("Finished embedding for ID:{}".format(id))
        definitions = tup[1]
        title_path = tup[2]
        content_tokens = tup[3]
        sql_update = "UPDATE ca_code SET "
        
        try:
            def_embedding, def_tokens = embedCodes.get_embedding_and_token(definitions)
            sql_update += "definition_embedding='{}', ".format(def_embedding)
        except:
            def_embedding = []
            def_tokens = 0
            
        try:
            title_embedding, title_tokens = embedCodes.get_embedding_and_token(title_path)
            sql_update += "title_path_embedding='{}', ".format(title_embedding)
        except:
            title_embedding = []
            title_tokens = 0
            
        total_tokens = content_tokens+def_tokens+title_tokens
        sql_update +=  " titles_tokens='{}', definition_tokens='{}', total_tokens='{}' WHERE id='{}';".format(title_tokens, def_tokens, total_tokens, id)
        cursor.execute(sql_update)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()