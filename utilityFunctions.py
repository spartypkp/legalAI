import tiktoken
import openai
import json
import config
import os
from tenacity import retry, wait_random_exponential, stop_after_attempt
import psycopg2
from config import config_psql
import time

# gpt-3.5-turbo-16k
# Tokens Per Minute: 180k
# Requests Per Minute: 3,500
# Input Cost: $0.003 per 1k
# Output Cost: $0.004 per 1k


# gpt-3.5-turbo-4k
# Tokens Per Minute: 80k
# Requests Per Minute: 3,500
# Input Cost: $0.0015 per 1k
# Output Cost: $0.002 per 1k

# gpt-4 (8k token limit)
# 
# $0.03/1k prompt tokens
# $0.06/1k sampled tokens

# gpt-4-32k
# $0.06/1k prompt tokens
# $0.12/1k sampled tokens

# TESTING SUITE COSTS
# Unit Cost:
# Low cost: $0.20, Mid Cost: $0.5, Worst Cost: $1.60)
# 
# 28 calls (14 answer, 14 score)
# 
# Total Cost:
# Low Cost: $5.6, Mid Cost: $14, Worst Cost: $44.8

openai.api_key = config.spartypkp_openai_key
codes = ["BPC","CCP","CIV","COM","CONS","CORP","EDC","ELEC","EVID","FAC","FAM","FGC","FIN","GOV","HNC","HSC","INS","LAB","MVC","PCC","PEN","PRC","PROB","PUC","RTC","SHC","UIC","VEH","WAT","WIC"]

def main():
    pass
    # DENOTES NEW SECTION
    # \u00a0\u00a0

## DECORATORS
# Debug decorator specifically for gpt completions
def gpt_wrapper(func):
    def inner(*args, **kwargs):
        if "debug_print" in kwargs:
            print_debug = kwargs["debug_print"]
        else:
            print_debug = False
        if print_debug:
            print("## Before openAI create_chat_completion:\n## Used Model: {}, API Key: {}\n## Function Input: {}".format(kwargs["used_model"], kwargs["api_key_choice"], kwargs["prompt_messages"]))
        begin = time.time()
        returned_value = func(*args, **kwargs)
        end = time.time()
        if print_debug:
            prompt_tokens = returned_value.usage["prompt_tokens"]
            completion_tokens = returned_value.usage["completion_tokens"]
            total_tokens = returned_value.usage["total_tokens"]
            total_cost = calculate_prompt_cost(kwargs["used_model"], prompt_tokens, completion_tokens)
            print("## After openAI create_chat_completion:\n## Total time in {}: {}, Prompt Tokens: {}, Completion Tokens: {}, Total Tokens: {}, Total Cost: ${},\n## GPT Output: {}".format(func.__name__, end-begin,prompt_tokens, completion_tokens, total_tokens, total_cost, returned_value.choices[0].message.content))
        return returned_value
    return inner

# General debug decorator
def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, \
        kwargs: {kwargs}")
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("{} ran in {}.".format(func.__name__, end-begin))
        print(f"{func.__name__} returned: {result}")
        return result

    return wrapper


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

# Create embeddings, previously embedCodes.py
def get_embedding_and_token(text, model="text-embedding-ada-002"):
    embed = openai.Embedding.create(input=[text], model=model)
    return embed["data"][0]["embedding"], embed["usage"]["total_tokens"]

# Return just the embedding
@retry(wait=wait_random_exponential(min=1, max=2), stop=stop_after_attempt(6))
def get_embedding(text, model="text-embedding-ada-002"):
    return openai.Embedding.create(input=[text],model=model)["data"][0]["embedding"]
    
# PSQL Access Functions, previously getPSQLConn.py
def psql_connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config_psql()

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error

def select_and_fetch_rows(conn, sql_select):
    cursor = conn.cursor()
    cursor.execute(sql_select)
    rows = cursor.fetchall()
    cursor.close()
    return rows


@gpt_wrapper
def create_chat_completion(used_model="gpt-3.5-turbo", api_key_choice="will", prompt_messages=None, debug_print=False, temp=0.4, top_p_val=1, n_responses=1, do_stream=False, stop_conditions=None, presence_p=0, frequency_p=0):
    openai.api_key = config.get_api_key(api_key_choice)
    try:
        chat_completion = openai.ChatCompletion.create(model=used_model,messages=prompt_messages, temperature=temp, n=n_responses, top_p=top_p_val, stream=do_stream, stop=stop_conditions, presence_penalty=presence_p, frequency_penalty=frequency_p)
        return chat_completion
    except Exception as e:
        print("***** Failed calling create_chat_completion!")
        print(e)
        raise e


# Prompt cost calculations
def calculate_prompt_cost(model, prompt_tokens, completion_tokens):
    model_rates = {"gpt-3.5-turbo-16k":[0.003, 0.004], "gpt-3.5-turbo-4k":[0.0015, 0.002], "gpt-4":[0.03, 0.06], "gpt-4-32k":[0.06, 0.12]}
    prompt_rate = model_rates[model][0]
    completion_rate = model_rates[model][1]
    cost = ((prompt_rate/1000)*prompt_tokens) + ((completion_rate/1000)*completion_tokens)
    #print("Prompt Tokens: {}, Completion Tokens: {}".format(prompt_tokens, completion_tokens))
    #print("Total cost of using {}: ${}".format(model, cost))
    return cost



if __name__ == "__main__":
    main()