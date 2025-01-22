import igraph as ig
from .utils import Database
import matplotlib.pyplot as plt

class SitesMap:
    """
    A class to visualize the map of sites and their links using a graph.

    Attributes:
        dbPath (str): Path to the SQLite database file.
        fixedPointsSize (bool): Whether to use a fixed size for points (nodes) in the graph.
        pointsSize (int): The size of the points (nodes) in the graph.
        edgesWidth (float): The width of the edges (links) in the graph.
        layout (str): The layout to use for the graph visualization.

    Methods:
        show():
            Displays the graph of sites and their links.
    """
    def __init__(self, dbPath: str="database.db", fixedPointsSize: bool=False, pointsSize: int=10, edgesWidth: float=0.4, layout: str="rt_circular"):
        self.dbPath = dbPath
        self.fixedPointsSize = fixedPointsSize
        self.pointsSize = pointsSize
        self.edgesWidth = edgesWidth
        self.layout = layout


    def show(self):
        db = Database(self.dbPath)
        sites = db.get_sites()
        links = db.get_links()

        g = ig.Graph(directed=True)
        g.add_vertices(len(sites))

        for i in range(len(sites)):
            g.vs[i]["name"] = sites[i][1]
            power = len(db.get_links(to_link_id=sites[i][0]))
            
            g.vs[i]['size'] = self.pointsSize if self.fixedPointsSize else power*self.pointsSize

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
            layout=self.layout,
            edge_width=self.edgesWidth,
            vertex_size=g.vs["size"],
            vertex_label=g.vs['label'],
            vertex_color='orange',
            edge_color='grey',
        )
        plt.show()



  