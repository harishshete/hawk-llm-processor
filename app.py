import os
import json
from utils.push_in_db import push_to_db
from utils.prepare_output_json import prepare_output_json_new

def main():
    print("hawk LLM processor started...")

    print("Preparing output JSON array...")
    result_json = prepare_output_json_new()    
    print("Output JSON array prepared successfully.")
    
    for one_json_output in result_json:
        push_to_db(one_json_output)




if __name__ == "__main__":
    main()