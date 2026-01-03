import pathlib

MY_ETF_LIST_FILE = 'my-etf-list.txt'
FETCH_LIST = False
FETCH_ETFS_DATA = True
FETCH_ALL_ETFS_DATA = False
PROCESS_ETFS_DATA = False

BASE_DIR = pathlib.Path(__file__).parent.absolute()
DATA_DIR = BASE_DIR / 'data'
OUT_DIR = BASE_DIR / 'out'
MY_ETF_LIST_FILE_PATH = DATA_DIR / MY_ETF_LIST_FILE
SLEEP_TIME = 1
PAUSE_AFTER_ETFS = 10
PAUSE_TIME = 10
