import json
import os

from settings import *

class EtfDataProcessor:
    def run(self):
        # collect
        files = [f
                 for f in os.listdir(ETFS_OUT_DIR)
                 if os.path.isfile(ETFS_OUT_DIR / f) and (ETFS_OUT_DIR / f).suffix == '.json']
        groups = {}
        for f in files:
            isin, rest = f.split('-')
            if isin not in groups:
                groups[isin] = []
            groups[isin].append(f)
        # avoid incomplete data
        groups = { k: v for k, v in groups.items() if len(v) == 2 }

        for isin, isin_files in groups.items():
            print(f"Processing {isin}...")
            data_file, values_file = sorted(isin_files)
            with open(ETFS_OUT_DIR / data_file, 'r') as f:
                data = json.load(f)
            with open(ETFS_OUT_DIR / values_file, 'r') as f:
                values = json.load(f)

            if not data['active']:
                print(f"Skipping {isin} as active is false...")
                continue

            output = {
                'isin': isin,
                'name': data['name'],
                'ter': data['ter']['raw'],
                'quote': data['quote']['raw'],
                'latestQuote': data['latestQuote']['raw'],
                'latestQuoteDate': data['latestQuoteDate'],
                'previousQuoteDate': data['previousQuoteDate'],
                'firstQuoteDate': data['firstQuoteDate'],
                'returns': data['returns']['raw'] if 'returns' in data and data['returns'] is not None else None,
                'fundSize': data['fundSize']['raw'] if 'fundSize' in data and data['fundSize'] is not None else None,
                'url': f"https://www.justetf.com/it/etf-profile.html?isin={isin}",
                'values' : [[v['date'], v['value']['raw']] for v in values['series']]
            }

            with open(AGGREGATED_DIR / f"{isin}.json", 'w') as f:
                json.dump(output, f, indent=2)
