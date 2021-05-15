import csv
import pandas as pd
import itertools
from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community.centrality import girvan_newman
import string
from os import path
import sys, os
frozen = 'not'
if getattr(sys, 'frozen', False):
        # we are running in a bundle
        frozen = 'ever so'
        bundle_dir = sys._MEIPASS
else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
print( 'we are',frozen,'frozen')
print( 'bundle dir is', bundle_dir )
print( 'sys.argv[0] is', sys.argv[0] )
print( 'sys.executable is', sys.executable )
print( 'os.getcwd is', os.getcwd() )

"""
https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python#fn:averagedegree

https://stackoverflow.com/questions/12977517/python-equivalent-of-d3-js

https://towardsdatascience.com/combining-python-and-d3-js-to-create-dynamic-visualization-applications-73c87a494396

https://pyinstaller.readthedocs.io/en/stable/runtime-information.html#using-file

https://github.com/brentvollebregt/auto-py-to-exe

"""

bundle_dir = path.abspath(os.path.dirname(sys.argv[0]))
path_to_dat = path.join(bundle_dir, 'Nodelist.csv')

print(path_to_dat)
# Open the file
# with open('Nodelist.csv', 'r') as nodecsv:
with open(path_to_dat, 'r') as nodecsv:
    # Read the csv
    nodereader = csv.reader(nodecsv)
    # Retrieve the data (using Python list comprhension and list slicing to remove the header row, see footnote 3)
    nodes = [n for n in nodereader][1:]

df = pd.read_csv(path_to_dat, encoding='utf-8')

# Get a list of only the node names
node_fakes = [n[1] for n in nodes]
node_names = [n[2] for n in nodes]

# print(node_fakes)
# print(node_names)
print(df)

total_c = df.count(axis='columns')[0]

edges = []
for i in range(3, total_c):
# for i in range(3, 4):
    print(i)
    coln = df.columns[i]
    print("-----------")
    a = df.iloc[:, [2, i]]
    b = a.loc[a[coln] == 'YES', :]
    print(b)
    c = list(b[b.columns[0]])
    print(c)
    d = list(itertools.combinations(c, 2))
    print(d)

    for i in d:
        print(i)
        edges.append(i)

print(node_names)
print(len(node_names))
print(edges)
print(len(edges))

G = nx.Graph()

G.add_nodes_from(node_names)
G.add_edges_from(edges)
# Average degree is the average number of connections of each node in your network.
# See more on degree in the centrality section of this tutorial
print(nx.info(G))

# A good metric to begin with is network density.
# This is simply the ratio of actual edges in the network to all possible edges in the network.
density = nx.density(G)
print("Network density:", density)

shortest = nx.shortest_path(G, source="Sean Huang", target="Gia")

print("Shortest path between Sean and Gia:", shortest)

components = nx.connected_components(G)
largest_component = max(components, key=len)
print(largest_component)
subgraph = G.subgraph(largest_component)
diameter = nx.diameter(subgraph)
print("Network diameter of largest component:", diameter)


# After getting some basic measures of the entire network structure, a good next step is to find which nodes are the most important ones in your network.
# In network analysis, measures of the importance of nodes are referred to as centrality measures.
# Degree is the simplest and the most common way of finding important nodes. A node’s degree is the sum of its edges. If a node has three lines extending from it to other nodes, its degree is three. Five edges, its degree is five. It’s really that simple. Since each of those edges will always have a node on the other end, you might think of degree as the number of people to which a given person is directly connected.
# The nodes with the highest degree in a social network are the people who know the most people. These nodes are often referred to as hubs, and calculating degree is the quickest way of identifying hubs.
degree_dict = dict(G.degree(G.nodes()))
nx.set_node_attributes(G, degree_dict, 'degree')
sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
print("Top 20 nodes by degree:")
for d in sorted_degree[:20]:
    print(d)

betweenness_dict = nx.betweenness_centrality(G) # Run betweenness centrality
eigenvector_dict = nx.eigenvector_centrality(G) # Run eigenvector centrality

# Assign each to an attribute in your network
nx.set_node_attributes(G, betweenness_dict, 'betweenness')
nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')

sorted_degree2 = sorted(betweenness_dict.items(), key=itemgetter(1), reverse=True)
print("Top 20 nodes by degree:")
for d in sorted_degree2[:20]:
    print(d)

sorted_degree3 = sorted(eigenvector_dict.items(), key=itemgetter(1), reverse=True)
print("Top 20 nodes by degree:")
for d in sorted_degree3[:20]:
    print(d)

for n in G.nodes(): # Loop through every node, in our data "n" will be the name of the person
    print(n, G.nodes[n])

# print(G.nodes['Christina Tseng'])
# print(G.nodes['Sean Huang'])
# print(G.nodes['Wei Bai'])
# print(G.nodes['Gia'])



nx.write_gexf(G, 'main_network.gexf')

nx.draw(G, with_labels=True)


##########

communities = girvan_newman(G)
node_groups = []
for com in next(communities):
  node_groups.append(list(com))

print(node_groups)

alphabet = list(string.ascii_uppercase)

grouplist = []
for i in list(df[df.columns[2]]):
    print(i)
    for g in range(len(node_groups)):
        print(alphabet[g])
        print('-------')
        print(node_groups[g])
        print(set([i]).issubset(node_groups[g]))
        if set([i]).issubset(node_groups[g]):
            grouplist.append(alphabet[g])

print(grouplist)
print(list(df[df.columns[2]]))
df['Group'] = grouplist

# bundle_dir = path.abspath(sys.argv[0])
bundle_dir = path.abspath(os.path.dirname(sys.argv[0]))
path_to_dat = path.join(bundle_dir, 'result.csv')
print(path_to_dat)
df.to_csv(path_to_dat, index=False)

# color_map = []
# for node in G:
#     if node in node_groups[0]:
#         color_map.append('blue')
#     else:
#         color_map.append('green')
# nx.draw(G, node_color=color_map, with_labels=True)
# plt.show()