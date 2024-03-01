const fs = require('fs');

function write_list_to_file(file_path, lst) {
    const data = lst.join('\n');

    fs.writeFile(file_path, data, err => {
        if (err) {
            console.error(`Error writing to file: ${err}`);
        } else {
            console.log(`List successfully written to ${file_path}`);
        }
    });
}


function quicksort_numbers(lst) {
    if (lst.length <= 1) {
        return lst;
    } else {
        const pivot = lst[0];
        const lesser = lst.slice(1).filter(x => parseFloat(x) <= parseFloat(pivot));
        const greater = lst.slice(1).filter(x => parseFloat(x) > parseFloat(pivot));
        return quicksort_numbers(lesser).concat([pivot], quicksort_numbers(greater));
    }
}

function quicksort_str(lst) {
    if (lst.length <= 1) {
        return lst;
    } else {
        const pivot = lst[0];
        const lesser = lst.slice(1).filter(x => String(x) <= String(pivot));
        const greater = lst.slice(1).filter(x => String(x) > String(pivot));
        return quicksort_str(lesser).concat([pivot], quicksort_str(greater));
    }
}

function custom_sort(lst) {
    if (!lst.length) {
        return [];
    }

    const pivot = lst[0];
    const integers_and_decimals = lst.slice(1).filter(x => (typeof x === 'number' || x instanceof Number) && !isNaN(x));
    const strings = lst.slice(1).filter(x => (typeof x !== 'number' && !(x instanceof Number)) || typeof x === 'boolean');
    
    return custom_sort(integers_and_decimals).concat([pivot], custom_sort(strings));
}

function basic_srch(n, array) {
    if (!array.length) {
        return false;
    }

    if (n === array[0]) {
        return true;
    }

    return basic_srch(n, array.slice(1));
}

function remove_duplicates_recursive(lst) {
    if (!lst.length) {
        return [];
    }

    const head = lst[0];
    const tail = lst.slice(1);

    if (!basic_srch(head, tail)) {
        return [head].concat(remove_duplicates_recursive(tail));
    } else {
        return remove_duplicates_recursive(tail);
    }
}


function get_decimal_substring(string, is_int, is_char, start=null, decimal=null, end=null, substring=null, index=0) {
    if (substring === null) {
        substring = string;
    }

    if (substring.length === 0) {
        if (start !== null && decimal !== null && decimal !== null) {
            let left = string.slice(0, start);
            let mid = null;
            let right = null;
            if (end === -1) {
                mid = string.slice(start);
                right = "";
            } else {
                mid = string.slice(start, end);
                right = string.slice(end);
            }
            left = get_decimal_substring(left, is_int, is_char);
            right = get_decimal_substring(right, is_int, is_char);
            left.push(mid);

            return left.concat(right);
        } else {
            return (string !== "" && string !== ".") ? [string] : [];
        }
    }

    const value = string[index];

    if (is_int(value)) {
        if (start === null) {
            start = index;
        }
        if (substring.slice(1) === "" && !end) {
            end = -1;
        }
    } else if (is_char(value)) {
        if (start !== null && decimal !== null) {
            end = index;
            let left = string.slice(0, start);
            let mid = string.slice(start, end);
            let right = string.slice(end);
            left = get_decimal_substring(left, is_int, is_char);
            right = get_decimal_substring(right, is_int, is_char);
            left.push(mid);
            return left.concat(right);
        } else if (start !== null && decimal === null) {
            start = null;
        }
    } else if (value === ".") {
        decimal = index;
        if (start === null) {
            start = index;
        }
        if (substring.slice(1) === "" && !end) {
            end = -1;
        }
    }
    return get_decimal_substring(string, is_int, is_char, start, decimal, end, substring.slice(1), index + 1);
}


function read_args(args)
{
	const operations = ["union", "difference", "intersection"];
	
	if(args.length < 2)
	{
		console.log('Improper arguments supplied. Usage: node setops.js "set1=[filename];set2=[filename];operation=[difference|union|intersection]"');
		process.exit(1);
	}

	let setops_instruction_str = args[2];
	let setops_instruction_list = setops_instruction_str.split(";");
	
	let file1_name_str, file2_name_str, operation_name_str = "";
	try
	{
		
		file_1_name_str = setops_instruction_list[0].split("set1=")[1];
		file_2_name_str = setops_instruction_list[1].split("set2=")[1];
		operation_name_str = setops_instruction_list[2].split("operation=")[1];
	}
	catch(err)
	{
		console.log('Improper arguments supplied -> "'+ setops_instruction_str + '"\nUsage:node setops.js "set1=[filename];set2=[filename];operation=[difference|union|intersection]"');
		process.exit(1);
	}
	
	if(!operations.includes(operation_name_str))
	{
		console.log('Improper arguments supplied -> "' + operation_name_str + '" does not match one of [' + operations.toString() + '] (case sensitive)');
		process.exit(1);
	}
	
	try
	{
		console.log('\nARGUMENTS SUPPLIED:\nFILENAME1: "' + file_1_name_str + '"\nFILENAME2: "' + file_2_name_str + '"\nOPERATION: "' + operation_name_str + '"');
	}
	catch(err)
	{
		console.log('Improper arguments supplied -> "' + setops_instruction_str + '"\nUsage:node setops.js "set1=[filename];set2=[filename];operation=[difference|union|intersection]"'); 
		process.exit(1);
	}

	return [file_1_name_str, file_2_name_str, operation_name_str];
	
}

function setops()
{
	// read in files based on args and determine action to take
	let [file_1_name_str, file_2_name_str, operation_name_str] = read_args(process.argv);
	
	DEBUG_MODE = process.argv[process.argv.length - 1] ==  "--debug"? true : false;

	if (!DEBUG_MODE)
	{
		process.argv.push("--debug");
		console.log("    Note:add '--debug' flag to run in debug mode. 'setops.js set1=" + file_1_name_str + ";set2=" + file_2_name_str + ";operation=" + operation_name_str + " --debug'");
	}

	// open file 1 and read its contents
	const file1_helper = require('node:fs');
	let file_1_str = "";

	try
	{
		const data = file1_helper.readFileSync(file_1_name_str);
		file_1_str = data.toString();
	}
	catch(err)
	{
		console.error("FileNotFoundError: " + err);
		process.exit(1);
	}

	file_1_size = file_1_str.length;

	if(file_1_size == 0)
	{
		console.log("FileSizeError: The file " + file_1_name_str + " is empty.");
		process.exit(1);
	}

	console.log("Loaded contents of " + file_1_name_str + " into memory successfully!");


	// open file 2 and read its contents
	const file2_helper = require('node:fs');
	let file_2_str = "";

	try
	{
		const data = file2_helper.readFileSync(file_2_name_str);
		file_2_str = data.toString();
	}
	catch(err)
	{
		console.error("FileNotFoundError: " + err);
		process.exit(1);
	}

	file_2_size = file_2_str.length;

	if(file_2_size == 0)
	{
		console.log("FileSizeError: The file " + file_2_name_str + " is empty.");
		process.exit(1);
	}

	console.log("Loaded contents of " + file_2_name_str + " into memory successfully!");
	let path = require("path");
	let stats1 = file1_helper.statSync(file_1_name_str);
	let stats2 = file2_helper.statSync(file_2_name_str);
	if(DEBUG_MODE)
	{
	
        	console.log("~" + file_1_name_str + " content\n");
        	console.log(file_1_str);

        	console.log("\n~" + file_2_name_str + " content\n");
        	console.log(file_2_str);
	}

// lambda helpers ____________________________________________________________________
	
	/*
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
    */
	const toLower = s => (
		s.length === 0 ? 
		"" : 
		(
			!/[A-Z]/.test(s[0]) ? 
			s[0] : 
			String.fromCharCode(s.charCodeAt(0) + 32)
		) + toLower(s.slice(1))
	);
    /*
        ~is_special: Checks if the given character is not alphanumeric
        ~Inputs: Any character
        ~Output: Bool True or False
		*/
	const is_special = char => !(/[A-Za-z0-9.]/.test(char));
	const is_int = char => ("0" <= char && char <= "9");
	const is_dot = char => (char === ".");
	const is_char = char => ("a" <= char && char <= "z") || ("A" <= char && char <= "Z");
	const is_str = str => str === '' ? true : (is_char(str[0]) ? is_str(str.slice(1)) : false);
	
	const get_substrings = (str, index_list) => (
		index_list.length === 1 ? 
		[] : 
		[str.slice(index_list[0] + 1, index_list[1])] 
		.concat(get_substrings(str, index_list.slice(1)))
	);
	const separate_decimals = word_bag => (
		word_bag.length === 0 ? 
		[] : 
		get_decimal_substring(word_bag[0], is_int, is_char)
		.concat(separate_decimals(word_bag.slice(1)))
	);
	
	const remove_remaining_spec = lst => (
		lst.length === 0 ? 
		[] : 
		(
			(![" ", ".", ""].includes(lst[0])) ? 
			[lst[0]] : 
			[]
		).concat(remove_remaining_spec(lst.slice(1)))
	);
	
	const check_inclusion = (string, list) => (
		list.length === 0 ? 
		false : 
		(list[0] === string ? true : check_inclusion(string, list.slice(1)))
	);
	
// // execution ________________________________________________________________
	console.log(`~processing indexes of non-alphanumeric characters from ${file_1_name_str}`);
	const special_indexes_str_1 = [-1].concat([...file_1_str].map((_, i) => i).filter(x => is_special(file_1_str[x]))).concat([file_1_str.length]);

	console.log(`~processing indexes of non-alphanumeric characters from ${file_2_name_str}`);
	const special_indexes_str_2 = [-1].concat([...file_2_str].map((_, i) => i).filter(x => is_special(file_2_str[x]))).concat([file_2_str.length]);

	console.log(`~separating into bag of substrings by non-alphanumeric characters`);
	const alphanumeric_words_bag_1 = get_substrings(file_1_str, special_indexes_str_1);
	const alphanumeric_words_bag_2 = get_substrings(file_2_str, special_indexes_str_2);

	if (DEBUG_MODE) {
		console.log("\n______________________________________________________");
		console.log(alphanumeric_words_bag_1);
		console.log("\n______________________________________________________");
		console.log(alphanumeric_words_bag_2);
		console.log();
	}

	console.log("~converting bag of substrings to lowercase");
	const lower_case_alphanumeric_words_bag_1 = alphanumeric_words_bag_1.map(word => toLower(word));
	const lower_case_alphanumeric_words_bag_2 = alphanumeric_words_bag_2.map(word => toLower(word));

	if (DEBUG_MODE) {
		console.log("\n______________________________________________________");
		console.log(lower_case_alphanumeric_words_bag_1);
		console.log("\n______________________________________________________");
		console.log(lower_case_alphanumeric_words_bag_2);
		console.log();
	}

	const lower_case_alphanumeric_words_no_decimal_bag_1 = separate_decimals(lower_case_alphanumeric_words_bag_1);
	const lower_case_alphanumeric_words_no_decimal_bag_2 = separate_decimals(lower_case_alphanumeric_words_bag_2);
	const bag_of_words_decimals_int_1 = remove_remaining_spec(lower_case_alphanumeric_words_no_decimal_bag_1);
	const bag_of_words_decimals_int_2 = remove_remaining_spec(lower_case_alphanumeric_words_no_decimal_bag_2);

	console.log("~separating into bag of words and string integers and decimals via numeric or (alpha) characters");

	if (DEBUG_MODE) {
		console.log("\n______________________________________________________");
		console.log(bag_of_words_decimals_int_1);
		console.log("\n______________________________________________________");
		console.log(bag_of_words_decimals_int_2);
		console.log();
	}

	const set_1_unsorted = remove_duplicates_recursive(bag_of_words_decimals_int_1);
	const set_2_unsorted = remove_duplicates_recursive(bag_of_words_decimals_int_2);
	console.log(`bag 1 -> set 1: removed ${bag_of_words_decimals_int_1.length - set_1_unsorted.length} duplicate word(s)`);
	console.log(`bag 1 -> set 2: removed ${bag_of_words_decimals_int_2.length - set_2_unsorted.length} duplicate word(s)`);
	if (DEBUG_MODE) {
		console.log();
		console.log(set_1_unsorted);
		console.log(set_2_unsorted);
		console.log();
	}
	// Operations
	const difference_operation = (set_1, set_2) => (
		set_1.length === 0 ? 
		[] : 
		(
			(!check_inclusion(set_1[0], set_2) ? [set_1[0]] : [])
			.concat(difference_operation(set_1.slice(1), set_2))
		)
	);

	const intersection_half_operation = (set_1, set_2) => (
		set_1.length === 0 ? 
		[] : 
		(
			(check_inclusion(set_1[0], set_2) ? [set_1[0]] : [])
			.concat(intersection_half_operation(set_1.slice(1), set_2))
		)
	);

	let result = [];
	console.log(`~performing operation "${operation_name_str}"`);
	if (operation_name_str === "difference") {
		result = difference_operation(set_1_unsorted, set_2_unsorted);
	} else if (operation_name_str === "union") {
		result = remove_duplicates_recursive(set_1_unsorted.concat(set_2_unsorted));
	} else if (operation_name_str === 'intersection') {
		const set_1_intersection = intersection_half_operation(set_1_unsorted, set_2_unsorted);
		const set_2_intersection = intersection_half_operation(set_2_unsorted, set_1_unsorted);
		result = remove_duplicates_recursive(set_1_intersection.concat(set_2_intersection));
	}

	// Post Sort
	const get_str_list = list => (
		list.length === 0 ? 
		[] : 
		(
			(is_str(list[0]) ? [list[0]] : [])
			.concat(get_str_list(list.slice(1)))
		)
	);

	const get_non_str_list = list => (
		list.length === 0 ? 
		[] : 
		(
			(!is_str(list[0]) ? [list[0]] : [])
			.concat(get_non_str_list(list.slice(1)))
		)
	);

	const strings_list = get_str_list(result);
	const decimal_and_int_list = get_non_str_list(result);
	const sorted_strings_list = quicksort_str(strings_list);
	const sorted_decimal_and_int_list = quicksort_numbers(decimal_and_int_list);
	result = sorted_decimal_and_int_list.concat(sorted_strings_list);
	console.log(`result -> ${result}`);
	write_list_to_file('result.txt', result);


}

setops();
