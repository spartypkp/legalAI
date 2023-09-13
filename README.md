# legalAI (Name subject to change)
created by Will Diamond 

## 1. What is legalAI?
LegalAI is a passion project which explores the applications of novel generative AI techniques to simplify the complexities of obtaining accurate legal information. I have created an AI program called Abe who is able to answer complex user legal questions. Abe will take in a user query, search for all relevant legal documentation, and create an in-depth answer which is returned to the user. Below is an example question answered by Abe.
### Example Question: Can I smoke cannabis?
**Rights to Possess, Use, and Distribute Cannabis and Cannabis Products**

Under Cal. HSC § 11362.1, a user aged 21 years or older has the right to possess, process, transport, purchase, obtain, or give away not more than 28.5 grams of cannabis not in the form of concentrated cannabis, and not more than eight grams of cannabis in the form of concentrated cannabis. They can also possess, plant, cultivate, harvest, dry, or process not more than six living cannabis plants and possess the cannabis produced by the plants. Additionally, they can smoke or ingest cannabis or cannabis products, and possess, transport, purchase, obtain, use, manufacture, or give away cannabis accessories to persons 21 years of age or older without any compensation. (Cal. HSC § 11362.1)

**Rights to Use Medical Cannabis**

Under Cal. HSC § 1649.2, a health care facility must permit patient use of medical cannabis. The patient or a primary caregiver is responsible for acquiring, retrieving, administering, and removing medicinal cannabis. The medicinal cannabis must be stored securely at all times in a locked container in the patient’s room, other designated area, or with the patient’s primary caregiver. (Cal. HSC § 1649.2)

**Rights to Possess, Use, and Distribute Cannabis Products**

According to Cal. HSC § 11018.1, "cannabis products" are defined as cannabis that has undergone a process whereby the plant material has been transformed into a concentrate, including, but not limited to, concentrated cannabis, or an edible or topical product containing cannabis or concentrated cannabis and other ingredients. This means that users also have the right to possess, use, and give away these types of cannabis products as well. (Cal. HSC § 11018.1)

**Rights Against Discrimination for Cannabis Use**

Under Cal. GOV § 12954, it is unlawful for an employer to discriminate against a person in hiring, termination, or any term or condition of employment, or otherwise penalizing a person, based on the person’s use of cannabis off the job and away from the workplace. This includes discrimination based on an employer-required drug screening test that has found the person to have nonpsychoactive cannabis metabolites in their hair, blood, urine, or other bodily fluids. (Cal. GOV § 12954)

**Rights to Use Cannabis for Animals**

The Medicinal and Adult-Use Cannabis Regulation and Safety Act establishes a comprehensive system to control and regulate the cultivation, distribution, transport, storage, manufacturing, processing, and sale of both medicinal cannabis and adult-use cannabis for adults 21 years of age and over. This includes cannabis products intended for use on, or consumption by, animals. (Cal. BPC § 26000)

**Rights to Have Cannabis Tested**

A user also has the right to have their cannabis and cannabis products tested by a licensed testing laboratory. This includes cannabis grown by the user for their own use. However, the testing laboratory cannot certify samples for resale or transfer to another person or licensee. (Cal. BPC § 26104)

**Rights to Possess, Use, and Distribute Cannabis Accessories**

"Cannabis accessories" are defined as any equipment, products or materials of any kind which are used, intended for use, or designed for use in planting, propagating, cultivating, growing, harvesting, manufacturing, compounding, converting, producing, processing, preparing, testing, analyzing, packaging, repackaging, storing, smoking, vaporizing, or containing cannabis, or for ingesting, inhaling, or otherwise introducing cannabis or cannabis products into the human body. This means that users also have the right to possess, use, and give away these types of cannabis accessories as well. (Cal. HSC § 11018.2)

**Rights to Administer Medicinal Cannabis at School**

The governing board of a school district, a county board of education, or the governing body of a charter school may adopt a policy that allows a parent or guardian of a pupil to possess and administer medicinal cannabis at a schoolsite to the pupil who is a qualified patient. However, the parent or guardian must not administer the medicinal cannabis in a manner that disrupts the educational environment or exposes other pupils, and after administering the medicinal cannabis, the parent or guardian must remove any remaining medicinal cannabis from the schoolsite. (Cal. EDC § 49414.1)

**Rights to Participate in Temporary Cannabis Events**

A user aged 21 years or older has the right to participate in temporary events where onsite cannabis sales and consumption are authorized, provided that the activities comply with the regulations promulgated and adopted by the department governing state temporary event licenses. The user also has the right to reconcile unsold inventory of cannabis or cannabis products and return it to the licensee’s retail premises after the temporary event. (Cal. BPC § 26200)

**Rights to Purchase Manufactured Cannabis Products**

A user has the right to purchase manufactured cannabis products that have been produced and packaged under specific standards. These products must not be designed to be appealing to children or easily confused with commercially sold candy or foods that do not contain cannabis. They must also be produced and sold with a standardized concentration of cannabinoids not to exceed 10 milligrams tetrahydrocannabinol (THC) per serving. If the cannabis product is intended for therapeutic effect or health supplementation use on, or for consumption by, an animal, the cannabis product shall also conform with any additional relevant standards. (Cal. BPC § 26130)

**Rights to Use Medicinal Cannabis While on Probation or Parole**

A criminal defendant who is eligible to use cannabis may request that the court confirm that he or she is allowed to use medicinal cannabis while he or she is on probation or released on bail. If a physician recommends that the probationer or defendant use medicinal cannabis, the probationer or defendant may request a modification of the conditions of probation or bail to authorize the use of medicinal cannabis. Similarly, any person who is to be released on parole and who is eligible to use medicinal cannabis may request that he or she be allowed to use medicinal cannabis during the period he or she is released on parole. If a physician recommends that the parolee use medicinal cannabis, the parolee may request a modification of the conditions of the parole to authorize the use of medicinal cannabis. (Cal. HSC § 11362.795)

**Rights to Possess Cannabis for Medical Needs**

A qualified patient or primary caregiver may possess no more than eight ounces of dried cannabis per qualified patient. In addition, a qualified patient or primary caregiver may also maintain no more than six mature or 12 immature cannabis plants per qualified patient. If a qualified patient or primary caregiver has a physician’s recommendation that this quantity does not meet the qualified patient’s medical needs, the qualified patient or primary caregiver may possess an amount of cannabis consistent with the patient’s needs. Counties and cities may retain or enact medicinal cannabis guidelines allowing qualified patients or primary caregivers to exceed the state limits set forth in subdivision (a). Only the dried mature processed flowers of female cannabis plant or the plant conversion shall be considered when determining allowable quantities of cannabis under this section. A qualified patient or a person holding a valid identification card, or the designated primary caregiver of that qualified patient or person, may possess amounts of cannabis consistent with this article. (Cal. HSC § 11362.77)

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

## 3. Project Status
   Legal AI is still in early development. So far, the entirety of the California Legal Code has been scraped from the official .gov website documentation (https://leginfo.legislature.ca.gov/faces/codes.xhtml). Using python, the data is read in, cleaned, and features are extracted from the raw text. Definitions, addendums, and section titles are extracted from the text and stored in their own columns. Each row in the database corresponds to a distinct section of the California Legal Code. Sections can be considered "leaf nodes" of the legal code tree, as a general rule being the smallest divisible piece of text. Codes are at the top level of the legal tree, followed by divisions/titles/.../Chapters which all are considered "parent" sections of a given section. All parent section's values are a useful positional identifier for a given leaf-node section. After cleaning and extraction, rows are inserted into a PostgreSQL table through the python package Psycopg2. Below is an example row containing the first section in the California constitution. <br>

| ID | Code | Division | Title | Part | Chapter | Article | Section | Raw Text Excluding Addendnum/Definitions | Addendnum - Date Added | Link |
| ---| ---- | -------- | ----- | ---- | ------- | ------- | ------- | ---------------------------------------- | ---------------------- | ---- |
|1  | CONS | 0        | 0	  | 0    | 0       |	I       |	1	   | All people are by nature free...blahblah |	(added Nov. 5, 1974..  | htt..|	

Headers for parent sections are given their own rows. After scraping and inserting to PostgreSQL, we have a table with 178,564 unique rows corresponding to actual sections in the California Legal Code.

Some quick analysis of the California Legal Code shows two things:
1. 99% of sections are short in length measured in tokens.
![log_token_distribution](https://github.com/spartypkp/legalAI/assets/59883254/f91ad92f-0ce7-4848-81c0-23c1da28f38a)
2. Certain codes contain MUCH more content than others.
![section_code_distribution](https://github.com/spartypkp/legalAI/assets/59883254/9b5029dc-d874-44ac-a859-c740a4b7d764)

It's interesting to help us understand the "normal" structure and format of a single law. This will be useful later when designing GPT prompts at scale, ie: Focus on finetuning prompts for dealing with 99% of the data formatting, worry about outliers later.


The next step is preparing the dataset for more efficient search and retrieval. Using OpenAI's embedding model "text-embeddings-ada-002", vector embeddings are automatically created for each section's:
   1. Raw section text
   2. Legal definitions applying specificially to this section and definitions applying to ALL parent sections.
   3. Titles of section and parent sections as if you were traversing the tree top to bottom.
      a) For section X, the path would look like("Code BPC, Division 10, Title 0, Part 0, Chapter 22, Article 7 , Section X")
      b) The title path trace would be ("Business Professions Code, Cannabis, Cannabis Cooperative Associations, Powers, Section X")

Below is a flowchart showing the flowchart of one "run" of the system. This flowchart assumes all previous data and embedding collection is complete.

![Flowchart](https://github.com/spartypkp/legalAI/assets/59883254/f8cd0cc9-2e69-40f4-8a6f-27fdef98d537)

I'm hoping to get a working prototype out within the next few weeks. Check back in at a later date or feel free to hit me up on linkedin.

## 4. A guide to installation and use
   TO DO: The project is currently not in a fully working state.
## 5. A list of technology used and any links to further information related to this technology
   Built in Python 3.8.9 in Visual Studio Code. Major python packages: psycopg2, openai, tokenify, beautifulSoup.
   - TODO: More version information
   PostgreSQL is used to store the database after scraping and cleaning.
   - TODO: More version information
   OpenAI: OpenAI is used to get text embeddings from the text-embeddings-ada-02 model. GPT 3.5 Turbo (maybe 4.0) will be used in the near future to incorporate embeddings into requests for legal information.

## 6.Open-source projects that the developers independently modify or expand should be contained in a section on “desired collaboration” in the readme.md file. How should problems be handled? How should developers advance the changes?
    Hypothetical Document Embedding HyDE: (https://arxiv.org/pdf/2212.10496.pdf)
## 7. Known bugs and any bug fixes
    A lot. Will update later upon public release.
## 8. FAQ section with all previously asked questions
    Will update later. Please reach out to me on LinkedIn if you have any questions, I would love to talk about the project! Please hire me.
## 9. Copyright and licensing information
    Will update later.
