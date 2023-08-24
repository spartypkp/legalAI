# legalAI (Name subject to change)
created by Will Diamond 

## 1. What is legalAI?
LegalAI is a passion project which strives to explore and simplify the complexities of obtaining legal information. This project is being implemented to achieve the following goals:
#### Project Goals
   1. Allow for smarter legal information search which includes more than just a simple answer to the question: "Is X legal?". Given a simple legal topic or question, legalAI will be able to provide all useful information about the topic, answered by GPT 4 following the format of a "Universal Question Answer". These universal questions are outlined in the universal answer document and will eliminate the need for followup queries of basic information. In one "run" of the program, a user should be able to ask a simple question and receive an answer which includes everything they want to know (even though they may not have directly asked for it).
   2. Simplify the surprisingly difficult task of searching for legal information. Complex legal questions about very specific topics can be hard to find on the internet and combing through the legal code is no easy task (trust me). LegalAI strives to provide accurate legal information to someone regardless of their legal knowledge or technological ability.
   3. Show exact source text and use citations when answering a complex legal question. It's important to me that our process to answer legal questions is transparent and we show exactly where our answers are found in official legislation. Answers to users that incorporate multiple ideas from different sections will cite those different sections in-line. After each answer we will provide to the user links and references to the exact text and legislation referred to in the answer, if they so wish to read for themselves.
   4. Remove the barriers to access legal information. Aware of legal information or not, citizens are governed by a multitude of laws which can be difficult to comprehend. I believe it's important for everyone to be able to find out exactly what law, statues, regulations, or legislation applies to them wherever they may be.

The ultimate goal of the current iteration of legalAI is to create an AI chatbot capable of conversing with a user, summarizing and extracting relevant text, and answering all legal questions with legal information to the best of its ability. All source material is directly scraped from the official California Legislature Legal Code. Exact text can be provided, along with citations, and instructions on how to find the information on the official documentation itself. In uncertain times it's difficult to fully understand all your rights as a citizen of the United States. LegalAI's goal is to be a tool for everyday citizens to provide accurate legal information easily, quickly, and with the ability to answer questions about every official piece of legislation that affects you.

## 2. What is legalAI not?
LegalAI is NOT a replacement for a licensed legal professional. 
#### LegalAI is NOT intended or designed to do the following:
   1. Provide any legal advice.
   2. Give recommendations or instructions on a legal course of action.
   3. Be used in a legal defense.
   4. Replace a human lawyer, attorney, or licensed legal professional.
   5. Give advice on ANYTHING to do or say in a legal court of law.
      
LegalAI is simply intended as a tool to provide legal information, nothing more. Currently it's at the proof of concept stage, but I am excited to be able to work on it and advance the project to its goals.

## 2. Project Status
   Legal AI is still in early development. So far, the entirety of the California Legal Code has been scraped from the official .gov website documentation (https://leginfo.legislature.ca.gov/faces/codes.xhtml). Using python, the data is read in, cleaned, and features are extracted from the raw text. Definitions, addendums, and section titles are extracted from the text and stored in their own columns. Each row in the database corresponds to a distinct section of the California Legal Code. Sections can be considered "leaf nodes" of the legal code tree, as a general rule being the smallest divisible piece of text. Codes are at the top level of the legal tree, followed by divisions/titles/.../Chapters which all are considered "parent" sections of a given section. All parent section's values are a useful positional identifier for a given leaf-node section. After cleaning and extraction, rows are inserted into a PostgreSQL table through the python package Psycopg2. Below is an example row containing the first section in the California constitution.\n
   ID | Code | Division | Title | Part | Chapter | Article | Section | Raw Text Excluding Addendnum/Definitions | Addendnum - Date Added | Link | Titles | Definitions | Total Tokens
   1  | CONS | 0        | 0	  | 0    | 0       |	I       |	1	   | All people are by nature free...blahblah |	(added Nov. 5, 1974..  | htt..| ...    | None        | 290			

Headers for parent sections are given their own rows. After scraping and inserting to PostgreSQL, we have a table with 178,564 unique rows corresponding to actual sections in the California Legal Code.
   
The next step is preparing the dataset for more efficient search and retrieval. Using OpenAI's embedding model "text-embeddings-ada-002", vector embeddings are automatically created for each section's:
   1. Raw section text
   2. Legal definitions applying specificially to this section and definitions applying to ALL parent sections.
   3. Titles of section and parent sections as if you were traversing the tree top to bottom.
      a) For section X, the path would look like("Code BPC, Division 10, Title 0, Part 0, Chapter 22, Article 7 , Section X")
      b) The title path trace would be ("Business Professions Code, Cannabis, Cannabis Cooperative Associations, Powers, Section X")

Below is a flowchart showing the flowchart of one "run" of the system. This flowchart assumes all previous data and embedding collection is complete.

![Flowchart](https://github.com/spartypkp/legalAI/assets/59883254/f8cd0cc9-2e69-40f4-8a6f-27fdef98d537)

I'm hoping to get a working prototype out within the next few weeks. Check back in at a later date or feel free to hit me up on linkedin.

## 3. A guide to installation and use
   TO DO: The project is currently not in a fully working state.
## 4. A list of technology used and any links to further information related to this technology
   Built in Python 3.8.9 in Visual Studio Code. Major python packages: psycopg2, openai, tokenify, beautifulSoup.
   - TODO: More version information
   PostgreSQL is used to store the database after scraping and cleaning.
   - TODO: More version information
   OpenAI: OpenAI is used to get text embeddings from the text-embeddings-ada-02 model. GPT 3.5 Turbo (maybe 4.0) will be used in the near future to incorporate embeddings into requests for legal information.

## 5.Open-source projects that the developers independently modify or expand should be contained in a section on “desired collaboration” in the readme.md file. How should problems be handled? How should developers advance the changes?
    Hypothetical Document Embedding HyDE: (https://arxiv.org/pdf/2212.10496.pdf)
## 6. Known bugs and any bug fixes
    A lot. Will update later upon public release.
## 7. FAQ section with all previously asked questions
    Will update later. Please reach out to me on LinkedIn if you have any questions, I would love to talk about the project! Please hire me.
## 8. Copyright and licensing information
    Will update later.
