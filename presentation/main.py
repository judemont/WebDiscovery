import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import igraph as ig
from database import Database
import matplotlib.pyplot as plt

db = Database("data.db")

sites = db.get_sites()
links = db.get_links()

g = ig.Graph(directed=True)
g.add_vertices(len(sites))

for i in range(len(sites)):
    g.vs[i]["name"] = sites[i][1]
    g.vs[i]['size'] = len(db.get_links(to_link_id=sites[i][0])) * 10

edges = []


for link in links:

    for y in range(len(sites)):
        if sites[y][0] == link[1]:
            site_from_index = y

        if sites[y][0] == link[2]:
            site_to_index = y


    
    edges.append((site_from_index, site_to_index))

g.add_edges(edges)
g.vs['label'] = g.vs['name']

 

fig, ax = plt.subplots()
ig.plot(
    g, 
    target=ax,
    vertex_size=g.vs["size"],
    vertex_label=g.vs['label'],
    vertex_color='orange',
    edge_color='black'
)
plt.show()
