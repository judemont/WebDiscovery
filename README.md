# NetExplorer

> __*Web analysis tool*__
---

![image](https://github.com/user-attachments/assets/6a35de5a-5f75-4959-8096-a192b404caf1)

## Installation :
```shell
pip install netexplorer
```

## Examples :
```python
from netexplorer import Crawler, SitesMap

crawler = Crawler("https://futureofthe.tech", maxSites=300, maxDepth=2, threads=5)
crawler.start()

sitesMap = SitesMap()
sitesMap.show()
```
### Example result :
![Screenshot From 2025-01-22 09-31-41](https://github.com/user-attachments/assets/b244ba06-37d1-4b40-9a2b-4ed7d5f11d35)

## Documentation :
### Crawler :
A web crawler class to recursively explore and store web pages.

**Parameters:**
- `entryUrl` (str): The initial URL to start crawling from.
- `maxSites` (int|None): The maximum number of sites to crawl. If None, there is no limit.
- `maxDepth` (int|None): The maximum depth to crawl. If None, there is no limit.
- `threads` (int): The maximum number of threads to use for crawling.
- `headers` (dict): Headers to use for HTTP requests.
- `dbPath` (str): Path to the SQLite database file.
- `resume` (bool): Whether to resume from the existing database or start fresh.

**Methods:**
- `start()`: Starts the crawling process.

### SitesMap :
A class to visualize the map of sites and their links using a graph.

**Attributes:**
- `dbPath` (str): Path to the SQLite database file.
- `fixedPointsSize` (bool): Whether to use a fixed size for points (nodes) in the graph.
- `pointsSize` (int): The size of the points (nodes) in the graph.
- `edgesWidth` (float): The width of the edges (links) in the graph.
- `layout` (str): The layout to use for the graph visualization.

**Methods:**
- `show()`: Displays the graph of sites and their links.
