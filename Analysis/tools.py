import json
import numpy as np
import pandas as pd
import scipy.stats as stats

from itertools import product

'''
Get corresponding questionnaire
    name (str)
'''
def get_questionnaire(name):
    try:
        with open('dataset/questionnaires.json') as dataset:
            data = json.load(dataset)
        try:
            return data[name]
        except ValueError: raise ValueError("Questionnaire not found.")
    except FileNotFoundError: raise FileNotFoundError("The 'questionnaires.json' file does not exist.")

'''
Construct the reference and fit to PCA to extract the projection matrix for dimensional reduction
'''
def construct_reference(questionnaire_name, savefile, mode='full'):
    reference = list()
    questionnaire = get_questionnaire(questionnaire_name)
    scales = questionnaire["scales"]
    categories = list(questionnaire["categories"].keys())
    combinations = list(product(scales, repeat=len(categories)))
    for item in combinations:
        reference.append(dict(zip(categories, item)))
    with open(savefile, 'w') as f:
        json.dump(reference, f, indent=4)
        
'''
Extract the fitting reference
'''
def extract_reference(filename):
    with open(filename, 'r') as f:
        reference = json.load(f)
    df = pd.DataFrame(reference)
    return df

'''
Extract the save data as DataFrame
'''
def extract_data(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileExistsError
    
    info = tuple(data["data"][0]["info"].keys())
    data = [{**d["info"], **d["data"]} for d in data["data"]]
    df = pd.DataFrame(data)
    return df, info


'''
Conduct hypothesis testing
    x, y (list)
'''
def hypothesis_testing(x, y, significant_level=0.001):
    mean1, std1, n1 = np.mean(x), np.std(x), len(x)
    mean2, std2, n2 = np.mean(y), np.std(y), len(y)
    
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
    
    diff = mean1 - mean2
    symbol = '=' if p_value > significant_level else '>' if t_value > 0 else '<'
    
    return symbol, diff, t_value, p_value
