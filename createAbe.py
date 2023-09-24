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
    answer = ask_abe("what are the aspects of the warrant of habitability for an apartment in california?", False, False, False)
    
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
    
    similar_queries_list, question_list_raw = process.processing_stage(user_query)
    question_list = []
    for question in question_list_raw:
        if question != "":
            question_list.append(question)
    
    similar_content_list, legal_text_list, legal_text_tokens, citation_list = search.searching_stage(similar_queries_list)
    summary_template, legal_documentation, question = answer.answering_stage(question_list, legal_text_list, user_query)
    
    #if do_stream:
        #for message in stream_answer(question, summary_template, legal_documentation):
            #yield message
    #else:
    
    final_answer = answer.populate_summary_template(question, legal_documentation, summary_template)
    cited_sections = find_sections_cited(citation_list, final_answer)
    #with open("response.md","w") as response_md:
        #response_md.write(final_answer)
    #response_md.close()
    #with open("citations.md","w") as citations_md:
        #citations_md.write(cited_sections)
    #citations_md.close()

   
    print()
    print("================================\n")
    print()
    
    #final_answer = gui.markdown_to_html(final_answer)
    #cited_sections = gui.markdown_to_html(cited_sections)
    return final_answer, cited_sections
    

#def stream_answer(question, summary_template, legal_documentation):
    #prompt_update = prompts.get_prompt_populate_summary_template(question, summary_template, legal_documentation)
    #for message in util.stream_chat_completion("gpt-3.5-turbo-16k", prompt_messages=prompt_update, do_stream=True):
        #yield message

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