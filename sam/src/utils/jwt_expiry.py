from dotenv import load_dotenv
import os
load_dotenv()

from datetime import timedelta, timezone, datetime

ACCESS_TOKEN_EXPIRY = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
TIMEDELTA_REFRESH = timedelta(seconds=  round(int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))/2) )
