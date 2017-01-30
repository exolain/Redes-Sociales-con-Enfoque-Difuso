import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skcmeans.algorithms import Probabilistic
from sklearn.datasets import make_blobs
class CosineProbabilistic(Probabilistic):
    metric = 'cosine'
plt.figure(figsize=(5, 5)).add_subplot(aspect='equal')
n_clusters = 4
df = pd.read_csv('./scikit-cmeans/data/clean/2014.csv')
data = df.as_matrix(columns=['titulo','condicion_actual'])
#print(data)
clusterer = CosineProbabilistic(n_clusters=n_clusters, n_init=20)
clusterer.fit(data)
xx, yy = np.array(np.meshgrid(np.linspace(-10, 10, 1000), np.linspace(-10, 10, 1000)))
z = np.rollaxis(clusterer.calculate_memberships(np.c_[xx.ravel(), yy.ravel()]).reshape(*xx.shape, -1), 2, 0)
colors = 'rgbyco'
print(clusterer.centers)
for membership, color in zip(z, colors):
    plt.contour(xx, yy, membership, colors=color, alpha=0.5)
plt.scatter(data[:, 0], data[:, 1], c='k')
plt.show()
