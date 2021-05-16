"""
https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python#fn:averagedegree

https://stackoverflow.com/questions/12977517/python-equivalent-of-d3-js

https://towardsdatascience.com/combining-python-and-d3-js-to-create-dynamic-visualization-applications-73c87a494396

https://pyinstaller.readthedocs.io/en/stable/runtime-information.html#using-file

https://github.com/brentvollebregt/auto-py-to-exe

"""

import csv
import sys,os
import string
import itertools
from os import path
import pandas as pd
from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community.centrality import girvan_newman

frozen = 'not'

# we are running in a bundle
if getattr(sys, 'frozen', False):
        frozen = 'ever so'
        bundle_dir = sys._MEIPASS
        # bundle_dir = path.abspath(os.path.dirname(sys.argv[0]))

# we are running in a normal Python environment
else:
        bundle_dir = path.abspath(os.path.dirname(os.path.abspath(__file__)))

path_to_dat = path.join(bundle_dir, 'Nodelist.csv')
path_to_gephi = path.join(bundle_dir, 'Gephi_Network.gexf')
path_to_result = path.join(bundle_dir, 'result.csv')
path_to_png = path.join(bundle_dir, 'network1.png')
path_to_png2 = path.join(bundle_dir, 'network2.png')

print('-------------------------------------')
print('we are', frozen, 'frozen')
print('bundle dir is ', bundle_dir)
print('sys.argv[0] is ', sys.argv[0])
print('sys.executable is ', sys.executable)
print('os.getcwd is ', os.getcwd())
print('Path to file is ', path_to_dat)
print('Path to Gephi is ', path_to_gephi)
print('Path to Result is ', path_to_result)
print('Path to Png is ', path_to_png)
print('-------------------------------------')

# Open the file
with open(path_to_dat, 'r') as nodecsv:
    # Read the csv
    nodereader = csv.reader(nodecsv)
    # Retrieve the data (using Python list comprhension and list slicing to remove the header row, see footnote 3)
    nodes = [n for n in nodereader][1:]

df_raw = pd.read_csv(path_to_dat, encoding='utf-8')

# Get a list of only the node names
node_fakes = [n[1] for n in nodes]
node_names = [n[2] for n in nodes]

print(df_raw)

edges = []
def calculate_edge(df):
    total_c = df.count(axis='columns')[0]
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

calculate_edge(df_raw)

print(node_names)
print(len(node_names))
print(edges)
print(len(edges))

G = nx.Graph()
def run_networkx(G):
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

    # After getting some basic measures of the entire network structure,
    # a good next step is to find which nodes are the most important ones in your network.
    # In network analysis, measures of the importance of nodes are referred to as centrality measures.
    # Degree is the simplest and the most common way of finding important nodes.
    # A node’s degree is the sum of its edges. If a node has three lines extending from it to other nodes,
    # its degree is three.
    # Five edges, its degree is five. It’s really that simple.
    # Since each of those edges will always have a node on the other end,
    # you might think of degree as the number of people to which a given person is directly connected.
    # The nodes with the highest degree in a social network are the people who know the most people.
    # These nodes are often referred to as hubs, and calculating degree is the quickest way of identifying hubs.
    degree_dict = dict(G.degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict, 'degree')
    sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)

    df_raw['Degree'] = ""
    print("Top 30 nodes by degree:")
    for d in sorted_degree[:30]:
        print(d)
        df_raw.loc[df_raw['Name'] == d[0], 'Degree'] = d[1]

    print(df_raw[['Name','Degree']])

run_networkx(G)

def run_other_Degree(G):
    betweenness_dict = nx.betweenness_centrality(G) # Run betweenness centrality
    eigenvector_dict = nx.eigenvector_centrality(G) # Run eigenvector centrality

    # Assign each to an attribute in your network
    nx.set_node_attributes(G, betweenness_dict, 'betweenness')
    nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')

    sorted_degree2 = sorted(betweenness_dict.items(), key=itemgetter(1), reverse=True)
    print("Top 30 nodes by between degree:")
    # dg = []
    for d in sorted_degree2[:30]:
        print(d)
        # df.append(d)

    sorted_degree3 = sorted(eigenvector_dict.items(), key=itemgetter(1), reverse=True)
    print("Top 30 nodes by eigenvector degree:")

    for d in sorted_degree3[:30]:
        print(d)

run_other_Degree(G)


# Loop through every node, in our data "n" will be the name of the person
for n in G.nodes():
    print(n, G.nodes[n])
    # print(G.nodes['Christina Tseng'])
    # print(G.nodes['Sean Huang'])
    # print(G.nodes['Wei Bai'])
    # print(G.nodes['Gia'])

def run_graph(G):
    # First draw for Gephi
    nx.write_gexf(G, path_to_gephi)

    # Second draw for png
    nx.draw(G, with_labels=True)
    plt.savefig(path_to_png)
    plt.close()

    # Third draw
    nx.draw_spring(G, with_labels=True)
    plt.savefig(path_to_png2)
    plt.close()

run_graph(G)

def run_Girvan(df):
    # Girvan Newman
    communities = girvan_newman(G)
    node_groups = []
    for com in next(communities):
      node_groups.append(list(com))

    print('This is node group ', node_groups)

    # alphabet = list(string.ascii_uppercase)
    My_list = [*range(1, 21, 1)]
    grouplist = []
    for i in list(df[df.columns[2]]):
        print(i)
        for g in range(len(node_groups)):
            print(My_list[g])
            print('-------')
            print(node_groups[g])
            print(set([i]).issubset(node_groups[g]))
            if set([i]).issubset(node_groups[g]):
                grouplist.append(My_list[g])

    print(grouplist)
    print(list(df[df.columns[2]]))
    df['Group'] = grouplist

run_Girvan(df_raw)
df_raw.to_csv(path_to_result, index=False)

print(df_raw['Group'].unique())

le = len(list(df_raw['Group'].unique()))

for i in range(1, le + 1):
    print(i)
    temp_d = df_raw[df_raw['Group'] == i]
    print(temp_d)
    print(len(temp_d.columns))
    temp = temp_d.iloc[:, :-2]

    temp_node_names = temp['Name'].tolist()

    temp_edges = []
    total_c = len(temp.columns)
    for i in range(3, total_c):
        # for i in range(3, 4):
        print(i)
        coln = temp.columns[i]
        print("-----------")
        a = temp.iloc[:, [2, i]]
        b = a.loc[a[coln] == 'YES', :]
        print(b)
        c = list(b[b.columns[0]])
        print(c)
        d = list(itertools.combinations(c, 2))
        print(d)
        for i in d:
            print(i)
            temp_edges.append(i)

        print(temp_node_names)
        print(len(temp_node_names))
        print(temp_edges)
        print(len(temp_edges))

    G = nx.Graph()
    G.add_nodes_from(temp_node_names)
    G.add_edges_from(temp_edges)
    # Average degree is the average number of connections of each node in your network.
    # See more on degree in the centrality section of this tutorial
    print(nx.info(G))

    betweenness_dict = nx.betweenness_centrality(G)  # Run betweenness centrality
    eigenvector_dict = nx.eigenvector_centrality(G)  # Run eigenvector centrality

    # Assign each to an attribute in your network
    nx.set_node_attributes(G, betweenness_dict, 'betweenness')
    nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')

    sorted_degree2 = sorted(betweenness_dict.items(), key=itemgetter(1), reverse=True)
    print("Top 30 nodes by between degree:")
    # dg = []
    for d in sorted_degree2[:30]:
        print(d)
        # df.append(d)

    sorted_degree3 = sorted(eigenvector_dict.items(), key=itemgetter(1), reverse=True)
    print("Top 30 nodes by eigenvector degree:")

    for d in sorted_degree3[:30]:
        print(d)