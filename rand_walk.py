import json
import networkx as nx
from datetime import datetime
import numpy as np
from random import choice
import queue
def MetaPathRandomWalk(network_G,style,v,length):
    MP = [0]*length
    MP[0] = v
    tmp = v
    for i in range(length-1):
        neighborlist = []
        neighbors = list(network_G.adj[tmp])
        if not neighbors:
            return 0
        if style[tmp] == 'a':
            Type = choice(['a', 'f'])
            for neighbor in neighbors:
                if style[neighbor] == Type:
                # if style[neighbor] == 'a' or style[neighbor] == 'f':
                    neighborlist.append(neighbor)
            if neighborlist != []:
                MP[i+1]=choice(neighborlist)
            else:
                MP[i+1]=choice(neighbors)
            neighborlist.clear()
        elif style[tmp] == 'v':
            for neighbor in neighbors:
                if style[neighbor] == 'f':
                    neighborlist.append(neighbor)
            if neighborlist != []:
                MP[i+1]=choice(neighborlist)
            else:
                MP[i+1]=choice(neighbors)
            neighborlist.clear()
        elif style[tmp] == 'f':
            if i!=0 and style[MP[i-1]]=='v':
                for neighbor in neighbors:
                    if style[neighbor] == 'a':
                        neighborlist.append(neighbor)
                if neighborlist != []:
                    MP[i+1]=choice(neighborlist)
                else:
                    MP[i+1]=choice(neighbors)
                neighborlist.clear()
            elif i!=0 and style[MP[i-1]]=='i':
                for neighbor in neighbors:
                    if style[neighbor] == 'i':
                        neighborlist.append(neighbor)
                if neighborlist != []:
                    MP[i+1]=choice(neighborlist)
                else:
                    MP[i+1]=choice(neighbors)
                neighborlist.clear()
            else:
                Type = choice(['a', 'v'])
                for neighbor in neighbors:
                    if style[neighbor] == Type:
                    # if style[neighbor] == 'a' or style[neighbor] == 'v':
                        neighborlist.append(neighbor)                
                if neighborlist != []:
                    MP[i+1]=choice(neighborlist)
                else:
                    MP[i+1]=choice(neighbors)
                neighborlist.clear()
        elif style[tmp] == 'i':
            for neighbor in neighbors:
                if style[neighbor] == 'f':
                    neighborlist.append(neighbor)
            if neighborlist != []:
                    MP[i+1]=choice(neighborlist)
            else:
                MP[i+1]=choice(neighbors)
            neighborlist.clear()
        tmp = MP[i+1]
        # if tmp==0:
        #     if i != 0:
        #         MP[i+1]=MP[i-1]
        #         tmp=MP[i-1]
        #     else:
        #         MP[i+1] = list(network_G.adj[v])[0]
        #         tmp = MP[i+1]
    return MP

def json_r(f_path):
    with open(f_path, 'r') as f:
        data = json.load(f)
    return data
totalres = [0] * 10
totalamo = [0] * 10
def get_prob(graph,v,MP):
    d = {}
    q = queue.Queue()   
    q.put((v,0))
    d[v] = 0
    depth = 0
    res = [0] * 10
    amount = [0] * 10
    
    while (not q.empty() and depth < 100):
        author, depth = q.get()
        amount[depth] += 1
        neighbors = list(graph.adj[author])
        for tmpaut in neighbors:
            if tmpaut not in d:
                q.put((tmpaut,depth+1))
                d[tmpaut] = depth + 1

    for tmp in MP:
        res[d[tmp]] += 1
    for i in range(len(res)):
        totalres[i] += res[i]
    for i in range(len(amount)):
        totalamo[i] += amount[i]
    for i in range(depth):
        res[i] = res[i]/amount[i]
    return res,amount


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

print(datetime.now())
data = json_r(r'C:\Users\Victor\Documents\WeChat Files\llmmzztony\Files\2014.json')
graph = get_graph(data)
# graph.remove_edges_from(remove_list)
nodes = graph.nodes()
style = nx.get_node_attributes(graph, 'style')
res = {}
amount = {}
num = 0
print(list(graph.adj['Ali.jiang']))
# for v in nodes:
#     num += 1
#     MP = MetaPathRandomWalk(graph, style, v, 100)
#     res[v],amount[v] = get_prob(graph,v,MP)
#     if num > 100:
#         break
# for i in range(10):
#     if(totalamo[i]>0):
#         totalres[i] = totalres[i]/totalamo[i]
# f1 = open('E:\大三上\AI_ZLQ\CS410A1Search\CS410A1Search\labres.txt','w')
# f2 = open('E:\大三上\AI_ZLQ\CS410A1Search\CS410A1Search\labamount.txt','w')

# for key,value in res.items():
#     f1.write('{key}:{value}'.format(key = key, value = value))
# for key,value in amount.items():
#     f2.write('{key}:{value}'.format(key = key, value = value))

# print(totalres)
# print(datetime.now())