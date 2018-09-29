from pathlib import Path


SYNC_INTERVEL = 600
LOG_FLODER = 'log'
DATABASE_FOLDER = "database"
DATABASE_PATH = Path(DATABASE_FOLDER, 'library_monitor.db')
DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
TARGET_STATE = '在架可借'
BOT_TOKEN = '12345678:abc'
NOTICE_COUNTER = 3
BOT_ALL_BURST_LIMIT = 15
BOT_GROUP_BURST_LIMIT = 10
PROXY_URL = 'socks5://127.0.0.1:1080' # str or None
BOOK_PAGE_REFERER = 'http://opac.bupt.edu.cn:8080/opac_two/search2/s_detail.jsp?sid={book_id}'
BOOK_STATE_API = 'http://opac.bupt.edu.cn:8080/opac_two/guancang.do'
MESSAGE_TEMPLATE = '图书到馆：`{book_location}`等可借出`{book_counter}`本《{book_name}》({book_id})。'
