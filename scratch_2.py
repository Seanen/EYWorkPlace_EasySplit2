import csv
from operator import itemgetter
import networkx as nx
from networkx.algorithms import community

with open('DET_Nodelist.csv', 'r') as nodecsv: # Open the file
    nodereader = csv.reader(nodecsv) # Read the csv
    # Retrieve the data (using Python list comprhension and list slicing to remove the header row, see footnote 3)
    nodes = [n for n in nodereader][1:]

node_names = [n[0] for n in nodes] # Get a list of only the node names

with open('DET_edgelist.csv', 'r') as edgecsv: # Open the file
    edgereader = csv.reader(edgecsv) # Read the csv
    edges = [tuple(e) for e in edgereader][1:] # Retrieve the data

print(node_names)
print(len(node_names))
print(edges)
print(len(edges))

G = nx.Graph()

G.add_nodes_from(node_names)
G.add_edges_from(edges)
print(nx.info(G))

id_dict = {}

for node in nodes: # Loop through the list, one row at a time
    id_dict[node[0]] = node[1]

nx.set_node_attributes(G, id_dict, 'sdfb_id')

density = nx.density(G)
print("Network density:", density)

Sean_Eureka_path = nx.shortest_path(G, source="Sean Huang", target="Gia")

print("Shortest path between Fell and Whitehead:", Sean_Eureka_path)

print("Length of that path:", len(Sean_Eureka_path)-1)

print(nx.is_connected(G))
components = nx.connected_components(G)
largest_component = max(components, key=len)

subgraph = G.subgraph(largest_component)
diameter = nx.diameter(subgraph)
print("Network diameter of largest component:", diameter)

triadic_closure = nx.transitivity(G)
print("Triadic closure:", triadic_closure)

degree_dict = dict(G.degree(G.nodes()))
nx.set_node_attributes(G, degree_dict, 'degree')

print(G.nodes['Sean Huang'])
print(G.nodes['Christina Tseng'])

sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)

print("Top 20 nodes by degree:")
for d in sorted_degree[:20]:
    print(d)

betweenness_dict = nx.betweenness_centrality(G) # Run betweenness centrality
eigenvector_dict = nx.eigenvector_centrality(G) # Run eigenvector centrality

# Assign each to an attribute in your network
nx.set_node_attributes(G, betweenness_dict, 'betweenness')
nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')

sorted_betweenness = sorted(betweenness_dict.items(), key=itemgetter(1), reverse=True)

print("Top 20 nodes by betweenness centrality:")
for b in sorted_betweenness[:20]:
    print(b)

#First get the top 20 nodes by betweenness as a list
top_betweenness = sorted_betweenness[:20]

#Then find and print their degree
for tb in top_betweenness: # Loop through top_betweenness
    degree = degree_dict[tb[0]] # Use degree_dict to access a node's degree, see footnote 2
    print("Name:", tb[0], "| Betweenness Centrality:", tb[1], "| Degree:", degree)

communities = community.greedy_modularity_communities(G)

modularity_dict = {} # Create a blank dictionary
for i,c in enumerate(communities): # Loop through the list of communities, keeping track of the number for the community
    for name in c: # Loop through each person in a community
        modularity_dict[name] = i # Create an entry in the dictionary for the person, where the value is which group they belong to.

# Now you can add modularity information like we did the other metrics
nx.set_node_attributes(G, modularity_dict, 'modularity')

nx.write_gexf(G, 'det_quaker_network.gexf')

from networkx.readwrite import json_graph
import json

data1 = json_graph.node_link_data(G)

# with open('personal.json', 'w') as json_file:
#     json.dump(data1, json_file)
json_dump = json.dumps(data1)
print(json_dump)

filename_out = 'pcap_export.json'
json_out = open(filename_out,'w')
json_out.write(json_dump)
json_out.close()


