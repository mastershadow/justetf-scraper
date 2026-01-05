from etf_data import EtfDataFetcher
from etf_data_processor import EtfDataProcessor
from etf_list import EtfList
from settings import *

if __name__ == "__main__":
    if FETCH_LIST:
        print("Fetching latest ETF list...")
        etf_list = EtfList()
        etf_list.run()
    if FETCH_ETFS_DATA:
        print("Fetching latest ETFs data...")
        edf = EtfDataFetcher(FETCH_ALL_ETFS_DATA)
        edf.run()
    if PROCESS_ETFS_DATA:
        processor = EtfDataProcessor()
        processor.run()
