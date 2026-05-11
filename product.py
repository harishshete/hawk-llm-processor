product_map = {
    "iphone": "https://apple.com/iphone",
    "samsung": "https://samsung.com",
    "macbook": "https://apple.com/macbook"
}

incoming_url = "https://shop.example.com/products/MACBOOK-pro-16"
product_name = ""

incoming_url_lower = incoming_url.lower()

matched_url = None

for product_nam, mapped_url in product_map.items():
    if product_nam in incoming_url_lower:
        product_name = product_nam
        matched_url = mapped_url
        break

print(matched_url)
print(product_name)