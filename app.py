import re

from flask import Flask
from flask import *
from tables import *

app = Flask(__name__)

admin = "admin"
manager = "manager"
worker = "worker"

currentUserRole = ""
currentUserLogin = ""

weatherParameters = ["stationId", "time", "temperature", "windSpeed", "windDirection", "pressure"]


@app.route('/')
def home():  # put application's code here
    return render_template("login.html")

@app.route('/adminPage')
def adminPage():
    documents = getUsersAsDicts()
    documents.reverse()
    return render_template("adminPage.html", modifying=True, allDocuments=documents, role=currentUserRole)



@app.route('/workerPage')
def workerPage():
    # doc = pop3FirstItems(weatherDataParameters)
    documents = getAllWeatherData()
    documents.reverse()
    return render_template("workerPage.html", allDocuments=documents)


@app.route('/managerPage')
def managerPage():
    # doc = pop3FirstItems(weatherDataParameters)
    documents = getAllWeatherData()
    documents.reverse()
    return render_template("managerPage.html", allDocuments=documents, role=manager, modifying=True)



@app.route('/addUserPage')
def addUserPage():
    return render_template("addUserPage.html")

@app.route('/editPage', methods=['GET', 'POST'])
def editPage():
    if request.method == 'POST':
        if currentUserRole == admin:
            userID = int(request.form["id"])
            return render_template("editPageAdmin.html", data=getUserAsDict(userID))
        else:
            stationID = int(request.form["station"])
            print(request.form["time"])
            time = changeStrToDatetime(request.form["time"])
            doc = getWeatherData(stationID, time)[0]
            return render_template("editPageManager.html", data=doc, manager=True)







@app.route('/login', methods=['GET', 'POST'])
def loginAction():
    global currentUserLogin, currentUserRole
    if request.method == 'POST':
        login = request.form["login"]
        password = request.form["password"]
        role = userExists(login, password)
        if role:
            currentUserLogin = login
            if role == Role.Admin:
                currentUserRole = admin
                return redirect(url_for("adminPage"))
            elif role == Role.Manager:
                currentUserRole = manager
                return redirect(url_for("managerOptionsPage"))
                # return redirect(url_for("managerPage"))
            else:
                currentUserRole = worker
                return redirect(url_for("workerPage"))
        else:
            return render_template("login.html", error="Spróbuj ponownie!")


@app.route('/addNewUser', methods=['GET', 'POST'])
def addNewUser():
    if request.method == 'POST':
        login = request.form["newUserLogin"]
        password = request.form["newUserPassword"]
        role = Role.getRoleByString(request.form["role"])
        if addUser(login, password, role):
            return render_template("addUserPage.html", result="Użytkownik został dodany!")
        else:
            return render_template("addUserPage.html", result="Login musi być unikalny!")

@app.route('/updateUserAction', methods=['GET', 'POST'])
def updateUserAction():
    if request.method == 'POST':
        idUser = int(request.form["id"])
        login = request.form["login"]
        password = request.form["password"]
        role = request.form["role"]

        if currentUserLogin == login:
            user = getUser(idUser)
            if Role.getRoleByString(role) != user.role:
                return render_template("editPageAdmin.html", data=request.form, result="Nie udało się zaktualizować danych!")
            else:
                updateUser(idUser, password, role)
                return render_template("editPageAdmin.html", data=request.form, result="Pomyślnie zaktualizowano dane!")
        else:
            updateUser(idUser, password, role)
            return render_template("editPageAdmin.html", data=request.form, result="Pomyślnie zaktualizowano dane!")

@app.route('/deletePosition', methods=['GET', 'POST'])
def deletePosition():
    if request.method == 'POST':
        if currentUserRole == admin:
            user = getUser(int(request.form["id"]))
            if deleteUser(user.idUser, currentUserLogin):
                return render_template("adminPage.html", modifying=True,
                                       allDocuments=getUsersAsDicts(), role=currentUserRole,
                                       result="Usunięcie powiodło się!")
            else:
                return render_template("adminPage.html", modifying=True,
                                       allDocuments=getUsersAsDicts(), role=currentUserRole,
                                       result="Usunięcie nie powiodło się!")
        else:
            stationId = request.form["stationId"]
            time = changeStrToDatetime(request.form["time"])
            if deleteWeatherData(int(stationId), time):
                return render_template("managerPage.html", modifying=True,
                                       allDocuments=getAllWeatherData(), role=currentUserRole,
                                       result="Usunięcie powiodło się!")
            else:
                return render_template("managerPage.html", modifying=True,
                                       allDocuments=getAllWeatherData(), role=currentUserRole,
                                       result="Usunięcie nie powiodło się!")



@app.route('/addWeatherPage')
def addWeatherPage():
    return render_template("addWeatherPage.html", weatherParameters=weatherParameters)

@app.route('/addWeatherAction', methods=["GET", "POST"])
def addWeatherAction():
    if request.method == "POST":
        stationId = int(request.form["stationId"])
        time = request.form["time"]+ ":00:00"
        print(bool(re.match("\d{4}-\d{2}-\d{2} \d{1,2}", time)), getStation(stationId) is None, getWeatherData(stationId, changeStrToDatetime(time))[1])
        if not re.match("\d{4}-\d{2}-\d{2} \d{1,2}", time) or getStation(stationId) is None or getWeatherData(stationId, changeStrToDatetime(time))[1]:
            return render_template("addWeatherPage.html", weatherParameters=weatherParameters, result="Podano błędne dane!")
        temp = float(request.form[temperature]) if request.form[temperature] != "" else None
        windSp = float(request.form[windSpeed]) if request.form[temperature] != "" else None
        windDir = float(request.form[windDirection]) if request.form[temperature] != "" else None
        pres = float(request.form[pressure]) if request.form[temperature] != "" else None
        time = changeStrToDatetime(time)
        addReading(stationId, time, temp, windSp, windDir, pres)
        return render_template("addWeatherPage.html", weatherParameters=weatherParameters, result="Pomyślnie dodano dane!")



@app.route('/updateWeatherAction', methods=["GET", "POST"])
def updateWeatherAction():
    if request.method == "POST":
        stationId = int(request.form["stationId"])
        time = changeStrToDatetime(request.form["time"])
        temp = changeStrToFloat(request.form[temperature])
        windSp = changeStrToFloat(request.form[windSpeed])
        windDir = changeStrToFloat(request.form[windDirection])
        pres = changeStrToFloat(request.form[pressure])
        data={"stationId":stationId, "time":time, temperature:temp, windSpeed:windSp, windDirection:windDir, pressure:pres}
        if updateWeather(stationId,time,temp, windSp, windDir, pres):
            return render_template("editPageManager.html", data=data, result="Pomyślnie zaktualizowano dane!")
        else:
            return render_template("editPageManager.html", data=data, result="Nie udało się zaktualizować danych!")



@app.route('/managerOptionsPage')
def managerOptionsPage():
    return render_template("managerOptionsPage.html")




@app.route('/diagnosticianPage')
def diagnosticianPage():
    return render_template("diagnosticianPage.html", allDocuments=getDiagnosticiansAsDicts())

@app.route('/editDiagnosticianPage', methods=["GET", "POST"])
def editDiagnosticianPage():
    if request.method == "POST":
        idDiag = int(request.form["idDiagnostician"])
        data = getDiagnosticianById(idDiag).toDict()
        return render_template("editDiagnosticianPage.html", data=data)

@app.route('/updateDiagnosticianAction', methods=["GET", "POST"])
def updateDiagnosticianAction():
    if request.method == "POST":
        idDiag = int(request.form["idDiagnostician"])
        updateDiagnostician(idDiag, request.form["name"], request.form["lastname"])
        data = getDiagnosticianById(idDiag).toDict()
        return render_template("editDiagnosticianPage.html", data=data, result="Pomyślnie zaktualizowano dane diagnosty!")

@app.route('/addDiagnosticianPage')
def addDiagnosticianPage():
    return render_template("addDiagnosticianPage.html")

@app.route('/addDiagnosticianAction', methods=["GET", "POST"])
def addDiagnosticianAction():
    if request.method == "POST":
        addDiagnostician(request.form["name"], request.form["lastname"])
        return render_template("addDiagnosticianPage.html", result="Pomyślnie dodano diagnostę!")

@app.route('/deleteDiagnosticianAction', methods=["GET", "POST"])
def deleteDiagnosticianAction():
    if request.method == "POST":
        idDiag = int(request.form["idDiagnostician"])
        if deleteDiagnostician(idDiag):
            return render_template("diagnosticianPage.html", allDocuments=getDiagnosticiansAsDicts(), result="Pomyślnie usunięto diagnostę!")
        else:
            return render_template("diagnosticianPage.html", allDocuments=getDiagnosticiansAsDicts(), result="Nie udało się usunąć diagnosty!")


if __name__ == '__main__':
    app.debug = True
    app.run()

