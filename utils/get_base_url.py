base_urls_map = {
    "akana":"https://help.akana.com/",
    "perfecto":"https://help.perfecto.io/perfecto-help/",
    "blazemeter":"https://help.blazemeter.com/docs/guide/intro.html",
    "gateway":"test",
    "":"",
    "":"",
    "":"",
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