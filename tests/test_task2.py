import unittest
import numpy as np
import pandas as pd
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
        dc = DataCleaning()
        with self.assertRaises(AttributeError):
            dc.get_people_with_no_interest(self.people_data)

    def test_clean_phone_numbers(self):
        expected_result = {
            "Name": ["Person1", "Person2", "Person3", "Person4"],
            "Interest1": ["biking", None, "hiking", None],
            "Interest2": ["painting", None, "hiking", "cubing"],
            "Interest3": ["boxing", None, "reading", "cycling"],
            "Interest4": ["singing", None, "boxing", None],
            "PhoneNumber": ["725-713-7311", "214-679-4284", "480-887-0512", None]
        }

        dc = DataCleaning()
        result = dc.clean_phone_numbers(self.people_data_df)

        result = result.to_dict(orient='list')
        self.assertEqual(result, expected_result)

    def test_spell_check(self):
        test_Series = np.array(['cycl ', 'badminton', '  hiking ', 'crckt'])
        expected_series = pd.Series(np.array(['cycle', 'badminton', 'hiking', 'cricket']))
        dc = DataCleaning()
        result = dc.spell_check(pd.Series(test_Series))
        self.assertTrue(result.compare(expected_series).empty)
