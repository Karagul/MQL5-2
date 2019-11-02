from datetime import datetime
menor='2019.07.10 15:40:02'
datetime_object = datetime.strptime(menor, '%Y.%m.%d %H:%M:%S')
print(datetime_object)