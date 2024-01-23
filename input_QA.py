import numpy as np
import openai
from openai import OpenAI
import os
import pandas as pd
import pickle
import json
from pathlib import Path
from tqdm import tqdm
from time import sleep

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

# Authenticate with OpenAI API
with open("apiKeys.txt", "r") as temp:
    apiKey = temp.read()
client = OpenAI(api_key=apiKey)


def gpt4(question, tokens=500):
    messages = [{"role": "user", "content": question}]

    response = client.chat.completions.create(
        model="gpt-4", max_tokens=tokens, temperature=0, messages=messages
    )

    # Extract the content
    content = response.choices[0].message.content

    # Split the content into text and code
    text_parts = []
    code_parts = []
    in_code_block = False

    for line in content.split("\n"):
        if line.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            code_parts.append(line)
        else:
            text_parts.append(line)

    # Print the text parts
    """for line in text_parts:
        print(line)"""

    # Print a separator
    """print("\n" + "-" * 50 + "\n")"""

    # Print the code parts
    for line in code_parts:
        print(line)
    return content


p1 = "Consider the following information provided: "
p2 = """Based solely on the data presented, create a list of 3 most common and not trivial Questions and Answers. This is used to fine-tune LLMs to answer technical user support tickets

Ensure each question:
1. Is directly related to the content given.
2. Can be answered with the information from the provided text only.
3. Questions must be technical and focused on questions a HPC user will ask for technical support. 

Avoid:
- Generating questions on general topics or external knowledge not contained in the text.
- Creating any questions if the information provided does not sufficiently cover 3 distinct points.
- Limit to fewer than 3 Q&A generation if the content is limited. 
- Do not overlap Q&A.

Output should be structured only as JSONL format. When not able to generate do not generate anything:
{"prompt": <Question>, "completion": <answer>}

If the content is not comprehensive enough to form 3 distinct questions and answers, state that insufficient data is provided.

Example context:{"filename": "actor.md", "prompt": "Install the Tapis Python SDK", "completion": "To interact with the TACC-hosted Abaco platform in Python, we will\nleverage the Tapis Python SDK, tapipy. To install it, simply run: pip3 install tapipy\n\n\n\n::: attention\n::: title\nAttention\n:::\n\n`tapipy` works with Python 3.\n:::"}

Example output: {"prompt": "How do I install the Tapis Python SDK to use with the Abaco platform?", "completion": "To install the Tapis Python SDK, simply run the the command `pip3 install tapipy` in the Python environment."}


Context:
<<<Insert context here>>>"""


# Generate the Question
with open("jsonl_files/combined.jsonl", "r") as f:
    temp = list(f)
content = []
for json_str in temp:
    result = json.loads(json_str)
    content.append(result)


jsonl_data = {}
for file in os.listdir("dummyin"):
    p_list = []
    p_holder = []
    for item in content:
        if sum(len(i) for i in p_holder) >= 6000:
            p_list.append("\n".join(p_holder))
            p_holder = []
        if item["filename"] == file:
            p_holder.append(f'Question: {item["prompt"]}, Result: {item["completion"]}')
            p_holder.append("\n")
    p_list.append("\n".join(p_holder))

    results = {}
    count = 1
    for p_context in p_list:
        print(f"Running batch {count} of {len(p_list) + 1} for {file}")
        prompt = f"{p1} {p_context}. \n {p2}"

        results[f"{file}{count}"] = gpt4(prompt, 2000)
        count += 1
        print("Allowing rate limit to reset, wait one minute please...")
        for i in tqdm(range(1)):
            sleep(1)
    with open(os.path.join("dummyout", str(Path(file).stem) + ".txt"), "w") as f:
        for i in results.keys():
            f.write(results[i])
            jsonl_data[i] = results[i]

bad_data = []
for i in jsonl_data.keys():
    print(type(jsonl_data[i]))
    if jsonl_data[i] == "Insufficient data is provided.":
        bad_data.append(i)
    else:
        print(jsonl_data[i], "\n ------------------------------- ")

for i in bad_data:
    del jsonl_data[i]

with open("dummyout/qa_output.jsonl", "w") as f:
    for i in jsonl_data.keys():
        f.write(jsonl_data[i])
