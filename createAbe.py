import os
import openai
import config
import json
import compareEmedding
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
    
    user_question = input("Input a question to ask about the California legal code or a specific topic you would like to know more about.")
    topic_dict = get_similar_topics(user_question)
    topics_str = " ".join(topic_dict["queries"])
    
    rows = compareEmedding.compare_all_embeddings(topics_str, match_count=10)
    total_tokens = 0
    for row in rows:
        print(row)
        print("\n\n\n\n")
        total_tokens += row[10]

    
    print(total_tokens)
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

        Queries should include legal language and formal structure as you would see in an official legal document.

        Queries should not be in the format of questions.

        Return 10 relevant search queries.

        User question: "{}"
                    
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

def get_final_answer(user_question, text):
    answer_prompt= [
        {"role": "system", "content": '''You will be provided with a document delimited by triple quotes and a user question. Your task is to answer the question using only the provided document and to cite the passage(s) of the document used to answer the question. If the document does not contain the information needed to answer this question then simply write: "Insufficient information." If an answer to the question is provided, it must be annotated with a citation. Use the following format for to cite relevant passages ({"section": …}).
        All provided legal documentation is verified to be up to date, legally accurate, and not subject to change.'''},
        {"role": "user", "content": '''User Question: \"{}\"\nLegal Documentation:\'\'\'{}\'\'\''''.format(user_question, text)}]
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",messages=answer_prompt)
    result = chat_completion.choices[0].message.content
    return result
        
         
if __name__ == "__main__":
    main()