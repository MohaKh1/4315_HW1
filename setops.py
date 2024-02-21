from pprint import pprint
import sys
import os
from functools import reduce
from datetime import datetime


def basic_srch(n, array, index=0):
    if len(array) == 0:
        return False

    if n == array[0]:
        return True

    return basic_srch(n, array[1:], index + 1)


def read_args(args: sys.argv) -> dict:
    operations = ["union", "difference", "intersection"]
    if len(sys.argv) < 2:
        print(
            f'Improper arguments supplied. Usage: python3 setops.py "set1=[filename];set2=[filename];operation=[difference|union|intersection]"'
        )
        exit(1)

    setops_instruction_str = sys.argv[1]
    setops_instruction_list = setops_instruction_str.split(";")
    try:
        file_1_name_str = setops_instruction_list[0].split("set1=")[1]
        file_2_name_str = setops_instruction_list[1].split("set2=")[1]
        operation_name_str = setops_instruction_list[2].split("operation=")[1]
    except IndexError as err:
        print(
            f'Improper arguments supplied -> "{setops_instruction_str}"\nUsage: python3 setops.py "set1=[filename];set2=[filename];operation=[difference|union|intersection]"'
        )
        exit(1)

    if operation_name_str not in operations:
        print(
            f'Improper arguments supplied -> "{operation_name_str}" does not match one of {operations} (case sensitive)'
        )
        exit(1)

    try:
        print(
            f'\nARGUMENTS SUPPLIED:\nFILENAME1: "{file_1_name_str}"\nFILENAME2: "{file_2_name_str}"\nOPERATION: "{operation_name_str}"'
        )
    except Exception as err:
        print(
            f'Improper arguments supplied -> "{setops_instruction_str}"\nUsage: python3 setops.py "set1=[filename];set2=[filename];operation=[difference|union|intersection]"'
        )
        exit(1)
    return (file_1_name_str, file_2_name_str, operation_name_str)


def setops():
    
# SETUP ________________________________________________________________

    # # read in files based on args and determine action to take
    file_1_name_str, file_2_name_str, operation_name_str = read_args(sys.argv)

    DEBUG_MODE = True if sys.argv[-1] == "--debug" else False

    # # Open the file 1 and read its content.
    try:
        file1_ = open(file_1_name_str, "r").read()
    except FileNotFoundError as err:
        print(f"FileNotFoundError: {err}") and exit(1)
    file_1_size = os.path.getsize(file_1_name_str)
    if os.path.getsize(file_1_name_str) == 0:
        print(f"FileSizeError: The file {file_1_name_str} is empty.") and exit(1)

    print(f"\n~Loaded contents of {file_1_name_str} into memory successfully!")

    # Open the file 2 and read its content.
    try:
        file2_ = open(file_2_name_str, "r").read()
    except FileNotFoundError as err:
        print(f"FileNotFoundError: {err}") and exit(1)

    file_2_size = os.path.getsize(file_2_name_str)
    if file_2_size == 0:
        print(f"FileSizeError: The file {file_2_name_str} is empty.") and exit(1)

    print(f"~Loaded contents of {file_2_name_str} into memory successfully!\n")
    file_1_str = str(file1_)
    file_2_str = str(file2_)

    if DEBUG_MODE:
        print(
            f"{file_1_name_str} content overview:\nFile path: {os.path.abspath(file_1_name_str)}\nFile Size: {file_1_size} bytes\nLast Modified: {datetime.fromtimestamp(os.path.getmtime(file_1_name_str))}\n"
        )
        print(
            f"{file_2_name_str} content overview:\nFile path: {os.path.abspath(file_2_name_str)}\nFile Size: {file_2_size} bytes\nLast Modified: {datetime.fromtimestamp(os.path.getmtime(file_2_name_str))}"
        )

        print(f"~{file_1_name_str} content\n")
        print(20 * "_")
        print(file_1_str)
        print(20 * "_")

        print(f"\n~{file_2_name_str} content\n")
        print(20 * "_")
        print(file_2_str)
        print(20 * "_")
        
# lambda helpers ________________________________________________________________

    """
        ~toLower: takes any valid string and returns the lowercase version of it. The convesrion will only affect
        uppercase alphabetic characters.
        ~Inputs: Any valid string
        ~Output: String with uppercase alphabetic characters converted to lowercase
        
        ~Example: "An21=-=;2"   becomes   "an21=-=;2"
        ______________________________________________
        Features: 
            - differentiate uppercase alphabetic character from other characters via 
            inclusion search against uppercase alphabetic character list.
            -  upper case to lower case conversion
            -  recursive iteration
    """
    toLower = lambda s: (
        ""
        if len(s) == 0
        else (
            (
                s[0]
                if not basic_srch(s[0], list(map(chr, range(65, 91))))
                else chr(ord(s[0]) + 32)
            )
            + toLower(s[1:])
        )
    )
    """
        ~is_special: Checks if the given character is not alphanumeric
        ~Inputs: Any character
        ~Output: Bool True or False
    """
    is_special = lambda char: not (
        "A" <= char <= "Z" or "a" <= char <= "z" or "0" <= char <= "9"
    )

    get_substrings = (
        lambda str, index_list: []
        if len(index_list) == 1
        else (
            [str[index_list[0] + 1 : index_list[1]]]
            + get_substrings(str, index_list[1:])
        )
    )
# execution ________________________________________________________________


    print(f"~processing indexes of non-alphanumeric characters from {file_1_name_str}")
    special_indexes_str_1 = (
        [-1]
        + list(filter(lambda x: is_special(file_1_str[x]), range(len(file_1_str))))
        + [len(file_1_str)]
    )
    print(f"~processing indexes of non-alphanumeric characters from {file_2_name_str}")

    special_indexes_str_2 = (
        [-1]
        + list(filter(lambda x: is_special(file_2_str[x]), range(len(file_2_str))))
        + [len(file_2_str)]
    )
    print(f"~separating into bag of substrings by non-alphanumeric characters")

    alphanumeric_words_bag_1 = get_substrings(file_1_str, special_indexes_str_1)
    alphanumeric_words_bag_2 = get_substrings(file_2_str, special_indexes_str_2)

    if DEBUG_MODE:
        print("\n______________________________________________________")
        print(alphanumeric_words_bag_1)
        print("\n______________________________________________________")
        print(alphanumeric_words_bag_2)
        print()

    print("~converting bag of substrings to lowercase")
    lower_case_alphanumeric_words_bag_1 = list(
        map(
            lambda word_index: toLower(alphanumeric_words_bag_1[word_index]),
            range(len(alphanumeric_words_bag_1)),
        )
    )
    lower_case_alphanumeric_words_bag_2 = list(
        map(
            lambda word_index: toLower(alphanumeric_words_bag_2[word_index]),
            range(len(alphanumeric_words_bag_2)),
        )
    )

    if DEBUG_MODE:
        print("\n______________________________________________________")
        print(lower_case_alphanumeric_words_bag_1)
        print("\n______________________________________________________")
        print(lower_case_alphanumeric_words_bag_2)
        print()

    print(
        "~separating into bag of words and string numbers via numeric or (alpha) characters IMPLEMENT ME!"
    )

    print("~creating set of distinct words by removing duplicate words IMPLEMENT ME!")


if __name__ == "__main__":
    setops()
