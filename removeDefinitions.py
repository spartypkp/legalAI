from calculateTokens import num_tokens_from_string as calc
import json
import re

def main():
    
    newText, topLevel, category = remove_manually(text)
    print("Text belongs to no higher section: ",topLevel)
    print("Category", category)
    print(newText)

    #1803511 token not including output


def remove_all_definitions():
    pass

def remove_manually(test_str):
    target = "following definitions"
    # 1. find start index of 'following definitions'
    i  = test_str.index(target)
    # 2. Set some initial values
    prev_section_start = 0
    next_subsection_start = test_str.index("(", i)
    end_section_start = len(test_str)
    topLevelDefinition = False
    category = None

    
    try:
        # Try and find the last subsection
        prev_section_start = test_str.rindex(")", 0, i)
        
        prev_id = test_str[prev_section_start-1]  #'h'
        prev_section_start -= 2
        
        # Find the next subsection using ord()+1
        next_id = chr(ord(prev_id)+1)
        
        end_of_definitions = "({})".format(next_id) +u'\xa0'
        print(end_of_definitions)
        end_section_start = test_str.index(end_of_definitions, i, len(test_str))
        

    except Exception as e:
        print(e)
        # Entirety of text is definitions, no last subsection
        topLevelDefinition=True
        
    print("Prev:{},Next section:{}".format(prev_section_start, next_subsection_start))
    text_to_search = test_str[prev_section_start:next_subsection_start]
    if "division" in text_to_search:
        category = "division"
    elif "title" in text_to_search:
        category = "title"
    elif "part" in text_to_search:
        category = "part"
    elif "chapter" in text_to_search:
        category = "chapter"
    elif "article" in text_to_search:
        category = "article"
    else:
        return text_str, topLevelDefinition, "section"
        
    
    newText = test_str[0:prev_section_start] + test_str[end_section_start:]

    return newText, topLevelDefinition, category



if __name__ == "__main__":
    main()