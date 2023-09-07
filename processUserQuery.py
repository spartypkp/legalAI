import promptStorage as prompts
import openai
import json



def main():
    pass

def convert_query_to_template(user_query, used_model):
    prompt_convert_question = prompts.get_prompt_convert_question(user_query)
    chat_completion =  openai.ChatCompletion.create(model=used_model,messages=prompt_convert_question, temperature=0)
    converted_questions = chat_completion.choices[0].message.content
    template = prompts.get_basic_universal_answer_template(user_query, converted_questions)
    return template


def get_similar_queries(user_query):
    
    prompt_similar_queries = prompts.get_prompt_similar_queries(user_query)
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=prompt_similar_queries, temperature=0.4)
    result = chat_completion.choices[0].message.content
    result_dct = json.loads(result)
    similar_queries = " ".join(result_dct["queries"])
    print("\n\n Calling GPT 3.5 to generate related questions...: \n", similar_queries)
    return similar_queries

def find_and_replace_definitions(user_query):
    pass

if __name__ == "__main__":
    main()