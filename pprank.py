import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community
import math
import numpy as np

# 有向グラフ
G = nx.DiGraph()
# 重み付きのデータの読み込み
G = nx.read_weighted_edgelist(
    './data/vtuber_data.txt', delimiter='  ', nodetype=str, create_using=nx.DiGraph)

name = 'リゼ・ヘルエスタ -Lize Helesta-'
pvector = []
for node in G.nodes():
    if name in node:
        pvector.append(1)
    else:
        pvector.append(0)

d = dict(zip(G.nodes(), pvector))

prDict = nx.pagerank(G, alpha=0.9, personalization=d)
sortedDict = sorted(prDict.items(), key=lambda x: x[1], reverse=True)

i = 0
count = 0
print(name, "に影響力の高いVtuber上位5名")
while count < 10:
    if sortedDict[i][0] != name:
        print(count, "番目", sortedDict[i])
        count += 1
    i += 1
