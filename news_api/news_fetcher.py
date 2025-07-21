from newsapi import NewsApiClient
from utils.helpers import get_logger

class NewsFetcher:
    def __init__(self, api_key):
        self.newsapi = NewsApiClient(api_key=api_key)
        self.logger = get_logger(self.__class__.__name__)

    def fetch_news(self, query):
        try:
            all_articles = self.newsapi.get_everything(q=query,
                                                      language='en',
                                                      sort_by='relevancy')
            return all_articles['articles']
        except Exception as e:
            self.logger.error(f"Error fetching news: {e}")
            return []