import os
import random
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull
from tools import *

class Visualize:
    '''
    Initialize a Visualize object for visualizing data using PCA.
        qname (dataframe), reference (df)
    '''
    def __init__(self, qname, reference):
        self.data = list()
        self.questionnaire = get_questionnaire(qname)
        dimensions = len(self.questionnaire["scales"])
        self.pca = PCA(n_components=dimensions)
        pca_basis = self.pca.fit_transform(reference)
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
    def add(self, data, color, label=None, marker="^", alpha=1.0):
        pca_data = self.pca_transform(data)
        self.data.append({
            "x": pca_data[:,0],
            "y": pca_data[:,1],
            "color": color,
            "label": label,
            "marker": marker,
            "alpha": alpha
        })
        
    def rotate_point(self, x, y, angle):
        """Rotate a point around the origin by a given angle."""
        radians = np.deg2rad(angle)
        x_rot = x * np.cos(radians) - y * np.sin(radians)
        y_rot = x * np.sin(radians) + y * np.cos(radians)
        return x_rot, y_rot
    
    def rotate_data(self, data, angle):
        """Rotate all points in the data by a given angle."""
        x_rot, y_rot = [], []
        for xi, yi in zip(data["x"], data["y"]):
            xi_rot, yi_rot = self.rotate_point(xi, yi, angle)
            x_rot.append(xi_rot)
            y_rot.append(yi_rot)
        return {"x": x_rot, "y": y_rot, "color": data["color"], "label": data["label"], "marker": data["marker"], "alpha": data["alpha"]}
    
    
    '''
    Plot all data points.
        savename (str), random_zorder (bool)
    '''
    def plot(self, savename=None, format="png", random_zorder=False, plot_reference=False, rotation_angle=0, exclude=[]):
        plt.scatter(**self.basis)
        all_points = []
        for index, data in enumerate(self.data):
            data = self.rotate_data(data, rotation_angle)
            all_points.extend(zip(data["x"], data["y"]))
            if random_zorder and index not in exclude:
                for i, (xi, yi) in enumerate(zip(data["x"],data["y"])):
                    if i == 0:
                        plt.scatter(xi, yi, color=data["color"], marker=data["marker"], label=data["label"], alpha=data["alpha"],
                                    facecolors=(1, 1, 1, 0.1), zorder=random.randint(3,1000000))
                    else:
                        plt.scatter(xi, yi, color=data["color"], marker=data["marker"], alpha=data["alpha"],
                                    facecolors=(1, 1, 1, 0.1), zorder=random.randint(3,1000000))
            else:
                plt.scatter(**data, facecolors=(1, 1, 1, 0.1), zorder=3)
                
        if plot_reference:
            all_points = np.array(all_points)
            hull = ConvexHull(all_points)
            hull_points = all_points[hull.vertices]
            plt.fill(hull_points[:, 0], hull_points[:, 1], color=(245/255, 245/255, 245/255), alpha=1, zorder=2)
                
        plt.legend(loc='upper left')
        plt.xlim(-3, 5)
        plt.ylim(-2, 6)
        plt.xticks([])
        plt.yticks([])
        if savename:
            os.makedirs('figures', exist_ok=True)
            plt.savefig(f"figures/{savename}.{format}", dpi=300, format=format)
            print(f'Saved "figures/{savename}.{format}".')
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
