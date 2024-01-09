with open("jsonl_files/qa_output.jsonl", "r") as r, open(
    "jsonl_files/qa_clean.jsonl", "w"
) as o:
    for line in r:
        # strip() function
        if line.strip():
            o.write(line)

f = open("jsonl_files/qa_clean.jsonl", "r")
print("New text file:\n", f.read())
