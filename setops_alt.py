

from pprint import pprint
import sys
import os

def read_args(args: sys.argv) -> dict:
    
    operations = ['union', 'difference', 'intersection']
    if len(sys.argv) < 2:
        print(f'Improper arguments supplied. Usage: python3 setops.py \"set1=[filename];set2=[filename];operation=[difference|union|intersection]\"')
        exit(1)
    
    setops_instruction_str = sys.argv[1]
    setops_instruction_list = setops_instruction_str.split(';')
    try:
        file_1_name_str = setops_instruction_list[0].split('set1=')[1]
        file_2_name_str = setops_instruction_list[1].split('set2=')[1]
        operation_name_str = setops_instruction_list[2].split('operation=')[1]
    except IndexError as err:
        print(f'Improper arguments supplied -> "{setops_instruction_str}"\nUsage: python3 setops.py \"set1=[filename];set2=[filename];operation=[difference|union|intersection]\"')
        exit(1)
        
    if operation_name_str not in operations:
        print(f'Improper arguments supplied -> "{operation_name_str}" does not match one of {operations} (case sensitive)')
        exit(1)
    
    try:
        print(f'FILENAME1: "{file_1_name_str}"\nFILENAME2: "{file_2_name_str}"\nOPERATION: "{operation_name_str}"')
    except Exception as err:
        print(f'Improper arguments supplied -> "{setops_instruction_str}"\nUsage: python3 setops.py \"set1=[filename];set2=[filename];operation=[difference|union|intersection]\"')
        exit(1)
    return (file_1_name_str, file_2_name_str, operation_name_str)

def setops():
    read_args(sys.argv)
    exit(0)

if __name__ == "__main__":
    setops()