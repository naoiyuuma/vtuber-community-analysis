import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community
from sklearn.cluster import SpectralClustering
from sklearn import metrics
import math
import queue
import numpy as np
import community

# 重み付きのデータの読み込み
G = nx.read_weighted_edgelist(
    './data/vtuber_data.txt', delimiter='  ', nodetype=str, create_using=nx.DiGraph)
print(nx.is_directed(G))
# as np matrix
adj_mat = nx.to_numpy_matrix(G)
print(adj_mat)
# 自己経路の排除 有向グラフに対してしか行えない？
G.remove_edges_from(nx.selfloop_edges(G))
# 有向グラフ -> 無向グラフ
G = nx.to_undirected(G)
print(nx.is_directed(G))

partition = community.best_partition(G)
########################################################
####Bad graph type, use only non directed graph#########
########################################################
print(float(len(set(partition.values()))))
print(set(partition.values()))  # setで重複をなくす-> クラスター数

pos = nx.spring_layout(G, iterations=11)
plt.figure(figsize=(14, 9))
colors = ['red', 'darkorange', 'green', 'yellow', 'darkred', 'plum', 'aqua', 'lime',
          'fuchsia', 'olive', 'purple', 'maroon', 'darksalmon', 'bisque',
          'tan', 'moccasin', 'gold', 'darkkhaki', 'palegreen', 'mediumspringgreen',
          'paleturquoise', 'darkcyan', 'darkturquoise', 'mediumpurple', 'plum', 'mistyrose',
          'seashell', 'peachpuff', 'navajowhite', 'ivory', 'lemonchiffon', 'skyblue', 'salmon',
          'beige', 'khaki', 'darkmagenta', 'lightcyan', 'thistle', 'oldlace']
count = 0
size = float(len(set(partition.values())))
cluster_list = list()
for com in set(partition.values()):
    print(com)
    list_nodes = [nodes for nodes in partition.keys()
                  if partition[nodes] == com]
    print(list_nodes)
    cluster_list.append(list_nodes)
    nx.draw_networkx_nodes(
        G, pos, list_nodes, node_size=10, node_color=colors[count])
    count += 1

"""
# check
print("----------------")
for clus in cluster_list:
    print(clus)

# クラスター外のPPR計算
name = 'リゼ・ヘルエスタ -Lize Helesta-'
same_list = list()
for clus in cluster_list:
    if name in clus:
        same_list = clus
        break

pvector = []
counter = 0
for node in G.nodes():
    if node in same_list:
        pvector.append(1)
        counter += 1
    else:
        pvector.append(0)
# pvectorの正規化
pvector = [x/counter for x in pvector]
d = dict(zip(G.nodes(), pvector))

prDict = nx.pagerank(G, alpha=0.9, personalization=d)
sortedDict = sorted(prDict.items(), key=lambda x: x[1], reverse=True)

i = 0
count = 0
print(name, "に影響力の高いVtuber上位5名")
while count < 100:
    if not (sortedDict[i][0] in same_list):
        print(count, "番目", sortedDict[i])
        count += 1
    i += 1
"""
edge_width = [d['weight']*0.045 for (u, v, d) in G.edges(data=True)]
nx.draw_networkx_edges(G, pos, edge_color='blue', width=edge_width, alpha=0.7)
nx.draw_networkx_labels(G, pos, font_size=4, font_color='k',
                        font_family='Hiragino Mincho ProN')
plt.axis('off')
plt.show()
