import datetime

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, TEXT, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import relationship
from sqlalchemy import *
from sqlalchemy.sql import select

# schema = "weatherdb"
schema = "test"




# inicjalizacja połaczenia z bazą danych
# engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/weatherdb', echo=False, pool_size=150)
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/test', echo=False, pool_size=150)
# obsluga zarządzania tabelami

insp = sqlalchemy.inspect(engine)
print(insp.has_table("Assignment", schema=schema))


Session = sessionmaker(bind=engine)
session = Session()


temperature = "temperature"
windSpeed = "windSpeed"
windDirection = "windDirection"
pressure = "pressure"


Base = declarative_base()
# metadata = MetaData(engine)
import enum
class Role(enum.Enum):
    Admin = 0
    Manager = 1
    Worker = 2

    @staticmethod
    def getRoleByString(role: str):
        if role == "admin":
            return Role.Admin
        elif role == "manager":
            return Role.Manager
        elif role == "worker":
            return Role.Worker
        else:
            return None



class User(Base):
    __tablename__ = "user"

    idUser = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    role = Column(Enum(Role))

    def toDictionary(self):
        return {"id":self.idUser, "login":self.login, "password":self.password, "role":str(self.role) }



class Station(Base):
    __tablename__ = "station"

    idStation = Column(Integer, primary_key=True)
    stationName = Column(Text)
    sensors = relationship("Sensor", cascade="all, delete")
    assignments = relationship("Assignment", cascade="all, delete")



class SensorType(enum.Enum):
    Temperature = 0
    WindSpeed = 1
    WindDirection = 2
    Pressure = 3

    @staticmethod
    def getMembers():
        return SensorType.Temperature,SensorType.WindSpeed,SensorType.WindDirection,SensorType.Pressure


class Sensor(Base):
    __tablename__ = "sensor"

    idSensor = Column(Integer, primary_key=True)
    coordinates = Column(String)
    type = Column(Enum(SensorType))
    stationId = Column(Integer, ForeignKey("station.idStation"))

    readings = relationship("Reading", cascade="all, delete")

    def __repr__(self):
        return "id: " + str(self.idSensor) + "; coordinates: " + self.coordinates + "; type: " + str(self.type) + "; stationId: " + str(self.stationId)

class Reading(Base):
    __tablename__ = "reading"

    idReading = Column(Integer, primary_key=True)
    sensorId = Column(Integer, ForeignKey("sensor.idSensor"))
    value = Column(Float)
    time = Column(DateTime)

class Diagnostician(Base):
    __tablename__ = "diagnostician"

    idDiagnostician = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    lastname = Column(VARCHAR)
    # code = Column(Integer)

    assignments = relationship("Assignment", cascade="all, delete")

    def toDict(self):
        # return {"idDiagnostician": self.idDiagnostician, "name": self.name, "lastname": self.lastname, "code":self.code}
        return {"idDiagnostician": self.idDiagnostician, "name": self.name, "lastname": self.lastname}


class Assignment(Base):
    __tablename__ = "assignment"

    diagnosticianId = Column(Integer, ForeignKey("diagnostician.idDiagnostician"), primary_key=True)
    stationId = Column(Integer, ForeignKey("station.idStation"), primary_key=True)



import random

# Session = sessionmaker(bind=engine)
# session = Session()

# session.close()

# session.add(Station(stationName="Gmund"))
#
# session.add(Sensor(coordinates="47°09'N, 11°41'E", type=SensorType.WindSpeed, stationId=1))
# session.add(Sensor(coordinates="47°09'N, 11°41'E", type=SensorType.WindDirection, stationId=1))
# session.add(Measurement(date=datetime.datetime(2021,month=11,day=11, hour=9), value=(random.randrange(9850, 10000) / 10)))
# session.add(Measurement(date=datetime.datetime(2021,month=11,day=11, hour=9), value=(random.randrange(10, 100) / 10)))
# session.add(Measurement(date=datetime.datetime(2021,month=11,day=11, hour=9), value=(random.randrange(0, 360))))
# def addSensors():
#     for station in session.query(Station):
#         session.add(Me)


'''
    doc = {"id": str(getNextId("weatherData")), "date": date, "hour": hour, "station_name": station,
                   "temperature": str(random.randrange(10, 40) / 10), "wind_speed": str(random.randrange(10, 100) / 10),
                   "wind_direction": str(random.randrange(0, 360)), "humidity": str(random.randrange(500, 1000) / 10),
                   "total_precipitation": str(random.randrange(0, 100) / 10),
                   "pressure": str(random.randrange(9850, 10000) / 10)}
'''


# for row in session.query(Station, Station.stationName).all():
#     print(row.Station, row.stationName)




# x = session.query(Sensor).get(9)
# # x.type = SensorType.WindSpeed
# session.commit()
# print(x, "hellloooooooooooo")




#
# session.delete(X)

# session.add(Station(stationName="Mayrhofen"))
# wysyła dane do bazy, session tylko śledzi zmiany
# session.commit()





# hintertux = session.query(Station).filter_by(idStation=1)
#
# for instance in session.query(Station):
#     print(instance.idStation, instance.stationName)


# print(hintertux)

def sensorExists(stationId: int, sensorType: SensorType):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    selectQuery = select(Sensor)
    result = session.execute(selectQuery)
    session.close()
    for row in result:
        # row to kolekcja
        sensor = row[0]
        if sensor.stationId == stationId or sensor.type == sensorType:
            return True
        # print(row[0].idSensor)
    return False



def getValidStations():
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # valid station has 4 sensors
    stations = {}
    selectQuery = select(Sensor)
    result = session.execute(selectQuery)
    for row in result:
        sensor = row[0]
        station = session.query(Station).get(sensor.stationId)
        if station in stations:
            stations[station] += 1
        else:
            stations[station] = 1
    validStations = []
    for key in stations.keys():
        if stations[key] == 4:
            validStations.append(key)
    # session.close()
    return validStations


def getStation(stationId: int):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    station = session.query(Station).get(stationId)
    # session.close()
    return station

print(getStation(100))



def deleteRecord(tableName, recordId):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    session.delete(session.query(tableName).get(recordId))
    session.commit()
    # session.close()


def addReading(stationId: int, time: datetime.datetime, temp: float, windSp: float, windDir: float, pres: float):

    stationSensors = sensorsFromStation(stationId)
    if len(stationSensors) != 4:
        return False

    tempSensorId = getSensor(SensorType.Temperature, stationSensors).idSensor
    windSpeedSensorId = getSensor(SensorType.WindSpeed, stationSensors).idSensor
    windDirectionSensorId = getSensor(SensorType.WindDirection, stationSensors).idSensor
    pressureSensorId = getSensor(SensorType.Pressure, stationSensors).idSensor

    sensors = (tempSensorId, windSpeedSensorId, windDirectionSensorId, pressureSensorId)
    sensorsValues = (temp, windSp, windDir, pres)

    # Session = sessionmaker(bind=engine)
    # session = Session()

    for i in range(len(sensorsValues)):
        session.add(Reading(sensorId=sensors[i], value=sensorsValues[i], time=time))
        session.commit()
    else:
        # session.close()
        return True

def addSensor(stationId: int, coordinates: str, sensorType:SensorType):
    # Session = sessionmaker(bind=engine)
    # session = Session()

    sensors = sensorsFromStation(stationId)
    sensorOfType = getSensor(sensorType, sensors)

    if sensorOfType is not None:
        # session.close()
        return False
    else:
        session.add(Sensor(coordinates=coordinates, type=sensorType, stationId=stationId))
        session.commit()
        # session.close()
        return True




# sensorExists(2, SensorType.WindSpeed)

def sensorsFromStation(stationId: int):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    selectQuery = select(Sensor)
    result = session.execute(selectQuery)
    sensors = []
    for row in result:
        if row[0].stationId == stationId:
            sensors.append(row[0])
    # session.close()
    return sensors

def getSensor(sensorType: SensorType, sensors):
    for sensor in sensors:
        if sensor.type == sensorType:
            return sensor
    return None



def userExists(login, password):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # check if login exists
    potentialUsers = list(session.query(User).filter_by(login=login))
    # session.close()

    if len(potentialUsers) > 0 and password == potentialUsers[0].password:
        return potentialUsers[0].role
    else:
        return None


def addUser(login, password, role: Role):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # check if login exists
    potentialUsers = list(session.query(User).filter_by(login=login))

    if potentialUsers:
        session.close()
        return False
    else:
        # dodajemy
        session.add(User(login=login, password=password, role=role))
        session.commit()
        # session.close()
        return True

def getUser(idUser):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    user = session.query(User).get(idUser)
    # session.close()
    return user

def getUsersAsDicts():
    # Session = sessionmaker(bind=engine)
    # session = Session()
    usersAsDicts = [user.toDictionary() for user in session.query(User)]
    # session.close()
    return usersAsDicts

def getUserAsDict(idUser: int):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    userAsDict = session.query(User).get(idUser).toDictionary()
    # session.close()
    return userAsDict

def updateUser(idUser: int, password, role):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    user = session.query(User).get(idUser)
    user.password = password
    user.role = role
    session.commit()
    # session.close()

def deleteUser(idUser, login):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    user = session.query(User).get(idUser)
    # session.close()
    if user.login == login:
        return False
    else:
        session.delete(user)
        session.commit()
        return True





def getWeatherData(stationId: int, time:datetime.datetime):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    allReadings = getReadings()
    stationSensors = sensorsFromStation(stationId)
    # session.close()
    sensorsIds = [x.idSensor for x in stationSensors]
    weatherData = {"stationId": stationId, "time":time}
    readings = []
    for reading in allReadings:
        if reading.sensorId in sensorsIds and reading.time == time:
            sensor = session.query(Sensor).get(reading.sensorId)
            readings.append(reading)
            if sensor.type == SensorType.Temperature:
                weatherData[temperature] = reading.value
            elif sensor.type == SensorType.WindSpeed:
                weatherData[windSpeed] = reading.value
            elif sensor.type == SensorType.WindDirection:
                weatherData[windDirection] = reading.value
            else:
                weatherData[pressure] = reading.value
    return weatherData, readings



def getReadings():
    # Session = sessionmaker(bind=engine)
    # session = Session()
    readings = session.query(Reading)
    # session.close()
    return readings





# addUser("","", Role.Admin)

# Session = sessionmaker(bind=engine)
# session = Session()
#
# x = session.query(User).get(1)
# session.delete(x)
#
# x = session.query(User).get(4)
# session.delete(x)
#
# x = session.query(User).get(5)
# session.delete(x)
#
#
#

#
# session.add(User(login="admin1", password="admin1", role=Role.Admin))
# session.add(User(login="kierownik1", password="kierownik1", role=Role.Manager))
# session.add(User(login="pracownik1", password="pracownik1", role=Role.Worker))
#
# session.commit()



""" Tutaj generujemy odczyty!"""

def generateData():
    # Session = sessionmaker(bind=engine)
    # session = Session()
    stations = session.query(Station)
    dates = [datetime.datetime(2021,11,11,hour=9), datetime.datetime(2021,11,11,hour=10), datetime.datetime(2021,11,11,hour=11)]
    for station in stations:
        sensors = sensorsFromStation(station.idStation)
        for date in dates:
            for sensor in sensors:
                if sensor.type == SensorType.Temperature:
                    session.add(Reading(sensorId=sensor.idSensor, value=(random.randrange(10, 40) / 10), time=date))
                elif sensor.type == SensorType.WindSpeed:
                    session.add(Reading(sensorId=sensor.idSensor, value=(random.randrange(10, 100) / 10), time=date))
                elif sensor.type == SensorType.WindDirection:
                    session.add(Reading(sensorId=sensor.idSensor, value=(random.randrange(0, 360)), time=date))
                else:
                    session.add(Reading(sensorId=sensor.idSensor, value=(random.randrange(9850, 10000) / 10), time=date))
    session.commit()

def generateSensors():
    # Session = sessionmaker(bind=engine)
    # session = Session()
    stations = session.query(Station)

    for station in stations:
        sensors = sensorsFromStation(station.idStation)
        if len(sensors) < 4:
            for sensorType in SensorType.getMembers():
                print(sensorType)
                addSensor(station.idStation, "47°09'N, 11°41'E", sensorType)




def getAllDateTimes():
    datetimes = []
    readings = getReadings()
    for reading in readings:
        if reading.time not in datetimes:
            datetimes.append(reading.time)
    return datetimes

# print(getAllDateTimes())

def getAllWeatherData():
    datetimes = getAllDateTimes()
    stations = getValidStations()
    weatherData = []
    for datetimeValue in datetimes:
        for station in stations:
            dateWeather = getWeatherData(station.idStation, datetimeValue)
            if dateWeather and len(dateWeather[0].keys()) > 2:
                weatherData.append(dateWeather[0])
    return weatherData



def changeStrToDatetime(time: str):
    date, hoursMinutesSeconds = time.split(" ")
    year, month, day = date.split("-")
    hour,_,_ = hoursMinutesSeconds.split(":")

    return datetime.datetime(int(year), int(month), int(day), int(hour))


def getReadingsFrom(stationId: int, time:datetime.datetime):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    readings = getReadings()
    sensorsIds = [x.idSensor for x in sensorsFromStation(stationId)]

    readingsToReturn = []
    for reading in readings:
        if reading.sensorId in sensorsIds and reading.time == time:
            readingsToReturn.append(reading)

    # session.close()
    return readingsToReturn



def deleteWeatherData(stationId: int, time:datetime.datetime):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    readings = getReadingsFrom(stationId, time)
    for reading in readings:
        session.delete(reading)
    else:
        session.commit()
        # session.close()
        return True

def updateWeather(stationId: int, time:datetime.datetime, temp, windSp, windDir, pres):
    sensors = sensorsFromStation(stationId)
    readings = getWeatherData(stationId, time)[1]

    for reading in readings:
        for sensor in sensors:
            if reading.sensorId == sensor.idSensor:
                if sensor.type == SensorType.Temperature:
                    reading.value = temp
                elif sensor.type == SensorType.WindSpeed:
                    reading.value =windSp
                elif sensor.type == SensorType.WindDirection:
                    reading.value =windDir
                else:
                    reading.value =pres
    else:
        session.commit()
        return True



def changeStrToFloat(value):
    if len(value) > 0:
        return float(value)
    else:
        return None


def getDiagnosticians():
    return session.query(Diagnostician)

def getDiagnosticiansAsDicts():
    return [x.toDict() for x in getDiagnosticians()]

def getDiagnosticianById(diagnosticianId: int):
    return session.query(Diagnostician).get(diagnosticianId)


def deleteDiagnostician(idDiagnostician: int):
    diagnostician = getDiagnosticianById(idDiagnostician)
    session.delete(diagnostician)
    session.commit()
    return True

def addDiagnostician(name: str, lastname: str):
    session.add(Diagnostician(name=name, lastname=lastname))
    session.commit()

def updateDiagnostician(diagId, name, lastname):
    diag = getDiagnosticianById(diagId)
    diag.name = name
    diag.lastname = lastname
    session.commit()



