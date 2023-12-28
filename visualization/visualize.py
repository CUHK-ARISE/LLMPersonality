"""
Author: LAM Man Ho (mhlam@link.cuhk.edu.hk)
"""
import os
import json
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product
from sklearn.decomposition import PCA

class Visualize:
    '''
    Initialize a Visualize object for visualizing data using PCA.
        qname (dataframe), basis (df)
    '''
    def __init__(self, qname, basis):
        self.data = list()
        self.questionnaire = get_questionnaire(qname)
        dimensions = len(self.questionnaire["scales"])
        self.pca = PCA(n_components=dimensions)
        # random.shuffle(basis.to_numpy())
        pca_basis = self.pca.fit_transform(basis)
        self.basis = {
            "x": pca_basis[:,0],
            "y": pca_basis[:,1],
            "color": "#FFF"
        }
        
    '''
    Extract the values for all dimensions.
        data (df)
    '''
    def extract(self, data):
        return data[list(self.questionnaire["categories"].keys())]
    
    '''
    Apply dimensionality reduction to data.
        data (df)
    '''
    def pca_transform(self, data):
        return self.pca.transform(self.extract(data))[:, :2]
    
    '''
    Add data points to pre-visualize collection.
        data (df), color (LightSalmon str), label (str)
    '''
    def add(self, data, color, label=None):
        pca_data = self.pca_transform(data)
        self.data.append({
            "x": pca_data[:,0],
            "y": pca_data[:,1],
            "color": color,
            "label": label
        })
    
    '''
    Plot all data points.
        savename (str), random_zorder (bool)
    '''
    def plot(self, savename=None, random_zorder=False, exclude=[]):
        plt.scatter(**self.basis)
        for index, data in enumerate(self.data):
            if random_zorder and index not in exclude:
                for i, (xi, yi) in enumerate(zip(data["x"],data["y"])):
                    if i == 0:
                        plt.scatter(xi, yi, color=data["color"], marker='^', label=data["label"],
                                    facecolors=(1, 1, 1, 0.5), zorder=random.randint(2,10000))
                    else:
                        plt.scatter(xi, yi, color=data["color"], marker='^',
                                    facecolors=(1, 1, 1, 0.5), zorder=random.randint(2,10000))
            else:
                plt.scatter(**data, marker='^', facecolors=(1, 1, 1, 0.5))
        plt.legend(loc = 'upper right')
        if savename:
            os.makedirs('figures', exist_ok=True)
            plt.savefig(f"figures/{savename}", dpi=500)
            print(f'Saved "figures/{savename}".')
        else:
            plt.show()
        plt.clf()
        
    '''
    Clear the pre-visualize data points.
    '''
    def clean(self):
        self.data = list()
    
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
Construct the basis and fit to PCA to extract the projection matrix for dimensional reduction
'''
def construct_basis(questionnaire_name, savefile, mode='full'):
    basis = list()
    questionnaire = get_questionnaire(questionnaire_name)
    scales = questionnaire["scales"]
    categories = list(questionnaire["categories"].keys())
    combinations = list(product(scales, repeat=len(categories)))
    for item in combinations:
        basis.append(dict(zip(categories, item)))
    with open(savefile, 'w') as f:
        json.dump(basis, f, indent=4)
        
'''
Extract the fitting basis
'''
def extract_basis(filename):
    with open(filename, 'r') as f:
        basis = json.load(f)
    df = pd.DataFrame(basis)
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
