base_urls_map = {
    "akana":"https://help.akana.com/content/current/Home.htm",
    "perfecto":"https://help.perfecto.io/perfecto-help/content/home.htm",
    "blazemeter":"https://help.blazemeter.com/docs/guide/intro.html",
}

release_notes_map = {
    "akana": "https://help.akana.com/release_notes/current/2026.1.0/Major_Release_2026.1.html",
    "perfecto": "https://help.perfecto.io/perfecto-help/content/perfecto/release-notes/release_notes.htm",
    "blazemeter": "https://help.blazemeter.com/docs/guide/release-notes.html",
}

def get_base_url(product_name):
    return base_urls_map.get(product_name)


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
    return release_notes_map.get(product_name)