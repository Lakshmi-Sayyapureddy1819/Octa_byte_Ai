import re
from bs4 import BeautifulSoup
import config
from .storage import get_storage_clients
from utils.helpers import get_logger
from crawlers.gnosis_freight_crawler import GnosisFreightCrawler
from crawlers.thelogisticsoflogistics_crawler import TheLogisticsOfLogisticsCrawler
from crawlers.freightwaves_crawler import FreightwavesCrawler
from crawlers.leadiq_crawler import LeadiqCrawler
from crawlers.g2_crawler import G2Crawler
from crawlers.marketsandmarkets_crawler import MarketsAndMarketsCrawler
from news_api.news_fetcher import NewsFetcher

def process_data(raw_data, source_type):
    """
    Cleans and transforms raw data into a processed format.
    """
    if not raw_data:
        return None

    if source_type == 'webpage':
        if not raw_data.get("raw_html"):
            return None
        # Use BeautifulSoup to parse HTML and extract text
        soup = BeautifulSoup(raw_data["raw_html"], 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        
        processed_data = {
            "url": raw_data.get("url"),
            "crawled_at": raw_data.get("crawled_at"),
            "metadata": raw_data.get("metadata"),
            "cleaned_content": text
        }
        return processed_data

    elif source_type == 'news':
        # For news articles, the content is often already clean
        if not raw_data.get("content"):
            return None
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
    Executes the full data pipeline: crawl, process, and store in all configured locations.
    """
    logger = get_logger("Orchestrator")
    logger.info("Pipeline run started.")
    
    # 1. Initialize all active storage clients from config
    storage_clients = get_storage_clients(config.STORAGE_CONFIG)
    if not storage_clients:
        logger.warning("No storage clients configured. Data will not be saved.")
        return

    def save_to_all(data, source, data_type):
        """Helper function to save data to all configured storage providers."""
        for client in storage_clients:
            client.save(data, source, data_type)

    # 2. Crawl websites
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
            # Save raw data to all storage locations
            save_to_all(raw_data, name, data_type='raw')
            
            # Process and save processed data to all locations
            processed_data = process_data(raw_data, source_type='webpage')
            if processed_data:
                save_to_all(processed_data, name, data_type='processed')
        else:
            logger.warning(f"No data returned from {name} crawler.")

    logger.info("Website crawling finished.")

    # 3. Fetch news articles
    logger.info("Starting news API fetch.")
    if config.NEWS_API_KEY and config.NEWS_API_KEY != "YOUR_NEWS_API_KEY":
        news_fetcher = NewsFetcher(config.NEWS_API_KEY)
        articles = news_fetcher.fetch_news(config.NEWS_API_QUERY)
        
        logger.info(f"Fetched {len(articles)} articles from News API.")
        
        for article in articles:
            # Save raw article data
            save_to_all(article, 'news_api', data_type='raw')
            
            # Process and save processed article data
            processed_article = process_data(article, source_type='news')
            if processed_article:
                save_to_all(processed_article, 'news_api', data_type='processed')
    else:
        logger.warning("News API key not configured. Skipping news fetch.")

    logger.info("News API fetch finished.")
    logger.info("Pipeline run completed successfully.")