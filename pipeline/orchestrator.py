import json
import os
import re
from bs4 import BeautifulSoup
import config
from crawlers.gnosis_freight_crawler import GnosisFreightCrawler
from crawlers.thelogisticsoflogistics_crawler import TheLogisticsOfLogisticsCrawler
from crawlers.freightwaves_crawler import FreightwavesCrawler
from crawlers.leadiq_crawler import LeadiqCrawler
from crawlers.g2_crawler import G2Crawler
from crawlers.marketsandmarkets_crawler import MarketsAndMarketsCrawler
from news_api.news_fetcher import NewsFetcher
from .storage import get_storage_client
from utils.helpers import get_logger

# Initialize logger for the orchestrator
logger = get_logger("Orchestrator")

def process_data(raw_data, source_type):
    """
    Cleans and transforms raw data into a processed format.
    - For 'webpage' source_type, it extracts and cleans text from HTML.
    - For 'news', it selects key fields for a cleaner record.
    """
    if not raw_data or not raw_data.get("content"):
        return None

    if source_type == 'webpage':
        # Use BeautifulSoup to parse HTML and extract text
        soup = BeautifulSoup(raw_data["content"], 'html.parser')
        text = soup.get_text()
        # Simple text cleaning: remove extra whitespace
        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        
        processed_data = {
            "url": raw_data.get("url"),
            "title": raw_data.get("title"),
            "cleaned_content": cleaned_text,
            "crawled_at": raw_data.get("crawled_at")
        }
        return processed_data

    elif source_type == 'news':
        # For news articles, the content is often already clean text
        processed_data = {
            "url": raw_data.get("url"),
            "title": raw_data.get("title"),
            "source": raw_data.get("source", {}).get("name"),
            "published_at": raw_data.get("publishedAt"),
            "content": raw_data.get("content")
        }
        return processed_data
    
    return None


def run_pipeline():
    """
    Executes the full data pipeline: crawl, process, and store.
    """
    logger.info("Pipeline run started.")
    storage_client = get_storage_client(config.STORAGE_CONFIG)

    # 1. Crawl websites
    logger.info("Starting website crawling.")
    crawlers = {
        "gnosis_freight": GnosisFreightCrawler(config.WEBSITES["gnosis_freight"]),
        "the_logistics_of_logistics": TheLogisticsOfLogisticsCrawler(config.WEBSITES["the_logistics_of_logistics"]),
        "freightwaves": FreightwavesCrawler(config.WEBSITES["freightwaves"]),
        "leadiq": LeadiqCrawler(config.WEBSITES["leadiq"]),
        "g2": G2Crawler(config.WEBSITES["g2"]),
        "markets_and_markets": MarketsAndMarketsCrawler(config.WEBSITES["markets_and_markets"]),
    }

    for name, crawler in crawlers.items():
        logger.info(f"Crawling {name}...")
        raw_data = crawler.crawl()
        if raw_data:
            # Save raw data
            storage_client.save(raw_data, name, data_type='raw')
            
            # Process and save processed data
            processed_data = process_data(raw_data, source_type='webpage')
            if processed_data:
                storage_client.save(processed_data, name, data_type='processed')
        else:
            logger.warning(f"No data returned from {name} crawler.")

    logger.info("Website crawling finished.")

    # 2. Fetch news articles
    logger.info("Starting news API fetch.")
    if config.NEWS_API_KEY and config.NEWS_API_KEY != "YOUR_NEWS_API_KEY":
        news_fetcher = NewsFetcher(config.NEWS_API_KEY)
        articles = news_fetcher.fetch_news(config.NEWS_API_QUERY)
        
        logger.info(f"Fetched {len(articles)} articles from News API.")
        
        for article in articles:
            # Save raw article data
            storage_client.save(article, 'news_api', data_type='raw')
            
            # Process and save processed article data
            processed_article = process_data(article, source_type='news')
            if processed_article:
                storage_client.save(processed_article, 'news_api', data_type='processed')
    else:
        logger.warning("News API key not configured. Skipping news fetch.")

    logger.info("News API fetch finished.")
    logger.info("Pipeline run completed successfully.")