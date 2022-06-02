import os
import pandas as pd


class DataCleaning:

    def __init__(self):
        pass

    def get_people_with_no_interest(self, df: pd.DataFrame) -> pd.DataFrame:
        people_with_no_interest = df[df['Interest3'].isnull() & df['Interest2'].isnull().values
                                     & df['Interest1'].isnull().values & df['Interest4'].isnull().values]

        return people_with_no_interest

    def clean_phone_numbers(self, df: pd.DataFrame):
        df['PhoneNumber'] = df['PhoneNumber'].replace(regex='\.', value="-")\
                   .replace(regex='x(.*?)', value="")
        return df

    def clean(self, csv_file_path: str):
        people_df = pd.read_csv(csv_file_path)

        # Cleaning Step 1 - Removing people with no interest
        people_with_no_interest = self.get_people_with_no_interest(people_df)

        people_with_at_least_1_interest = pd.concat([people_df, people_with_no_interest]).drop_duplicates(keep=False)

        # Cleaning Step 2 - Formatting phone numbers by removing garbage value
        clean_df = self.clean_phone_numbers(people_with_at_least_1_interest)
        print(clean_df)


if __name__ == "__main__":
    folder_path = "/Users/amanmishra/Desktop/aman/asessment/ml_data_engineer_assessment/data/"
    input_file_path = os.path.join(folder_path, "people.csv")
    DataCleaning().clean(input_file_path)