import sys
import os
from datetime import datetime
from pprint import pprint,pformat


def write_list_to_file(file_path, lst):
    with open(file_path, 'w') as file:
        for item in lst:
            if lst[-1] == item:
                file.write(item)
            else:
                file.write(item + '\n')
            
            
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



def quicksort_numbers(lst):
    if len(lst) <= 1:
        return lst
    else:
        pivot = lst[0]
        lesser = list(filter(lambda x: float(x) <= float(pivot), lst[1:]))
        greater = list(filter(lambda x: float(x) > float(pivot), lst[1:]))
        return quicksort_numbers(lesser) + [pivot] + quicksort_numbers(greater)

def quicksort_str(lst):
    if len(lst) <= 1:
        return lst
    else:
        pivot = lst[0]
        lesser = list(filter(lambda x: str(x) <= str(pivot), lst[1:]))
        greater = list(filter(lambda x: str(x) > str(pivot), lst[1:]))
        return quicksort_str(lesser) + [pivot] + quicksort_str(greater)

def custom_sort(lst):
    if not lst:
        return []
    
    pivot = lst[0]
    integers_and_decimals = [x for x in lst[1:] if isinstance(x, (int, float)) and not isinstance(x, bool)]
    strings = [x for x in lst[1:] if not isinstance(x, (int, float)) or isinstance(x, bool)]
    
    return custom_sort(integers_and_decimals) + [pivot] + custom_sort(strings)


def basic_srch(n, array, index=0):
    if len(array) == 0:
        return False

    if n == array[0]:
        return True

    return basic_srch(n, array[1:], index + 1)

def remove_duplicates_recursive(lst):
    if not lst:
        return []
    if not basic_srch(lst[0],lst[1:]):
        return [lst[0]] + remove_duplicates_recursive(lst[1:])
    else:
        return remove_duplicates_recursive(lst[1:])
    


def get_decimal_substring(
    string, is_int, is_char, start=None, decimal=None, end=None, substring=None, index=0
):
    if substring == None:  # init sub
        substring = string

    if len(substring) == 0:
        if start != None and decimal != None and decimal != None:
            # print('found SUBSTRING decimal')
            left = string[:start]
            mid = None
            right = None
            if end == -1:
                mid = string[start:]
                right = ""

            else:
                mid = string[start:end]
                right = string[end:]
            left = get_decimal_substring(left, is_int, is_char)
            right = get_decimal_substring(right, is_int, is_char)
            left.append(mid)

            return left + right
        else:
            return [string] if not string in ["", "."] else []

    value = string[index]

    if is_int(value):
        if start == None:
            start = index
        if substring[1:] == "" and not end:
            end = -1
    elif is_char(value):
        if (
            start != None and decimal != None
        ):  # first non numeric character after . found # DECIMAl
            end = index
            left = string[:start]
            mid = string[start:end]
            right = string[end:]
            left = get_decimal_substring(left, is_int, is_char)
            right = get_decimal_substring(right, is_int, is_char)
            left.append(mid)
            return left + right
        elif (
            start != None and decimal == None
        ):  # first non numeric char before . found: NOT DECIMAL
            start = None
    elif value == ".":
        decimal = index
        if start == None:
            start = index

        if substring[1:] == "" and not end:
            end = -1
    return get_decimal_substring(
        string, is_int, is_char, start, decimal, end, substring[1:], index + 1
    )


def setops():
    # SETUP ________________________________________________________________

    # # read in files based on args and determine action to take
    file_1_name_str, file_2_name_str, operation_name_str = read_args(sys.argv)

    DEBUG_MODE = True if sys.argv[-1] == "--debug" else False
    if not DEBUG_MODE:
        sys.argv.append("--debug")
        print(
            f"    NOTE:add '--debug' flag to run in debug mode. '{' '.join(sys.argv)}'"
        )
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
        "A" <= char <= "Z" or "a" <= char <= "z" or "0" <= char <= "9" or char == "."
    )
    is_int = lambda char: ("0" <= char <= "9")
    is_dot = lambda char: (char == ".")
    is_char = lambda char: ("a" <= char <= "z" or "A" <= char <= "Z")
    is_str = lambda str: True if str == '' else (is_str(str[1:]) if is_char(str[0]) else False)
    get_substrings = (
        lambda str, index_list: []
        if len(index_list) == 1
        else (
            [str[index_list[0] + 1 : index_list[1]]]
            + get_substrings(str, index_list[1:])
        )
    )

    separate_decimals = (
        lambda word_bag: []
        if len(word_bag) == 0
        else (
            get_decimal_substring(word_bag[0], is_int, is_char)
            + separate_decimals(word_bag[1:])
        )
    )
    remove_remaining_spec = lambda lst: (
        []
        if len(lst) == 0
        else (
            ([lst[0]] if not (lst[0] == " " or lst[0] == "." or lst[0] == "") else [])
            + remove_remaining_spec(lst[1:])
        )
    )

    check_inclusion = lambda string, list: (
        False
        if len(list) == 0
        else (True if list[0] == string else (check_inclusion(string, list[1:])))
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

    lower_case_alphanumeric_words_no_decimal_bag_1 = separate_decimals(
        lower_case_alphanumeric_words_bag_1
    )
    lower_case_alphanumeric_words_no_decimal_bag_2 = separate_decimals(
        lower_case_alphanumeric_words_bag_2
    )
    bag_of_words_decimals_int_1 = remove_remaining_spec(
        lower_case_alphanumeric_words_no_decimal_bag_1
    )
    bag_of_words_decimals_int_2 = remove_remaining_spec(
        lower_case_alphanumeric_words_no_decimal_bag_2
    )

    print(
        "~separating into bag of words and string integers and decimals via numeric or (alpha) characters "
    )

    if DEBUG_MODE:
        print("\n______________________________________________________")
        print(bag_of_words_decimals_int_1)
        print("\n______________________________________________________")
        print(bag_of_words_decimals_int_2)
        print()

    set_1_unsorted = remove_duplicates_recursive(bag_of_words_decimals_int_1)
    set_2_unsorted = remove_duplicates_recursive(bag_of_words_decimals_int_2)
    print(
        f"bag 1 -> set 1: removed {len(bag_of_words_decimals_int_1) - len(set_1_unsorted)} duplicate word(s)"
    )
    print(
        f"bag 1 -> set 2: removed {len(bag_of_words_decimals_int_2) - len(set_2_unsorted)} duplicate word(s)"
    )
    if DEBUG_MODE:
        print()
        print(set_1_unsorted)
        print(set_2_unsorted)
        print()

    # ~~OPERATIONS

    #   DIFFERENCE
    difference_operation = lambda set_1, set_2: (
        []
        if len(set_1) == 0
        else (
            ([set_1[0]] if not check_inclusion(set_1[0], set_2) else [])
            + difference_operation(set_1[1:], set_2)
        )
    )
    intersection_half_operation = lambda set_1, set_2: (
        []
        if len(set_1) == 0
        else (
            ([set_1[0]] if check_inclusion(set_1[0], set_2) else [])
            + intersection_half_operation(set_1[1:], set_2)
        )
    )
    #   Union
    # No code needed. The Union of two lists is just the 2 lists combined remove duplicates
    #   Intersection

    
    result = []
    print(f'~performing operation "{operation_name_str}"')
    if operation_name_str == "difference":
        result = difference_operation(set_1_unsorted,set_2_unsorted)
    elif operation_name_str == "union":
        result = remove_duplicates_recursive(set_1_unsorted+set_2_unsorted)
    elif operation_name_str == 'intersection':
        set_1_intersection = intersection_half_operation(set_1_unsorted,set_2_unsorted)
        set_2_intersection = intersection_half_operation(set_2_unsorted,set_1_unsorted)
        result = set_1_intersection + set_2_intersection
        result = remove_duplicates_recursive(result)
        
        

    
        
    
    # POST SORT
    get_str_list = lambda list: [] if len(list) == 0 else (
        ([list[0]] if is_str(list[0]) else []) + get_str_list(list[1:])
    )
    get_non_str_list = lambda list: [] if len(list) == 0 else (
        ([list[0]] if not is_str(list[0]) else []) + get_non_str_list(list[1:])
    )
    
    strings_list = get_str_list(result)
    decimal_and_int_list = get_non_str_list(result)
    sorted_strings_list = quicksort_str(strings_list)
    sorted_decimal_and_int_list = quicksort_str(decimal_and_int_list)    
    result = sorted_decimal_and_int_list + sorted_strings_list
    print(f'result -> {pformat(result)}')
    
    write_list_to_file('result.txt', result)
        
    

if __name__ == "__main__":
    orig_stdout = sys.stdout
    f = open('log.txt', 'w')
    sys.stdout = f
    setops()
    sys.stdout = orig_stdout
    f.close()  
