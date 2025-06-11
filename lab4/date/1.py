from datetime import datetime, timedelta
import datetime

today = datetime.datetime.now()

result = today- timedelta(days = 5)

print(result)

