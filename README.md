# Logistics and Supply Chain Data Pipeline

[cite_start]This project is a scalable, automated pipeline designed to continuously crawl specified logistics/supply chain websites and news APIs. [cite: 6, 7] [cite_start]It processes the collected data and stores both raw and processed versions in AWS S3 and/or locally. [cite: 28] [cite_start]The entire pipeline is designed for automated, scheduled execution using AWS Lambda. [cite: 34]

## Features
-   [cite_start]Crawls 6 specified logistics and supply chain websites. [cite: 11]
-   [cite_start]Integrates with a free news API to fetch relevant articles. [cite: 23]
-   [cite_start]Handles both static and dynamic (JavaScript-rendered) web content. [cite: 19]
-   [cite_start]Stores data in both raw (HTML/JSON) and processed (cleaned text) formats. [cite: 28]
-   Supports dual storage to local filesystem and AWS S3.
-   [cite_start]Uses GZIP compression for efficient storage in S3. [cite: 31]
-   [cite_start]Designed for automated, serverless deployment on AWS Lambda. [cite: 49]

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd logistics-data-pipeline
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the application:**
    Open `config.py` and set your `NEWS_API_KEY` and S3 `bucket_name`.

## Local Setup and Execution

To run and test the pipeline on your local machine, you must first configure your AWS credentials.

1.  **Install the AWS CLI** (if you haven't already).
2.  **Configure credentials:**
    ```bash
    aws configure
    ```
    Enter your AWS Access Key ID and Secret Access Key when prompted.

3.  **Run the pipeline locally:**
    ```bash
    python main.py
    ```
    This will execute the entire pipeline and save the data to the locations specified in your `config.py` (`data/` folder and/or your S3 bucket).

## AWS Deployment for Automation

[cite_start]To deploy this as an automated pipeline, you will use several AWS services. [cite: 50]

1.  **Prepare AWS Resources**:
    * Create an S3 bucket to store the data.
    * Create an IAM Role for the Lambda function with permissions for S3 (`s3:PutObject`) and CloudWatch Logs.

2.  **Package the project**:
    Create a `.zip` file containing all project code (`.py` files, `crawlers/`, etc.) and the installed Python libraries from your virtual environment's `site-packages` directory.

3.  **Deploy to AWS Lambda**:
    * Create a new Lambda function with a Python runtime.
    * Upload your `.zip` file.
    * Set the **Handler** to `lambda_function.lambda_handler`.
    * Increase the **Timeout** to at least 3 minutes.
    * Attach the IAM Role you created.

4.  **Schedule the Pipeline**:
    In the Lambda console, add a trigger using **Amazon EventBridge (CloudWatch Events)**. [cite_start]Set a schedule using a cron expression (e.g., `cron(0 2 * * ? *)` for a daily run). [cite: 34]