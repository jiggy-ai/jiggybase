import jiggybase

collection = jiggybase.JiggyBase().collection('hackernews-summary')   # replace with your collection name

messages = [{'role':'user',  'content': 'articles about python 3.11'}]

rsp = collection._chat_completion(messages)   # note _ as this is preliminary low-level interface

print(rsp)

"""
Here are some articles about Python 3.11:

1. Python 3.11.1, 3.10.9, 3.9.16, 3.8.16, 3.7.16, and 3.12.0 alpha 3 now available - This is a blog post from the official Python Software Foundation blog. The post is announcing the release of Python 3.11.1, 3.10.9, 3.9.16, 3.8.16, 3.7.16, and 3.12.0 alpha 3. The post goes over some of the security content in the new releases.

2. Python 3.11 Is Much Faster, but Pyston and PyPy Still Show Advantages - This is a news article from the website www.phoronix.com. It discusses the recent Python 3.11 beta benchmarks and compares them to alternative Python implementations like PyPy and Pyston. It also includes Python 3.11b3 results.

3. A Team at Microsoft Is Helping Make Python Faster - This is a blog post about the Faster CPython Team at Microsoft. It details the team's mission to make Python faster, the specialized knowledge and collaboration of the team, and Microsoft's commitment to the Python community. It also highlights the team's work on Python 3.11 and their plans for Python 3.12.

I hope this helps!
"""
