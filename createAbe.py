import os
import openai
import config
import json
import utilityFunctions as util
import promptStorage as prompts
import testWithCurrentBuild as test
import embeddingSimilarity
import time
import math
from typing import Union
import processUserQuery as process
import searchRelevantSections as search


openai.api_key = config.spartypkp_openai_key

def main():
    ask_abe("can I smoke cannabis?", True, False)
    
# Starts one "run" of the project    
def ask_abe(user_query, print_sections, do_testing):  
    
   
    
    
    # continue to answer = input("Would you like to continue to GPT 4's answer? (y/n):\n")
    continue_to_answer = "y"
    if continue_to_answer == "y":
        legal_text, final_answer, cost = get_final_answer(user_query, rows)
        if print_sections == False:
            legal_text = "Relevant Sections Redacted"
        return legal_text, final_answer, cost

def processing_stage(user_query, print_sections, do_testing):

    # Get similar queries by calling GPT 3.5, maybe Google BARD instead
    similar_queries = process.get_similar_queries(user_query)
    user_query_as_template = process.convert_query_to_template(user_query, used_model="gpt-3.5-turbo")
    return similar_queries, user_query_as_template
    
def searching_stage(user_query, print_sections):
    similar_content = search.search_similar_content_sections(user_query, print_sections)
    legal_text, legal_text_tokens = search.accumulate_legal_text_from_sections(similar_content, used_model="gpt-3.5-turbo-16k")
    legal_text = search.format_legal_text(legal_text)
    return similar_content, legal_text, legal_text_tokens

def answering_stage():
    pass
def testing_stage():
    pass
# All relevant sections are found, now generate an answer
def get_final_answer(user_query, rows, use_gpt_4=True):
    
    prompt_final_answer= prompts.get_prompt_final_answer(user_query, legal_text, template)
    
    if use_gpt_4:
        openai.api_key = config.seangrove_openai_key
        used_model = "gpt-4-32k"
        chat_completion = openai.ChatCompletion.create(model=used_model,messages=prompt_final_answer, temperature=0.2)
    else:
        chat_completion = openai.ChatCompletion.create(model=used_model,messages=prompt_final_answer, temperature=0.2)
    result_str = chat_completion.choices[0].message.content
    result = result_str.split("*")
    result = "\n".join(result[1:])
    print(result)
    prompt_tokens = chat_completion.usage["prompt_tokens"]
    completion_tokens = chat_completion.usage["completion_tokens"]
    cost = util.calculate_prompt_cost(used_model, prompt_tokens, completion_tokens)
    return legal_text, result, cost


def find_and_replace_definitions(user_query):
    pass
    # Find relevant definition embeddings
    # Prompt gpt-4 to determine which definitions are most relevant
    # If there are multiple similar definitions, ask user to define which is most relevant
    # Reformat user_query with applicable definitions and return




if __name__ == "__main__":
    main()