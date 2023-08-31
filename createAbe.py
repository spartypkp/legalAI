import os
import openai
import config
import json
import utilityFunctions as util
import promptStorage as prompts

openai.api_key = config.spartypkp_openai_key



def main():
    '''
    with open("testQueries.txt", "r") as test_file:
        text = test_file.read()
        dct = json.loads(text)
    test_file.close()
    print(dct)
    '''
    test = ["Yes, you can smoke cannabis if you are 21 years of age or older. (Cal. HSC § 11362.1)", 

"The exact legal text that permits smoking cannabis is: 'it shall be lawful under state and local law, and shall not be a violation of state or local law, for persons 21 years of age or older to: (4) Smoke or ingest cannabis or cannabis products.' (Cal. HSC § 11362.1)", 

"Users have the right to possess, process, transport, purchase, obtain, or give away to persons 21 years of age or older without any compensation whatsoever, not more than 28.5 grams of cannabis not in the form of concentrated cannabis. They can also possess, plant, cultivate, harvest, dry, or process not more than six living cannabis plants and possess the cannabis produced by the plants. (Cal. HSC § 11362.1)", 

"Restrictions to smoking cannabis include not smoking or ingesting cannabis in a public place, in a location where smoking tobacco is prohibited, within 1,000 feet of a school, day care center, or youth center while children are present, except in or upon the grounds of a private residence or if such smoking is not detectable by others on the grounds of the school, day care center, or youth center while children are present. You also cannot smoke or ingest cannabis while driving, operating a motor vehicle, boat, vessel, aircraft, or other vehicle used for transportation. (Cal. HSC § 11362.3)", 

"Penalties for violating restrictions of smoking cannabis are not specified in the provided legal documentation."]

    user_query = input("What question would you like abe to answer?\n")
    ask_abe(user_query)
    
# Starts one "run" of the project    
def ask_abe(user_query):  
    # Get similar queries by calling GPT 3.5, maybe Google BARD instead
    topic_dict = get_similar_queries(user_query)
    topics_str = " ".join(topic_dict["queries"])
    # Debug prints, print related queries
    print("\n\n Calling GPT 3.5 to generate related questions...: \n", topics_str)
    print("\n Comparing vector embeddings in the database to embedding of all related quries....\n")
    # Get cosine similarity score of related queries to all content embeddings
    rows = util.compare_all_embeddings(user_query, print_relevant_sections=True, match_count=20)
    

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
        return final_answer

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

def get_final_answer(user_query, rows, use_gpt_4=True):
    current_tokens = 0
    row = 0
    legal_text = []
    used_model = "gpt-3.5-turbo-16k"
    if use_gpt_4:
        max_tokens = 24000
    else:
        max_tokens = 12000
    while current_tokens < max_tokens and row < len(rows):
        #print(rows[row])
        current_tokens += rows[row][10]
        legal_text.append(rows[row])
        row += 1
        
    legal_text = util.format_sql_rows(legal_text)
    #print("Number of tokens in legal_text: ", current_tokens)
    prompt_convert_question = prompts.get_prompt_convert_question(user_query)
    chat_completion =  openai.ChatCompletion.create(model=used_model,messages=prompt_convert_question, temperature=0)
    converted_questions = chat_completion.choices[0].message.content
    template = prompts.get_basic_universal_answer_template(user_query, converted_questions)
    # This is stupid as fuck and I love it
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
    cost = util.calculate_prompt_cost(used_model, prompt_tokens, completion_tokens)
    result = result[1:len(result)-1]
    result = list(result)
    print(result)
    exit(1)
    test_all_questions(user_query, legal_text, template)
    return result

def find_and_replace_definitions(user_query):
    pass
    # Find relevant definition embeddings
    # Prompt gpt-4 to determine which definitions are most relevant
    # If there are multiple similar definitions, ask user to define which is most relevant
    # Reformat user_query with applicable definitions and return

def test_all_questions(user_query, legal_text, template, answer_list):
    questions_list = template.split("\n")
    # This is stupid as fuck and I love it
    try:
        while True:
            questions_list.remove(" ")
    except:
        pass
    try:
        while True:
            questions_list.remove("")
    except:
        pass
    print(questions_list)
    used_model = "gpt-4-32k"
    prompt_score_questions = prompts.get_prompt_score_questions(legal_text, questions_list, answer_list)
    chat_completion = openai.ChatCompletion.create(model=used_model, messages=prompt_score_questions)
    result = chat_completion.choices[0].message.content
    print(result)
    exit(1)
    relevance_scores = [0]
    answer_scores = [0]

    with open("testQueries.txt","r") as read_file:
        text = read_file.read()
        test_dict = json.loads(text)
    read_file.close()
    if user_query in test_dict:
        copy = test_dict[user_query]
        copy[legal_text] = legal_text
        copy["questions"][0]["best_answer"] = answer_list[0]
        copy["questions"][0]["best_answer_metadata"]["relevance_score"] = relevance_scores[0]
        copy["questions"][0]["best_answer_metadata"]["answer_score"] = answer_scores[0]
        


if __name__ == "__main__":
    main()