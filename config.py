# List of websites to crawl
WEBSITES = {
    "gnosis_freight": "http://www.gnosisfreight.com",
    "the_logistics_of_logistics": "https://www.thelogisticsoflogistics.com/",
    "freightwaves": "https://www.freightwaves.com",
    "leadiq": "https://leadiq.com/c/gnosis-freight/5fcf6529a856d346f831079f",
    "g2": "https://www.g2.com/",
    "markets_and_markets": "https://www.marketsandmarkets.com/Market-Reports/supply-chain-management-market-190997554.html"
}

# News API configuration
NEWS_API_KEY = "091b719164eb4bbbbbbdc05c4b07477c"  # Replace with your actual NewsAPI key
NEWS_API_QUERY = "logistics OR supply chain"

# Storage configuration to enable multiple providers
# Add or remove providers from the 'active' list as needed.
STORAGE_CONFIG = {
    "active": ["local", "aws"], # Use both local and aws
    "providers": {
        "local": {
            "base_path": "data"
        },
        "aws": {
            "bucket_name": "your-logistics-data-bucket" # <-- Change to your S3 bucket name
        }
    }
}