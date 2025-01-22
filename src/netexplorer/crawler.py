import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
from .utils import Url, Database
import socket
import threading

class Crawler():
    """
    A web crawler class to recursively explore and store web pages.

    Initializes the Crawler with the given parameters.
    Parameters:
        entryUrl (str): The initial URL to start crawling from.
        maxSites (int|None): The maximum number of sites to crawl. If None, there is no limit.
        maxDepth (int|None): The maximum depth to crawl. If None, there is no limit.
        threads (int): The maximum number of threads to use for crawling.
        headers (dict): Headers to use for HTTP requests.
        dbPath (str): Path to the SQLite database file.
        resume (bool): Whether to resume from the existing database or start fresh.

    Methods:
        start():
            Starts the crawling process.
    """

    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    crawlI = 0

    def __init__(self, entryUrl: str, maxSites: int|None=None, maxDepth: int|None=None, threads: int=3, headers: dict=HEADERS, dbPath: str="database.db", resume: bool=False):
        self.entryUrl = entryUrl
        self.maxSites = maxSites
        self.maxDepth = maxDepth
        self.threads = threads
        self.headers = headers
        self.dbPath = dbPath
        self.resume = resume

    def start(self):
        """
        Starts the crawling process. If resume is False, it removes the existing database file.
        """
        if not self.resume:
            try:
                os.remove(self.dbPath)
            except:
                pass
        self.crawl()

    def crawl(self, url: str=None, from_site_id: int=None, depth: int=0):
        if self.maxSites is not None and self.crawlI >= self.maxSites:
            return

        db = Database(self.dbPath)

        if url is None:
            url = self.entryUrl

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            # print(e)
            return
        
        soup = BeautifulSoup(response.text, "html.parser")

        domain = Url.normalize_domain(url)
        normalized_url = Url.normalize_url(url)
        pages = db.get_pages(url=normalized_url)
        sites = db.get_sites(domain=domain)

        if len(pages) > 0:
            return
        
        newSite = len(sites) == 0
        if newSite:
            try:
                IP = socket.gethostbyname(domain)
            except:
                IP = -1
            db.new_site(domain=domain, IP=IP)
            sites = db.get_sites(domain=domain)

        site_id = sites[0][0]

        pages_ = db.get_pages(url=normalized_url)

        if len(pages_) == 0:
            db.new_page(site_id, normalized_url)

        if from_site_id != None and site_id != from_site_id:    
            link = db.get_links(from_site_id=from_site_id, to_link_id=site_id)
            if len(link) == 0:
                db.new_link(from_site_id, site_id)

        if self.maxSites is not None and self.crawlI >= self.maxSites:
                return
        self.crawlI += 1
        print(f"{self.crawlI} - CRAWLING : {normalized_url} - DEPTH : {depth}")
    
        if self.maxDepth is not None and depth >= self.maxDepth:
            return

        for a in soup.find_all("a"):
            a_url = a.get("href")

            if a_url is None:
                continue

            if not a_url.startswith("http"):
                a_url = urljoin(url, a_url)

            normalized_url = Url.normalize_url(a_url)
            pages = db.get_pages(url=normalized_url)

            if len(pages) == 0:
                if threading.active_count() < self.threads:
                    threading.Thread(target=self.crawl, args=(a_url, site_id, depth+ (1 if newSite else 0))).start()
                else:
                    self.crawl(a_url, site_id, depth+ (1 if newSite else 0))


