# import enum
#
# import mysql.connector
#
# from sqlalchemy import *
#
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root"
# )
#
# print(mydb.user)
#
# engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/weatherdb', echo=True)
#
# role = None
#
# if role:
#     print("henlo")
# else:
#     print("not henlo")
#
#
#
# class MyEnum(enum.Enum):
#     HELL = 0
#     HEAVEN = 1
#
#
# for enum in MyEnum:
#     print(enum)
import datetime

d1 = datetime.datetime(2000,10,16,5)
d2 = datetime.datetime(2000,10,16,6)

print(str(d1))

def changeStrToDatetime(time: str):
    date, hoursMinutesSeconds = time.split(" ")
    year, month, day = date.split("-")
    hour,_,_ = hoursMinutesSeconds.split(":")

    return datetime.datetime(int(year), int(month), int(day), int(hour))

print(changeStrToDatetime("2000-20-16 05:0:0"))
