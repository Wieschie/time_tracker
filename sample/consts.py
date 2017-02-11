from datetime import datetime

""" method used to log events:
    sheets
    txt
    sqlite
"""
RECORD_METHOD = 'sheets'

""" google sheets config """
# actual time sheet
ID = '1abkU6C-H3pUg6CNdNTEHYnXXwfsSE7wPScJs0N2PpJc'

# columns to be edited on google sheet
RANGE = 'experimental!A:B'

# app name is for the sheets api
APP_NAME = 'python_time_tracker'

# used for calculating time differences with deltas
DT_ZERO = datetime(1970, 1, 1)

