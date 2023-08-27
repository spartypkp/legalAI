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


def main():
    ask_abe("Placeholder")
    
    
    
def ask_abe(user_query):  
    user_query = input("What question would you like abe to answer?\n")
    topic_dict = get_similar_queries(user_query)
    topics_str = " ".join(topic_dict["queries"])
    print("\n\n Calling GPT 3.5 to generate related questions...: \n", topics_str)
    print("\n Comparing vector embeddings in the database to embedding of all related quries....\n")
    rows = compareEmedding.compare_all_embeddings(topics_str, print_relevant_sections=False, match_count=20)
    formatted_section = compareEmedding.format_sql_rows(rows)
    #continue_to_answer = input("These are all the relevant sections above. Would you like to continue to get a full answer from GPT? (y/n)")
    continue_to_answer = "y"
    if continue_to_answer == "y":
        print("Using gpt-3.5-turbo, 16k token limit")
        final_answer = get_final_answer(user_query, rows)
        print("\n\n")
        print(final_answer)
        print("Using gpt-4-32k, sorry Sean it's expensive")
        final_answer = get_final_answer(user_query, rows, use_gpt_4=True)
        print("\n\n")
        print(final_answer)
        return final_answer, formatted_section

def get_similar_queries(user_query):
    similar_topics= prompts.get_prompt_similar_queries(user_query)
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=similar_topics, temperature=0.4)
    result = chat_completion.choices[0].message.content
    result_dct = json.loads(result)
    return result_dct

def generate_hypothetical_questions():
    prompt = prompts.get_prompt_generate_hypothetical_questions()
    # Call openai.ChatCompletion.create(model, messages=, temperature=)
    return

def get_final_answer(user_query, rows, use_gpt_4=False):
    current_tokens = 0
    row = 0
    legal_text = ""
    if use_gpt_4:
        max_tokens = 24000
    else:
        max_tokens = 12000
    while current_tokens < max_tokens and row < len(rows):
        #print(rows[row])
        current_tokens += rows[row][10]
        legal_text = legal_text + "\n" + rows[row][9]
        row += 1
    
    answer_prompt= prompts.get_prompt_final_answer(user_query, legal_text)

    if use_gpt_4:
        openai.api_key = config.spartypkp_openai_key
        chat_completion = openai.ChatCompletion.create(model="gpt-4-32k",messages=answer_prompt, temperature=0.2)
    else:
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",messages=answer_prompt, temperature=0.2)
    result = chat_completion.choices[0].message.content
    return result

if __name__ == "__main__":
    main()