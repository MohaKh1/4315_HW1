function basic_srch(n, array, index=0)
{
	if(array.length == 0)
	{
		return false;
	}
	
	if(n == array[0])
	{
		return true;
	}
	
	return basic_srch(n, array.slice(1,), index + 1);
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
        	console.log(file_1_name_str + " content overview:\nFile path: " + path.resolve(file_1_name_str) + "\nFile Size: " + stats1.size + " bytes\nLast Modified: " + stats1.mtime + "\n");
	
        	console.log(file_2_name_str + " content overview:\nFile path: " + path.resolve(file_2_name_str) + "\nFile Size: " + stats2.size + " bytes\nLast Modified: " + stats2.mtime + "\n");
        	console.log("~" + file_1_name_str + " content\n");
        	console.log(20 * "_");
        	console.log(file_1_str);
        	console.log(20 * "_");

        	console.log("\n~" + file_2_name_str + " content\n");
        	console.log(20 * "_");
        	console.log(file_2_str);
        	console.log(20 * "_");
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
    let toLower = s =>
	{
        if(!s.length == 0)
		{
           	!(basic_srch(s[0], ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'])? s[0] : [String.fromCharCode(String.charCodeAt(s[0]) + 32)].concat(toLower(s.slice(1,)));
		}
	}
    /*
        ~is_special: Checks if the given character is not alphanumeric
        ~Inputs: Any character
        ~Output: Bool True or False
		*/
		let is_special = char => !("A" <= char <= "Z" || "a" <= char <= "z" || "0" <= char <= "9" || char == '.');

    let get_substrings = (str, index_list) => !(len(index_list) == 1) ? [] : [str.slice(index_list[0] + 1, index_list[1])].concat(get_substrings(str, index_list.slice(1,)));
// execution ________________________________________________________________


    console.log("~processing indexes of non-alphanumeric characters from " + file_1_name_str);

    let special_indexes_str_1 = (
        [-1]
        + list(filter(x => is_special(file_1_str[x]), range(len(file_1_str))))
        + [len(file_1_str)]
    )
    
	console.log("~processing indexes of non-alphanumeric characters from {file_2_name_str}")

    special_indexes_str_2 = (
        [-1]
        + list(filter(x => is_special(file_2_str[x]), range(len(file_2_str))))
        + [len(file_2_str)]
    )
    console.log("~separating into bag of substrings by non-alphanumeric characters")

    alphanumeric_words_bag_1 = get_substrings(file_1_str, special_indexes_str_1)
    alphanumeric_words_bag_2 = get_substrings(file_2_str, special_indexes_str_2)

    if(DEBUG_MODE)
	{
        console.log("\n______________________________________________________")
        console.log(alphanumeric_words_bag_1)
        console.log("\n______________________________________________________")
        console.log(alphanumeric_words_bag_2)
        console.log()
	}

    console.log("~converting bag of substrings to lowercase")
    lower_case_alphanumeric_words_bag_1 = list(
        map(
            word_index => toLower(alphanumeric_words_bag_1[word_index]),
            range(len(alphanumeric_words_bag_1)),
        )
    )
    lower_case_alphanumeric_words_bag_2 = list(
        map(
            word_index => toLower(alphanumeric_words_bag_2[word_index]),
            range(len(alphanumeric_words_bag_2)),
        )
    )

    if(DEBUG_MODE)
	{
        console.log("\n______________________________________________________")
        console.log(lower_case_alphanumeric_words_bag_1)
        console.log("\n______________________________________________________")
        console.log(lower_case_alphanumeric_words_bag_2)
        console.log()
	}

    console.log("~separating into bag of words and string integers and decimals via numeric or (alpha) characters IMPLEMENT ME!")

    console.log("~creating set of distinct words by removing duplicate words IMPLEMENT ME!")
}

setops();
