import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import igraph as ig
from database import Database
import matplotlib.pyplot as plt

FIXED_EDGES_SIZE = True
SHOW_EDGES = True


db = Database("data.db")

sites = db.get_sites()
links = db.get_links()

g = ig.Graph(directed=True)
g.add_vertices(len(sites))

for i in range(len(sites)):
    g.vs[i]["name"] = sites[i][1]
    power = len(db.get_links(to_link_id=sites[i][0]))
    
    g.vs[i]['size'] = 10 if FIXED_EDGES_SIZE else power*10

edges = []

if SHOW_EDGES:
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
    layout="dh",
    edge_width=0.4,
    vertex_size=g.vs["size"],
    vertex_label=g.vs['label'],
    vertex_color='orange',
    edge_color='grey',
)
plt.show()
