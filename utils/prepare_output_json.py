import requests
import os
import json
from pathlib import Path
from utils.get_base_url import (detect_product_name,get_base_url,get_base_url_release_notes)
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
    print(f"Generating summary of changes between old file: {old_file} and new file: {new_file}")
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

    #output_json["what_changed"] = summary
    return summary





def generate_summary_of_new_article(new_file):
    print(f"Generating summary for new article: {new_file}")
    # Extract sections
    new_sections = extract_sections(new_file)    

    # Build prompt
    prompt = build_prompt_for_new_article(new_sections)

    # Call LLM
    summary = call_llm(prompt)

    #output_json["what_changed"] = summary
    return summary


'''
def prepare_output_json():
    source_result = os.getenv("SOURCE_RESULT")
    
    if not source_result:
        raise ValueError("SOURCE_RESULT environment variable is not set")
    
    # Parse as JSON
    try:
        payload = json.loads(source_result)
    except (json.JSONDecodeError, TypeError) as e:
        raise ValueError(f"SOURCE_RESULT must be valid JSON: {e}") from e
    
    # Extract git diff data - handle both old array format and new nested format
    if isinstance(payload, list):
        # Old format: array of objects
        data = payload[0]
    elif "gitDiff" in payload:
        # New format: object with nested gitDiff
        data = payload["gitDiff"]
    else:
        # Fallback: treat payload as data directly
        data = payload

    output_json["source_name"] = data.get("name")
    output_json["commit_id"] = data.get("targetCommit")
    output_json["product_name"] = detect_product_name(data.get("exportedNewFiles", data.get("ExportedNewFiles", []))[0])
    output_json["link"] = get_base_url(output_json["product_name"])
    
    
    new_files = data.get("exportedNewFiles", data.get("ExportedNewFiles", []))
    old_files = data.get("exportedOldFiles", data.get("ExportedOldFiles", []))

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

        if contains_release:
            output_json["link"] = get_base_url_release_notes(output_json["product_name"])

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
'''



#Get the old and new file pairs
def prepare_file_pairs(old_files, new_files):
    print("Preparing old:new file pairs array...")
    result = []

    # Create lookup maps using filename
    old_map = {
        os.path.basename(path): path
        for path in old_files
    }

    # Iterate over new files
    for new_file in new_files:
        filename = os.path.basename(new_file)

        result.append({
            "new": new_file,
            "old": old_map.get(filename, None)
        })

    print(f"Prepared {len(result)} old:new file pairs.")
    return result


# Extract remaining properties of the JSON output
def extract_remaining_properties(new_file, old_file, product_name):
    output_json = {}
    
    output_json["tag"] = "updated" if old_file else "added"
    if new_file:
        new_file_lower = new_file.lower()

        # Extract title and set in output_json
        output_json["title"] = extract_title(new_file)

        # Check release in path
        contains_release = "release" in new_file_lower

        if contains_release:
            output_json["tag"] = "release_notes"
            output_json["link"] = get_base_url_release_notes(product_name)
        else:
            output_json["link"] = get_base_url(product_name)
        
    
    if not old_file:
        output_json["what_changed"] = generate_summary_of_new_article(new_file)
    else:
        output_json["what_changed"] = generate_summary_of_changes(old_file, new_file)

    return output_json
    


def prepare_output_json_new():
    source_result = os.getenv("SOURCE_RESULT")
    output_json_array = []
    
    if not source_result:
        raise ValueError("SOURCE_RESULT environment variable is not set")
    
    # Parse as JSON
    try:
        payload = json.loads(source_result)
    except (json.JSONDecodeError, TypeError) as e:
        raise ValueError(f"SOURCE_RESULT must be valid JSON: {e}") from e
    
    # Extract git diff data - handle both old array format and new nested format
    if isinstance(payload, list):
        # Old format: array of objects
        data = payload[0]
    elif "gitDiff" in payload:
        # New format: object with nested gitDiff
        data = payload["gitDiff"]
    else:
        # Fallback: treat payload as data directly
        data = payload 
    
    #Extract common properties
    source_name = data.get("name")
    commit_id = data.get("TargetCommit") or data.get("targetCommit")
    product_name = detect_product_name(data.get("exportedNewFiles", data.get("ExportedNewFiles", []))[0])
    print("Common properties extracted")

    new_files = data.get("exportedNewFiles", data.get("ExportedNewFiles", []))
    old_files = data.get("exportedOldFiles", data.get("ExportedOldFiles", []))

    old_new_file_pairs = prepare_file_pairs(old_files, new_files)

    for pair in old_new_file_pairs:
        print(f"Extracting remaining properties for pair - New: {pair['new']}, Old: {pair['old']}")
        output_json = extract_remaining_properties(pair["new"], pair["old"], product_name)
        output_json["source_name"] = source_name
        output_json["commit_id"] = commit_id
        output_json["product_name"] = product_name
        output_json_array.append(output_json)
        print("Extracted remaining properties and appended to output array")

    return output_json_array
    


    



