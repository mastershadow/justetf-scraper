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

            output = {
                'isin': isin
            }
            with open(AGGREGATED_DIR / f"{isin}.json", 'w') as f:
                json.dump(output, f, indent=2)
