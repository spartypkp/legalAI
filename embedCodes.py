import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt
import json
import config


# legalMap Secret API Key
openai.api_key = config.spartypkp_openai_key
codes = ["BPC","CCP","CIV","COM","CONS","CORP","EDC","ELEC","EVID","FAC","FAM","FGC","FIN","GOV","HNC","HSC","INS","LAB","MVC","PCC","PEN","PRC","PROB","PUC","RTC","SHC","UIC","VEH","WAT","WIC"]

# Left blank for testing
def main():
    pass

# Deprecated function
def embed_Codes(textDct):
    embedded={}
    code = None
    for key, value in textDct.items():
        splt = value.split(",")
        numTokens = int(splt[0])
        if numTokens > 7000:
            continue
        embedding = get_embedding(value)
        print("Embedded for key {}".format(key))
        embedded[key] = embedding
    with open("/codeEmbeds/{}embed.txt".format(code), "w") as out_file:
        out_file.write(json.dumps(embedded))
    out_file.close()

# Need tweaking on the min and max parameters.
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text, model="text-embedding-ada-002"):
    return openai.Embedding.create(input=[text], model=model)["data"][0]["embedding"]

if __name__ == '__main__':
    main()