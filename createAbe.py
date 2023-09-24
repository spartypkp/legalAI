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
    answer = ask_abe("What legal actions do I have if my landlord sells my lease 3 months before my current lease ends and is evicting?", False, False, False)
    
# Starts one "run" of the project    
def ask_abe(user_query, print_sections, do_testing, do_stream):
    
    print()
    print("================================")
    print("Initializing instance of Abe...")
    print(f"User Query:\n    {user_query}")
   
    similar_queries_list, question_list_raw = process.processing_stage(user_query)
    question_list = []
    for question in question_list_raw:
        if question != "":
            question_list.append(question)
    
    similar_content_list, legal_text_list, legal_text_tokens, citation_list = search.searching_stage(similar_queries_list)
    summary_template, legal_documentation, question = answer.answering_stage(question_list, legal_text_list, user_query)
    
    
    
    final_answer = answer.populate_summary_template(question, legal_documentation, summary_template)
    cited_sections = find_sections_cited(citation_list, final_answer)

    print()
    print("================================\n")
    print()
    return final_answer, cited_sections
    
def find_sections_cited(citation_list, final_answer):
    cited_sections = ""
    
    for tup in citation_list:
        citation = tup[0]
        content = tup[1]
        link = tup[2]
        if citation in final_answer:
            result = "{}: {}\n{}".format(citation, link, content)
            cited_sections = cited_sections + result + "\n"
    return cited_sections

if __name__ == "__main__":
    main()