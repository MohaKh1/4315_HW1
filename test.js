const toLower = s => (
    s.length === 0 ? 
    "" : 
    (
        !/[A-Z]/.test(s[0]) ? 
        s[0] : 
        String.fromCharCode(s.charCodeAt(0) + 32)
    ) + toLower(s.slice(1))
);

const is_special = char => !(/[A-Za-z0-9.]/.test(char));
const is_int = char => ("0" <= char && char <= "9");
const is_dot = char => (char === ".");
const is_char = char => ("a" <= char && char <= "z") || ("A" <= char && char <= "Z");
const is_str = str => str === '' ? true : (is_char(str[0]) ? is_str(str.slice(1)) : false);



let special_char_str = '['
let str_char = 'j'
let int_char = '1'
// console.log(`${special_char_str} special -> ${is_special(special_char_str)}`)
// console.log(`${notspecial_char_str} special -> ${is_special(notspecial_char_str)}`)

console.log(`${is_int(int_char)} ${is_int(str_char)}`)
console.log(`${is_dot(int_char)} ${is_dot('.')}`)
console.log(`${is_char(str_char)} ${is_char(special_char_str)}`)
console.log(`${is_str('int_char')} ${is_char('isstring')}`)
const get_substrings = (str, index_list) => (
    index_list.length === 1 ? 
    [] : 
    [str.slice(index_list[0] + 1, index_list[1])] 
    .concat(get_substrings(str, index_list.slice(1)))
);
console.log(get_substrings('isstring', [0,3]))
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

console.log(check_inclusion('321',[]))
console.log(check_inclusion('321',['321','213']))
console.log(remove_remaining_spec(['321','213','.', ' s',' da','', 's']))




