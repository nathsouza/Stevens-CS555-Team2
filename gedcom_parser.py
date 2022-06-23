class Individual:
    def __init__(self, id, name, gender, birth, alive, death):
        self.id = id
        self.name = name
        self.gender = gender
        self.birth = birth
        self.alive = alive
        self.death = death

class Family:
    def __init__(self, id, married, husband, wife, children, divorced):
        self.chil_list = []
        self.id = id
        self.married = married
        self.husband = husband
        self.wife = wife
        self.children = children
        self.divorced = divorced


from prettytable import PrettyTable
p_table = PrettyTable()
f_table = PrettyTable()


def gedcom_table(file_name):
    file = open(file_name, 'r')
    valid_tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE", "N/A"]
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
    div_list = []
    birt_or_deat = "BIRT"
    marr_or_div = "DIV"
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
                        elif (tag=="DIV"):
                            marr_or_div = "DIV"
                        elif (tag=="DATE"):
                            if (birt_or_deat=="BIRT"):
                                birth_list.append(arg)
                            elif (birt_or_deat=="DEAT"):
                                death_list.append(arg)
                            else:
                                div_list.append(arg)
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
    p_table.add_column("Child", child_list)
    p_table.add_column("Spouse", spouse_list)
    p_table.add_column("Death", death_list)
    f_table.add_column("ID", fam_list)
    f_table.add_column("Married", marr_list)
    f_table.add_column("Divorced",div_list)
    f_table.add_column("Husband ID", husb_list)
    f_table.add_column("Wife ID", wife_list)
    f_table.add_column("Children", chil_list)
    # print(p_table)
    # print(f_table)
    file.close()
    ans = []
    fam_ans = []
    for i in range(len(id_list)):
        ans.append(Individual(id_list[i], name_list[i], gender_list[i], birth_list[i], alive_list[i], death_list[i]))
    
    for i in range(len(fam_list)):
        fam_ans.append(Family(fam_list[i], marr_list[i], husb_list[i], wife_list[i], chil_list[i], div_list[i]))
    
    # for i in range(len(fam_list)):
    #     print(fam_ans[i].married)

    return [ans, fam_ans]
    
gedcom_table("gedcom_test.ged")
