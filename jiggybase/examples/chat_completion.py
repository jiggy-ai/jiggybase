import jiggybase

collection = jiggybase.JiggyBase().collection('hackernews-summary')

messages = [{'role':'user',  'content': 'articles about python 3.11'}]

rsp = collection._chat_completion(messages)

print(rsp)