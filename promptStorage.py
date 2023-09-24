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

def get_prompt_summary_template(question, legal_documentation):
    # 201 tokens in system message
    system = '''Using the supplied legal question and its corresponding legal documentation, produce a markdown structure that outlines the essential themes and ideas. This structure will guide a legal expert in answering the posed question.

**Input Description:**

- **Question**: A distinct legal query needing expert interpretation.
- **Legal Documentation**: The reference material that a legal expert will use to formulate an answer.

**Instructions:**

1. Start by dissecting the question to understand its primary themes and key concerns.
2. Delve into the legal documentation, extracting the principal ideas and related concepts that will aid in answering the question.
3. While structuring the markdown:
   - Use "#" for principal ideas taken from the legal documentation.
   - For each main idea, establish secondary points and label them using "##".
   - Beneath each secondary point, highlight any tertiary points with "###". 
   - For each detail or specific concept which applies to an idea, write ">" and guidance to the legal expert on how to answer the legal question, as well as legal citations from where this answer may come from.
4. Keep the guidance concise, especially for the ">" level. Avoid placeholders or lengthy notes. The emphasis should be on clear headers and brief guidance.

The first main idea should always be a rephrasing of the question followed by a sub-idea called TLDR, which has guidance on giving a simple and short answer to the user question.

**Output:**

A carefully curated markdown blueprint with clear titles, headers, and succinct guidance. This blueprint should seamlessly guide a legal expert in their endeavor to comprehensively address the posed question using the supplied legal documentation. 
    '''
    user = json.dumps({"Question":question,"Legal Documentation":legal_documentation})
    messages = apply_to_generic(system, user)
    return messages

def get_prompt_populate_summary_template(question, template, legal_documentation):
    user = json.dumps({"Template":template,"Legal Documentation":legal_documentation,"Question":question})
    system = '''Using the provided markdown template and the associated legal documentation, improve the initial guidance from the legal expert to become a full answer with pertinent details and in line citations.

**Input Description:**

- **Template**: A structured markdown outline utilizing various levels of headers (#, ##, ###, ####). The ">" symbol in the template signifies guidance from a legal expert, which should be improved and refined.
  
- **Legal Documentation**: Your primary reference material containing all necessary information to address the legal question. Use this document to derive content to replace the guidance after the ">" in the template.
  
- **Question**: The specific legal inquiry that will be answered using the populated template and the legal documentation.

**Instructions:**

1. Thoroughly acquaint yourself with the template. Note areas marked by the ">" symbol; these are pointers from the legal expert that should be improved and refined with content and citations.
  
2. Delve into the legal documentation, sourcing information that aligns with the ">" pointers and the related headers.
  
3. In the sections with ">", substitute the expert's guidance with relevant content from the legal documentation, ensuring to include legal citations in line.
  
4. Emphasize accuracy and integrity, ensuring that the content reflects the essence and specifics of the original legal documentation.

**Output:**

A refined markdown template where guidance after the ">" symbol has been seamlessly refined with content from the legal documentation, resulting in a well-structured response to the legal inquiry.
    '''
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
