import json
import psycopg2



def main():
    pass

def apply_to_generic(system, user):
    return [{"role": "system","content": "{}".format(system)},{"role": "user","content": "{}".format(user)}]
# PRE PROCESSING PROMPTS
def get_prompt_similar_queries(user_query):
    system = "All output shall be in JSON format."
    user = '''Generate an array of similar search queries that are relevant to the user query.

        Use a variation of related keywords for the queries, trying to be as general as possible.

        Queries should include legal language such as ["lawful", "violation", "authorized", "restrictions", "legitimate", "defined", "according to law", "legal"].

        Generate 15 queries of varying length.

        User query: {}
                    
        Format: {{\\"queries\\": [\\"query_1\\", \\"query_2\\", \\"query_3\\"]}}";
    '''.format(user_query)
    messages = apply_to_generic(system, user)
    return messages

def get_prompt_generate_hypothetical_questions(legal_text):
    system = '''You are an editor for a law firm that helps explain legal text. 

    You will be given a section of legal code delimitted by triple quotes. 

    Make a list of questions that could be answered by this section of legal code. Questions you make will be used to link a frequently asked section page to this document. 

    Be creative and create as many question as you can from every part of the text.

    '''
    user = " '''{}''' ".format(legal_text)
    messages = apply_to_generic(system, user)
    return messages

# ANSWER PROMPTS
def get_prompt_final_answer(user_query, legal_text, template):
    system = '''You are a helpful legal assistant that answers a user query by summarizing information in a legal document.

        You will be provided with a user query and legal documentation in the format of a dictionary. 

        Output will be in the format of a python list.

        All provided legal documentation is verified to be up to date, legally accurate, and not subject to change.'''
    user = '''Carefully read the entire legal documentation and answer the following from the documentation:
        
        {}
         
        For every question you answer with information from the legal documentation, annotate the answer with a citation using the format:
        Question answer. (Section). 

        Append each answer to the python output list.

        If a question isn't related to the user's query, do not answer it.
            
        The more detail you include in your answers, the more you help the user. Include all relevant information in each answer.

        [User query: {}, Legal documentation:{}]
    '''.format(template, user_query, legal_text)
    messages = apply_to_generic(system, user)
    return messages


# SCORING PROMPTS
def get_prompt_score_questions(legal_text, template_questions, generated_answers):
    system= '''You are LawProfessorGPT, a witheringly critical legal scholar who reviews answers to legal questions to ensure that they are comprehensive and grounded entirely in the provided legal text.

    You will be provided pairs of questions and answers to score.
    For each pair, answer the following questions and output a score in the format [(Relevance_score 1, Answer_score 1), (), (), (), ()].
        Relevance_score: Based on the provided legal text, how relevant are the given sections of legal text to the user's question (on a scale from 0 to 100)?
        Answer_score: How well does the provided answer address the user's question based on the legal text (on a scale from 0 to 100)?
    '''
    user = '''Legal Text: {}\n\n
    (Question 1: {}, Answer 1: {})\n
    (Question 2: {}, Answer 2: {})\n
    (Question 3: {}, Answer 3: {})\n
    (Question 4: {}, Answer 4: {})\n
    (Question 5: {}, Answer 5: {})\n
    '''.format(legal_text, template_questions[0], generated_answers[0],template_questions[1], generated_answers[1],template_questions[2], generated_answers[2],template_questions[3], generated_answers[3],template_questions[4], generated_answers[4])
    messages = apply_to_generic(system, user)
    return messages

def get_prompt_compare_questions():
    pass

def get_prompt_convert_question(user_query):
    system='''You will be provided with a user query and 3 generic questions.

    Rephrase question 3,4,5 by applying the topics in the user_query. Keep question 2 in its original phrasing.

    Output should be in a single string with the following format:
    2. QUESTION 2 \n
    3. QUESTION 3 \n
    4. QUESTION 4 \n
    5. QUESTION 5 \n
    '''
    user = '''User_Query: {}
    QUESTION 2: What is the exact legal text that answers the user query?
    Question 3: What rights and privileges does a user have relating to TOPICS?
    Question 4: What are restrictions, caveats, and conditions to TOPICS?
    Question 5: What are any penalties, punishments, or crimes which apply to violating restrictions of TOPICS?'''.format(user_query)
    messages = apply_to_generic(system, user)
    return messages

# UNIVERSAL ANSWER TEMPLATES
def get_basic_universal_answer_template(user_query, converted_questions):

    basic_template=''' 
    QUESTION 1: {}?
    {}
    '''.format(user_query, converted_questions)
    return basic_template

def get_original_universal_answer_template():
    original_template=''' 
    1. After reading the entire document, what is the simple answer to the user's query? One positive validation of the user's query overrides any other negatives in the documentation.
    2. What exact text of the legal documentation shows the simple answer to the user's query?
    3. What rights and privileges does a user have relating to their query?
    4. What are restrictions, caveats, and conditions to the user's query?
    5. What are any penalties, punishments, or crimes which apply to violating restrictions of the user's query?
    '''
    return original_template

def get_extended_universal_answer_template():
    extended_template='''
    1. After reading the entire document, what is the simple answer to the user's query? One positive validation of the user's query overrides any other negatives in the documentation.
    2. What exact text of the legal documentation shows the simple answer to the user's query?
    3. What rights and privileges does a user have relating to their query?
    4. What are restrictions, caveats, and conditions to the user's query?
    5. What are any penalties, punishments, or crimes which apply to violating restrictions of the user's query?
    6. What are other relevant sections cited in the document?
    7. If you can, answer the related questions:
    - Blah
    - Blah
    - Will be formatted
    8. Related questions that can't be answered:
    - Blah
    - Blah
    - Will be formatted
    '''
    return extended_template
