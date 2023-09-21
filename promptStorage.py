import json
import psycopg2
import answerUserQuery as answer

def main():
    pass

# Apply prompts to generic chatCompletion with a system and user, returns chatCompletion.messages
def apply_to_generic(system, user):
    return [{"role": "system","content": "{}".format(system)},{"role": "user","content": "{}".format(user)}]

# PRE PROCESSING PROMPTS ===============================================
# generates an array of similar search queries
def get_prompt_similar_queries_lawful(user_query):
    system = '''You are a helpful legal assistant that rephrases a user's legal question into many legal statements that include key terms. The goal is to generate 16 new legal statements that have the same terminology and format as actual legislation.

Generate legal statements that follow these criteria:
1. Include similar meaning of the original question.
2. Include variation of related keywords from this list ["Lawful", "legal", "valid", "warranted", "legitimate", "permissible", "rights", "privileges", "authority", "as authorized by", "as otherwise provided by law", "shall not be a violation of state or local law", "shall be lawful"]

Return in JSON format: {{\\"queries\\": [\\"query_1\\", \\"query_2\\", \\"query_3\\"]}}";.'''
    user = '''User question: {}'''.format(user_query)
    messages = apply_to_generic(system, user)
    return messages
def get_prompt_similar_queries_unlawful(user_query):
    system = '''You are a helpful legal assistant that rephrases a user's legal question into many legal statements that include key terms. The goal is to generate 16 new legal statements that have the same terminology and format as actual legislation.

Generate legal statements that follow these criteria:
1. Include similar meaning of the original question.
2. Include variation of related keywords from this list ["unlawful", "criminal", "illicit", "prohibited", "illegitimate", "against the law", "shall be punished", "guilty of", "restrictions", "does not permit", "violation", "the offense"]

Return in JSON format: {{\\"queries\\": [\\"query_1\\", \\"query_2\\", \\"query_3\\"]}}";.'''
    user = '''User question: {}'''.format(user_query)
    messages = apply_to_generic(system, user)
    return messages

# Generates hypothetical questions that could be answered by some legal text
def get_prompt_generate_hypothetical_questions(legal_text):
    system = '''You are an editor for a law firm that helps explain legal text. 

    You will be given a section of legal code delimitted by triple quotes. 

    Make a list of questions that could be answered by this section of legal code. Questions you make will be used to link a frequently asked section page to this document. 

    Be creative and create as many question as you can from every part of the text.

    '''
    user = " '''{}''' ".format(legal_text)
    messages = apply_to_generic(system, user)
    return messages

def get_prompt_extract_definitions(legal_text):
    system = '''You are a helpful assistant at a law firm. You help people by trimming unnecessary text off of definitions.

You will be provided with a legal term and a definition in the following format:
 '“TERM” means DEFINITION. Extraneous text'

Follow these steps:
1. Take your time to read each sentence in order. The first sentence is guaranteed to be part of the definition.
2. For each sentence, determine if it is strictly defining the term and explain your reasoning.
3. If at any time the current sentence does not strictly define the meaning of the term, cut the remaining text and print out the text to the user.
4. If all sentences do strictly define the meaning of the term, return the exact provided input text to the user. 

Before displaying your answer to the user, remove your reasoning.
'''
    user = "{}".format(legal_text)
    messages = apply_to_generic(system, user)
    return messages

# ANSWER PROMPTS ===============================================
# Using legal text as input, answer all questions from a specific answer template

def get_prompt_summarize_answer(question, partial_answer):
    # 201 tokens in system message
    system = '''As a professional summarizer, create a concise and comprehensive summary of the provided legal documentation already verified by an expert. The summary should collect and reorganize legal text sections to help answer a user's question in full detail.

You will be provided with legal documentation, separated by '====', and a user question.

1. Craft a summary that is detailed, thorough, in-depth, and complex, while maintaining clarity and conciseness.

2. Incorporate main ideas and essential information and focusing on critical aspects.

3. Rely strictly on the provided text, without including external information.

4. Format the summary in paragraph form for easy understanding.

5. Utilize markdown to cleanly format your output.
-give meaningful titles for distinct parts of the summary
-Subparts of each distinct part that list multiple concepts should be listed in line before continuing your answer.
-All citations should be surrounded by parenthesis like (Cal. HSC § 11362.1)
    '''
    user = '''User Legal Question: {}
    Legal Documentation: {}
    '''.format(question, partial_answer)
    messages = apply_to_generic(system, user)
    return messages

def get_prompt_iterate_answer_rights(legal_text, question, previous_answer):
    system = '''As a helpful legal assistant, your goal is to answer a legal question by improving a partial answer provided by an expert. You will also have access to a new section of legal text that may help enhance the partial answer. Your task is to carefully read the legal text and modify the partial answer by correcting mistakes, adding new relevant information, or doing nothing if the section isn't relevant. If you add new information, make sure to cite the current section. Your final response should provide an improved partial answer to the user's question.
    You will be provided with three things by the user:
    1. Question: A legal question which you are helping to answer.
    2. Partial Answer: A partial answer to the question already partially answered by an expert.
    3. Legal Text: A new section of legal text that might help further improve the partial answer.

    
    Include a citation of any relevant legal principles or statutes from the legal text that support or clarify the partial answer.
    Example Citation Format:
        REVISED ANSWER (Cal. HSC § 11362.785)
    Ensure the revised partial answer is clear and concise, addressing the specific legal question asked.
    '''
    user='''question:{}
    partial answer: {}
    legal text: {}
    '''.format(question, previous_answer, legal_text)
    messages = apply_to_generic(system, user)
    return messages

def get_prompt_simple_answer(legal_text, question):
    system = '''As a helpful legal assistant, your goal is to answer a user's question by referencing information in a legal document. Your answer should be brief, concise, and provide a simple response to the question. Once you have answered the question accurately, exit the conversation. All provided legal documentation is verified to be up to date, legally accurate, and not subject to change.
    Include a citation of any relevant legal principles or statutes from the legal text that support the answer given.
    Citation Format Example: (Cal. HSC § 11362.785)
        
    Ensure the generated answer directly addresses the question asked by the user.
    If absolutely none of the legal text does not specifically address the question, return "[IGNORE]" at the end of your answer.
    '''
    user = '''Read the entire legal documentation and answer the following question from the documentation:
    Question: {}
    Legal documentation:{}'''.format(question, legal_text)
    messages = apply_to_generic(system, user)
    return messages

def get_prompt_update_answer(legal_text, question):
    system = '''As a helpful legal assistant, answer a legal question in a simple and concise manner. You will be provided with a legal question and accompanying legal documentation. 

Follow these guidelines:
1. Ensure the answer directly addresses the legal question and is easy to understand.
2. Include a clear citation to the specific legal section that supports the answer.
3. Keep the answer concise, and answer the question in 1 topic sentence.
4. If you can answer yes or no to the question, include yes or no in your answer.

    '''
    user = '''question: {}
    documentation: {}'''.format(question, legal_text)
    messages = apply_to_generic(system, user)
    return messages

# SCORING PROMPTS ===============================================
# Score questions on a) relevancy of legal text (sections) to user's question, b) quality of generated answer based on legal text
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

# TODO: Compare two answers and their relevant template questions
def get_prompt_compare_questions():
    pass

# Combine and rephrase all template questions to ask about specific topics in a user query
def get_prompt_convert_question(question_list):
    n_questions = len(question_list)
    system_format = ""
    
    for i in range(0, n_questions-1):
        system_format += "QUESTION {}:".format(i+1)
    
    system='''You will be provided with a user query and generic questions.

    Rephrase all questions by applying the topics in the user_query. Keep question 1 and 2 in their original phrasing.

    Output should be in a single string with the following format:
    {}
    '''.format(system_format)
    user = question_list
    messages = apply_to_generic(system, user)
    return messages

# UNIVERSAL ANSWER TEMPLATES ===============================================

# USE THIS
def get_original_universal_answer_template(user_query):
    template = ["User_Query: {}\n".format(user_query),
    "QUESTION 1: What is the simple answer to {}?\n".format(user_query),
    "QUESTION 2: What is the exact legal text that answers {}?\n".format(user_query),
    "Question 3: What rights and privileges does a user have relating to TOPICS?\n",
    "Question 4: What are restrictions, caveats, and conditions to TOPICS?\n",
    "Question 5: What are any penalties, punishments, or crimes which apply to violating restrictions of TOPICS?"]
    return template

# Deprecated
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
