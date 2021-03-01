import requests 
import lxml.html
import random

def our_crawler(url):
    prefix = "http://en.wikipedia.org"
    result=set()
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    
    for path in doc.xpath("//a[contains(@href,'/wiki/')and not(contains(@href,':'))]/@href"):
        temp = prefix+path
        if(len(result)<10):
                result.add(temp)
    
    result= list(result)
    if len(result)==0:
        result.append(url)
    return result
    
def do_it_3(url):
    graph={}
    visited=set()
    not_visited=[]
    not_visited.append(url)
    temp=[]
    result_for_last=[]
    for i in range(3):
        for j in range(len(not_visited)):
            if not_visited[j] in visited:
                continue 
            result=our_crawler(not_visited[j])
            temp= temp+result
            visited.add(not_visited[j])
            if not_visited[j] not in graph and i!=2:
                graph[not_visited[j]]=result
            if not_visited[j] not in graph and i==2:
                for item in result:
                    if item in visited:
                        result_for_last.append(item)
                if len(result_for_last)==0:
                    result_for_last.append(not_visited[j])
                graph[not_visited[j]]=result_for_last
                     
        not_visited=temp
        temp=[]
    return graph

def print_graph2(g): 
    for item in g.keys():
        print(item+" = {",end="")
        result=g[item]
        for i in range(len(result)):
            if i< len(result)-1:
               print(result[i]+", ",end="")
            else:
                print(result[i],end="")
        print("}")
    
