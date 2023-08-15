import json
import psycopg2
import testPSQLConnection as psqlCon

CODES = ["BPC","CCP","CIV","COM","CONS","CORP","EDC","ELEC","EVID","FAC","FAM","FGC","FIN","GOV","HNC","HSC","INS","LAB","MVC","PCC","PEN","PRC","PROB","PUC","RTC","SHC","UIC","VEH","WAT","WIC"]
# This guy's the goat, helped me speed up insertion.
# https://www.confessionsofadataguy.com/performance-testing-postgres-inserts-with-python/

def main():
    # Connect to the database
    conn = psqlCon.connect()
    
    # Format template for code_list
    # [[ID, Code, Division, Title, Part, Chapter, Article, Section, isCodeDescription, text, addendum, embedding, link],[...]]
    code_list = []
    for code in CODES:
        print("Inserting rows from legal code {} into database table ca_code...".format(code))
        read_from_file(code, code_list)
        insert_code_list(code_list, conn)
        code_list = []

    conn.close()

def read_from_file(code, code_list):
    ''' Read in a dictionary from a file with name {code}.txt and convert to list of tuples. Append each tup to code_list'''
    with open("{}.txt".format(code), "r") as text_file:
        rawText = text_file.read()
        texts = json.loads(rawText)
    text_file.close()
    # [[ID, key, Code, Division, Title, Part, Chapter, Article, Section, isCodeDescription, text, addendum, embedding, link],[...]]
    for key,sectionTags in texts.items():
        # Insert the dictionary key in position 1
        sectionTags.insert(key, 1)
        code_list.append(tuple(sectionTags))

def insert_code_list(code_list, conn):
    """ Add each row (tuple) in code_list to an sql insert statement using string formatting. Execute large insert statement and committ """
    # Format of code_list: [(id, "section_info","content","embedding"),]
    print("Number of chained sql insert statements to execute: ",len(code_list))

    cur = conn.cursor()
    # Mogrify is used as it is one of the most efficient ways to parse multiple insert statements in psycopg2
    sql = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", row).decode('utf8') for row in code_list)
    cur.execute("INSERT INTO ca_code VALUES " + sql)
    # Commit and close
    conn.commit()
    cur.close()

if __name__== "__main__":
    main()