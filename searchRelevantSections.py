import json
import openai
import promptStorage as prompts
import embeddingSimilarity

def main():
    pass

def search_similar_content_sections(user_query, print_sections, matches=20):
    print("\n Comparing vector embeddings in the database to embedding of all related quries....\n")
    # Get cosine similarity score of related queries to all content embeddings
    rows = embeddingSimilarity.compare_content_embeddings(user_query, print_relevant_sections=print_sections, match_count=matches)
    return rows

def accumulate_legal_text_from_sections(sections, used_model):
    current_tokens = 0
    row = 0
    legal_text = []
    used_model = "gpt-3.5-turbo-16k"
    if used_model == "gpt-4-32k":
        max_tokens = 24000
    elif used_model == "gpt-4":
        max_tokens = 5000
    elif used_model == "gpt-3.5-turbo-16k":
        max_tokens = 12000
    elif used_model == "gpt-3.5-turbo":
        max_tokens = 2000

    while current_tokens < max_tokens and row < len(sections):
        current_tokens += sections[row][12]
        legal_text.append(sections[row])
        row += 1
    return legal_text, current_tokens

def format_legal_text(legal_text):
    legal_text = embeddingSimilarity.format_sql_rows(legal_text)
    return legal_text

if __name__ == "__main__":
    main()