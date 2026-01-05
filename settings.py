import pathlib

MY_ETF_LIST_FILE = 'my-etf-list.txt'
FETCH_LIST = False

FETCH_ETFS_DATA = False
FETCH_ALL_ETFS_DATA = False

PROCESS_ETFS_DATA = True

BASE_DIR = pathlib.Path(__file__).parent.absolute()
DATA_DIR = BASE_DIR / 'data'
OUT_DIR = BASE_DIR / 'out'
ETFS_OUT_DIR = OUT_DIR / 'etfs'
AGGREGATED_DIR = OUT_DIR / 'aggregated'

MY_ETF_LIST_FILE_PATH = DATA_DIR / MY_ETF_LIST_FILE
SKIP_EXISTING = True
MAX_RETRIES = 3
SLEEP_TIME = 1
PAUSE_AFTER_ETFS = 6
PAUSE_TIME = 15
