from datetime import timedelta

import requests_cache


class Scrappy:
    def __init__(self):
        self.session = requests_cache.CachedSession('justetf_cache', backend='sqlite', expire_after=timedelta(hours=1))
        self.session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6825.154 Safari/537.36"
