import unittest
import gedcom_parser
import datetime

table = gedcom_parser.gedcom_table("gedcom_test.ged")
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

class TestGedcomFile(unittest.TestCase):
    # def test_birth_marr(self):
    #     for family in table[1]:
    #         for indiv in table[0]:
    #             if (indiv.id == family.husband or indiv.id == family.wife):
    #                 print(family.married)
    #                 temp_married = family.married.split(" ")
    #                 temp_birth = indiv.birth.split(" ")
    #                 self.assertTrue(datetime.datetime(int(temp_married[2]), month_dict[temp_married[1]], int(temp_married[0])) > datetime.datetime(int(temp_birth[2]), month_dict[temp_birth[1]], int(temp_birth[0])))
    
    def test_us_10(self):
        for family in table[1]:
            for indiv in table[0]:
                if (indiv.id == family.husband or indiv.id == family.wife):
                    temp_married = family.married.split(" ")
                    temp_birth = indiv.birth.split(" ")
                    check_14 = datetime.datetime(int(temp_married[2]), month_dict[temp_married[1]], int(temp_married[0])) > datetime.datetime(int(temp_birth[2])+14, month_dict[temp_birth[1]], int(temp_birth[0]))
                    if (not check_14):
                        print(indiv.name + "Marriage date is before 14")
                        break

    def test_us_07(self):
        for indiv in table[0]:
            temp_birth = indiv.birth.split(" ")
            check = datetime.datetime(int(temp_birth[2])+150, month_dict[temp_birth[1]], int(temp_birth[0])) > datetime.datetime.now()
            if (not check):
                print(indiv.name + "is Less Than 150 years old")
                break
    
    
