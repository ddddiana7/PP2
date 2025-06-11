from datetime import datetime, timedelta

import datetime

today = datetime.datetime.now()

yesterday = today - timedelta (days = 1)

tomorrow = today + timedelta (days = 1)

print (yesterday)
print (today)
print (tomorrow)