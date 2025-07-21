# Testing Report

## 1. Sample Crawled Data

Here is a sample of the data structure for a crawled webpage:

```json
{
    "url": "[http://www.gnosisfreight.com](http://www.gnosisfreight.com)",
    "title": "Gnosis Freight | The Leader in Container Tracking Visibility",
    "content": "..."
}
```

And for a news article:

```json
{
    "source": {
        "id": "reuters",
        "name": "Reuters"
    },
    "author": "Reuters",
    "title": "Global supply chain pressures ease in June - NY Fed",
    "description": "...",
    "url": "...",
    "urlToImage": "...",
    "publishedAt": "2024-07-05T15:01:00Z",
    "content": "..."
}
```

*Note: 10 sample JSON files per source would be generated in the `data/raw` directory upon running the pipeline.*

## 2. Validation of Incremental Updates

The current storage mechanism saves each crawled item as a new file with a unique timestamp (`YYYYMMDDHHMMSSf.json`). This ensures that:

* **No data is overwritten:** Each run creates new files.
* **Incremental by nature:** By processing files based on their creation date, you can easily identify new data.

A more advanced deduplication logic could be implemented by calculating a checksum of the article's content and checking if it already exists before saving.