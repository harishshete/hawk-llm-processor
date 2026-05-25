import requests
import re
import os
import json
from push_in_db import push_to_db
from utils.get_base_url import get_base_url
#from get_base_url import get_base_url


def write_output(output):
    output_path = os.getenv("SOURCE_SHARED_VOLUME_PATH")
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=4)


def post():
    data = {
        "added": False,
        "summary": "No changes detected wow"
    }
    write_output(data)


#post()


arr = [
{
    "link": "https://help.akana.com/release_notes/current/2026.1.0/Major_Release_2026.1.html",
    "what_changed": " In the new documentation, after activating and attaching a policy, it is now necessary to restart the PMCM container for the changes to be effective. This step was not mentioned in the old version of the article.",
    "product_name": "akana",
    "tag": "release_notes",
    "title": "Using the Auditing Message Policy",
    "source_name": "basic-git",
    "commit_id": "jnasusia79873jh3789u"
},
{
    "link": "https://help.akana.com/release_notes/current/2026.1.0/Major_Release_2026.1.html",
    "what_changed": " In the new documentation, after activating and attaching a policy, it is now necessary to restart the PMCM container for the changes to be effective. This step was not mentioned in the old version of the article.",
    "product_name": "akana",
    "tag": "release_notes",
    "title": "Using the Auditing Message Policy",
    "source_name": "basic-git",
    "commit_id": "jnasusia79873jh3789u"
},
{
    "link": "https://help.akana.com/release_notes/current/2026.1.0/Major_Release_2026.1.html",
    "what_changed": " In the new documentation, after activating and attaching a policy, it is now necessary to restart the PMCM container for the changes to be effective. This step was not mentioned in the old version of the article.",
    "product_name": "akana",
    "tag": "release_notes",
    "title": "Using the Auditing Message Policy",
    "source_name": "basic-git",
    "commit_id": "jnasusia79873jh3789u"
}

]

'''
for one_json_output in arr:
    push_to_db(one_json_output)
    print("pushed to db/n")
'''



''' ====================================================================================================================================================================== '''


def normalize_path(path):
    HEX_CHARS = set('0123456789abcdefABCDEF')
    SKIP_FOLDERS = {'new', 'old'}
    path = path.strip('",')
    parts = path.split('/')

    for i, part in enumerate(parts):
        if part and all(c in HEX_CHARS for c in part):

            return '/' + '/'.join(
                p.lower()
                for p in parts[i + 1:]
                if p.lower() not in SKIP_FOLDERS
            )

    return None


# Example usage
paths = [
    '/opt/hawk-data/basic-git/caf62e31dd290dcb7fd50eb1c963d/content/Perfecto/manual-testing/New/Inject_an_image.htm',
    '/random/path/content/Perfecto/Old/manual-testing/Inject_an_image.htm'
]


for p in paths:
    base_ur = get_base_url("perfecto")
    full_url = base_ur + normalize_path(p)
    print(full_url)
    #print(normalize_path(p))



''' ====================================================================================================================================================================== '''

def check_url(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200

    except requests.exceptions.RequestException:
        return False

# Example usage
#url = "https://google.com"
#print(check_url(url))


