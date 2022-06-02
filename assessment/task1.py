import pandas as pd
import os
import logging

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger("task1")


def convert_csv_to_json(source_file_path: str, destination: str) -> None:
    logger.info("Reading CSV file")
    df = pd.read_csv(source_file_path)
    logger.info("Converting CSV file to JSON")
    df.to_json(destination, orient='records')
    logger.info("Completed conversion of CSV to JSON")


folder_path = "./data/"
folder_path = "/Users/amanmishra/Desktop/aman/asessment/ml_data_engineer_assessment/data/"
csv_file_path = os.path.join(folder_path, "people.csv")
destination_path = os.path.join(folder_path, "people.json")

convert_csv_to_json(csv_file_path, destination_path)