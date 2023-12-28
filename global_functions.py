"""
Author: LAM Man Ho (mhlam@link.cuhk.edu.hk)
"""
import json
import numpy as np
import scipy.stats as stats
from statistics import mean

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

# Hypothesis Testing
def hypothesis_testing(sample1, sample2, significant_level=0.001):
    mean1, std1, n1 = np.mean(sample1), np.std(sample1), len(sample1)
    mean2, std2, n2 = np.mean(sample2), np.std(sample2), len(sample2)
    
    # Add an epsilon to prevent the zero standard deviarion
    epsilon = 1e-8
    std1 += epsilon
    std2 += epsilon
    
    # Perform F-test
    if std1 > std2:
        f_value = std1 ** 2 / std2 ** 2
        df1, df2 = n1 - 1, n2 - 1
    else:
        f_value = std2 ** 2 / std1 ** 2
        df1, df2 = n2 - 1, n1 - 1

    p_value = (1 - stats.f.cdf(f_value, df1, df2)) * 2
    equal_var = True if p_value > significant_level else False
    

    # Performing T-test
    df = n1 + n2 - 2 if equal_var else ((std1**2 / n1 + std2**2 / n2)**2) / ((std1**2 / n1)**2 / (n1 - 1) + (std2**2 / n2)**2 / (n2 - 1))
    t_value, p_value = stats.ttest_ind_from_stats(mean1, std1, n1, mean2, std2, n2, equal_var=equal_var)
    
    if p_value > significant_level:
        # return f'- ({(mean1 - mean2):.2f})'
        return f'$= {(mean1 - mean2):.2f}_{{{p_value:.2f}}}$'
        # return f'<font color="F54747">= ({(mean1 - mean2):.2f})</font>'

    else:
        if t_value > 0:
            # return '>'
            # return f'> ({(mean1 - mean2):.2f})'
            return f'$> {(mean1 - mean2):.2f}_{{{p_value:.2f}}}$'
        else:
            # return '<'
            # return f'< ({(mean1 - mean2):.2f})'
            return f'$< {(mean1 - mean2):.2f}_{{{p_value:.2f}}}$'
