# lambda_function.py

# This block allows the Lambda environment to find your project's modules
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from pipeline.orchestrator import run_pipeline
from utils.helpers import get_logger

# Initialize a logger for the Lambda handler
logger = get_logger("LambdaHandler")

def lambda_handler(event, context):
    """
    AWS Lambda handler function. 
    
    This function is the starting point for execution on AWS Lambda. It is
    triggered by an event, such as a schedule from Amazon EventBridge.
    """
    logger.info("Lambda function execution started.")
    try:
        # Call the main pipeline function from the orchestrator
        run_pipeline()
        logger.info("Pipeline executed successfully.")
        return {
            'statusCode': 200,
            'body': 'Pipeline executed successfully.'
        }
    except Exception as e:
        # Log any errors that occur during the pipeline run 
        logger.error(f"An error occurred during pipeline execution: {e}")
        # This could be extended to send an alert to email or Slack 
        return {
            'statusCode': 500,
            'body': f'Pipeline execution failed: {e}'
        }