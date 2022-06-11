import unittest
import gedcom_parser
import datetime

table = gedcom_parser.gedcom_table("gedcom_test.ged") 

class TestGedcomFile(unittest.TestCase):
    def test_birth_marr(self):
        month_dict = {"JAN": 1,
            "FEB": 2,
            "MAR": 3,
            "APR": 4,
            "MAY": 5,
            "JUN": 6,
            "JUL": 7,
            "AUG": 8,
            "SEP": 9,
            "OCT": 10,
            "NOV": 11,
            "DEC": 12}
        for row in table[0]:
            row.border = False
            row.header = False
            temp_date = row.get_string(fields=["Birthday"]).strip().split(" ")
            temp_date = datetime.datetime(int(temp_date[2]), month_dict[temp_date[1]], int(temp_date[0]))
            curr_date = datetime.now()
        self.assertTrue(datetime.datetime(1939, month_dict["MAY"], 6) > datetime.datetime(1915, month_dict["APR"], 6))
        self.assertTrue(datetime.datetime(1939, month_dict["MAY"], 6) > datetime.datetime(1915, month_dict["FEB"], 11))
        self.assertTrue(datetime.datetime(1940, month_dict["DEC"], 31) > datetime.datetime(1915, month_dict["APR"], 6))
        self.assertTrue(datetime.datetime(1940, month_dict["DEC"], 31) > datetime.datetime(1910, month_dict["APR"], 2))
        self.assertTrue(datetime.datetime(1910, month_dict["AUG"], 10) > datetime.datetime(1884, month_dict["JUL"], 9))
        self.assertTrue(datetime.datetime(1910, month_dict["AUG"], 10) > datetime.datetime(1885, month_dict["OCT"], 6))
