### What is JiggyBase?

JiggyBase is a service that enables you to extend ChatGPT with your own knowledge and data. It works by searching your documents and providing the contents to ChatGPT in a way that allows it to respond using the knowledge and data found therein. This is the single most powerful technique to avoid ChatGPT hallucinations and adapt ChatGPT to work with custom and current data.

### Does this use ChatGPT?

Yes, there are two different ways you can chat with ChatGPT using the knowledge in your JiggyBase documents.  

JiggyBase is available as a plugin on the ChatGPT Plugin store.  ChatGPT Plus subscribers can select it there and then chat with the GPT-4 plugin model which knows how to use JiggyBase to search through your document collections and use the information it finds there.

The chat.jiggy.ai chat interface is another option powered by OpenAI APIs, utilizing the same AI models that power OpenAI's ChatGPT service.  We enable the ChatGPT AI models to utilize the knowledge in your document collection in a way that keeps your data secure. 

### Is my data secure?

Yes, the documents you upload to a JiggyBase Collection are stored in a dedicated database separate from other collections and the data of other organizations.   Your data resides in a SOC2 Type 2 certified data center.    The team building and operating JiggyBase has prior experience with SOC2 certification and JiggyBase expects to be SOC2 Type 2 certified in early 2024.

Subsets of your data and chat messages are sent to OpenAI via their APIs in order to provide the AI model output, [OpenAI does not use this data](https://openai.com/policies/api-data-usage-policies) for model training purposes or otherwise permanently store it. 

### Will you sign an NDA to cover the data we upload to JiggyBase?

Sure, send us your NDA or you can request our [standard MNDA](https://app.commonpaper.com/pages/9752456e6f721fbf).

### Can I easily get my data out of JiggyBase?

Yes, we make it easy for you to get your data out of JiggyBase.  You can download a sqlite file that contains your document text data, metadata, embedding vectors, and embedding index.  This can be used directly in the open source hnsqlite package.

In the enterprise tier, there is even an option for JiggyBase to create ready-to-run docker container images with your latest data, so you can run your collections in production in your own infrastructure!

### Is JiggyBase open source?

Yes, the core of the JiggyBase service is based on the following open source packages:

- [Collection Index and Search & ChatGPT Plugin](https://github.com/jiggy-ai/jiggybase-chatgpt-retrieval-plugin)    
- [JiggyBase Chat UI (chat.jiggy.ai)](https://github.com/jiggy-ai/jiggybase-chatbot-ui)
- [Hnsqlite (Database integrating sqlite & hnswlib for vector search)](https://github.com/jiggy-ai/hnsqlite)
- [JiggyBase python client](https://github.com/jiggy-ai/jiggybase)

### Who is behind JiggyBase?

JiggyBase was founded in May 2023 by Amy Wang and Bill Kish, entrepreneurs who have worked together for over a decade at multiple startups.  Bill started his career as an early employee at several successful networking equipment startups after graduating from Carnegie Mellon University with a degree in Computer Engineering.  Amy narrowly escaped from Tsinghua University and earned her EE PhD from Columbia University, complete with a stint at Bell Labs.  Around 2004, Bill started Ruckus Wireless, which, after hiring Amy, grew to be the third largest enterprise WiFi company in the world, going public on the NYSE in 2012.  In 2015, Bill and Amy founded Cogniac, an industrial AI computer vision company which now has some of the largest scale industrial vision applications in production in the world. Their largest customer uses Cogniac to inspect millions of images a day to help prevent very bad things from happening to freight trains.  

Now with JiggyBase they are excited to start building again.  Transformer neural network architectures trained on the sum of the Internet and scaled up with cleverness and compute result in something at least as magical as the previous tech mega-waves of semiconductors, internet, and mobile.  The applications of GPT-class models are going to touch every business in the world, multiple times over.  JiggyBase is building the fabric that allows this highly capable AI to work with and amplify the knowledge that makes your organization unique, while preserving that knowledge for the benefit of your organization.  

### What AI Models does JiggyBase use?

Our collection search and plugin search functionality are currently built with the OpenAI ada–002 embedding model.

Our chat application is currently built with OpenAI GPT-3.5-turbo, GPT-4 (aka ChatGPT APIs).

Please contact JiggyBase if you are interested in using other models with your data. 


### What is a Collection in JiggyBase?

A collection is a group of one or more documents that you upload to JiggyBase that are used to help inform ChatGPT model responses using knowledge in the documents.   


### What is a Page?

A page of text is considered to be about 500 words of text. 

### What does a a page of text translate to and what is a token?

A page of text translates to about 700 tokens.   With extra document metadata one page of text ends up closer to 900 tokens as represented in the database.   For simplicity (and as a bonus to our customers) we consider 1 page of text  to be 1000 tokens for JiggyBase accounting purposes. 

Most JiggyBase users dont need to worry about tokens.  If you are interested, a token is the basic unit of text, usually a short word or part of a longer word, that forms the input and output of AI language models such as ChatGPT.  On average one token corresponds to 0.75 words in English.  In JiggyBase we define a page of text to be 1000 tokens, which is roughly equal to 500 words of text plus associated metadata. 


### When using chat with my collections, are the responses taking into account knowledge from outside my collection?

The JiggyBase chat is responding using data from your collection plus a distillation of the data that the underlying ChatGPT model was trained on.  The JiggyBase prompt customization feature allows you to tune the response to more heavily favor the information in the prompt.  Contact JiggyBase support if you require assistance with this prompt tuning.  


### When using JiggyBase Chat, does the ChatGPT model use any internet search to help respond?

No, there is no internet search function; the model is responding based on text passages selected from your collection, your recent messages, and a distillation of the data the model was originally trained trained on.


### What else do you do with my data?

We use your data to provide the JiggyBase service.  Our policy is to not otherwise access or utilize user data unless it is necessary to address an issue with the system.


### How do I chat with my documents after uploading them?

Click on the orange “Go To Chat” button in the upper left hand corner of the page to chat via chat.jiggy.ai and then select the collection that contains the information you want to use in your chat.  

Alternatively you can chat against your collections with ChatGPT Plus by enabling JiggyBase in the ChatGPT plugin store. 


### How do I select the documents that are used during a chat?

When chatting via the ChatGPT plugin, the collection is automatically selected via ChatGPT based on your messages.  In some cases you might need to guide ChatGPT into the right collection, but this effort can be minimized by providing clear names and descriptions for your collections within the JiggyBase management console.

From the chat.jiggy.ai chat interface you can choose a collection from the dropdown menu that is used to inform the ChatGPT model completions with the relevant contents of the documents in that collection.  The chat currently works with one collection at a time, but you can change the  collection used for chat at any time.

### What is happening behind the scenes when I chat on chat.jiggy.ai?

1. We take the last few messsages from your current chat history and run it through a query to GPT-3.5 where we ask GPT-3.5 to reformulate your message as a search query 

2. We take the reformulated search query and use that to perform a symantic search of your collection.  This returns the 4-8 pages of content that should be relevant to responding to your message.

3.  We feed that content into the model (GPT-3.5 or 4 depending on what you selected), along with your recent chat message history with instructions to GPT to respond using the retrieved content.

4. The GPT model responds to your message using the subset of relevant content that was retrieved from your collection.


### What types of tasks is JiggyBase best for?

Currently JiggyBase chat works best for answering questions from knowledge found scattered within a collection, where the knowledge can be surfaced via a semantic search based on the user’s chat messages.

Examples of good tasks:

For a collection with one contract document uploaded:  
Q: What are the cancellation terms in this contract?

For a collection with a lot of service manuals uploaded:
Q: What does error code E407 mean for the turbo-encabulator? 


### What type of tasks do not currently work well?

While your document collection can be quite large (many 1000's of pages of text depending on the subscription plan), the language models are limited in how much information they can process at a time.  

The current algorithm looks at a maximum of 4 to 8 text pages of content (for GPT-3.5 and GPT-4 respectively) when answering your question.    Queries that require more than 4 to 8 pages of content to answer are currently not a good fit. 

Examples of tasks that are not currently a good fit:

For a collection with one document uploaded:  
Q:  Summarize this document

Why it may not work: The current logic performs a query and reads 4-8 pages of context to answer a question. If the document is larger than 4-8 pages then the summarization will be based on incomplete information.

For a collection with one contract uploaded:  
Q: What are the red flags in this contract?

Why it probably won’t work:  The current logic performs a query and reads 4-8 pages of context to answer a question.   Because we cannot perform a reliable semantic search for “red flags” the query portion is unlikely to produce the good results, and because the language model is only seeing a subset of the document it is likely to miss things.  


Please get in contact with us if you have workflows that require full document summarization, explicit comparison of different documents, or processing of entire documents to extract specific sets of information as we are working on extensions to JiggyBase to support these use cases.

### What is the Collection description used for?

The collection description is use to help inform the language model and chat users the purpose of a collection and the type of information that can be found within it.  It is also helpful to provide an example of the type of question that users could answer using this collection.


### Is JiggyBase SOC2 certified?

Not currently,  but the team building and operating JiggyBase has prior experience with SOC2 certification and JiggyBase expects to be SOC2 Type 2 certified in early 2024.

### Can I invite friends or co-workers to my JiggyBase Organization?

Yes, JiggyBase is designed to work well for individuals, organizations, and teams.  You can invite others to your organization and control their level of access to Organization's collections.

### Can I add web site to a Collection?

We currently support adding a single web page at a time by sending a url to the chat.jiggy.ai interface. We will extend this capability over time.   Not all sites are supported since many make it difficult to extract readable text.


### Can I create unlimited number of trial accounts and use your awesomely augmented GPT-4 indefinitely for free?

Sorry, no, that is a violation of our terms of service. Also consider that the same AI embedding technology that allows us to help answer your questions so effectively also helps us detect duplicate accounts since duplicate accounts tend to chat in the same style and with similar content as the original account.


### Whats the difference between using JiggyBase with chat.jiggy.ai and with the ChatGPT Plugin?

The JiggyBase chat app at chat.jiggy.ai currently only accesses a single collection at a time while the JiggyBase ChatGPT plugin can access all of your collections from a single chat session.  There are other subtle differences in how the search terms are composed to search your collection documents.  The chat.jiggy.ai interface is built on top of OpenAI APIs, but unlike the default ChatGPT terms of service, OpenAI will not use your chat messages for training purposes when using the chat.jiggy.ai interface.   

One key difference is that when using the chat.jiggy.ai interfaces, your chat usage is subject to the message limit of your JiggyBase subscription plan tier.  When chatting via ChatGPT, you there is no per-message limit on JiggyBase and you are just subject to the normal ChatGPT rate limits.


### The JiggyBase console is stuck with the spinning logo, what is going on?

We are working to streamline the document ingestion process which at this point is not optimized for documents larger than several hundred pages or csv files with more than 10,000 records.  Larger documents, and in particular csv files with > 10k records, may cause the collection to hang during ingestion or when trying to list the documents from the dashboard.  We are working to fix this, but if you run into this issue please do reach out so we can prioritize it appropriately. 


### What causes the error message "No useable content found in documents"?

JiggyBase processed the document but was unable to find any text to use. An example would be a PDF that contains scanned text, as we do not currently support OCR.  We expect to support text extraction via OCR as well as support some image data in the second half of 2023.  Please contact us to discuss accelerating support for these types of documents for enterprise use cases. 

PDF documents also support features for encrypting the content and disabling printing or text extraction.  It is possible that the PDF has these settings configured.

### What causes the error message "Error extracting text from file"?

JiggyBase encountered an unexpected error while processing the document.  We want to fix these errors, so if you can email us the document (under NDA) we will provide you with a coupon for a month of free service!


### What file types are supported?

- Microsoft Word (doc/docx)
- Microsoft Excel (see limitations below)
- Microsoft Powerpoint (text content only)
- CSV
- PDF
- Text
- Markdown


### What are the limitations for Excel files?

Currently we only support excel files that contain a single sheet per file.  Contact us if you have a use case that requires many excel files with multiple sheets and we will prioritize this feature.

We convert the excel sheet to csv before processing it. The data in the spreadsheet must be strictly in a tabular format.  Ideally the first row should contain a nice human readable name for each column. Very large (>10K rows) are slow to process (see CSV below).

### What are the limitations for CSV files?

Ideally the first row of the CSV file should contain the name of each column of data. Although this is not a strict requirement, it provides extra semantic context that helps the models make sense of your data. 

Currently CSV files with more than 10K rows of data are slow to process and may hang.  Please contact us if you have a use case that requires ingestion of large csv files and we will prioritize the fix for this.


### What are the limitations for PDF files?

We do not currently support scanned PDF's.  Support for OCR is coming later in 2024.  Please contact us if you would like us to prioritize this.

Some PDFs contain settings that prohibit text extraction or printing.  We are unable to process these to access the text content and will produce an error message.

### Sometimes ChatGPT doesn't use JiggyBase when it should. How to make ChatGPT use JiggyBase?

The simplest way is to start your query with a reference to JiggyBase.  We have found that starting a chat with "per jiggybase," usually puts the GPT in the right mood to use JiggyBase.  You can also open with something like "in jiggybase collection XYZ," to further guide it.

### How can I get ChatGPT to provide references?

When JiggyBase searches your collections on behalf of ChatGPT, JiggyBase returns a lot of additional metadata along with the document content to help the GPT model make better sense of it all.  We also include a reference URL which can be used to access each portion of the original text material.

ChatGPT will often provide these reference URLS on its own, but if it doesnt you can ask it to "provide references".  We are working to improve the presentation of the reference material and eventually want to be able to show you the relevant material in the format of the original document.  


