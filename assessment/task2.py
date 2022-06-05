"""
I was able to think of the following cleanings possible:
1. Remove the unnecessary spaces in the interest column.
2. Converting all the texts in interests column to lowercase
3. Spelling check for incorrect spelled words in interests column
4. Formatting the phone numbers. Replacing `.` with `-` to maintain consistency
5. [Optional] Removing records that have no entries in any of the interests column depending upon the criteria
"""

import os
import pandas as pd
from autocorrect import Speller
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s',
                    level=logging.NOTSET)
logger = logging.getLogger(__name__)


class DataCleaning:
    """
    The DataCleaning class contains 3 main cleaning functions:
    1. clean_phone_numbers : Cleans and convert all the Phone Numbers in a uniform format
    2. get_people_with_no_interest: AS the name suggests, it cleans the records that has no entry in any
    of the interest column.
    3. casing_and_spell_check: This function formats every value to lowercase for better grouping and improves the spelling
    error
    """

    def __init__(self):
        pass

    def get_people_with_no_interest(self, df: pd.DataFrame) -> pd.DataFrame:
        people_with_no_interest = df[df['Interest3'].isnull() & df['Interest2'].isnull().values
                                     & df['Interest1'].isnull().values & df['Interest4'].isnull().values]

        return people_with_no_interest

    def clean_phone_numbers(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'PhoneNumber' in df.columns:
            df['PhoneNumber'] = df['PhoneNumber'].replace(regex='\.', value="-") \
                .replace(regex='x(.*?)$', value="")
        return df

    def casing_and_spell_check(self, series: pd.Series) -> pd.Series:
        """
        This functions, takes in a a series as the input and does the following:
        1. Removes the trailing spaces
        2. Converts all the elements in
        3. Modifies the element if there is any spell check i.e., if there is a spelling mistake
        in the word `crckt`, the function will convert it to `cricket`.
        Note: This function is not 100% accurate when it comes to correcting the spelling mistakes.
        For e.g., it will convert the word `crick' to `click' instead of `cricket`
        lower case
        :param series: DataFrame Series
        :return: DataFrame Series
        """
        spell = Speller(lang='en')
        series = series.map(lambda x: x.strip() if type(x) == str else x)
        series = series.map(lambda x: x.lower() if type(x) == str else x)
        series = series.map(lambda x: spell(x) if type(x) == str else x)
        return series

    def clean(self, csv_file_path: str) -> pd.DataFrame:
        people_df = pd.read_csv(csv_file_path)

        # [Optional] Cleaning Step 1 - Removing people with no interest
        logger.info("Removing people with no interests")
        people_with_no_interest = self.get_people_with_no_interest(people_df)

        people_with_at_least_1_interest = pd.concat([people_df, people_with_no_interest]).drop_duplicates(keep=False)

        # Cleaning Step 2 - Formatting phone numbers by removing garbage value
        logger.info("Formatting Phone Number")
        df = self.clean_phone_numbers(people_with_at_least_1_interest)

        # Cleaning Step 3 - Formatting Interests column
        logger.info("Formatting Interests1 column")
        df['Interest1'] = self.casing_and_spell_check(df['Interest1'])

        logger.info("Formatting Interests2 column")
        df['Interest2'] = self.casing_and_spell_check(df['Interest2'])

        logger.info("Formatting Interests3 column")
        df['Interest3'] = self.casing_and_spell_check(df['Interest3'])

        logger.info("Formatting Interests4 column")
        df['Interest4'] = self.casing_and_spell_check(df['Interest4'])

        logger.info("Completed cleaning of data")
        return df


if __name__ == "__main__":
    folder_path = "/Users/amanmishra/Desktop/aman/asessment/ml_data_engineer_assessment/data/"
    input_file_path = os.path.join(folder_path, "people.csv")
    DataCleaning().clean(input_file_path)
