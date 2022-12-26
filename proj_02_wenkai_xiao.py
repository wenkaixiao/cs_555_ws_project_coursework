# -*- coding: utf-8 -*-
# SSW 555 - WS
# Project 02
# wenkai xiao
# cwid 10471308

import sys, os
from typing import List, Optional, IO, Tuple

def program_header(msg: str) -> None:

    print('\n' + msg)
    print('*' * (len(msg)) + '\n')

def quit() -> None:

    print("\n* Thanks You! *\n")
    sys.exit()

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

def read_and_print_gedcom_file(theFile: IO) -> Optional[List]:

    supported_Tags_Set: Tuple = ('INDI', 'NAME', 'SEX', 'BIRT', 'DEAT',
                                 'FAMC', 'FAMS', 'FAM',
                                 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV',
                                 'DATE', 'HEAD', 'TRLR', 'NOTE') #! <- The GEDCOM format supported tags set.

    __Valid_Tag_Stamp: str = 'Y'
    __Invalid_Tag_Stamp: str = 'N'
    
    with theFile:

        line: str
        for line in theFile.readlines():
            print(f"--> {line}", end='')

            line = line.strip('\n') 
            splitted_Line: List = [ tag for tag in line.split(' ') ]
            validated_Line: List = []

            for tag in splitted_Line:
                validated_Line.append(tag)
            if splitted_Line[1] in supported_Tags_Set:
                validated_Line.insert(2, __Valid_Tag_Stamp)
            elif splitted_Line[1] not in supported_Tags_Set:
                validated_Line.insert(2, __Invalid_Tag_Stamp)

            print(f"<-- {'|'.join(validated_Line)}", end='')
            print('\n', end="")

def main():

    program_header('Read GEDCOM File')
    read_and_print_gedcom_file(get_file('WXF.ged'))
    quit()

if __name__ == '__main__':
    main()
