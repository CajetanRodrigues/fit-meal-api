import datetime
import pytz

# datetime object with timezone awareness:
print(datetime.datetime.now(tz=pytz.utc))
timestamp = str(datetime.datetime.now(tz=pytz.utc))
print(timestamp[0:11])
print(timestamp[11:26])
print(timestamp[27:33])