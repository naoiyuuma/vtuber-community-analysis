# vtuber-community-analysis
Youtube でのVtuber 影響力解析とおすすめVtuber 推定
- 事前準備
```
$pip3 install <任意のライブラリ>
// for youtube API
$ pip3 install google-api-python-client --user
$ brew install forego
```

## 影響力解析
pagerank , Personalized PageRank
```
$ python3 pagerank_v.py
```
## コミュニティ分析
louvain algorithm or scan algorithm or k-means
 ```
$ python3 pagerank_v.py
```
- 分析例
!(./img/result.png)
## dataset
- YouTubeAPIを用いた自作データセット
    ./data/vtuber-data.txt
    ```
    node1 node2 weight
    node1 node3 weight
    ...
    ```
- MovieLens
https://grouplens.org/datasets/movielens/