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
import gui


openai.api_key = config.spartypkp_openai_key

def main():
    print("Here")
    answer = ask_abe("what company can sponsor h1b?", False, False, False)
    
# Starts one "run" of the project    
def ask_abe(user_query, print_sections, do_testing, do_stream):
    
    print()
    print("================================")
    print("Initializing instance of Abe...")
    print(f"User Query:\n    {user_query}")
    #print("Universal Answer Template:")
    #print("  - QUESTION 1: What is the simple answer to QUERY?")
    #print("  - QUESTION 2: What is the exact legal text that answers QUERY?")
    #print("  - Question 3: What rights and privileges does a user have relating to QUERY TOPICS?")
    #print("  - Question 4: What are restrictions, caveats, and conditions to QUERY TOPICS?")
    #print("  - Question 5: What are any penalties, punishments, or crimes which apply to violating restrictions of QUERY TOPICS?")
    print("here")
    similar_queries_list, question_list = process.processing_stage(user_query)
    similar_content_list, legal_text_list, legal_text_tokens = search.searching_stage(similar_queries_list)
    

    summary_template, legal_documentation, question = answer.answering_stage(question_list, legal_text_list, user_query)
    
    #if do_stream:
        #for message in stream_answer(question, summary_template, legal_documentation):
            #yield message
    #else:
    final_answer = answer.populate_summary_template(question, legal_documentation, summary_template)
    print(final_answer)
    return final_answer
    print("================================\n")

#def stream_answer(question, summary_template, legal_documentation):
    #prompt_update = prompts.get_prompt_populate_summary_template(question, summary_template, legal_documentation)
    #for message in util.stream_chat_completion("gpt-3.5-turbo-16k", prompt_messages=prompt_update, do_stream=True):
        #yield message

def find_sections_cited(legal_text_list, final_answer):
    cited_sections = []
    for section_full in legal_text_list:
        index = section_full.index("\n")
        citation = section_full[0:index]
        content = section_full[index+1:]
        if citation in final_answer:
            cited_sections.append((citation, content))
    return cited_sections

if __name__ == "__main__":
    main()