import os
import openai
import config
import json
import compareEmedding
import tkinter as tk
openai.api_key = config.spartypkp_openai_key

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


def main():
    
    user_question = input("\n\nInput a question to ask about the California legal code or a specific topic you would like to know more about:\n")
    topic_dict = get_similar_topics(user_question)
    topics_str = " ".join(topic_dict["queries"])
    print("\n\n Calling GPT 3.5 to generate related questions...: \n", topics_str)
    print("\n Comparing vector embeddings in the database to embedding of all related quries....\n")
    rows = compareEmedding.compare_all_embeddings(topics_str, match_count=20)
    #continue_to_answer = input("These are all the relevant sections above. Would you like to continue to get a full answer from GPT? (y/n)")
    continue_to_answer = "y"
    if continue_to_answer == "y":
        final_answer = get_final_answer(user_question, rows)
        print("\n\n")
        print(final_answer)
    
    '''

    messages= [
        {"role": "system", "content": "System instructions here!"},
        {"role": "user", "content": "Instructions and inputs go in here"}      
    ]
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])
    '''
    


def get_similar_topics(user_question):
    similar_topics= [
        {"role": "system", "content": "All output shall be in JSON format."},
        {"role": "user", "content": '''Generate an array of search queries that are relevant to this question.

Use a variation of related keywords for the queries, trying to be as general as possible.

Queries should include legal language such as ["lawful", "violation", "authorized", "restrictions", "legitimate", "defined", "according to law", "legal"].

Queries should be short.

Generate 15 queries.

User question: {}
            
Format: {{\\"queries\\": [\\"query_1\\", \\"query_2\\", \\"query_3\\"]}}";'''.format(user_question)}]
    
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=similar_topics)
    result = chat_completion.choices[0].message.content
    result_dct = json.loads(result)
    return result_dct

def extract_questions_from_text():
    prompt1 = '''You are an editor for a law firm that helps explain legal text. 

    You will be given a section of legal code delimitted by triple quotes. 

    Make a list of questions that could be answered by this section of legal code. Questions you make will be used to link a frequently asked section page to this document. 

    Be creative and create as many question as you can from every part of the text.

    '''
    prompt2 = '''You are a helpful and thorough teachers assistant in a law school. You focus on assisting professors by creating rigorous questions that test's a student understanding of a piece of legislation.

    Generate questions that this piece of legislation answers.

    Read carefully and take your time. Create a list of 20 questions.
        '''
    return

def get_final_answer(user_question, rows):
    current_tokens = 0
    row = 0
    text = ""
    max_tokens = 12000
    while current_tokens < max_tokens and row < len(rows):

        #print(rows[row])
        current_tokens += rows[row][10]
        text = text + "\n" + rows[row][9]
        row += 1
    
    answer_prompt= [
        {"role": "system", "content": '''You are a helpful legal assistant that answers a user query by summarizing information in a legal document.

        You will be provided with a user query and legal documentation in the format of a dictionary. 

        All provided legal documentation is verified to be up to date, legally accurate, and not subject to change.'''},
        {"role": "user", "content":''' Carefully read the entire legal documentation and answer the following from the documentation:
1. After reading the entire document, what is the simple answer to the user's query?
2. What exact text of the legal documentation shows the simple answer to the user's query?
3. What rights and privileges does a user have relating to their query?
4. What are restrictions, caveats, and conditions to the user's query?
5. What are any penalties, punishments, or crimes which apply to violating restrictions of the user's query?

For every question you answer with information from the legal documentation, annotate the answer with a citation using the format:
Question answer. (Section). 

If a question isn't related to the user's query, do not answer it.
         
The more detail you include in your answers, the more you help the user. Include all relevant information in each answer.

[User query: {}, Legal documentation:{}]'''.format(user_question, text)}]
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",messages=answer_prompt)
    result = chat_completion.choices[0].message.content
    return result
        
         
if __name__ == "__main__":
    main()