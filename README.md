# Logistics and Supply Chain Data Pipeline

This project contains a data pipeline to crawl logistics and supply chain websites and fetch news from a news API.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd logistics-data-pipeline
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the News API Key:**
    Open `config.py` and replace `"YOUR_NEWS_API_KEY"` with your actual key from [NewsAPI](https://newsapi.org/).

## How to Run

To run the entire pipeline, execute the `main.py` script:

```bash
python main.py
```

This will crawl the configured websites and fetch news, saving the raw data into the `data/raw` directory.

## Alternative to AWS

This project uses local file storage as a free alternative to AWS S3. The `pipeline/storage.py` file handles saving the data in a structured way under the `data/` directory. For scheduling, you can use your operating system's built-in tools:

* **Cron (Linux/macOS):**
    ```bash
    # Edit your crontab
    crontab -e

    # Add this line to run the pipeline daily at 2 AM
    0 2 * * * /path/to/your/project/venv/bin/python /path/to/your/project/main.py
    ```

* **Task Scheduler (Windows):**
    You can use the Task Scheduler GUI to create a new task that runs the `main.py` script at your desired interval.