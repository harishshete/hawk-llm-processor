import os
import json
from utils.push_in_db import push_to_db
from utils.prepare_output_json import prepare_output_json


def main():
    print("hawk LLM processor started...")

    print("Preparing output JSON...")
    result_json = prepare_output_json()    
    print("Output JSON prepared successfully.")

    print("Pushing results to the database...")
    push_to_db(result_json)


if __name__ == "__main__":
    main()