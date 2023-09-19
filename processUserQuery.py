import promptStorage as prompts
import openai
import json
import utilityFunctions as util



def main():
    pass

def find_and_replace_definitions(user_query):
    pass
    # Find relevant definition embeddings
    # Prompt gpt-4 to determine which definitions are most relevant
    # If there are multiple similar definitions, ask user to define which is most relevant
    # Reformat user_query with applicable definitions and return

def processing_stage(user_query):
    print("Starting processing stage...")
    # Get similar queries by calling GPT 3.5, maybe Google BARD instead
    similar_queries_list = []
    question_list = convert_query_to_question_list(user_query, used_model="gpt-3.5-turbo")
    
    for question in question_list:
        print(question)
        similar_query = get_similar_queries(question)
        print(similar_query)
        similar_queries_list.append(similar_query)
    return similar_queries_list, question_list

def convert_query_to_question_list(user_query, used_model):
    question_list = prompts.get_original_universal_answer_template(user_query)
    prompt_convert_question = prompts.get_prompt_convert_question(question_list)

    chat_completion =  util.create_chat_completion(used_model, api_key_choice="will", prompt_messages=prompt_convert_question, temp=0)
    converted_questions = chat_completion.choices[0].message.content
    
    converted_questions = converted_questions.split("\n")
    #print(converted_questions)
    #converted_questions.pop()
    return converted_questions


def get_similar_queries(user_query):
    prompt_similar_queries = prompts.get_prompt_similar_queries(user_query)
    chat_completion = util.create_chat_completion(prompt_messages=prompt_similar_queries)
    result = chat_completion.choices[0].message.content
    result_dct = json.loads(result)
    similar_queries = " ".join(result_dct["queries"])
    return similar_queries

def find_and_replace_definitions(user_query):
    pass

if __name__ == "__main__":
    main()