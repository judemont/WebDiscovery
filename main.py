import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from database import Database
import socket
from utils import Utils
import random

db = Database("data.db")


def crawl(url: str, from_site_id: int|None,):
    try:
        response = requests.get(url)
    except:
        return
    
    soup = BeautifulSoup(response.text, "html.parser")

    parsed_url = urlparse(url)
    domain = Utils.normalize_domain(url)
    normalized_url = Utils.normalize_url(url)
    pages = db.get_pages(url=normalized_url)
    sites = db.get_sites(domain=domain)

    if len(pages) > 0:
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
        normalized_url = Utils.normalize_url(a_url)
        pages = db.get_pages(url=normalized_url)

        if len(pages) == 0:
            crawl(a_url, site_id)




crawl("https://github.com/judemont", None)