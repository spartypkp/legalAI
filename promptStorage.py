import json
import psycopg2

def main():
    pass

def get_prompt_similar_queries(user_query):
    prompt = [
        {"role": "system", "content": "All output shall be in JSON format."},
        {"role": "user", "content": '''Generate an array of search queries that are relevant to this question.

        Use a variation of related keywords for the queries, trying to be as general as possible.

        Queries should include legal language such as ["lawful", "violation", "authorized", "restrictions", "legitimate", "defined", "according to law", "legal"].

        Generate 15 queries of varying length.

        User question: {}
                    
        Format: {{\\"queries\\": [\\"query_1\\", \\"query_2\\", \\"query_3\\"]}}";'''.format(user_query)}]
    return prompt

def get_prompt_generate_hypothetical_questions():
    prompt1 = '''You are an editor for a law firm that helps explain legal text. 

    You will be given a section of legal code delimitted by triple quotes. 

    Make a list of questions that could be answered by this section of legal code. Questions you make will be used to link a frequently asked section page to this document. 

    Be creative and create as many question as you can from every part of the text.

    '''
    prompt2 = '''You are a helpful and thorough teachers assistant in a law school. You focus on assisting professors by creating rigorous questions that test's a student understanding of a piece of legislation.

    Generate questions that this piece of legislation answers.

    Read carefully and take your time. Create a list of 20 questions.
    '''
    return prompt1

def get_prompt_final_answer(user_query, legal_text):
    answer_prompt= [
        {"role": "system", "content": '''You are a helpful legal assistant that answers a user query by summarizing information in a legal document.

        You will be provided with a user query and legal documentation in the format of a dictionary. 

        All provided legal documentation is verified to be up to date, legally accurate, and not subject to change.'''},
        {"role": "user", "content":''' Carefully read the entire legal documentation and answer the following from the documentation:
        1. After reading the entire document, what is the simple answer to the user's query? One positive validation of the user's query overrides any other negatives in the documentation.
        2. What exact text of the legal documentation shows the simple answer to the user's query?
        3. What rights and privileges does a user have relating to their query?
        4. What are restrictions, caveats, and conditions to the user's query?
        5. What are any penalties, punishments, or crimes which apply to violating restrictions of the user's query?

        For every question you answer with information from the legal documentation, annotate the answer with a citation using the format:
        Question answer. (Section). 

        If a question isn't related to the user's query, do not answer it.
            
        The more detail you include in your answers, the more you help the user. Include all relevant information in each answer.

        [User query: {}, Legal documentation:{}]'''.format(user_query, legal_text)}]
    return answer_prompt

