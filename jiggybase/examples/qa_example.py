import csv
import os
import tempfile
import shutil
from dotenv import load_dotenv
import jiggybase

def get_answer(question):
    messages = [{'role':'user',  'content': question}]
    collection_name = os.getenv("JIGGYBASE_COLLECTION_NAME")
    collection = jiggybase.JiggyBase().collection(collection_name)
    rsp = collection._chat_completion(messages)
    return rsp

def fill_answers(input_csv):
    with tempfile.NamedTemporaryFile(mode='w+', newline='', delete=False) as temp_file:
        with open(input_csv, "r", newline='') as infile, open(temp_file.name, "w", newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
    
            # Verify the header and write it to the output file
            header = next(reader)
            assert header == ["question", "answer"], "Invalid header"
            writer.writerow(header)
    
            # Iterate over the rows, filling in answers when needed
            for row in reader:
                question, answer = row
                if not answer or answer.strip() == "":
                    answer = get_answer(question)
                    row = [question, answer]
                writer.writerow(row)

        # Replace the original input file with the updated file
        shutil.move(temp_file.name, input_csv)

load_dotenv()
input_csv = "input.csv"
fill_answers(input_csv)
