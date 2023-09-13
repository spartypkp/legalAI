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
    ask_abe("can I smoke cannabis?", True, False)
    
# Starts one "run" of the project    
def ask_abe(user_query, print_sections, do_testing):  
    similar_queries, question_list = process.processing_stage(user_query)
    similar_content, legal_text, legal_text_tokens = search.searching_stage(similar_queries, print_sections)

    # continue to answer = input("Would you like to continue to GPT 4's answer? (y/n):\n")
    use_gpt_4 = True
    continue_to_answer = "y"
    if continue_to_answer == "y":
        result, prompt_tokens, completion_tokens = answer.answering_stage(question_list, legal_text, use_gpt_4)
        if print_sections == False:
            legal_text = "Relevant Sections Redacted"
        
        print(result)
        
        return legal_text, result


    
def testing_stage():
    pass



if __name__ == "__main__":
    main()