import unittest
import gedcom_parser
# from dateutil.parser import parse
import datetime
from datetime import date, timedelta
from gedcom_parser import Individual, p_table, f_table, Family


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


# print(p_table)
# print(f_table)

class TestGedcomFile(unittest.TestCase):

    #US 01 - Dates (birth, marriage, divorce, death) should not be after the current date
    def test_us_1(self):
        for family in table[1]:
            for indiv in table[0]:
                if (indiv.id == family.husband or indiv.id == family.wife):
                    temp_married = family.married.split(" ")
                    temp_birth = indiv.birth.split(" ")
                    checkDate = (datetime.datetime(int(temp_married[2]), month_dict[temp_married[1]], int(temp_married[0])) > datetime.datetime(int(temp_birth[2]), month_dict[temp_birth[1]], int(temp_birth[0])))
                    if(not checkDate):
                        print('Dates (birth, marriage, divorce, death) should not be after the current date')
                        return
        print('Test 1 passed succesfully')

    #US 02 - Birth should occur before marriage of an individual
    def test_us_2(self):
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
    def test_us_3(self):
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
    def test_us_4(self):
        for family in table[1]:
            for indiv in table[0]:
                if (indiv.id == family.husband or indiv.id == family.wife):
                    temp_divorce = family.divorced.split(" ")
                    temp_married = family.married.split(" ")
                    marriage = datetime.datetime(int(temp_married[2]), month_dict[temp_married[1]], int(temp_married[0]))   
                    divorce = datetime.datetime(int(temp_divorce[2]), month_dict[temp_divorce[1]], int(temp_divorce[0]))
                    if marriage > divorce:
                        print("ERROR: INDIVIDUAL: US06: {}: {}: divorce {} before marriage {}".format(indiv['num']+4, indiv['INDI'],divorce, marriage))
                        return
        print('Test 4 passed succesfully')

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
    def test_us_6(self):
        for family in table[1]:
            for indiv in table[0]:
                if (indiv.id == family.husband or indiv.id == family.wife):
                    temp_death = indiv.death.split(" ")
                    temp_divorce = family.divorced.split(" ")
                    death = datetime.datetime(int(temp_death[2]), month_dict[temp_death[1]], int(temp_death[0]))
                    divorce = datetime.datetime(int(temp_divorce[2]), month_dict[temp_divorce[1]], int(temp_divorce[0]))
                    if divorce > death:
                        print("ERROR: INDIVIDUAL: US06: {}: {}: death {} before divorce {}".format(indiv['num']+4, indiv['INDI'],death, divorce))
                        return
        print('Test 6 passed succesfully')


    #User story 07 -Death should be less than 150 years after birth for dead people, and current date should be less than 150 years after birth for all living people
    def test_us_7(self):
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
    def test_us_8(self):
        for family in table[1]:
            for indiv in table[0]:
                if (family.children == indiv.id):
                    temp_child_birth = indiv.birth.split(" ")
                    for indiv in table[0]:
                        if(indiv.id == family.wife or indiv.id == family.husband):
                            temp_marriage = family.married.split(" ")
                            checkBirthDate = datetime.datetime(int(temp_child_birth[2]), int(month_dict[temp_child_birth[1]]), int(temp_child_birth[0])) > datetime.datetime(int(temp_marriage[2]), int(month_dict[temp_marriage[1]]), int(temp_marriage[0]))
                            if(not checkBirthDate):
                                print("Children should be born after marriage of parents (and not more than 9 months after their divorce)")
                                return
        print('Test 8 passed succesfully')
    #User story 9 - Child should be born before death of mother and before 9 months after death of father
    def test_us_9(self):
        for family in table[1]:
            for indiv in table[0]:
                if (family.children == indiv.id):
                    temp_child_birth = indiv.birth.split(" ")
                    for indiv in table[0]:
                        if(indiv.id == family.wife or indiv.id == family.husband):
                            if(indiv.id == family.wife):
                                temp_wife = indiv.birth.split(" ")
                                temp_alive = indiv.alive
                                if(temp_alive == 'False'):
                                    temp_death = indiv.death.split(" ")
                                    checkBirthDate = datetime.datetime(int(temp_child_birth[2]), int(month_dict[temp_child_birth[1]]), int(temp_child_birth[0])) < datetime.datetime(int(temp_death[2]), int(month_dict[temp_death[1]]), int(temp_death[0]))
                                    if(not checkBirthDate):
                                        print("Child should be born before death of mother and before 9 months after death of father")
                                        return
                                else:
                                    checkWife = datetime.datetime(int(temp_child_birth[2]), int(month_dict[temp_child_birth[1]]), int(temp_child_birth[0]))<datetime.datetime(int(temp_wife[2]), int(month_dict[temp_wife[1]]), int(temp_wife[0]))
                                    if(not checkWife):
                                        print("Child should be born before death of mother and before 9 months after death of father")
                                        return
                            else:
                                temp_husband = indiv.birth.split(" ")
                                temp_alive = indiv.alive
                                if(temp_alive == 'False'):
                                    temp_death = indiv.death.split(" ")
                                    if (month_dict[temp_death[1]] + 9 > 12):
                                        month_dict[temp_death[1]] = month_dict[temp_death[1]] + 9
                                        month_dict[temp_death[1]] = month_dict[temp_death[1]] - 12
                                        temp_death[2] = int(temp_death[2]) + 1
                                    checkBirthDate = datetime.datetime(int(temp_child_birth[2]), int(month_dict[temp_child_birth[1]]), int(temp_child_birth[0])) < datetime.datetime(int(temp_death[2]), int(month_dict[temp_death[1]]), int(temp_death[0]))
                                    if(not checkBirthDate):
                                        print("Child should be born before death of mother and before 9 months after death of father")
                                        return
                                else:
                                    checkWife = datetime.datetime(int(temp_child_birth[2]), int(month_dict[temp_child_birth[1]]), int(temp_child_birth[0]))<datetime.datetime(int(temp_husband[2]), int(month_dict[temp_husband[1]]), int(temp_husband[0]))
                                    if(not checkWife):
                                        print("Child should be born before death of mother and before 9 months after death of father")
                                        return
        print('Test 9 passed succesfully')


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


    #User story 13 - Birth dates of siblings should be more than 8 months apart or less than 2 days apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)
    def test_us_13(self):
        for family in table[1]:
            for indiv in table[0]:
                if indiv.id in family.children:
                    if len(family.children) >= 2:
                        for child in family.children:
                            for i in table[0]:
                                if (child==i.id):
                                    temp_birth = indiv.birth.split(" ")
                                    indiv_birth = datetime.datetime(int(temp_birth[2]), month_dict[temp_birth[1]], int(temp_birth[0]))
                                    temp_child = i.birth.split(" ")
                                    child_birth = datetime.datetime(int(temp_child[2]), month_dict[temp_child[1]], int(temp_child[0]))
                                    check_birth = abs((indiv_birth.year - child_birth.year)*12 + (indiv_birth.month - child_birth.month)) > 8 or abs( (indiv_birth - child_birth).days ) < 2
                                    if not check_birth:
                                        print("Children should be born more than 8 months apart or less than 2 days apart")
                                        return
        print('Test 13 passed succesfully')
    #User story 14 - No more than five siblings should be born at the same time
    def test_us_14(self):
        for family in table[1]:
            for indiv in table[0]:
                count = 0
                if indiv.id in family.children:
                    if len(family.children) > 5:
                        for child in family.children:
                            for i in table[0]:
                                if (child==i.id):
                                    temp_birth = indiv.birth.split(" ")
                                    indiv_birth = datetime.datetime(int(temp_birth[2]), month_dict[temp_birth[1]], int(temp_birth[0]))
                                    temp_child = i.birth.split(" ")
                                    child_birth = datetime.datetime(int(temp_child[2]), month_dict[temp_child[1]], int(temp_child[0]))
                                    check_birth = abs( (indiv_birth - child_birth).days ) < 2
                                    if check_birth:
                                        count+=1
                                        if count>5:
                                            print("No more than five siblings should be born at the same time")
                                            return
                    else:
                        break
        print('Test 14 passed succesfully')

    #User story 15 - There should be fewer than 15 siblings in a family
    def test_us_15(self):
        for family in table[1]:
            for indiv in table[0]:
                if indiv.id in family.children:
                    if len(family.children) >= 15:
                        print("There should be fewer than 15 siblings in a family")
                        return
        print('Test 15 passed succesfully')

    #User story 16 - All male members of a family should have the same last name
    def test_us_16(self):
        for family in table[1]:
            checker = False
            for indiv in table[0]:
                if(family.husband == indiv.id):
                    temp_family_name = indiv.name.split(" ")
                    last_name = temp_family_name[1]
                    checker = True
                if (indiv.gender == "M" and indiv.name.split(" ")[1] != last_name and checker == True):
                    print('All male members of a family should have the same last name')
                    return    
        print('Test 16 passed successfully')


    #User story 21 - Husband in family should be male and wife in family should be female
    def test_us_21(self):
        for family in table[1]:
            for indiv in table[0]:
                if(family.husband == indiv.id):
                    if(indiv.gender != 'M'):
                        print('Husband in family should be male')
                if(family.wife == indiv.id):
                    if(indiv.gender != 'F'):
                        print('Wife in family should be female')
        print("Test 21 passed successfully")

    #User story 23 - No more than one individual with the same name and birth date should appear in a GEDCOM file
    def test_us_23(self):
        unique = []
        for indiv in table[0]:
            if [indiv.name, indiv.birth] not in unique:
                unique.append([indiv.name, indiv.birth])
            else:
                print("No more than one individual with the same name and birth date should appear in a GEDCOM file")
                return
        print('Test 23 passed successfully')

    #User story 24 - No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file
    def test_us_24(self):
        unique = []
        for family in table[1]:
            if [family.husband, family.wife, family.married] not in unique:
                unique.append([family.husband, family.wife, family.married])
            else:
                print("No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file")

    #User story 27 - List individuals with age
    def test_us_27(self):
        listOfNames = []
        for indiv in table[0]:
            temp_alive = indiv.alive
            temp_birth = indiv.birth.split(" ")
            if(temp_alive == 'False'):
                temp_death = indiv.death.split(" ")
                checkBirthDate = datetime.datetime(int(temp_death[2]), int(month_dict[temp_death[1]]), int(temp_death[0])) - datetime.datetime(int(temp_birth[2]), int(month_dict[temp_birth[1]]), int(temp_birth[0]))
                age = str(int(checkBirthDate.total_seconds()/(3600*24*365)))
                listOfNames.append(indiv.name + ", Age: " + age)
            else:
                checkBirthDate = datetime.datetime.now() - datetime.datetime(int(temp_birth[2]), int(month_dict[temp_birth[1]]), int(temp_birth[0]))
                age = str(int(checkBirthDate.total_seconds()/(3600*24*365)))
                listOfNames.append(indiv.name + ", Age: " + age)
        print(listOfNames)
        print("Test 27 passed successfully")

    #User story 29 - List all deceased individuals in a GEDCOM file
    def test_us_29(self):
        for indiv in table[0]:
            if (indiv.death != "N/A"):
                death_list = f"Test 29: {indiv.name} ({indiv.id}) is deceased"
                print(death_list)
                return(death_list)
            else:
                print('Test 29 passed successfully')
                return

    #User story 30 - List all living married people in a GEDCOM file
    def test_us_30(self):
        for indiv in table[0]:
            if (indiv.death == "N/A" and indiv.spouse != "N/A"):
                married_list = f"Test US30: {indiv.name} ({indiv.id}) is alive and married"
                print(married_list)
                return(married_list)
            else:
                print('Test 30 had no living married people')
                return

    # #User story 31 - List all living people over 30 who have never been married in a GEDCOM file
    def test_us_31(self):
        for family in table[1]:
            for indiv in table[0]:
                if (family.husband == "N/A" and family.wife.age > 30 and family.wife.alive):
                    print("into loop")
                    info_str = f"Story US31: {indiv.name} ({indiv.id}) is over 30 years old at {indiv.age} and not married"
                    print(info_str)
                    return info_str
                else:
                    print('Test 31 passed successfully')
                    return

    # #User story 32 - List all multiple births in a GEDCOM file
    def test_us_32(self):
        for family in table[1]:
            leng = len(family.chil_list)
            if (leng > 1):
                info_str = f"Story US32: Family {family.id} has multiple births ({leng}) on line "
                print(info_str)
                return info_str
            else:
                print('Test 32 passed successfully')
                return

    #User story 38 - List all living people in a GEDCOM file whose birthdays occur in the next 30 days
    def test_us_38(self):
        list_recent = []
        for indiv in table[0]:
            if (indiv.alive=='True'):
                temp_birth = indiv.birth.split(" ")
                indiv_birth = datetime.datetime(int(temp_birth[2]), month_dict[temp_birth[1]], int(temp_birth[0]))
                recent_birth = datetime.datetime.now()
                check_recent = (indiv_birth - recent_birth).days < 30
                if (check_recent):
                    list_recent.append(indiv.name)

        if not list_recent:
            print(f"Story US38: No living people whose birthdays occur in the next 30 days")
        else:
            for i in list_recent:
                print(i)
        print('Test 38 passed succesfully')

    #User story 39 - List all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days
    def test_us_39(self):
        list_recent = []
        for family in table[1]:
            for indiv in table[0]:
                if (indiv.alive=='True'):
                    temp_marr = family.marriage.split(" ")
                    fam_marr = datetime.datetime(int(temp_marr[2]), month_dict[temp_marr[1]], int(temp_marr[0]))
                    recent_marr = datetime.datetime.now()
                    check_recent = (fam_marr - recent_marr).days < 30
                    if (check_recent):
                        for i in table[0]:
                            if i.id==family.husband or i.id==family.wife:
                                list_recent.append([family.husband, family.wife])
                                break

        if not list_recent:
            print(f"Story US39: No living couples whose marriage anniversaries occur in the next 30 days")
        else:
            for i in list_recent:
                print(i)
        
        print('Test 39 passed succesfully')


if __name__ == '__main__':
    unittest.main()
