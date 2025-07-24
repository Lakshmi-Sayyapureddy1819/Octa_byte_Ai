# Design Document: Logistics Data Pipeline

## 1\. Architecture and Data Flow

The data pipeline is designed as a serverless, modular architecture on AWS to ensure scalability and automation.

### High-Level Architecture

```text
+----------------------+      +-----------------------+      +-------------------------+
| Amazon EventBridge   |----->|  AWS Lambda Function  |----->|  Amazon CloudWatch      |
| (Scheduler)          |      |  (Orchestrator)       |      |  (Logs & Alerts)        |
+----------------------+      +-----------------------+      +-------------------------+
                                      |
                                      |
             +------------------------+------------------------+
             |                                                |
             v                                                v
+--------------------------+                         +----------------------+
|  Crawlers & API Fetcher  |                         |  Amazon S3 Bucket    |
|  (Data Ingestion)        |------------------------>|  (Raw & Processed)   |
+--------------------------+                         +----------------------+
```

### Flow of Execution

1.  An **Amazon EventBridge** rule triggers the pipeline on a defined schedule (e.g., daily).
2.  The **AWS Lambda Function** starts, executing the orchestration logic.
3.  The orchestrator calls the **Crawlers** and the **News API Fetcher** to ingest data from all specified sources.
4.  Each crawler fetches the full HTML, extracts metadata, media URLs, and text content.
5.  The orchestrator creates both a `raw` version (original data) and a `processed` version (cleaned data).
6.  Both versions are saved to the **Amazon S3 Bucket**, organized into partitioned directories.
7.  All execution logs and errors are automatically sent to **Amazon CloudWatch**.

-----

## 2\. S3 Bucket Structure

The S3 bucket is organized with a partitioned structure to allow for efficient data querying and management.

```text
s3://<your-bucket-name>/
├── raw/
│   ├── <source_name>/
│   │   └── <date>/
│   │       └── <timestamp>.json.gz
│   └── ...
└── processed/
    ├── <source_name>/
    │   └── <date>/
    │       └── <timestamp>.json.gz
    └── ...
```

  * **`<source_name>`**: The name of the website (e.g., `freightwaves`) or `news_api`.
  * **`<date>`**: The date of the crawl (e.g., `2025-07-24`).
  * **`<timestamp>.json.gz`**: The data saved in a compressed GZIP JSON file, named with a unique timestamp to prevent overwrites.

-----

## 3\. Adding a New Website

The modular design makes it simple to add new data sources.

1.  **Create a New Crawler File**: In the `crawlers/` directory, create a new file (e.g., `new_site_crawler.py`) with a class that inherits from `BaseCrawler`.
2.  **Add to Configuration**: Open `config.py` and add the new website's name and URL to the `WEBSITES` dictionary.
3.  **Update Orchestrator**: In `pipeline/orchestrator.py`, import the new crawler class and add it to the `crawlers` dictionary.
4.  **Redeploy**: Package the updated code and redeploy it to AWS Lambda.