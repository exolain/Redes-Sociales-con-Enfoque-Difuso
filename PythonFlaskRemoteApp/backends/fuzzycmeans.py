import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from skcmeans.algorithms import Probabilistic
from scikitcmeans.skcmeans.algorithms import Probabilistic
from sklearn.datasets import make_blobs
class GowerProbabilistic(Probabilistic):
    metric = 'euclidean'


plt.figure(figsize=(5, 5)).add_subplot(aspect='equal')
n_clusters = 6
df = pd.read_csv('./scikitcmeans/data/clean/2015.csv')
#df = pd.read_csv('./scikit-cmeans/data/clean/iris.csv')
#data = df.as_matrix(columns=['SepalLength','SepalWidth'])
data = df.as_matrix(columns=['region_residencia', 'residencia_hace_dos_anos'])
#print(data)
clusterer = GowerProbabilistic(n_clusters=n_clusters, n_init=20)
clusterer.fit(data)
xx, yy = np.array(np.meshgrid(np.linspace(-10, 10, 1000), np.linspace(-10, 10, 1000)))
z = np.rollaxis(clusterer.calculate_memberships(np.c_[xx.ravel(), yy.ravel()]).reshape(*xx.shape, -1), 2, 0)

colors = 'rgbyc'
print(clusterer.memberships)
for membership, color in zip(z, colors):
    plt.contour(xx, yy, membership, colors=color, alpha=0.5)
plt.scatter(data[:, 0], data[:, 1], c='k')


print(clusterer.fpcs)

#fig2, ax2 = plt.subplots()
#ax2.plot(np.r_[2:11], fpcs)
#ax2.set_xlabel("Number of centers")
#ax2.set_ylabel("Fuzzy partition coefficient")


plt.show()