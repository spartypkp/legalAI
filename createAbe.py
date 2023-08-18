import os
import openai
import config
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

    system_prompt = """You will be provided with a document delimited by triple quotes. 
    The document contains key words encapsulated in double quotes and immediately followed by the key word's definition.
    Key word and definitions can apply to the category, Division, Title, Part, Chapter, Article, Section, or subdivision.

    Use the following step by step instruction to respond to user inputs.
    Step 1 - Search the document for key words and following definition.
    Step 2 - Print out the key word and definition.
    Step 3 - Repeat until all key words and definitions are found.
    Step 4 - Finally, determine which category these key word and definition pairs apply to and print it out to the user. 
    
    Definitions which have text longer than two sentences can be cut off after two sentences.
    """

    response = openai.ChatCompletion.create(
              model="MODEL_NAME",
              messages=[{"role": "system", "content": 'SPECIFY HOW THE AI ASSISTANT SHOULD BEHAVE'},
                        {"role": "user", "content": 'SPECIFY WANT YOU WANT THE AI ASSISTANT TO SAY'}
              ])





if __name__ == "__main__":
    main()