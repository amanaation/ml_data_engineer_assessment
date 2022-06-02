import unittest

import pandas as pd
import pytest
from assessment.task2 import DataCleaning


class TestTask2(unittest.TestCase):
    def setUp(self) -> None:
        self.people_data = {
            "Name": ["Person1", "Person2", "Person3", "Person4"],
            "Interest1": ["biking", None, "hiking", None],
            "Interest2": ["painting", None, "hiking", "cubing"],
            "Interest3": ["boxing", None, "reading", "cycling"],
            "Interest4": ["singing", None, "boxing", None],
            "PhoneNumber": ["725-713-7311x162", "214.679.4284", "480.887.0512x484", None]
        }

        self.people_data_df = pd.DataFrame(self.people_data)

    def test_get_people_with_no_interest(self):
        expected_data = [{"Name": "Person2", "Interest1": None, "Interest2": None,
                         "Interest3": None, "Interest4": None, "PhoneNumber": "214.679.4284"}]

        dc = DataCleaning()
        result = dc.get_people_with_no_interest(self.people_data_df)
        result_json = result.to_dict(orient='records')

        self.assertEqual(expected_data, result_json)

    def test_get_people_with_no_interest_failure(self):
        pass