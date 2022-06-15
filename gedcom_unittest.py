import unittest
import gedcom_parser
# from dateutil.parser import *
import datetime
from datetime import date
from gedcom_parser import p_table, f_table


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


print(p_table)
print(f_table)

class TestGedcomFile(unittest.TestCase):

    #US 01 - Dates (birth, marriage, divorce, death) should not be after the current date
    def test_birth_marr(self):
        for family in table[1]:
            for indiv in table[0]:
                if (indiv.id == family.husband or indiv.id == family.wife):
                    # print(family.married)
                    temp_married = family.married.split(" ")
                    temp_birth = indiv.birth.split(" ")
                    checkDate = (datetime.datetime(int(temp_married[2]), month_dict[temp_married[1]], int(temp_married[0])) > datetime.datetime(int(temp_birth[2]), month_dict[temp_birth[1]], int(temp_birth[0])))
                    if(not checkDate):
                        print('Dates (birth, marriage, divorce, death) should not be after the current date')
                        return
        print('Test 1 passed succesfully')

    #US 02 - Birth should occur before marriage of an individual
    def test_us_02(self):
        for family in table[1]:
            for indiv in table[0]:
                if(indiv.id == family.husband or indiv.id == family.wife):
                    temp_birth = indiv.birth.split(" ")
                    temp_married = family.married.split(" ")
                    checkMarriage = datetime.datetime(int(temp_birth[2]), month_dict[temp_birth[1]], int(temp_birth[0])) < datetime.datetime(int(temp_married[2]), month_dict[temp_married[1]], int(temp_married[0]))
                    if(not checkMarriage):
                        print('Birth should occur before marriage of an individual')
                        return
        print('Test 2 passed succesfully')
        
    #User story 3 - Birth should occur before death of an individual
    def test_us_03(self):
            for indiv in table[0]:
                temp_death = indiv.death.split(" ")
                temp_birth = indiv.birth.split(" ")
                if indiv.death is not None:
                    birth = datetime.datetime(int(temp_birth[2]), month_dict[temp_birth[1]], int(temp_birth[0]))
                    death = datetime.datetime(int(temp_death[2]), month_dict[temp_death[1]], int(temp_death[0]))
                    if birth > death:
                        print("ERROR: INDIVIDUAL: US03: {}: {}: death {} before birth {}".format(indiv['num']+4, indiv['INDI'],death, birth))
                        return
            print('Test 3 passed succesfully')


    #User story 4 - Marriage should occur before divorce of spouses, and divorce can only occur after marriage


    #User story 5 - Marriage should occur before death of either spouse
    def test_us_5(self):
        for family in table[1]:
            for indiv in table[0]:
                if (indiv.id == family.husband or indiv.id == family.wife):
                    temp_death = indiv.death.split(" ")
                    temp_married = family.married.split(" ")
                    marriage = datetime.datetime(int(temp_married[2]), month_dict[temp_married[1]], int(temp_married[0]))     
                    death = datetime.datetime(int(temp_death[2]), month_dict[temp_death[1]], int(temp_death[0]))
                    if marriage > death:
                        print("ERROR: INDIVIDUAL: US05: {}: {}: death {} before marriage {}".format(indiv['num']+4, indiv['INDI'],death, marriage))
                        return
        print('Test 5 passed succesfully')

    #User story 6 - Divorce can only occur before death of both spouses

    #User story 07 -Death should be less than 150 years after birth for dead people, and current date should be less than 150 years after birth for all living people
    def test_us_07(self):
        for indiv in table[0]:
            temp_birth = indiv.birth.split(" ")
            temp_alive = indiv.alive
            if(temp_alive == 'False'):
                temp_death = indiv.death.split(" ")
                checkDeathDate = int(temp_death[2]) - int(temp_birth[2])
                if checkDeathDate > 150:
                    print("Death should be less than 150 years after birth for dead people")
                    return
            else:
                checkBirthDate = date.today().year - int(temp_birth[2])
                if(checkBirthDate > 150):
                    print("Current date should be less than 150 years after birth for all living people")
                    return
        print('Test 7 passed succesfully')
    
    #User story 8 - Children should be born after marriage of parents (and not more than 9 months after their divorce)

    #User story 9 - Child should be born before death of mother and before 9 months after death of father

    #User story 10 - Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
    def test_us_10(self):
        for family in table[1]:
            for indiv in table[0]:
                if (indiv.id == family.husband or indiv.id == family.wife):
                    temp_married = family.married.split(" ")
                    temp_birth = indiv.birth.split(" ")
                    check_14 = datetime.datetime(int(temp_married[2]), month_dict[temp_married[1]], int(temp_married[0])) > datetime.datetime(int(temp_birth[2])+14, month_dict[temp_birth[1]], int(temp_birth[0]))
                    if (not check_14):
                        print(indiv.name + "Marriage date is before 14")
                        return
        print('Test 10 passed succesfully')

if __name__ == '__main__':
    unittest.main()

 
