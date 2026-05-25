import requests

base_urls_map = {
    "akana":"https://help.akana.com/content/current",
    "perfecto":"https://help.perfecto.io/perfecto-help/content",
    "blazemeter":"https://help.blazemeter.com/docs/guide",
}

release_notes_map = {
    "akana": "https://help.akana.com/release_notes/current",
    "perfecto": "https://help.perfecto.io/perfecto-help/content/perfecto/release-notes",
    "blazemeter": "https://help.blazemeter.com/docs/guide",
}


base_urls_map_fallback = {
    "akana":"https://help.akana.com/content/current/Home.htm",
    "perfecto":"https://help.perfecto.io/perfecto-help",
    "blazemeter":"https://help.blazemeter.com/docs/guide/intro.html",
}

release_notes_map_fallback = {
    "akana": "https://help.akana.com/release_notes/current/2026.1.0/Major_Release_2026.1.html",
    "perfecto": "https://help.perfecto.io/perfecto-help/content/perfecto/release-notes/release_notes.htm",
    "blazemeter": "https://help.blazemeter.com/docs/guide/release-notes.html",
}





def get_base_url(product_name):
    return base_urls_map_fallback.get(product_name)


def detect_product_name(exported_files):

    #print("Inside detect_product_name function")
    #print(exported_files)
    if not exported_files:
        return None

    first_path = exported_files.lower()
    for product in base_urls_map.keys():
        if product.lower() in first_path:
            return product

    return None


def get_base_url_release_notes(product_name):
    return release_notes_map_fallback.get(product_name)


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


def check_url(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200

    except requests.exceptions.RequestException:
        return False


def get_article_url(path,product_name,is_release_notes):
    
    base_url = get_base_url_release_notes(product_name) if is_release_notes else get_base_url(product_name)

    normalized_path = normalize_path(path)
    print("Normalized Path:", normalized_path)

    if normalized_path:
        full_url = base_url + normalized_path
        print("Constructed URL:", full_url)
        if check_url(full_url):
            return full_url
    else:
        return False


