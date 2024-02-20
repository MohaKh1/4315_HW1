


from pprint import pprint

def setops():
    
    uppercase_to_lowercase = {chr(i): chr(i + 32) for i in range(65, 91)}
    
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