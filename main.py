import json

import pandas as pd
import requests_cache
from datetime import timedelta
from bs4 import BeautifulSoup
from settings import *

class Scrappy:
    def __init__(self):
        self.session = requests_cache.CachedSession('justetf_cache', backend='sqlite', expire_after=timedelta(hours=1))
        self.session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6825.154 Safari/537.36"

class EtfList(Scrappy):
    def __init__(self):
        super().__init__()
        self.url = "https://www.justetf.com/en/etf-list-overview.html"

    def run(self):
        scraped = []
        req = self.session.get(self.url)
        if req.status_code < 400:
            soup = BeautifulSoup(req.text, 'html.parser')
            blocks = soup.select("#etflist div[category-container]")

            for block in blocks:
                title = block.select_one("h3 span").text
                table_id = block.select_one("table[etf-data-table]").attrs["data-id"]
                code = ''.join(soup.select_one(f"#{table_id}").text.splitlines()[2:-1])
                extracted = f"[{code.split('[', 1)[1]}"[:-1]
                data = json.loads(extracted)
                for d in data:
                    d['category'] = title
                scraped = scraped + data
        with open(OUT_DIR / "etf_list.json", "w") as f:
            f.write(json.dumps(scraped, indent=2))
        df = pd.read_json(OUT_DIR / "etf_list.json")
        df.to_csv(OUT_DIR / "etf_list.csv")

if __name__ == "__main__":
    etf_list = EtfList()
    etf_list.run()