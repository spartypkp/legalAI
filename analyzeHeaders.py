import json
import os
import psycopg2
import calculateTokens
import getPSQLConn

def main():
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