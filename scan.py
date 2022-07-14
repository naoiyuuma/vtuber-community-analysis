
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community
import math
import queue
from collections import deque


def sigma(edges):

    set1 = set(G.adj[edges[0]])
    set2 = set(G.adj[edges[1]])

    # 自分自身を加える
    set1.add(edges[0])
    set2.add(edges[1])

    len_set1 = len(set1)
    len_set2 = len(set2)
    setand = set1 & set2

    setand_gamma = len(setand)
    gamma = setand_gamma/(math.sqrt(len_set1*len_set2))
    # edgesに属性値を付与
    # g.edges[edges[0]][edges[1]]['sigma']=gamma
    return gamma


def scan(G, eps, mu):

    for nodes in G.nodes():
        # 初期化
        G.nodes[nodes]['node_class'] = 0

    clusterID = 0
    # clusterSet = set()
    clusterList = list()

    for node in G.nodes():
        neighbors_set = set(G.adj[node])
        count = 0
        set_node_over_eps = set()
        # core条件
        for neighbors in neighbors_set:
            sigma_vaule = sigma([node, neighbors])
            if sigma_vaule >= eps:
                set_node_over_eps.add(neighbors)
                count = count+1
        # end for

        # core判断
        if ((count >= mu) and (G.nodes[node]['node_class'] == 0)):

            # generate new clusterID
            clusterID = clusterID+1
            #print("clusterID", clusterID)
            # print(clusterID)

            # キュー
            que = queue.Queue()
            # 近隣ノード(閾値超え)と自分自身を加える
            set_node_over_eps.add(node)
            # que.put(neighbors_set)
            setR = set()
            # まず、coreの近隣nodeをsetRに入れる
            setR = (setR | set_node_over_eps)

            clusterSet = set()
            flag = 1
            while ((not que.empty()) or flag == 1):
                flag = 0
                set_over_eps = set()
                for neigh in setR:
                    set_neigh_neighs = set(G.adj[neigh])
                    for neighs in set_neigh_neighs:
                        #core_counter = 0
                        if sigma([neigh, neighs]) >= eps:
                            set_over_eps = (set_over_eps | set({neighs}))
                            #core_counter = core_counter+1
                    if len(set_over_eps) >= mu:
                        setR = (setR | set_over_eps)

                # for each x ∈ R do
                for x in setR:
                    if G.nodes[x]['node_class'] == 0:  # unclassifed
                        que.put(set({x}))

                    if G.nodes[x]['node_class'] <= 0:  # unclassifed or non-number
                        G.nodes[x]['node_class'] = clusterID
                # end for
                # remove y from Q;
                q_node = set(que.get())

                clusterSet = (clusterSet | q_node)
            # end while
            clusterList.append(clusterSet)
    # end for

    # hub
    hubSet = set()

    hazureSet = set()

    for nodes in G.nodes():
        if G.nodes[nodes]['node_class'] <= 0:

            neighbors_set_hub = set(G.adj[nodes])
            hub_dif = set()
            for hub_neigh in neighbors_set_hub:
                if(G.nodes[hub_neigh]['node_class']) >= 1:
                    hub_dif = hub_dif | set({G.nodes[hub_neigh]['node_class']})
            # end for
            if(len(hub_dif) >= 2):
                G.nodes[nodes]['node_class'] = -2  # hub
                hubSet = (hubSet | set({nodes}))
            else:
                G.nodes[nodes]['node_class'] = -3  # 外れ値
                hazureSet = (hazureSet | set({nodes}))
    # end for

    clusterList.append(hubSet)
    clusterList.append(hazureSet)

    return clusterList


eps = 0.7  # 閾値
mu = 5  # コア条件
G = nx.read_edgelist('./data/vtuber_data.txt', nodetype=str)
print(scan(G, eps, mu))
