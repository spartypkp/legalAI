import openai
import utilityFunctions as util
import config
import promptStorage as prompts


def main():
    pass

def answering_stage(question_list, legal_text, use_gpt_4=True):
    print("Starting answering stage...")
    print("================")
    full_result, total_prompt_tokens, total_completion_tokens = answer_all_questions(question_list, use_gpt_4, legal_text)
    return full_result, total_prompt_tokens, total_completion_tokens

def answer_all_questions(question_list, use_gpt_4, legal_text):
    final_result = [""]*len(question_list)
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_cost = 0
    n_questions = len(question_list)

    for i in range(2, n_questions):
        
        question = question_list[i]
        full_result = "Question {}: {}\n".format(i, question)
        print("Current question: ", question)

        starting_sections = legal_text[i][0] + legal_text[i][1] + legal_text[i][2] + legal_text[i][3]
        prompt = prompts.get_prompt_simple_answer(starting_sections, question)
        partial_answer, prompt_tokens, completion_tokens, cost = answer_one_question(prompt, True)
        print("Starting answer: ", partial_answer)

        for j in range(4, len(legal_text[i])):
            section = legal_text[i][j]
            #print("\n i: {}, section: {}\n".format(i, section))
            prompt = prompts.get_prompt_iterate_answer_rights(section, question, partial_answer)
            partial_answer, prompt_tokens, completion_tokens, cost = answer_one_question(prompt, True)
            #print(partial_answer)
            total_prompt_tokens += prompt_tokens
            total_completion_tokens += completion_tokens
            total_cost += cost
            
        
        prompt = prompts.get_prompt_refine_answer(question, partial_answer)
        chat_completion = util.create_chat_completion(used_model="gpt-4", prompt_messages=prompt, api_key_choice="sean")
        revised_answer = chat_completion.choices[0].message.content
        full_result += revised_answer
        full_result += "\n"
        final_result += full_result
        print(final_result)
        print(cost)
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