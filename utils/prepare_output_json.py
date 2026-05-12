import os
import json
from pathlib import Path
from utils.get_base_url import (detect_product_name,get_base_url)
from utils.html_parser import extract_title, extract_sections
from utils.section_diff import compare_sections
from utils.prompt_builder import build_prompt,build_prompt_for_new_article
from utils.llm_client import call_llm


output_json = {
    "title": "",
    "source_name": "",
    "commit_id": "",
    "link": "",
    "what_changed": "",
    "product_name": "",
    "tag": ""
}


def generate_summary_of_changes(old_file, new_file):
    # Extract sections
    old_sections = extract_sections(old_file)
    new_sections = extract_sections(new_file)    

    # Generate section-aware diff
    changes_text = compare_sections(
        old_sections,
        new_sections
    )

    #print("Generated section differences:")

    # No changes
    if not changes_text.strip():

        output = {
            "added": False,
            "summary": "No changes detected"
        }

        #write_output(output_path, output)

        print("No changes detected.")
        return

    # Build prompt
    prompt = build_prompt(changes_text)

    # Call LLM
    summary = call_llm(prompt)

    output_json["what_changed"] = summary





def generate_summary_of_new_article(new_file):
    # Extract sections
    new_sections = extract_sections(new_file)    

    # Build prompt
    prompt = build_prompt_for_new_article(new_sections)

    # Call LLM
    summary = call_llm(prompt)

    output_json["what_changed"] = summary



def prepare_output_json():
    file_path = os.getenv("FILE_PATH")
    #print(file_path)
    with open(file_path, "r") as file:
        data = json.load(file)
    
    output_json["source_name"] = data[0].get("name")
    output_json["commit_id"] = data[0].get("TargetCommit")
    output_json["product_name"] = detect_product_name(data[0].get("ExportedNewFiles")[0])
    output_json["link"] = get_base_url(output_json["product_name"])
    
    
    new_files = data[0].get("ExportedNewFiles", [])
    old_files = data[0].get("ExportedOldFiles", [])

    new_file = new_files[0] if new_files else None
    old_file = old_files[0] if old_files else None
    
    exists_in_old = False
    contains_release = False

    if new_file:
        new_file_lower = new_file.lower()

        # Extract title and set in output_json
        output_json["title"] = extract_title(new_file)

        # Check release in path
        contains_release = "release" in new_file_lower

        # Compare filenames if old file exists
        if old_file:
            old_file_lower = old_file.lower()
            new_filename = Path(new_file_lower).name
            old_filename = Path(old_file_lower).name
            exists_in_old = new_filename == old_filename

    
    if exists_in_old:
        #output_json["tag"] = "updated"
        output_json["tag"] = "release_notes" if contains_release else "updated"
        generate_summary_of_changes(old_file, new_file)
    elif contains_release:
        output_json["tag"] = "release_notes"
        generate_summary_of_new_article(new_file)
    else:
        output_json["tag"] = "added"
        generate_summary_of_new_article(new_file)


    return output_json

