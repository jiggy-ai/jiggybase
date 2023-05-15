import jiggybase
import sys


collection = jiggybase.JiggyBase().collection('hackernews-summary')

messages = [{'role':'user',  'content': 'articles about python 3.11'}]

for outstr in collection._chat_completion_stream_str(messages):
    sys.stdout.write(outstr)
    sys.stdout.flush()
print()
