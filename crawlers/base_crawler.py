import requests
from bs4 import BeautifulSoup
import time
from utils.helpers import get_logger

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

    def crawl(self):
        raise NotImplementedError("Each crawler must implement the crawl method.")