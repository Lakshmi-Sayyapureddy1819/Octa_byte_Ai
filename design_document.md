# Design Document: Logistics Data Pipeline

## 1. Architecture and Data Flow

The data pipeline is designed to be modular and extensible. The high-level architecture is as follows:

```
+----------------+      +-----------------+      +---------------+
|   Orchestrator |----->|     Crawlers    |----->|    Storage    |
|   (main.py)    |      | (for each site) |      | (Local/S3)    |
+----------------+      +-----------------+      +---------------+
       |
       |                +-----------------+
       +--------------->|   News Fetcher  |
                        |    (NewsAPI)    |
                        +-----------------+
```

### Flow of Execution

1.  The `main.py` script calls the `run_pipeline` function in the `orchestrator`.
2.  The orchestrator initializes the storage client (in this case, for local storage).
3.  It then iterates through a list of crawler objects, calling the `crawl` method for each.
4.  Each crawler fetches the HTML (or uses Selenium for dynamic pages), parses the content, and returns a structured dictionary.
5.  The orchestrator takes the returned data and passes it to the storage client to be saved.
6.  Next, the orchestrator initializes the `NewsFetcher` and retrieves relevant news articles.
7.  Each article is then saved to storage.

## 2. Local Storage Structure

As an alternative to AWS S3, the local file system is used with the following structure:

```
data/
├── raw/
│   ├── <source_name>/
│   │   ├── <date>/
│   │   │   ├── <timestamp>.json
│   │   │   └── ...
│   │   └── ...
│   └── ...
└── processed/
    └── ... (for future use)
```

* **`<source_name>`**: The name of the website or 'news\_api'.
* **`<date>`**: The date of the crawl (e.g., `2025-07-21`).
* **`<timestamp>.json`**: The raw data saved in a JSON file, named with a unique timestamp.

## 3. Adding a New Website

To add a new website to the crawler:

1.  **Create a new crawler file** in the `crawlers/` directory (e.g., `new_site_crawler.py`). It should inherit from `BaseCrawler` and implement the `crawl` method.
2.  **Add the website URL** to the `WEBSITES` dictionary in `config.py`.
3.  **Update `pipeline/orchestrator.py`** to import and instantiate your new crawler.