import datetime

d1 = datetime.datetime.strptime("2024-12-29", '%Y-%m-%d').date()
d2 = datetime.date.today()
print(d1>d2)
print(d2)
