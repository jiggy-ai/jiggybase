
# Is my data secure?

Yes, the documents you upload to a JiggyBase Collection are stored in a dedicated database separate from other collections and the data of other organizations.   Your data resides in a SOC2 Type 2 certified data center.    The team building and operating JiggyBase has prior experience with SOC2 certification and JiggyBase expects to be SOC2 Type 2 certified in early 2024.

Your chat messages are currently not saved by JiggyBase.  While subsets of your data and chat messages are sent to OpenAI via their APIs in order to provide the final model completions, [OpenAI does not use this data](https://openai.com/policies/api-data-usage-policies) for model training purposes or otherwise permanently store it. 


# Can I easily get my data out of JiggyBase?

Yes, we make it easy for you to get your data out of JiggyBase.  You can download a sqlite file that contains your document text data, metadata, embedding vectors, and embedding index.  This can be used directly in the open source hnsqlite package.

In the enterprise tier, there is even an option for JiggyBase to create ready-to-run docker container images with your latest data, so you can run your collections in production in your own infrastructure!


# Is JiggyBase open source?

Yes, the core of the JiggyBase service is based on the following open source packages:

- [Collection Index and Search & ChatGPT Plugin](https://github.com/jiggy-ai/jiggybase-chatgpt-retrieval-plugin)    
- [JiggyBase Chat UI (chat.jiggy.ai)](https://github.com/jiggy-ai/jiggybase-chatbot-ui)
- [Hnsqlite (Database integrating sqlite & hnswlib for vector search)](https://github.com/jiggy-ai/hnsqlite)
- [JiggyBase python client](https://github.com/jiggy-ai/jiggybase)


# What AI Models does JiggyBase use?

Our collection search and plugin search functionality are currently built with the OpenAI ada–002 embedding model.

Our chat application is currently built with OpenAI GPT-3.5-turbo, GPT-4 (aka ChatGPT APIs).

Please contact JiggyBase if you are interested in using other models with your data. 


# What is a Collection in JiggyBase?

A collection is a group of one or more documents that you upload to JiggyBase that are used to help inform ChatGPT model responses using knowledge in the documents.   


# What is a Page?

A page of text is considered to be about 500 words or about 700 tokens.   With extra document metadata one page of text ends up closer to 900 tokens as represented in the database.   For simplicity (and as a bonus to our customers) we consider 1 page of text  to be 1000 tokens for JiggyBase accounting purposes. 



# What is a Token?

A token is the basic unit of text, usually a short word or part of a longer word, that forms the input and output to language processing models such as ChatGPT.  On average one token corresponds to 0.75 words in English.  In JiggyBase we define a page of text to be 1000 tokens, which is roughly equal to 500 words of text plus associated metadata. 


# When using chat with my collections, are the responses taking into account knowledge from outside my collection?

The JiggyBase chat is responding using data from your collection plus a distillation of the data that the underlying ChatGPT model was trained on.  The JiggyBase prompt customization feature allows you to tune the response to more heavily favor the information in the prompt.  Contact JiggyBase support if you require assistance with this prompt tuning.  


# When using JiggyBase Chat, does the ChatGPT model use any internet search to help respond?

No, there is not internet search function; there model is responding based on the text passages we provide from your collection, your recent messages, and a distillation of the data the model was originally trained trained on.


# What else do you do with my data?

We use your data to provide the JiggyBase service.  Our policy is to not otherwise access or utilize user data unless it is necessary to address an issue with the system.


# How do I chat with my documents after uploading them?
C
lick on the orange “Go To Chat” button in the upper left hand corner of the page and then select the collection that contains the information you want to use in your chat.


# How do I select the documents that are used during a chat?

From the chat.jiggy.ai chat interface you can choose a collection from the dropdown menu that is used to inform the ChatGPT model completions with the relevant contents of the documents in that collection.  The chat currently works with one collection at a time, but you can change the  collection used for chat at any time.


# What types of tasks is JiggyBase best for?

Currently JiggyBase chat works best for answering questions from knowledge found scattered within a collection, where the knowledge can be surfaced via a semantic search based on the user’s chat messages.

Examples of good tasks:

For a collection with one contract document uploaded:  
Q: What are the cancellation terms in this contract?

For a collection with a lot of service manuals uploaded:
Q: What does error code E407 mean for the turbo-encabulator? 


# What type of tasks do not currently work well?

The current algorithm looks at a maximum of 4 to 8 text pages of content (for GPT-3.5 and GPT-4 respectively) when answering your question.    Queries that require more than 4 to 8 pages of content to answer are currently not a good fit. 

Examples of tasks that are not currently a good fit:

For a collection with one document uploaded:  
Q:  Summarize this document

Why it may not work: The current logic performs a query and reads 4-8 pages of context to answer a question. If the document is larger than 4-8 pages then the summarization will be based on incomplete information.

For a collection with one contract uploaded:  
Q: What are the red flags in this contract?

Why it probably won’t work:  The current logic performs a query and reads 4-8 pages of context to answer a question.   Because we cannot perform a reliable semantic search for “red flags” the query portion is unlikely to produce the good results, and because the language model is only seeing a subset of the document it is likely to miss things.  


Please get in contact with us if you have workflows that require full document summarization, explicit comparison of different documents, or processing of entire documents to extract specific sets of information as we are working on extensions to JiggyBase to support these use cases.


# Is JiggyBase SOC2 certified?

Not currently,  but the team building and operating JiggyBase has prior experience with SOC2 certification and JiggyBase expects to be SOC2 Type 2 certified in early 2024.


# Who is JiggyBase?

JiggyBase was founded in May 2023 by Amy Wang and Bill Kish, entrepreneurs who have worked together for over a decade at multiple startups.  Bill started his career as an early employee at several successful networking equipment startups after graduating from Carnegie Mellon University with a degree in Computer Engineering.  Amy narrowly escaped from Tsinghua University and earned her EE PhD from Columbia University, complete with a stint at Bell Labs.  Around 2004, Bill started Ruckus Wireless, which, after hiring Amy, grew to be the third largest enterprise WiFi company in the world, going public on the NYSE in 2012.  In 2015, Bill and Amy founded Cogniac, an industrial AI computer vision company which now has some of the largest scale industrial vision applications in production in the world. Their largest customer uses Cogniac to inspect millions of images a day to help prevent very bad things from happening to freight trains.  

Now with JiggyBase they are excited to start building again.  Transformer neural network architectures trained on the sum of the Internet and scaled up with cleverness and compute result in something at least as magical as the previous tech mega-waves of semiconductors, internet, and mobile.  The applications of GPT-class models are going to touch every business in the world, multiple times over.  JiggyBase is building the fabric that allows this highly capable AI to work with and amplify the knowledge that makes your organization unique, while preserving that knowledge for the benefit of your organization.  



