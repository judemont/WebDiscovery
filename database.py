import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS sites (id INTEGER PRIMARY KEY, domain TEXT, IP TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS pages (id INTEGER PRIMARY KEY, domain_id INTEGER, url TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY, from_site_id INTEGER, to_link_id INTEGER)")

        self.conn.commit()

    def new_site(self, domain: str, IP: str):
        self.cur.execute("INSERT INTO sites (domain, IP) VALUES (?, ?)", (domain, IP))
        self.conn.commit()
    
    def new_link(self, from_site_id: int, to_link_id: int):
        self.cur.execute("INSERT INTO links (from_site_id, to_link_id) VALUES (?, ?)", (from_site_id, to_link_id))
        self.conn.commit()

    def new_page(self, domain_id: int, url: str):
        self.cur.execute("INSERT INTO pages (domain_id, url) VALUES (?, ?)", (domain_id, url))
        self.conn.commit()

    def get_sites(self, domain:str=None, IP:str=None, id:int=None):
        if id is not None:
            self.cur.execute("SELECT * FROM sites WHERE id=?", (id))

        elif IP is not None:
            self.cur.execute("SELECT * FROM sites WHERE ip=?", (IP))

        elif domain is not None:
            self.cur.execute("SELECT * FROM sites WHERE domain=?", (domain,))
        
        else:
            self.cur.execute("SELECT * FROM sites")
            
        return self.cur.fetchall()
    


    def get_links(self, from_site_id:int=None, to_link_id:int=None, id:int=None):
        if id is not None:
            self.cur.execute("SELECT * FROM links WHERE id=?", (id,))
        elif to_link_id is not None and from_site_id is not None:
            self.cur.execute("SELECT * FROM links WHERE from_site_id=? AND to_link_id=?", (from_site_id, to_link_id))
        elif to_link_id is not None:
            self.cur.execute("SELECT * FROM links WHERE to_link_id=?", (to_link_id,))

        elif from_site_id is not None:
            self.cur.execute("SELECT * FROM links WHERE from_site_id=?", (from_site_id,))

        else:
            self.cur.execute("SELECT * FROM links")
        return self.cur.fetchall()

    

    def get_pages(self, domain_id:int=None, url:str=None, id:int=None):
        if id is not None:
            self.cur.execute("SELECT * FROM pages WHERE id=?", (id,))

        elif url is not None:
            self.cur.execute("SELECT * FROM pages WHERE url=?", (url,))

        elif domain_id is not None:
            self.cur.execute("SELECT * FROM pages WHERE domain_id=?", (domain_id,))

        else:
            self.cur.execute("SELECT * FROM pages")

        return self.cur.fetchall()

    


    def __del__(self):
        self.conn.close()