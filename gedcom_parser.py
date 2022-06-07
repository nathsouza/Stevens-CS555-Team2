# def gedcom_parser(file_name):
#     file = open(file_name, 'r')
#     valid_tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
#     while (True):
#         file_line = file.readline()
#         if (file_line==""):
#             break
#         print("--> " + file_line, end="")
#         file_line_copy = file_line.split()
#         for tag in valid_tags:
#             if (tag in file_line_copy):
#                 y_n = "Y"
#                 print("<--", end="")
#                 if (tag=="INDI" or tag=="FAM"):
#                     print(file_line_copy[0] + "|" + tag + "|" + y_n + "|" + file_line_copy[1])
#                 else:
#                     count=1
#                     for i in file_line_copy:
#                         if (count==1):
#                             print(i, end="")
#                         elif (not count==2):
#                             if (not i==file_line_copy[-1]):
#                                 print(i + " ", end="")
#                             else:
#                                 print(i)
#                                 break
#                         else:
#                             if (len(file_line_copy) <= 2):
#                                 print("|" + tag+ "|" + y_n)
#                             else: 
#                                 print("|" + tag+ "|" + y_n + "|", end="")
#                         count+=1
#                 break
#             else:
#                 if (tag==valid_tags[-1]):
#                     y_n = "N"
#                     print("<--", end="")
#                     if (len(file_line_copy) <= 2):
#                         print(file_line_copy[0] + "|" + file_line_copy[1] + "|" + "N")
#                     else: 
#                         count=1
#                         for i in file_line_copy:
#                             if (count==1):
#                                 print(i, end="")
#                             elif (not count==2):
#                                 if (not i==file_line_copy[-1]):
#                                     print(i + " ", end="")
#                                 else:
#                                     print(i)
#                             else:
#                                 print("|" + file_line_copy[1]+ "|" + y_n + "|", end="")
#                             count+=1
#                     break
#     file.close()

from prettytable import PrettyTable
p_table = PrettyTable()
f_table = PrettyTable()


def gedcom_table(file_name):
    file = open(file_name, 'r')
    valid_tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
    id_list = []
    name_list = []
    gender_list = []
    birth_list = []
    age_list = []
    alive_list = []
    death_list = []
    child_list = []
    spouse_list = []
    fam_list = []
    husb_list = []
    wife_list = []
    chil_list = []
    marr_list = []
    birt_or_deat = "BIRT"
    starter = False
    checker = True
    while (True):
        file_line = file.readline()
        if (file_line==""):
            break
        file_line_copy = file_line.split()
        for tag in valid_tags:
            if (tag in file_line_copy):
                if (tag=="INDI"):
                    id_list.append(file_line_copy[1])
                    child_list.append("N/A")
                    spouse_list.append("N/A")
                    starter = True
                elif (tag=="FAM"):
                    if (checker==False):
                        chil_list.append("N/A")
                    checker = True
                    fam_list.append(file_line_copy[1])
                else:
                    if (starter):
                        arg = ' '.join(file_line_copy[2:])
                        if (arg==""):
                            arg = "N/A"
                        if (tag=="NAME"):
                            name_list.append(arg)
                        elif (tag=="SEX"):
                            gender_list.append(arg)
                        elif (tag=="BIRT"):
                            birt_or_deat = "BIRT"
                        elif (tag=="DEAT"):
                            birt_or_deat = "DEAT"
                            if (arg=="Y"):
                                arg="False"
                            else:
                                arg="True"
                            alive_list.append(arg)

                        elif (tag=="MARR"):
                            birt_or_deat = "MARR"
                        elif (tag=="DATE"):
                            if (birt_or_deat=="BIRT"):
                                birth_list.append(arg)
                            elif (birt_or_deat=="DEAT"):
                                death_list.append(arg)
                            else:
                                marr_list.append(arg)
                        elif (tag=="HUSB"):
                            checker = False
                            husb_list.append(arg)
                        elif (tag=="WIFE"):
                            wife_list.append(arg)
                        elif (tag=="CHIL"):
                            checker = True
                            chil_list.append(arg)

                            

    p_table.add_column("ID", id_list)
    p_table.add_column("Name", name_list)
    p_table.add_column("Gender", gender_list)
    p_table.add_column("Birthday", birth_list)
    p_table.add_column("Alive", alive_list)
    # p_table.add_column("Child", child_list)
    # p_table.add_column("Spouse", spouse_list)
    # p_table.add_column("Death", death_list)
    f_table.add_column("ID", fam_list)
    f_table.add_column("Married", marr_list)
    f_table.add_column("Husband ID", husb_list)
    f_table.add_column("Wife ID", wife_list)
    f_table.add_column("Children", chil_list)
    print(p_table)
    print(f_table)
    file.close()
         
gedcom_table("gedcom_test.ged")