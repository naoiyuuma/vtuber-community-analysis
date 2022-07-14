import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community
from sklearn.cluster import SpectralClustering
from sklearn import metrics
from sklearn.cluster import KMeans
import math
import queue
import numpy as np

# 重み付きのデータの読み込み
G = nx.read_weighted_edgelist(
    'vtuber_data.txt', delimiter='  ', nodetype=str, create_using=nx.DiGraph)

# as np matrix
adj_mat = nx.to_numpy_matrix(G)
pred = KMeans(n_clusters=6).fit_predict(adj_mat)
print(pred)
