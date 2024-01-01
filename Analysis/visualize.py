"""
Author: LAM Man Ho (mhlam@link.cuhk.edu.hk)
"""

import os
import random
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from Analysis.tools import *

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
        
    
    def detect_outlier(self, df, eps, min_samples):
        pca_data = self.pca_transform(df)
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(pca_data)
        print(f"Number of Inliers: {len(labels[labels != -1])}")
        print(f"Number of Outliers: {len(labels[labels == -1])}")
        print(f"{len(labels[labels != -1]) + len(labels[labels == -1])}")
        df['Label'] = labels
        return df
