import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL')
S2_URL = os.getenv('S2_URL')
S2_LOGIN = os.getenv('S2_LOGIN')
S2_PASSWORD = os.getenv('S2_PASSWORD')
TIMEOUT = int(os.getenv('TIMEOUT', 5))
THREADS = int(os.getenv('THREADS', 1))