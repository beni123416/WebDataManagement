import random

def cal_PR(graph):
    iteration=10000
    damp=0.3
    flag=random.uniform(0, 1)
    vertexs= list(graph.keys())
    g_PR={}
    f=print_graph(graph)
    f.write("--------------The PR------------------\n")
    for item in list(g.keys()):
        g_PR[item]=0   
    index=random.randint(0,len(vertexs)-1)
    jump=vertexs[index]
    g_PR[jump]+=1
    for i in range(0,iteration):
        if flag>damp:
            index=random.randint(0,len(graph[jump])-1)
            jump=graph[jump][index]
        else:
            index=random.randint(0,len(vertexs)-1)
            jump=vertexs[index]
        g_PR[jump]+=1
    for key in list(g_PR.keys()):
        g_PR[key]=g_PR[key]/float(iteration)
        
    for item in g_PR.keys():
        f.write("The url is: "+item+" The page rank is: " + str(g_PR[item])+"\n")
    
def print_graph(g):
    f= open("question3c.txt","w+")
    f.write("---------------The graph-------------------\n")
    for item in g.keys():
        f.write(item+" = {")
        result=g[item]
        for i in range(len(result)):
            if i< len(result)-1:
                f.write(result[i]+", ")
            else:
                f.write(result[i])
        f.write("}\n")
    return f