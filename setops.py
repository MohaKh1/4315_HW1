
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
    file_1_name_str, file_2_name_str, operation_name_str = read_args(sys.argv)
    print(file_1_name_str, file_2_name_str, operation_name_str)
    # read in args + handle input errors errors  
    
    # errors while reading in ARGS
    # 1. not correct format -> 'set1=[filename];set2=[filename];operation=[difference|union|intersection]'
    
    
    # read in files based on args and determine action to take

    # Open the file and read its content.
    
    try:
        file1_ = open(file_1_name_str, "r").read()
    except FileNotFoundError as err:
        raise err

    if os.path.getsize(file_1_name_str) == 0:
        raise EOFError("The file is empty")
            
        

    # Open the file and read its content.
    try:
        file2_ = open(file_2_name_str, "r").read()
    except FileNotFoundError as err:
        raise err
    
    if os.path.getsize(file_2_name_str) == 0:
        raise EOFError("The file is empty")
    
    for i in range(len(file1_)):
        if file1_[i] == '\n':
            print('newline!',end="")
        print(f'_{file1_[i]}_')
    print('hooray')
    exit(1)
    # 1. File not found
    # 2. operation is not of list (difference|union|intersection) -> InvalidArgument Error
    # 3. (BONUS) inappropriate file type (not extension '.txt') -> InvalidArgument Error
    # 4. (BONUS) file contents are not ok (binary)
    
    action = 'union' ## CHANGE ME
    
    str_1 = "" ## CHANGE ME
    str_2 = "" ## CHANGE ME
    
    # variables
    uppercase_to_lowercase = {chr(i): chr(i + 32) for i in range(65, 91)}
    
    # lambda helpers
    toLower = lambda s, mapping: '' if len(s) == 0 else (mapping.get(s[0], s[0]) + toLower(s[1:],mapping))
    
    
    
    test_positive_str_1 = 'JOHNATHON'
    test_positive_str_2 = 'EMiLy'
    test_neg_str_1 = 'AnDer1sOn'
    test_neg_str_2 = 'poOP0'
    print(toLower(test_positive_str_1,uppercase_to_lowercase))
    print(toLower(test_positive_str_2,uppercase_to_lowercase))
    print(toLower(test_neg_str_1,uppercase_to_lowercase))
    print(toLower(test_neg_str_2,uppercase_to_lowercase))
    
    
    
    

if __name__ == "__main__":
    setops()
