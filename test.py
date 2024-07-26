import datetime

d1 = datetime.datetime.strptime("2028-12-29", '%Y-%m-%d').date()
d2 = datetime.date.today()
dateList = [d1, d2]
dateList.sort()

print(dateList)
