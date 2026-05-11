import os
import json

from utils.html_parser import extract_sections
from utils.section_diff import compare_sections
from utils.prompt_builder import build_prompt
from utils.llm_client import call_llm
from utils.get_base_url import get_base_url

def write_output(output_path, data):
    print("Inside write_output function")
    print(output_path)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main():

    old_path = os.getenv("OLD_FILE_PATH")
    new_path = os.getenv("NEW_FILE_PATH")
    output_path = os.getenv("OUTPUT_PATH")

    print("Inside Main function")
    print(output_path)
    # New article case
    if not old_path or not os.path.exists(old_path):

        output = {
            "added": True,
            "summary": "New article added"
        }

        write_output(output_path, output)

        print("New article detected.")
        return

    # Extract sections
    old_sections = extract_sections(old_path)
    new_sections = extract_sections(new_path)

    # Generate section-aware diff
    changes_text = compare_sections(
        old_sections,
        new_sections
    )

    
    print("Generated section differences:")
    print(changes_text)
    
    # No changes
    if not changes_text.strip():

        output = {
            "added": False,
            "summary": "No changes detected"
        }

        write_output(output_path, output)

        print("No changes detected.")
        return

    # Build prompt
    prompt = build_prompt(changes_text)

    # Call LLM
    summary = call_llm(prompt)

    # Save output
    output = {
        "title":"",
        "source_name":"",
        "commit_id":"",
        "link": "",
        "what_changed": summary,
        "product_name": "",
        "tag": "",
    }

    write_output(output_path, output)

    print("Processing complete.")


if __name__ == "__main__":
    main()