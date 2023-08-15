import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt
import json
import config
import os

# legalMap Secret API Key
openai.api_key = config.spartypkp_openai_key
codes = ["BPC","CCP","CIV","COM","CONS","CORP","EDC","ELEC","EVID","FAC","FAM","FGC","FIN","GOV","HNC","HSC","INS","LAB","MVC","PCC","PEN","PRC","PROB","PUC","RTC","SHC","UIC","VEH","WAT","WIC"]
DIR = os.path.dirname(os.path.realpath(__file__))

# Left blank for testing
def main():
    for code in codes:
        print("Started embedding codes for code {}...".format(code))
        embed_Codes(code)
        print("Finished embedding for code {}".format(code))

# TODO: Write fn description
def embed_Codes(code):
    with open("{}/scrapedData/{}.txt", "r") as text_file:
        rawText = text_file.read()
        textDct = json.loads(rawText)
    text_file.close()

    file = open("embeddingErrorLog.txt", "a")
    for key, value in textDct.items():
        embed = []
        try:
            embed = get_embedding(value[9])
        except Exception as e:
            
            file.write("({})\n".format(key))
    file.close()
        
    with open("{}/scrapedData/{}.txt", "w") as out_file:
        out_file.write(json.dumps(textDct))
    out_file.close()

# Need tweaking on the min and max parameters.
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text, model="text-embedding-ada-002"):
    return openai.Embedding.create(input=[text], model=model)["data"][0]["embedding"]

if __name__ == '__main__':
    main()