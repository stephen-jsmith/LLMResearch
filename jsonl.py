import json
import re
import os


def md_to_jsonl(md_file_dir, jsonl_file):
    """Converts a given directory of markdown files to a combined jsonl file."""
    jsonl_data = []

    for md_file_path in os.listdir(md_file_dir):
        with open(
            os.path.join(md_file_dir, md_file_path), "r", encoding="utf-8"
        ) as file:
            content = file.read()

        # Regular expression to match headings and subheadings
        heading_regex = re.compile(r"^#+\s(.+)$", re.MULTILINE)
        code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)

        # Find all headings and their positions
        headings = [
            (match.group(0), match.start()) for match in heading_regex.finditer(content)
        ]
        count = 0
        # Split the content based on these headings and process each
        for i in range(len(headings)):
            count += 1
            heading, start = headings[i]
            # Find the end of the current section as the start of the next heading or end of file
            end = headings[i + 1][1] if i + 1 < len(headings) else len(content)

            # Extract the section's content
            section_content = content[start:end].strip()

            # Find and remove the code block if present
            code_match = code_block_regex.search(section_content)
            code = code_match.group(1).strip() if code_match else ""

            # Clean the section from code and extra headings
            clean_section = code_block_regex.sub("", section_content).strip()
            clean_section = heading_regex.sub("", clean_section).strip()

            # Create a JSON object for this section
            section_json = {
                "filename": md_file_path,
                "heading": heading.strip("# ").strip(),
                "text": clean_section,
                "code": code,
            }

            # Append to the list if there's meaningful content
            if section_json["text"] or section_json["code"]:
                jsonl_data.append(section_json)
        print(f"Formatted {md_file_path}, contained {count} lines")

    # Write the JSONL data to a file
    with open(jsonl_file_path, "w", encoding="utf-8") as jsonl_file:
        for entry in jsonl_data:
            jsonl_file.write(json.dumps(entry) + "\n")

    print(
        jsonl_file_path, len(jsonl_data)
    )  # Return the path to the JSONL file and the number of sections processed


# Specify your .md directory and the output .jsonl file path
md_file_dir = "md_files"
jsonl_file_path = "jsonl_files/combined.jsonl"

# Convert the markdown content to JSONL format
jsonl_data = md_to_jsonl(md_file_dir, jsonl_file_path)
