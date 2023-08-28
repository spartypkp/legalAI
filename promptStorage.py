import json
import psycopg2


GENERIC_SYSTEM_USER_MSG = '''[
{
"role": "system",
"content": "{}"
},
{
"role": "user",
"content": "{}"
}
]'''

def main():
    pass

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
    messages = GENERIC_SYSTEM_USER_MSG.format(system, user)
    return messages

def get_prompt_generate_hypothetical_questions(legal_text):
    system = '''You are an editor for a law firm that helps explain legal text. 

    You will be given a section of legal code delimitted by triple quotes. 

    Make a list of questions that could be answered by this section of legal code. Questions you make will be used to link a frequently asked section page to this document. 

    Be creative and create as many question as you can from every part of the text.

    '''
    user = " '''{}''' ".format(legal_text)
    messages = GENERIC_SYSTEM_USER_MSG.format(system, user)
    return messages

# ANSWER PROMPTS
def get_prompt_final_answer(user_query, legal_text):
    template = get_basic_universal_answer_template(user_query)
    system = '''You are a helpful legal assistant that answers a user query by summarizing information in a legal document.

        You will be provided with a user query and legal documentation in the format of a dictionary. 

        All provided legal documentation is verified to be up to date, legally accurate, and not subject to change.'''
    user = '''Carefully read the entire legal documentation and answer the following from the documentation:
        
        {}
         
        For every question you answer with information from the legal documentation, annotate the answer with a citation using the format:
        Question answer. (Section). 

        If a question isn't related to the user's query, do not answer it.
            
        The more detail you include in your answers, the more you help the user. Include all relevant information in each answer.

        [User query: {}, Legal documentation:{}]
    '''.format(template, user_query, legal_text)
    messages = GENERIC_SYSTEM_USER_MSG.format(system, user)
    return messages


# SCORING PROMPTS
def get_prompt_score_individual_question(legal_text, template_question, generated_answer):
    system= '''"As a sophisticated AI model trained on vast amounts of legal texts and familiar with the nuances of legal interpretation,
    carefully analyze the provided legal text. Consider the user's question and evaluate the relevance of the legal text to the question. 
    Further, judge the quality of the provided answer based on its fidelity to the legal text, its clarity, and its comprehensiveness. 
    Provide scores on a scale from 0 to 100 for both the relevance of the legal text and the quality of the answer.
    Your evaluation should be as precise and nuanced as a seasoned legal expert."
    '''
    user = '''Legal Text: {legal_text}\n\n
    User's Question: {user_question}\n\n"
    Generated Answer: {answer}\n\n"
    '''.format(legal_text, template_question, generated_answer)
    messages = GENERIC_SYSTEM_USER_MSG.format(system, user)
    return messages

def get_prompt_compare_questions():
    pass
# UNIVERSAL ANSWER TEMPLATES
def get_basic_universal_answer_template(user_query):
    basic_template=''' 
    1. After reading the entire document, what is the simple answer to {}? Show the exact text in the legal document that proves this.
    '''
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
