# -*- coding: utf-8 -*-
# SSW 555 - WS
# Project 03
# wenkai xiao
# cwid 10471308

import sys, os
from typing import List, Optional, IO, Dict
from datetime import datetime
from prettytable import PrettyTable

def program_header(msg: str) -> None:

    print('\n' + msg)
    print('*' * (len(msg)) + '\n')

def quit() -> None:

    print("\n* Thanks You! *\n")
    sys.exit()

# func, read input file
def get_file(file_name: str) -> IO:

    curr_script_path = os.path.split(os.path.realpath(__file__))[0] + '/'

    while True:

        try:
            get_FileName: str = curr_script_path + file_name
            gotten_File: IO = open(get_FileName, 'r', encoding = 'gbk', errors = 'ignore')
            return gotten_File 

        except FileNotFoundError:
            print("The file does not exist or invalid file name.\n")
            sys.exit()

# core features
class File_Analyzer:

    def __init__(self, open_file_command: IO) -> Optional[List]:
     
        self.open_file_command = open_file_command

        self.label_keys: List = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']
        self.tab_keys: List = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']

        self.lines = self.get_gedcom_file_lines()
        
        self.generate_individuals_block()        
        self.generate_families_block()
        
        self.format_individuals_block()
        self.format_families_block()

        self.pretty_print()
        
    def get_gedcom_file_lines(self) -> Optional[List]:

        with self.open_file_command:

            wrap_free_lines: List = []
            line: str
            for line in self.open_file_command.readlines():
                line = line.strip('\n')
                wrap_free_lines.append(line)

        return wrap_free_lines

    def generate_individuals_block(self) -> Optional[List]:

        lines = self.lines

        individual_info_index: int
        family_info_index: int
        cur_index:int = 0
        
        for item in lines:
                cur_index += 1
                if item == '0 @I1@ INDI':
                    individual_info_index = cur_index
                elif item == '0 @F1@ FAM':
                    family_info_index = cur_index
        
        individual_info_block: List = lines[individual_info_index-1 : family_info_index-1]
        individual_info_block = individual_info_block + ['000INDI']

        each_family_individuals: List = []
        ele_cur_index: int = 0
        ele_head_index: int = 0
        individual: List = []
        for element in individual_info_block[ele_head_index : ]:
                
            ele_cur_index += 1
            if ('0' and 'INDI' in element) and (element != individual_info_block[ele_head_index]):
                individual = individual_info_block[ele_head_index : ele_cur_index-1]                    
                ele_head_index = ele_cur_index-1                
                each_family_individuals.append(individual)

        return each_family_individuals
 
    def generate_families_block(self) -> Optional[List]:

        lines = self.lines

        family_info_index: int
        cur_index:int = 0

        for item in lines:
                cur_index += 1
                if item == '0 @F1@ FAM':
                    family_info_index = cur_index

        family_info_block: List = lines[family_info_index-1 : len(lines)-1]
        family_info_block = family_info_block + ['000FAM']

        every_family_info: List = []
        uni_cur_index: int = 0
        uni_head_index: int = 0
        info: List = []
        for unit in family_info_block[uni_head_index : ]:
                
            uni_cur_index += 1
            if ('0' and 'FAM' in unit) and (unit != family_info_block[uni_head_index]):
                info = family_info_block[uni_head_index : uni_cur_index-1]                    
                uni_head_index = uni_cur_index-1                
                #print(info)
                every_family_info.append(info)

        # print(every_family_info) # <- VTest
        return every_family_info
  
    def format_individuals_block(self) -> Optional[List]:

        all_individuals: List = []
        

        _now: datetime = datetime.today()
        cur_idx: int = 0
        cur_ID: int = 0
        for individual in self.generate_individuals_block():
            formatted_row: Dict = dict.fromkeys(self.label_keys)
            
            cur_ID += 1
            if cur_ID <= 9:
                formatted_row['ID'] = 'I' + str('0'+str(cur_ID))
            elif cur_ID >= 10:
                formatted_row['ID'] = 'I' + str(cur_ID)

            for item in individual:
                cur_idx += 1

                if 'NAME' in item:
                    formatted_row['Name'] = item[7:]

                if 'SEX' in item:
                    formatted_row['Gender'] = item[6:]

                if 'BIRT' not in individual[6]:
                    formatted_row['Birthday'] = 'Unknown'
                elif 'BIRT' in individual[6]:
                    if len(individual[7][7:]) == 4:
                        formatted_row['Birthday'] = str(individual[7][7:])
                    elif len(individual[7][7:]) > 4:
                        b_date: datetime = datetime.strptime(individual[7][7:], '%d %b %Y')
                        formatted_row['Birthday'] = str(b_date.date())
                
                if ('DEAT' in individual[6]) and ('DATE' not in individual[7]):
                    formatted_row['Death'] = 'Unknown'
                    formatted_row['Alive'] = 'False'
                elif ('DEAT' in individual[8]) and ('DATE' in individual[9]):
                    d_date: datetime = datetime.strptime(individual[9][7:], '%d %b %Y')
                    formatted_row['Death'] = str(d_date.date())
                    formatted_row['Alive'] = 'False'
                elif 'DEAT' not in individual[8]:
                    formatted_row['Death'] = 'NA'
                    formatted_row['Alive'] = 'True'
                
                if ('DEAT' in individual[6]) and ('DATE' not in individual[7]):
                    formatted_row['Age'] = 'Unknown'
                elif ('DEAT' in individual[8]) and ('DATE' in individual[9]):
                    d_date: datetime = datetime.strptime(individual[9][7:], '%d %b %Y')
                    formatted_row['Age'] = str(d_date.year - b_date.year)
                elif 'DEAT' not in individual[8]:
                    if len(individual[7][7:]) == 4:
                        formatted_row['Age'] = str(int(_now.year) - int(individual[7][7:]))
                    elif len(individual[7][7:]) > 4:
                        b_date: datetime = datetime.strptime(individual[7][7:], '%d %b %Y')
                        formatted_row['Age'] = str(_now.year - b_date.year)

                if 'FAMC' not in individual[len(individual)-1]:
                    formatted_row['Child'] = 'NA'
                elif 'FAMC' in individual[len(individual)-1]:
                    famc_string: str = ''.join([char for char in individual[len(individual)-1]])
                    formatted_row['Child'] = str("{'" + famc_string[7:].strip('@') + "'}")

                if 'FAMC' in individual[len(individual)-2]:
                    famc_string: str = ''.join([char for char in individual[len(individual)-2]])
                    formatted_row['Child'] = str("{'" + famc_string[7:].strip('@') + "'}")

                if 'FAMS' in individual[len(individual)-5]:
                    fams_string: str = ''.join([char for char in individual[len(individual)-5]])
                    formatted_row['Spouse'] = str("{'" + fams_string[7:].strip('@') + "'}")

                elif 'FAMS' not in individual[len(individual)-2]:
                    formatted_row['Spouse'] = 'NA'
                elif 'FAMS' in individual[len(individual)-2]:
                    fams_string: str = ''.join([char for char in individual[len(individual)-2]])
                    formatted_row['Spouse'] = str("{'" + fams_string[7:].strip('@') + "'}")

                if 'FAMS' in individual[len(individual)-1]:
                    lfams_string: str = ''.join([char for char in individual[len(individual)-1]])
                    formatted_row['Spouse'] = str("{'" + lfams_string[7:].strip('@') + "'}")

            all_individuals.append(formatted_row)

        # print(all_individuals, '\n') # <- Visualization Test
        return all_individuals  

    def format_families_block(self) -> Optional[List]:

        all_families: List = []

        _now: datetime = datetime.today()
        cur_ID: int = 0
        for family in self.generate_families_block():
            patterned_row: Dict = dict.fromkeys(self.tab_keys)
            
            cur_ID += 1
            if cur_ID <= 9:
                patterned_row['ID'] = 'F' + str('0'+str(cur_ID))
            elif cur_ID >= 10:
                patterned_row['ID'] = 'F' + str(cur_ID)

            kids_set: List = []
            cur_idx: int = 0
            for record in family:
                cur_idx += 1

                if 'DIV' not in record:
                    patterned_row['Divorced'] = 'NA'

                if '1 MARR' not in family[:len(family)-1]:
                    patterned_row['Married'] = 'Unknown'
                elif ('2 DATE' in record) and record[len(record)-5 : len(record)-1]:
                    m_date: datetime = datetime.strptime(record[7:], '%d %b %Y')
                    patterned_row['Married'] = str(m_date.date())

                if 'HUSB' in record:
                    hID:str
                    patterned_row['Husband ID'] = record[7:].strip('@')
                    hID = patterned_row['Husband ID']
                    for indvd in self.generate_individuals_block():
                        if '@'+hID+'@' in indvd[0]:
                            patterned_row['Husband Name'] = indvd[1][7:]

                if 'WIFE' in record:
                    wID: str
                    patterned_row['Wife ID'] = record[7:].strip('@')
                    wID = patterned_row['Wife ID']
                    for indvd in self.generate_individuals_block():
                        if '@'+wID+'@' in indvd[0]:
                            patterned_row['Wife Name'] = indvd[1][7:]

                if '1 CHIL' in record:                    
                    kID: str = record[7:].strip('@')
                    kids_set.append(kID)
                    kids: set = {char for char in kids_set}
                    patterned_row['Children'] = kids
            
            all_families.append(patterned_row)

        # print(all_families, '\n') # <- Visualization Test
        return all_families

    #  print output by prettytable 
    def pretty_print(self) -> None:
        """ Print out the formatted presentation of the given analyzed summary info from the file. """
                  
        individuals_table: PrettyTable = PrettyTable(self.label_keys)
        i: Dict
        for i in self.format_individuals_block():
            individuals_table.add_row([v for k, v in i.items()])

        families_table: PrettyTable = PrettyTable(self.tab_keys)
        f: Dict
        for f in self.format_families_block():
            families_table.add_row([v for k, v in f.items()])
        
        print('Individuals:')
        print(individuals_table)
        
        print('Families:')
        print(families_table)
        

    # ((/))

def main():
    
    program_header('Individuals and Families')
    File_Analyzer( get_file('WXF.ged') )
    quit()

if __name__ == '__main__':
    main()

main()
