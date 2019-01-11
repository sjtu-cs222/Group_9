import numpy as np
import operator
import json
import networkx as nx
from datetime import datetime
from random import choice
import queue
def json_r(f_path):
    with open(f_path, 'r') as f:
        data = json.load(f)
    return data

def get_graph(data):
    authors, keywords, conf, paper = [], [], [], []
    for dic in data:
        authors.extend(dic['author_name'])
        keywords.extend(dic['keyword'])
        conf.append(dic['conf'])
        paper.append(dic['paperid'])
    authors, keywords, conf, paper = list(set(authors)), list(set(keywords)), list(set(conf)), list(set(paper))
    ''' 构建Graph '''
    # 添加节点
    graph = nx.Graph()
    [graph.add_node('a'+i.replace(' ', '.'), style='a') for i in authors]
    [graph.add_node('f'+i.replace(' ', '.'), style='f') for i in keywords]
    [graph.add_node('v'+i.replace(' ', '.'), style='v') for i in conf]
    [graph.add_node('i'+i.replace(' ', '.'), style='i') for i in paper]
    # 添加连接
    for Dict in data:
        for i in range(len(Dict['author_name'])):
                for j in range(i+1, len(Dict['author_name'])):
                    graph.add_edge('a'+Dict['author_name'][i].replace(' ', '.'), 'a'+Dict['author_name'][j].replace(' ', '.'))
                if i == len(Dict['author_name'])-2:
                    break
        for i in range(len(Dict['author_name'])):
            for j in Dict['keyword']:
                graph.add_edge('a'+Dict['author_name'][i].replace(' ', '.'), 'f'+j.replace(' ', '.'))
            graph.add_edge('a'+Dict['author_name'][i].replace(' ', '.'), 'v'+Dict['conf'].replace(' ', '.'))
        for i in Dict['keyword']:
            graph.add_edge('f'+i.replace(' ', '.'), 'v'+Dict['conf'].replace(' ', '.'))
            graph.add_edge('f'+i.replace(' ', '.'), 'i'+Dict['paperid'].replace(' ', '.'))
    return graph


data = json_r(r'C:\Users\Victor\Documents\WeChat Files\llmmzztony\Files\2014.json')
graph = get_graph(data)


totalres = [0] * 10
totalamo = [0] * 10


node_vec = {}
dis_vec = {}
#17301657855 
f = open('vecres2014_1_1.txt','r', encoding='UTF-8')
for line in f.readlines():
    if line[0]=='A' or line[0]=='V' or line[0]=='K':
        tmp_nodes = line.split()
        tmpnode = tmp_nodes[0]
        a = np.array(tmp_nodes[1:])
        a = a.astype('float64')
        node_vec[tmpnode] = a
for i in node_vec.keys():
     dis_vec[i] = {}
n = 0
for i in node_vec.keys(): 
    if i[0][0] == 'A' :
        for j in node_vec.keys():
            if j != i:
                dis_vec[i][j] = np.sqrt(np.sum(np.square(node_vec[j] - node_vec[i])))
                print(dis_vec[i][j])
sorted_dic = {}
for i in node_vec.keys():
        sorted_dic[i]=sorted(dis_vec[i].items(),key=operator.itemgetter(1))

countA = 0
countK = 0
countV = 0
listA = {}
listK = {}
listV = {}
for j in node_vec.keys():
    listA[j] = []
    listK[j] = []
    listV[j] = []
for j in node_vec.keys():
    if j[0][0] == 'A' :
        for i in sorted_dic[j]:
                if i[0][0] == 'A' and countA < 10 :
                        listA[j].append(i[0])
                        countA += 1
                if i[0][0] == 'K' and countK < 10 :
                        listK[j].append(i[0])
                        countK += 1
                if i[0][0] == 'V' and countV < 3 :
                        listV[j].append(i[0])
                        countV += 1
    countA = 0
    countK = 0
    countV = 0
cntA = 0
cntK = 0
cntV = 0
resA = 0
resK = 0
resV = 0
a = 0

for j in node_vec.keys() and a < 10000:
    if j[0][0] == 'A' :
        for i in listA[j]:
            cntA += 1
            print(listA[j])
            if i in graph.adj[j]:
                resA += 1
        for i in listK[j]:
            cntK += 1
            if i in graph.adj[j]:
                resK += 1
        for i in listV[j]:
            cntV+=1 
            if i in graph.adj[j]:
                resV += 1 
    a += 1 
    

resA = float(resA/cntA)
resK = float(resK/cntK)
resV = float(resV/cntV)

print(resA)
print(resK)
print(resV)