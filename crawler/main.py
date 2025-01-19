import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from database import Database
import socket
from utils import Utils
import random
import time
import threading

MAX_THEADS = 7

def crawl(url: str, from_site_id: int|None, resume: bool = False):
    db = Database("data.db")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        # print(e)
        return
    
    soup = BeautifulSoup(response.text, "html.parser")

    domain = Utils.normalize_domain(url)
    normalized_url = Utils.normalize_url(url)
    pages = db.get_pages(url=normalized_url)
    sites = db.get_sites(domain=domain)
    if len(pages) > 0 and not resume:
        return
    
    
    if random.randint(0, 43) == 42:
        pages = db.get_pages()
        sites = db.get_sites()
        print(f"Pages: {len(pages)}, Sites: {len(sites)}")

    
    if len(sites) == 0:
        try:
            IP = socket.gethostbyname(domain)
        except:
            IP = -1
        db.new_site(domain=domain, IP=IP)
        sites = db.get_sites(domain=domain)

    site_id = sites[0][0]

    
    db.new_page(site_id, normalized_url)

    if from_site_id != None and site_id != from_site_id:    
        link = db.get_links(from_site_id=from_site_id, to_link_id=site_id)
        if len(link) == 0:
            db.new_link(from_site_id, site_id)

    print(f"{normalized_url}")
    

    for a in soup.find_all("a"):
        a_url = a.get("href")

        if a_url is None:
            continue

        if not a_url.startswith("http"):
            a_url = urljoin(url, a_url)

        normalized_url = Utils.normalize_url(a_url)
        pages = db.get_pages(url=normalized_url)

        if len(pages) == 0:
            if threading.active_count() < MAX_THEADS:
                time.sleep(random.randint(1, 3))
                threading.Thread(target=crawl, args=(a_url, site_id)).start()
            else:
                crawl(a_url, site_id)


if __name__ == "__main__":
    crawl("https://news.ycombinator.com/", None, os.path.isfile("data.db"))