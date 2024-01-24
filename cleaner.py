import json
import ast
import os


def cleaner(input_file: str, output_file: str):
    """Clean the jsonl file to be readable by the database
    
    Args:
        input_file (str): File to clean
        output_file (str): File to output to
    """

    # Load data and get it in a readable format
    ls = []
    with open(input_file, "r") as f:
        for item in f:
            temp = item.split("}{")

            # Get the individual items in dict format
            for i in temp:
                i.strip()
                i = i[1:-1]
                if i.endswith("}"):
                    i = i[:-1]
                if i.startswith('"'):
                    pass
                else:
                    i = '"' + i
                if i.endswith(".") or i.endswith("`"):
                    i += '"'
                # Disregard "Insufficient data" type messages
                if len(i) < 50:
                    pass
                else:
                    i = "{" + i + "}"
                    ls.append(i)
                    ls.append("\n")

    # Write to output file
    with open(output_file, "w") as f:
        for i in ls:
            # print(i, type(i), "\n")
            if type(i) == list:
                for j in i:
                    if j != "{":
                        f.write(j)
            else:
                if i != "{":
                    f.write(i)


cleaner("jsonl_files/qa_output.jsonl", "jsonl_files/qa_clean.jsonl")
