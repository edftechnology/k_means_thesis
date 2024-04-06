# REFERÊNCIA(S): -------------------------------------------------------------------------------------------------------

# [1] https://www.youtube.com/watch?v=JcfIeaGzF8A

# PACOTE(S): -----------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Métodos Hierarquicos:
import scipy
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

from pylab import rcParams
import seaborn as sb

import sklearn
from sklearn.cluster import AgglomerativeClustering
import sklearn.metrics as sm

np.set_printoptions(precision=4, suppress=True)
plt.figure(figsize=(10, 3))
plt.style.use("seaborn-whitegrid")

address = "banco_de_dados\\mtcars.csv"

cars = pd.read_csv(address)

cars.columns = ["car_names", "mpg", "cyl", "disp", "hp",
                "drat", "wt", "qsec", "vs", "am", "gear",
                "carb"]
X = cars.ix[:, (1, 3, 4, 6)].values
y = cars.ix[:, (9)].values

# Usando scipy para gerar dendrogramas
Z = linkage(X, "ward")
dendrogram(Z,
           truncate_mode="lastp",
           p=12,
           leaf_rotation=90.,
           leaf_font_size=15.,
           show_contracted=True)
plt.title("Truncated Hierarchical Clustering Dendrogram")
plt.xlabel("Cluster Size")
plt.ylabel("Distance")

plt.axhline(y=500) # Inserir uma linha em y = 500 no dendrograma
plt.axhline(y=150) # Inserir uma linha em y = 150 no dendrograma

plt.show()

# Gerar Clusters Hierarquicos
k = 2

Hclustering = AgglomerativeClustering(n_clusters=k,
                                      affinity="euclidean",
                                      linkage="ward")

Hclustering.fit(X)

print(sm.accuracy_score(y, Hclustering.labels_))

Hclustering = AgglomerativeClustering(n_clusters=k,
                                      affinity="euclidean",
                                      linkage="complete")

Hclustering.fit(X)

print(sm.accuracy_score(y, Hclustering.labels_))

Hclustering = AgglomerativeClustering(n_clusters=k,
                                      affinity="euclidean",
                                      linkage="average")

Hclustering.fit(X)

print(sm.accuracy_score(y, Hclustering.labels_))

Hclustering = AgglomerativeClustering(n_clusters=k,
                                      affinity="manhattan",
                                      linkage="average")

Hclustering.fit(X)

print(sm.accuracy_score(y, Hclustering.labels_))







