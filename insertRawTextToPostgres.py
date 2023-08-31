import json
import psycopg2
import os
from utilityFunctions import get_embedding_and_token
from utilityFunctions import num_tokens_from_string
from utilityFunctions import psql_connect

DIR = os.path.dirname(os.path.realpath(__file__))

CODES = ["BPC","CCP","CIV","COM","CONS","CORP","EDC","ELEC","EVID","FAC","FAM","FGC","FIN","GOV","HNC","HSC","INS","LAB","MVC","PCC","PEN","PRC","PROB","PUC","RTC","SHC","UIC","VEH","WAT","WIC"]

# This guy's the goat, helped me speed up insertion.
# https://www.confessionsofadataguy.com/performance-testing-postgres-inserts-with-python/

def main():
    # Connect to the database
    conn = psql_connect()
    
    # Format template for code_list
    # # [ID: 0, Code: 1, Division: 2, Title: 3, Part:4, Chapter: 5, Article: 6, Section: 7,
    #  isCodeDescription: 8, text: 9, addendum: 10, embedding: 11, link: 12]
    code_list = []
    for code in CODES:
        print("Inserting rows from legal code {} into database table ca_code...".format(code))
        read_from_file(code, code_list)
        insert_code_list(code_list, conn)
        code_list = []

    conn.close()

def read_from_file(code, code_list):
    ''' Read in a dictionary from a file with name {code}.txt and convert to list of tuples. Append each tup to code_list'''

    with open("{}/scrapedData/{}.txt".format(DIR, code), "r") as text_file:
        rawText = text_file.read()
        texts = json.loads(rawText)
    text_file.close()
    print("Opened text file.")
    # # # [ID: 0, Key: 1, Code: 2, Division: 3, Title: 4, Part: 5, Chapter: 6, Article: 7, Section: 8,
    #  isCodeDescription: 9, text: 10, addendum: 11, embedding: 12, link: 13, totalTokens: 14]
    
    errorLog = open("embeddingErrorLog.txt", "a")
    for key, sectionTags in texts.items():
        # Insert the dictionary key in position 1
        sectionTags.insert(1, key)
        embed = None
        totalTokens = 0
        try:
            embed, totalTokens = get_embedding_and_token(sectionTags[10])
        except Exception as e:
            errorLog.write("({})\n".format(key))
        
        print("Completed embedding with size: ", totalTokens)
        sectionTags[12] = embed
        sectionTags.append(totalTokens)
        code_list.append(tuple(sectionTags))

    errorLog.close()
    
def insert_code_list(code_list, conn):
    """ Add each row (tuple) in code_list to an sql insert statement using string formatting. Execute large insert statement and committ """
    # Format of code_list: [(id, "section_info","content","embedding"),]

    print("Number of chained sql insert statements to execute: ",len(code_list))
    cur = conn.cursor()

    # Mogrify is used as it is one of the most efficient ways to parse multiple insert statements in psycopg2
    sql = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", row).decode('utf8') for row in code_list)
    cur.execute("INSERT INTO ca_code VALUES " + sql)
    
    # Commit and close
    conn.commit()
    cur.close()
    print("Committed sql insert into ca_code.")

if __name__== "__main__":
    main()