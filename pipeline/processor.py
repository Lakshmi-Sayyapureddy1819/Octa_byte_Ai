import re
from bs4 import BeautifulSoup

def process_raw_data(raw_data):
    """
    A simple processor to clean text from raw HTML content.
    """
    # Ensure there is content to process
    if not raw_data.get("content"):
        return None

    # Use BeautifulSoup to parse HTML and extract text
    soup = BeautifulSoup(raw_data["content"], 'html.parser')
    text = soup.get_text()

    # Simple text cleaning: remove extra whitespace
    cleaned_text = re.sub(r'\s+', ' ', text).strip()

    processed_data = {
        "url": raw_data.get("url"),
        "title": raw_data.get("title"),
        "cleaned_content": cleaned_text
    }

    return processed_data