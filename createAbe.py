import os
import openai
import config
import json
import compareEmedding
import promptStorage as prompts

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

# gpt-4 (8k token limit)
# 
# $0.03/1k prompt tokens
# $0.06/1k sampled tokens

# gpt-4-32k
# $0.06/1k prompt tokens
# $0.12/1k sampled tokens

def main():
    user_query = input("What question would you like abe to answer?\n")
    ask_abe(user_query)
    
    
def ask_abe(user_query):  
    # Get similar queries by calling GPT 3.5, maybe Google BARD instead
    topic_dict = get_similar_queries(user_query)
    topics_str = " ".join(topic_dict["queries"])
    # Debug prints, print related queries
    print("\n\n Calling GPT 3.5 to generate related questions...: \n", topics_str)
    print("\n Comparing vector embeddings in the database to embedding of all related quries....\n")
    # Get cosine similarity score of related queries to all content embeddings
    rows = compareEmedding.compare_all_embeddings(user_query, print_relevant_sections=True, match_count=20)
    formatted_section = compareEmedding.format_sql_rows(rows)

    # continue to answer = input("Would you like to continue to GPT 4's answer? (y/n):\n")
    
    continue_to_answer = "y"
    if continue_to_answer == "y":
        print("Using gpt-3.5-turbo, 16k token limit")
        final_answer = get_final_answer(user_query, rows)
        print("\n\n")
        print(final_answer)
        '''
        print("Using gpt-4-32k, sorry Sean it's expensive")
        final_answer = get_final_answer(user_query, rows, use_gpt_4=True)
        print("\n\n")
        print(final_answer)
        '''
        return final_answer, formatted_section

def get_similar_queries(user_query):
    prompt_similar_queries = prompts.get_prompt_similar_queries(user_query)
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=prompt_similar_queries, temperature=0.4)
    result = chat_completion.choices[0].message.content
    result_dct = json.loads(result)
    return result_dct

def generate_hypothetical_questions():
    prompt = prompts.get_prompt_generate_hypothetical_questions()
    # Call openai.ChatCompletion.create(model, messages=, temperature=)
    return

def calculate_prompt_cost(model, prompt_tokens, completion_tokens):
    model_rates = {"gpt-3.5-turbo-16k":[0.003, 0.004], "gpt-3.5-turbo-4k":[0.0015, 0.002], "gpt-4":[0.03, 0.06], "gpt-4-32k":[0.06, 0.12]}
    prompt_rate = model_rates[model][0]
    completion_rate = model_rates[model][1]
    cost = ((prompt_rate/1000)*prompt_tokens) + ((completion_rate/100)*completion_tokens)
    print("Prompt Tokens: {}, Completion Tokens: {}".format(prompt_tokens, completion_tokens))
    print("Total cost of using {}: ${}".format(model, cost))
    return cost

def get_final_answer(user_query, rows, use_gpt_4=False):
    current_tokens = 0
    row = 0
    legal_text = ""
    used_model = "gpt-3.5-turbo-16k"
    if use_gpt_4:
        max_tokens = 24000
    else:
        max_tokens = 12000
    while current_tokens < max_tokens and row < len(rows):
        #print(rows[row])
        current_tokens += rows[row][10]
        legal_text = legal_text + "\n" + rows[row][9]
        row += 1
    #print("Number of tokens in legal_text: ", current_tokens)
    prompt_convert_question = prompts.get_prompt_convert_question(user_query)
    chat_completion =  openai.ChatCompletion.create(model=used_model,messages=prompt_convert_question, temperature=0)
    converted_questions = chat_completion.choices[0].message.content
    template = prompts.get_basic_universal_answer_template(user_query, converted_questions)
    prompt_final_answer= prompts.get_prompt_final_answer(user_query, legal_text, template)
    
    if use_gpt_4:
        openai.api_key = config.seangrove_openai_key
        used_model = "gpt-4-32k"
        chat_completion = openai.ChatCompletion.create(model=used_model,messages=prompt_final_answer, temperature=0.2)
    else:
        chat_completion = openai.ChatCompletion.create(model=used_model,messages=prompt_final_answer, temperature=0.2)
    result = chat_completion.choices[0].message.content
    prompt_tokens = chat_completion.usage["prompt_tokens"]
    completion_tokens = chat_completion.usage["completion_tokens"]
    cost = calculate_prompt_cost(used_model, prompt_tokens, completion_tokens)
    return result

if __name__ == "__main__":
    main()