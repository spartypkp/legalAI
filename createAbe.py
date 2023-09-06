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


openai.api_key = config.spartypkp_openai_key

def main():
    ask_abe("can I smoke cannabis?", True, False)
    
# Starts one "run" of the project    
def ask_abe(user_query, print_sections, do_testing):  
    # Get similar queries by calling GPT 3.5, maybe Google BARD instead
    topic_dict = get_similar_queries(user_query)
    topics_str = " ".join(topic_dict["queries"])
    # Debug prints, print related queries
    print("\n\n Calling GPT 3.5 to generate related questions...: \n", topics_str)
    print("\n Comparing vector embeddings in the database to embedding of all related quries....\n")
    # Get cosine similarity score of related queries to all content embeddings
    rows = embeddingSimilarity.compare_content_embeddings(user_query, print_relevant_sections=print_sections, match_count=20)
    
    # continue to answer = input("Would you like to continue to GPT 4's answer? (y/n):\n")
    continue_to_answer = "y"
    if continue_to_answer == "y":
        legal_text, final_answer, cost = get_final_answer(user_query, rows)
        if print_sections == False:
            legal_text = "Relevant Sections Redacted"
        return legal_text, final_answer, cost

# Given a user query, generate similar queries with related language
def get_similar_queries(user_query):
    prompt_similar_queries = prompts.get_prompt_similar_queries(user_query)
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=prompt_similar_queries, temperature=0.4)
    result = chat_completion.choices[0].message.content
    result_dct = json.loads(result)
    return result_dct

# All relevant sections are found, now generate an answer
def get_final_answer(user_query, rows, use_gpt_4=True):
    current_tokens = 0
    row = 0
    legal_text = []
    used_model = "gpt-3.5-turbo-16k"
    if use_gpt_4:
        max_tokens = 24000
    else:
        max_tokens = 12000
    while current_tokens < max_tokens and row < len(rows):
        current_tokens += rows[row][12]
        legal_text.append(rows[row])
        row += 1
        
    legal_text = embeddingSimilarity.format_sql_rows(legal_text)
    prompt_convert_question = prompts.get_prompt_convert_question(user_query)
    chat_completion =  openai.ChatCompletion.create(model=used_model,messages=prompt_convert_question, temperature=0)
    converted_questions = chat_completion.choices[0].message.content
    template = prompts.get_basic_universal_answer_template(user_query, converted_questions)
    
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