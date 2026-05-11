from bs4 import BeautifulSoup

HEADINGS = ["h1", "h2", "h3", "h4"]

def extract_title(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    h1 = soup.find("h1")

    if h1:
        return h1.get_text(strip=True)

    return "Untitled"



def extract_sections(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    # Remove noisy elements
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    sections = {}

    headings = soup.find_all(HEADINGS)

    for i, heading in enumerate(headings):
        title = heading.get_text(strip=True)

        content = []

        current = heading.next_sibling

        while current:
            if getattr(current, "name", None) in HEADINGS:
                break

            text = ""

            if hasattr(current, "get_text"):
                text = current.get_text(" ", strip=True)
            else:
                text = str(current).strip()

            if text:
                content.append(text)

            current = current.next_sibling

        clean_content = "\n".join(content).strip()

        if clean_content:
            sections[title] = clean_content

    return sections