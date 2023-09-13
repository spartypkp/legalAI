import openai
import utilityFunctions as util
import config
import promptStorage as prompts


def main():
    pass

def answering_stage(question_list, legal_text, use_gpt_4=True):
    print("Starting answering stage...")
    full_result, total_prompt_tokens, total_completion_tokens = answer_all_questions(question_list, use_gpt_4, legal_text)
    return full_result, total_prompt_tokens, total_completion_tokens

def answer_all_questions(question_list, use_gpt_4, legal_text):
    full_result = ""
    total_prompt_tokens = 0
    total_completion_tokens = 0
    
    for i, question in enumerate(question_list):
        if i == 0 or i == 1:
            prompt_final_answer = prompts.get_prompt_simple_answer(legal_text, question)
        else:
            prompt_final_answer = prompts.get_prompt_final_answer(legal_text, question)
        result, prompt_tokens, completion_tokens, cost = answer_one_question(prompt_final_answer, use_gpt_4)
        
        full_result += result
        total_prompt_tokens += prompt_tokens
        total_completion_tokens += completion_tokens
        print(cost)
    return full_result, total_prompt_tokens, total_completion_tokens


def answer_one_question(prompt_final_answer, use_gpt_4):
    model = "gpt-3.5-turbo-16k"
    who = "will"
    if use_gpt_4:
        who = "sean"
        model = "gpt-4-32k"

    chat_completion = util.create_chat_completion(used_model=model, messages=prompt_final_answer, temp=0.2, api_key_choice=who)

    result_str = chat_completion.choices[0].message.content
    prompt_tokens = chat_completion.usage["prompt_tokens"]
    completion_tokens = chat_completion.usage["completion_tokens"]
    cost = util.calculate_prompt_cost(model, prompt_tokens, completion_tokens)
    return result_str, prompt_tokens, completion_tokens, cost

if __name__ == "__main__":
    main()