import requests
from bs4 import BeautifulSoup
import time
from utils.helpers import get_logger
from datetime import datetime

class BaseCrawler:
    def __init__(self, url):
        self.url = url
        self.logger = get_logger(self.__class__.__name__)

    def fetch_html(self):
        try:
            response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {self.url}: {e}")
            return None

    def parse(self, html):
        """Parses HTML to extract detailed data."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract metadata
        metadata = {
            'title': soup.title.string.strip() if soup.title else None,
            'description': None,
            'keywords': None,
            'og:image': None
        }
        for meta in soup.find_all('meta'):
            if meta.get('name') == 'description':
                metadata['description'] = meta.get('content')
            if meta.get('name') == 'keywords':
                metadata['keywords'] = meta.get('content')
            if meta.get('property') == 'og:image':
                metadata['og:image'] = meta.get('content')

        # Extract media URLs (images)
        media_urls = [img['src'] for img in soup.find_all('img') if img.get('src')]
        
        # Extract main text content
        text_content = soup.get_text(separator=' ', strip=True)

        return {
            "url": self.url,
            "crawled_at": datetime.utcnow().isoformat(),
            "metadata": metadata,
            "text_content": text_content,
            "media_urls": list(set(media_urls)), # Use set to get unique image URLs
            "raw_html": html
        }

    def crawl(self):
        html = self.fetch_html()
        if html:
            return self.parse(html)
        return None