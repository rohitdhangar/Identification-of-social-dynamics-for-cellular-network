import networkx as nx
import matplotlib.pyplot as plt
import math,random
import collections


#Generation of random graph with 50 nodes and probability of 0.1 having edge between two nodes
G=nx.gnp_random_graph(50,0.1)


#Assigning viewing probability to each node
for n in range(0, 50):
    G.node[n]['Pview']=random.random()


#Assigning sharing probability to each node
for n in range(0, 50):
    G.node[n]['Pshare']=random.random()

#printing both probabilities
print nx.get_node_attributes(G,'Pview')
print nx.get_node_attributes(G,'Pshare')


#drawing above constructed graph
nx.draw(G, with_labels=True)
plt.show()


#DFS algo for single source node
def dfs_tree(G, source):
     
    T = nx.DiGraph()
    if (G.node[source]['Pview']<0.30 or G.node[source]['Pshare']<0.20):#Checking condition for source node
        return 
    else:
        T.add_node(source)
    T.add_edges_from(dfs_edges(G,source))
    return T


def dfs_edges(G, source=None):

    
    if source is None:
          nodes = G
    else:
        nodes = [source]
    visited=set()
    for start in nodes:
        if start in visited:
            continue
        visited.add(start)
        stack = [(start,iter(G[start]))]
        while stack:
            parent,children = stack[-1]
            try:
                child = next(children)
                if child not in visited and (G.node[child]['Pview']>0.30 and G.node[child]['Pshare']>0.20):#Adding child to dfs tree     only if viewing and sharing probability is greater than threshold
                    yield parent,child
                    visited.add(child)
                    stack.append((child,iter(G[child])))
            except StopIteration:
                stack.pop()

#myList holds all the DFS trees
myList=[]
for i in range(10): #taking 10 random source nodes
    n=random.randint(1, 49)
    myList.append(dfs_tree(G, n))
    if myList[i] is None: #if source node does not meet the threshold
       print "Empty tree"
    else:
       nx.draw(myList[i], with_labels=True)#printing generated dfs tree
       plt.show()


edgelist=[]#Edgelist holds all the edges of all the trees
for i in range(10):
    if myList[i] is None:#if tree is empty
       continue
    else:
       edgelist.extend(nx.edges(myList[i]))#Adds edges of tree to edgelist

print edgelist

print"**************************"
counter=collections.Counter(edgelist)#Extracting frequencies of each edge
print(counter)

#Creating new inference graph by combing all trees
K=nx.Graph()
K.add_edges_from(edgelist)
nx.draw(K, with_labels=True)
plt.show()


      


