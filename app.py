import os
import json
from utils.prepare_output_json import prepare_output_json

def write_output(output_path, data):    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main():
    print("LLM Gateway started...")
    output_path = os.getenv("SOURCE_SHARED_VOLUME_PATH")

    result_json = prepare_output_json()    
    write_output(output_path, result_json)
    


if __name__ == "__main__":
    main()