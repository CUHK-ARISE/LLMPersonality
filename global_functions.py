import json

# Convert number to specified label
def convert_number(label, number):
    if label.startswith('n'):
        return number
    elif label.startswith('a'):
        lower_case = True if label.endswith('l') else False
        return num_to_alphabet(number, lower_case)
    elif label.startswith('r'):
        lower_case = True if label.endswith('l') else False
        return num_to_roman(number, lower_case)
    else:
        raise ValueError("Label wrong")

# Convert label back to number
def convert_symbol(label, symbol):
    if label.startswith('n'):
        return int(symbol)
    elif label.startswith('a'):
        lower_case = True if label.endswith('l') else False
        return int(alphabet_to_num(symbol))
    elif label.startswith('r'):
        lower_case = True if label.endswith('l') else False
        return int(roman_to_num(symbol))

# Convert number to Roman number
def num_to_roman(num, lower_case=False):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num.lower() if lower_case else roman_num

# Convert number to alphabet(s)
def num_to_alphabet(num, lower_case=False):
    alphabet = ''
    while num > 0:
        remainder = (num - 1) % 26
        alphabet = chr(65 + remainder) + alphabet
        num = (num - 1) // 26
    return alphabet.lower() if lower_case else alphabet

# Convert Roman number to number
def roman_to_num(roman):
    roman = roman.upper()
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    result = 0
    i = 0
    while i < len(roman):
        for v, s in zip(val, syb):
            if roman.startswith(s, i):
                result += v
                i += len(s)
                break
    return result

# Convert alphabet(s) to number
def alphabet_to_num(alphabet):
    result = 0
    for char in alphabet.upper():
        result = result * 26 + ord(char) - ord('A') + 1
    return result

# Get Prompt Template
def get_prompt(filename, inputs):
    with open(filename, 'r') as file:
        generated_prompt = file.read().split("<commentblockmarker>###</commentblockmarker>")[1].strip()
    for index, item in enumerate(inputs):
        key = f"!<INPUT {index}>!"
        generated_prompt = generated_prompt.replace(key, str(item))
    return generated_prompt

# Get questionnaire
def get_questionnaire(name):
    try:
        with open('dataset/questionnaires.json') as dataset:
            data = json.load(dataset)
        try:
            questionnaire = data[name]
            return questionnaire
        except ValueError:
            raise ValueError("Questionnaire not found.")
    except FileNotFoundError:
        raise FileNotFoundError("The 'questionnaires.json' file does not exist.")

# Add statements to dataset
def add_statement(qname, language, statements):
    with open('dataset/questionnaires.json', 'r') as f:
        data = json.load(f)
    
    # If language not exist, create it
    if language not in data[qname]["questions"]:
        data[qname]["questions"][language] = {}
        
    # Get the latest version
    version_list = list(data[qname]['questions'][language].keys())
    version_list = [item for item in version_list if item.startswith('v') and item[1:].isdigit()]
    if version_list:
        new_version = f'v{max([int(item[1:]) for item in version_list]) + 1}'
    else:
        new_version = 'v1'

    if new_version not in data[qname]["questions"][language]:
        data[qname]["questions"][language][new_version] = dict()
        data[qname]["questions"][language][new_version]["statements"] = dict()
    
    for i, s in enumerate(statements):
        data[qname]["questions"][language][new_version]["statements"][str(i+1)] = s
    
    with open('dataset/questionnaires.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)