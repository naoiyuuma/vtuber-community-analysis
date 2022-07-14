import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community
import math
import numpy as np

# 有向グラフ
D = nx.DiGraph()
# 重み付きのデータの読み込み
D = nx.read_weighted_edgelist(
    './data/vtuber_data.txt', delimiter='  ', nodetype=str, create_using=nx.DiGraph)
prDict = nx.pagerank(D, alpha=0.9)
# print("prDict= \n", prDict)
print(len(prDict))

sortedDict = sorted(prDict.items(), key=lambda x: x[1], reverse=True)
print("pagerank")
"""
i = 0
while i < len(sortedDict):
    print(i, "番目 : ", sortedDict[i])
    i += 1
"""

# 可視化
pos = nx.spring_layout(D, k=0.70, iterations=11)
plt.figure(figsize=(14, 9))
edge_width = [d['weight']*0.045 for (u, v, d) in D.edges(data=True)]
nx.draw_networkx_edges(D, pos, edge_color='blue', width=edge_width, alpha=0.7)
nx.draw_networkx_nodes(D, pos, node_color='red',
                       node_size=[4000*v for v in prDict.values()], alpha=0.9)
nx.draw_networkx_labels(D, pos, font_size=4,
                        font_color='k', font_family='Hiragino Mincho ProN')

plt.axis('off')
plt.show()
