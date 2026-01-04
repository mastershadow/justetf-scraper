import json
import time
import random

from scrappy import Scrappy
from requests.exceptions import RequestException
from settings import *

class EtfDataFetcher(Scrappy):
    def __init__(self, fetch_all = False):
        super().__init__()
        self.isins = []
        self.URL_CARDS = "https://www.justetf.com/api/etfs/cards?locale=it&currency=EUR&isin="
        self.URL_QUOTE = "https://www.justetf.com/api/etfs/LU1287022708/quote?locale=en&currency=EUR&isin="
        self.URL_PERF = "https://www.justetf.com/api/etfs/___ISIN___/performance-chart?locale=en&currency=EUR&valuesType=MARKET_VALUE&reduceData=false&includeDividends=true&features=DIVIDENDS&dateFrom=___FROM___&dateTo=___TO___"

        if fetch_all:
            with open(OUT_DIR / 'etf_list.json', mode='r') as f:
                data = json.load(f)
                self.isins = [d['isin'] for d in data]
        else:
            if MY_ETF_LIST_FILE_PATH.exists() and MY_ETF_LIST_FILE_PATH.is_file():
                with open(MY_ETF_LIST_FILE_PATH, mode='r') as f:
                    for line in f.readlines():
                        isin = line.strip()
                        if SKIP_EXISTING:
                            if not (OUT_DIR / f'{isin}-data.json').exists() or not (OUT_DIR / f'{isin}-values.json').exists():
                                self.isins.append(isin)
                            else:
                                print(f"Skipping {isin} as it already has data.")
                        else:
                            self.isins.append(isin)
            else:
                print(f"No ETFs list found at {MY_ETF_LIST_FILE_PATH}.")

    def run(self):
        counter = 0
        errors = {}
        for isin in self.isins:
            if isin in errors and errors[isin] > MAX_RETRIES:
                print(f"Skipping {isin} which is having too many errors.")
                continue

            if counter > 0 and counter % PAUSE_AFTER_ETFS == 0:
                print(f"Pausing for {PAUSE_TIME} seconds...")
                time.sleep(PAUSE_TIME)
            counter += 1

            try:
                print(f"Fetching data for {isin}: Data...", end='')
                req = self.session.get(self.URL_CARDS + isin)
                if req.status_code >= 400:
                    print("Error!")
                    continue
                time.sleep(SLEEP_TIME)

                cards = req.json()
                etf_data = cards['etfs'][0]
                with open(OUT_DIR / f'{isin}-data.json', mode='w') as f:
                    json.dump(etf_data, f)

                print("Values...", end='')
                first_quote_date = etf_data['firstQuoteDate']
                latest_quote_date = etf_data['latestQuoteDate']
                values_url = (self.URL_PERF
                              .replace("___ISIN___", isin)
                              .replace("___FROM___", first_quote_date)
                              .replace("___TO___", latest_quote_date))
                req = self.session.get(values_url)
                if req.status_code >= 400:
                    print("Error!")
                    continue
                values_data = req.json()
                with open(OUT_DIR / f'{isin}-values.json', mode='w') as f:
                    json.dump(values_data, f)
                print("Done!")
                time.sleep(SLEEP_TIME * random.uniform(1, 3))
            except RequestException as e:
                print("Error", e)
                # add back to queue
                self.isins.append(isin)
                # increase error counter
                if isin not in errors:
                    errors[isin] = 0
                errors[isin] += 1
