import os

from dotenv import load_dotenv

load_dotenv()

authjwt_secret_key = os.getenv('authjwt_secret_key', default='fake-access-token')
