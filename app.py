import os
import json

from utils.html_parser import extract_sections
from utils.section_diff import compare_sections
from utils.prompt_builder import build_prompt
from utils.llm_client import call_llm
from utils.get_base_url import (get_base_url,detect_product_name)

def write_output(output_path, data):

    # Compare
    changes_text = compare_sections(
        old_sections,
        new_sections
    )

    # No changes
    if not changes_text.strip():

        output = {
            "title": title,
            "source_name": source_name,
            "commit_id": target_commit,
            "link": base_url,
            "what_changed": "No changes detected",
            "product_name": product_name,
            "tag": tag
        }

        write_output(output_file, output)
        return

    # Build prompt
    prompt = build_prompt(changes_text)

    # LLM summary
    summary = call_llm(prompt)

    output = {
        "title": title,
        "source_name": source_name,
        "commit_id": target_commit,
        "link": base_url,
        "what_changed": summary,
        "product_name": product_name,
        "tag": tag
    }

    write_output(output_file, output)



def main():

    data = load_input_json()

    output_dir = os.getenv("OUTPUT_PATH")

    for item in data:

        source_name = item.get("name")
        target_commit = item.get("TargetCommit")

        exported_files = item.get("ExportedFiles", [])
        old_files = item.get("ExportedOldFiles", [])
        new_files = item.get("ExportedNewFiles", [])

        for index, new_file in enumerate(new_files, start=1):

            old_file = get_old_file(new_file, old_files)

            output_filename = f"output_{index}.json"
            output_file = os.path.join(
                output_dir,
                output_filename
            )

            process_article(
                source_name,
                target_commit,
                exported_files,
                old_file,
                new_file,
                output_file
            )

            print(f"Processed: {new_file}")



if __name__ == "__main__":
    main()