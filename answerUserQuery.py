import openai
import utilityFunctions as util
import config
import promptStorage as prompts
import time
import asyncio
import json

def main():
    
    with open("questionList.txt","r") as question_read:
        text = question_read.read()
        question_list = json.loads(text)
    question_read.close()
    with open("lawful.txt", "r") as lawful_read:
        text = lawful_read.read()
        lawful = json.loads(text)
    lawful_read.close()
    with open("unlawful.txt","r") as unlawful_read:
        text = unlawful_read.read()
        unlawful = json.loads(text)
    unlawful_read.close()
    
    # 15047 tokens
    #response_list = separate_answer(question_list[2], True, lawful[0:12], "gpt-3.5-turbo")
    #print(response_list)
    
    responses_list = separate_answer(question_list[2], True, lawful, "gpt-3.5-turbo")
    total_tokens = 0
    with open("OUTPUTFILE.txt","w") as write_file:
        for response in responses_list:
            if "[IGNORE]" in response:
                continue
            total_tokens += util.num_tokens_from_string(response)
            write_file.write(f"=====\n{response}\n")
            
    print(total_tokens)
    write_file.close()


def answering_stage(question_list, legal_text, use_gpt_4=True):
    print("Starting answering stage...")
    
    full_result, total_prompt_tokens, total_completion_tokens = answer_all_questions(question_list, use_gpt_4, legal_text)
    return full_result, total_prompt_tokens, total_completion_tokens

def separate_answer(question, use_gpt_4, legal_text, model):
    message_list = []
    response_list = []
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    for section in legal_text:
        message_list.append(prompts.get_prompt_simple_answer(section, question))
    
    begin = time.time()
    
    results = asyncio.run(util.get_completion_list(message_list, 100, used_model=model))
    
    for completion in results:
        #print(completion)
        prompt_tokens += completion["usage"]["prompt_tokens"]
        completion_tokens += completion["usage"]["completion_tokens"]
        total_tokens += completion["usage"]["total_tokens"]
        response_list.append(completion["choices"][0]["message"]["content"])
    total_cost = util.calculate_prompt_cost(model, prompt_tokens, completion_tokens)
    end = time.time()
    print("    * Total time: {}, Total Tokens: {}, Total Cost: ${}".format(round(end-begin, 2), total_tokens, round(total_cost, 2)))
    return response_list
    #print(response_list)


def answer_all_questions(question_list, use_gpt_4, legal_text):
    final_result = []
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_cost = 0
    n_questions = len(question_list)
    start_time = time.perf_counter()
    

    for i in range(2, n_questions):
        
        question = question_list[i]
        full_result = "Question {}: {}\n".format(i+1, question)
        print("  - Answering for question: ", question)

        starting_sections = legal_text[i][0]
        prompt = prompts.get_prompt_simple_answer(starting_sections, question)
        partial_answer, prompt_tokens, completion_tokens, cost = answer_one_question(prompt, True)
        #print("Starting answer: ", partial_answer)

        #results = asyncio.run(util.get_completion_list(content_list, 100))
        for j in range(1, len(legal_text[i])):
            
            section = legal_text[i][j]
            print(section)
            exit(1)
            prompt = prompts.get_prompt_iterate_answer_rights(section, question, partial_answer)
            partial_answer, prompt_tokens, completion_tokens, cost = answer_one_question(prompt, True)
            
            total_prompt_tokens += prompt_tokens
            total_completion_tokens += completion_tokens
            total_cost += cost
            
        #print("Current answer: ", partial_answer)
        prompt = prompts.get_prompt_refine_answer(question, partial_answer)
        chat_completion = util.create_chat_completion(used_model="gpt-4", prompt_messages=prompt, api_key_choice="sean")
        revised_answer = chat_completion.choices[0].message.content
        #print("Revised answer:", revised_answer)
        full_result += revised_answer
        full_result += "\n"
        final_result.append(full_result)
        print(final_result)
        print(cost)
        print("    * Time elapsed: ", round(time.perf_counter() - start_time, 3), "seconds.")
        return final_result, total_prompt_tokens, total_completion_tokens
        
        
        
    return final_result, total_prompt_tokens, total_completion_tokens


def answer_one_question(prompt_final_answer, use_gpt_4):
    model = "gpt-3.5-turbo-16k"
    who = "will"
    if use_gpt_4:
        who = "sean"
        model = "gpt-4"

    chat_completion = util.create_chat_completion(used_model=model, prompt_messages=prompt_final_answer, temp=0.2, api_key_choice=who)
    result_str = chat_completion.choices[0].message.content

    prompt_tokens = chat_completion.usage["prompt_tokens"]
    completion_tokens = chat_completion.usage["completion_tokens"]
    cost = util.calculate_prompt_cost(model, prompt_tokens, completion_tokens)
    return result_str, prompt_tokens, completion_tokens, cost




if __name__ == "__main__":
    main()