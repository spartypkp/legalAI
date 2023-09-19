import os
import openai
import config
import json
import utilityFunctions as util
import promptStorage as prompts
import embeddingSimilarity
import time
import math
from typing import Union
import processUserQuery as process
import searchRelevantSections as search
import answerUserQuery as answer
import testWithCurrentBuild as test


openai.api_key = config.spartypkp_openai_key

def main():
    ask_abe("can I smoke cannabis?", False, False)
    
# Starts one "run" of the project    
def ask_abe(user_query, print_sections, do_testing):
    print()
    print("================================")
    print("Initializing instance of Abe...")
    print(f"User Query:\n    {user_query}")
    print("Universal Answer Template:")
    print("  - QUESTION 1: What is the simple answer to QUERY?")
    print("  - QUESTION 2: What is the exact legal text that answers QUERY?")
    print("  - Question 3: What rights and privileges does a user have relating to QUERY TOPICS?")
    print("  - Question 4: What are restrictions, caveats, and conditions to QUERY TOPICS?")
    print("  - Question 5: What are any penalties, punishments, or crimes which apply to violating restrictions of QUERY TOPICS?")

    similar_queries_list, question_list = process.processing_stage(user_query)
    
    
    similar_content_list, legal_text_list, legal_text_tokens = search.searching_stage(similar_queries_list)
    print(legal_text_list)
    

    use_gpt_4 = True
    result, prompt_tokens, completion_tokens = answer.answering_stage(question_list, legal_text_list, use_gpt_4)
    print("================================\n")
    
       
    #print(result)
        
    return legal_text_list, result

def testing_stage():
    pass



if __name__ == "__main__":
    main()