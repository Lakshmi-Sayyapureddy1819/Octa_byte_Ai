# Testing Report
## 1. Sample Crawled Data

The pipeline successfully ingests and processes data, storing both a raw and a processed version. Below is a sample of a **processed** record, showing the cleaned text and extracted media URLs and metadata. [cite: 66]

```json
{
    "url": "[https://www.freightwaves.com/](https://www.freightwaves.com/)",
    "crawled_at": "2025-07-24T07:10:00.123456Z",
    "metadata": {
        "title": "FreightWaves | The #1 Source for Freight News & Analytics",
        "description": "FreightWaves is the world's leading supply chain intelligence platform, providing news, data, and analytics.",
        "keywords": "freight, logistics, supply chain, trucking, maritime",
        "og:image": "[https://www.freightwaves.com/static/images/og-image.jpg](https://www.freightwaves.com/static/images/og-image.jpg)"
    },
    "text_content": "SONAR provides the fastest freight market data in the world. More stories from FreightWaves. American Shipper. Subscribe to our newsletter...",
    "media_urls": [
        "[https://www.freightwaves.com/static/images/logo.svg](https://www.freightwaves.com/static/images/logo.svg)",
        "[https://www.freightwaves.com/static/images/og-image.jpg](https://www.freightwaves.com/static/images/og-image.jpg)"
    ]
}
```

## 2. Validation of Incremental Updates

The current storage mechanism saves each crawled item as a new file with a unique timestamp (`YYYYMMDDHHMMSSf.json`). This ensures that:

* **No data is overwritten:** Each run creates new files.
* **Incremental by nature:** By processing files based on their creation date, you can easily identify new data.

A more advanced deduplication logic could be implemented by calculating a checksum of the article's content and checking if it already exists before saving.