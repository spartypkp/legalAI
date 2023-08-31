import tiktoken
import openai
import json
import embedCodes
import config
import os

DIR = os.path.dirname(os.path.realpath(__file__))

codes = ["BPC","CCP","CIV","COM","CONS","CORP","EDC","ELEC","EVID","FAC","FAM","FGC","FIN","GOV","HNC","HSC","INS","LAB","MVC","PCC","PEN","PRC","PROB","PUC","RTC","SHC","UIC","VEH","WAT","WIC"]

def main():
    openai.api_key = config.spartypkp_openai_key
    with open("{}/scrapedData/{}.txt".format(DIR, "BPC"), "r") as text_file:
        rawText = text_file.read()
        texts = json.loads(rawText)
    text_file.close()
    text = texts["BPC#9#0#0#3#2#23320"]
    print(text)
    exit(1)
    embedding = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
    embed = embedding["data"][0]["embedding"]
    tokens = embedding["usage"]["total_tokens"]
   
    # DENOTES NEW SECTION
    # \u00a0\u00a0

# Deprecated
def find_big_tokens():
    bigTokens = {}
    for code in codes:
        with open("{}.txt".format(code), 'r') as convert_file:
            rawText = convert_file.read()
            text = json.loads(rawText)

        for k,v in text.items():
            splt = v.split(",")
            numTokens = int(splt[0])
            if numTokens > 7000:
                print("Key {} has BIGTOKENS {}".format(k, numTokens))
                bigTokens[k] = numTokens
    print("Number of bigtoken offenders:", len(bigTokens.keys()))
    with open("bigtokens.txt", 'w') as out_file:
        out_file.write(json.dumps(bigTokens))
    out_file.close

def num_tokens_from_string(string):
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens


    

if __name__ == "__main__":
    main()