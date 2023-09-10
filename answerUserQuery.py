import openai
import utilityFunctions as util
import config


def main():
    pass

def get_final_answer(prompt_final_answer, use_gpt_4):
    used_model = "gpt-3.5-turbo-16k"
    if use_gpt_4:
        openai.api_key = config.seangrove_openai_key
        used_model = "gpt-4-32k"
        chat_completion = openai.ChatCompletion.create(model=used_model,messages=prompt_final_answer, temperature=0.2)
    else:
        chat_completion = openai.ChatCompletion.create(model=used_model,messages=prompt_final_answer, temperature=0.2)
    result_str = chat_completion.choices[0].message.content
    result = result_str.split("*")
    result = "\n".join(result[1:])
    prompt_tokens = chat_completion.usage["prompt_tokens"]
    completion_tokens = chat_completion.usage["completion_tokens"]
    cost = util.calculate_prompt_cost(used_model, prompt_tokens, completion_tokens)
    return result, prompt_tokens, completion_tokens, cost

if __name__ == "__main__":
    main()