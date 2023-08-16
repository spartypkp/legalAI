# legalAI (Name subject to change)
created by Will Diamond 

#### 1. What is legalAI?
LegalAI is a passion project which strives to explore and simplify the complexities of obtaining legal information. For US citizens it can be incredibly difficult to find answers to simple legal questions such as "is marijuana legal in california?". The top google search result for this question returns "Today, cannabis is legal in California for both medicinal and adult (recreational) use." Seems simple enough, but often a user would like to know more specific rules, limitations, and caveats which cannot be easily found. For more complex legal questions a top level google search is not nearly enough, instead prompting you to seek help from a legal professional. If you are committed to finding an answer you can attempt to search through the official California Legislative Code, although unless you have a degree in law, (I don't) it's probably not worth your time because of the inherent complexity.

The idea of legalAI is to use Machine Learning and AI principles to construct a program which can help a user find any legal information they need. LegalAI will be able to quickly answer simple questions while maintaining the ability to show the user specific rules, limitations, and caveats pertaining to the question. Through a discourse with legalAI, a user should be able to narrow down and find the exact information they need without having to exactly know the legal definitions and requirements. LegalAI will be able to directly cite sources from the California Legal Code and show exact text upon request. LegalAI has the knowledge of the entire California Legal Code and can answer questions of any complexity.

The ultimate goal of the current iteration of legalAI is to create an AI chatbot capable of conversing with a user, summarizing and extracting relevant text, and answering all legal questions with legal information to the best of its ability. All source material is directly scraped from the official California Legislature Legal Code. Exact text can be provided, along with citations, and instructions on how to find the information on the official documentation itself. In uncertain times it's difficult to fully understand all your rights as a citizen of the United States. LegalAI's goal is to be a tool for everyday citizens to provide accurate legal information easily, quickly, and with the ability to answer questions about every official piece of legislation that affects you.

#### 2. Project Status
   Legal AI is still in early development. So far, the entirety of the California Legal Code has been scraped from the official .gov documentation. Using python, the data is read in, cleaned, and features are extracted from the raw text. Each piece of legislation is separated by a multitude of hierarchiecal identifiers. In descending order it goes: Code identifier, Division, Title, Part, Chapter, Article, Section. 
   Below is a random example for the Food and Agriculture Code (FAC).
   FAC - Division 22 - Title 0 - Part 2 - Chapter 9.5 - Article 6 - Section 71123: Every person who handles rice in any quantity shall keep a complete and accurate record of all transactions involving the purchase or sale of rice and shall submit the record to the commission in the time and manner specified by the commission....
   
The section is the smallest way to divide a legislative code and is therefore the base we use. Every section has its own heirarchiecal identifiers to exactly categorize where it exists in the legal code. There are currently 178, 581 unique sections in the California Legal Code. For each section, the section text is parsed into OpenAI.createEmbedding to return a vector embedding of the text. The section identifiers, text, embedding, https link, and other attributes are then loaded into a postGresSQL table as a unique row using psycopg2.
  Currently, I am working on the implementation of searching for specific relevant text using cosine search on vector embeddings. Next, these embeddings can be fed to GPT 3.5 in a prompt in order to help answer a user's legal question.
Possible refinements to my strategy include using GPT 3.5 to automatically summarize and categorize entire Articles, Chapters, and even Divisions into "common" language. Embedding these summary and "common translations" will allow for a user's question to be searched on these instead. More analysis will have to be done on the accuracy of using GPT 3.5 summaries/translations as embeddings themselves. The project currently stands as an investigation into how AI can conduct a unique combination of search, recommendation, and classification. Everything is subject to change, so check back in for updates on the direction and scope of the project!

#### 3. A guide to installation and use
   TO DO: I'm a very junior programmer.
#### 4. A list of technology used and any links to further information related to this technology
   Built in Python 3.8.9 in Visual Studio Code. Major python packages: psycopg2, openai, tokenify, beautifulSoup.
   - TODO: More version information
   PostgreSQL is used to store the database after scraping and cleaning.
   - TODO: More version information
   OpenAI: OpenAI is used to get text embeddings from the text-embeddings-ada-02 model. GPT 3.5 Turbo (maybe 4.0) will be used in the near future to incorporate embeddings into requests for legal information.

#### 5.Open-source projects that the developers independently modify or expand should be contained in a section on “desired collaboration” in the readme.md file. How should problems be handled? How should developers advance the changes?
    Will update later.
#### 6. Known bugs and any bug fixes
    A lot. Will update later.
#### 7. FAQ section with all previously asked questions
    Will update later. Please reach out to me on LinkedIn if you have any questions, I would love to talk about the project! Please hire me.
#### 8. Copyright and licensing information
    Will update later.
