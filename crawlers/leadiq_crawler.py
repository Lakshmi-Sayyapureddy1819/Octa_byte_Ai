from .base_crawler import BaseCrawler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class LeadiqCrawler(BaseCrawler):
    def crawl(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        try:
            with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
                driver.get(self.url)
                time.sleep(5)  # Wait for dynamic content to load
                return {"url": self.url, "title": driver.title, "content": driver.page_source}
        except Exception as e:
            self.logger.error(f"Error crawling {self.url} with Selenium: {e}")
            return None