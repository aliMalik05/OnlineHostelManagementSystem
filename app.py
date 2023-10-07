from flask import Flask, jsonify,request, render_template,session
from flask_session import Session
from flask_restful import Api,Resource
from database import db
from resources import routes

from datetime import datetime
from database.models import Admin,StudentLogin,studentBooking


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb://localhost:27017/hostel'
}
app.secret_key = "HELLO"
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)
api=Api(app)
db.initialize_db(app)
routes.initialize_routes(api)

@app.route('/')
def home():  # put application's code here
    return render_template("home.html")
@app.route('/AdminLog',methods=["POST"])
def adminLog():
    email=request.form["email"]
    password=request.form["password"]
    try:
        obj=Admin.objects.get(email=email,password=password)
        session["adminid"]=obj.id
    except Exception as e:
        return render_template("adminSignin.html")
    print(obj)

    return render_template("admin.html")

@app.route('/loginForm')
def loginForm():
    return render_template("signin.html")

@app.route('/registerForm')
def registerForm():
    return render_template("registerForm.html")

@app.route('/adminLogin')
def adminLogin():  # put application's code here
    return render_template("adminSignin.html")

@app.route('/studentLogin')
def studentLogin():  # put application's code here
    return render_template("signin.html")


@app.route('/addRoom')
def addRoom():  # put application's code here
    if session.get("adminid")==None:
        return render_template("adminSignin.html")
    return render_template("addRoom.html")

@app.route('/delstudent')
def delstudent():  # put application's code here
    if session.get("adminid")==None:
        return render_template("adminSignin.html")
    return render_template("deletestudent.html")

@app.route('/updatestudent')
def updatestudent():  # put application's code here
    if session.get("adminid")==None:
        return render_template("adminSignin.html")
    return render_template("updatestudent.html")

@app.route('/adminDashboard')
def adminDashboard():  # put application's code here
    if session.get("adminid")==None:
        return render_template("adminSignin.html")
    return render_template("admin.html")

@app.route('/updateRoom')
def updateRoom():  # put application's code here
    if session.get("adminid")==None:
        return render_template("adminSignin.html")
    return render_template("updateRoom.html")

@app.route('/deleteroom')
def deleteroom():  # put application's code here
    if session.get("adminid")==None:
        return render_template("adminSignin.html")
    return render_template("deleteroom.html")

@app.route('/showRooms')
def showRooms():  # put application's code here
    if session.get("adminid")==None:
        return render_template("adminSignin.html")
    return render_template("showRooms.html")



@app.route('/studentSignup')
def studentSignup():  # put application's code here
    return render_template("studentSignup.html")
@app.route('/stdlogout')
def studentlogout():
    try:
        session.pop("email")
        session.pop("name")
        session.pop("stid")
        session.pop("status")
        session.pop("city")
        session.pop("phone")
        session.pop("room")
        session.pop("date")
    except Exception as e:
        return render_template("signin.html")
    print(session)
    return render_template("signin.html")


@app.route('/bookRoom')
def bookRoom():  # put application's code here
    if session.get("stid")==None:
        return render_template("signin.html")
    if session.get("status") == "true":
        print("abc")
        return render_template("bookedStudent.html",  name = session.get("name"))
    if session.get("status") == "pending":
        return render_template("pending.html",  name = session.get("name"))
    return render_template("student.html", name = session.get("name"))

@app.route('/studentSignin' , methods = ["POST"])
def studentSignin():
    obj = StudentLogin.objects()
    msg = ""
    status = False
    status1 = False
    email = request.form["email"]
    name = request.form["name"]
    password = request.form["password"]
    if email == "" or name == "" or password == "":
        return render_template("studentSignup.html" , msg="ENTER PROPER DETAILS")
    for i in obj:
        print(email)
        if i.email == email:
            status = True
    if status == False:
        StudentLogin(name = name , email = email , password = password, status="false").save()
        return render_template("signin.html")
    if status == True:
        print("hello")
        return render_template("studentSignup.html" , msg = "ACCOUNT ALREADY EXISTS")
    return render_template("studentSignup.html" , msg="")


@app.route('/stdLogin' , methods = ["POST"])
def stdLogin():
    email = request.form["email"]
    password = request.form["password"]
    print(session.get("status"))
    print("Hello")
    try:
        obj = StudentLogin.objects.get(email=email, password=password)
        session["name"] = obj.name
        session["stid"] = obj.id
    except Exception as e:
        print(str(e))
        return render_template("signin.html")
    obj = StudentLogin.objects.get(email=email)
    session["status"] = obj.status
    if session.get("status") == "true":
        print("abc")
        obj1 = studentBooking.objects.get(email = obj.email1)
        session["city"] = obj1.city
        session["room"] = obj1.roomNo
        session["phone"] = obj1.phone
        session["email"]=obj.email1
        session["date"] = obj1.date
        print(session)
        return render_template("bookedStudent.html",name = session.get("name") ,email = session.get("email"),city = session.get("city"),room = session.get("room"),phone = session.get("phone"))
    if session.get("status") == "pending":
        return render_template("pending.html",  name = session.get("name"))
    else:
        return render_template("student.html" , name = session.get("name"))

@app.route('/pending')
def pedning():
    if session.get("stid")==None:
        return render_template("signin.html")
    return render_template("pending.html", name = session.get("name"))

@app.route('/avaiableRooms')
def avaiableRooms():
    if session.get("stid")==None:
        return render_template("signin.html")
    if session.get("status") == "true":
        print("abc")
        return render_template("bookedStudent.html",  name = session.get("name"))
    if session.get("status") == "pending":
        return render_template("pending.html",  name = session.get("name"))
    return render_template("availableRooms.html", name = session.get("name"))

@app.route('/bookedStudent')
def bookedStudent():
    if session.get("stid")==None:
        return render_template("signin.html")
    return render_template("bookedStudent.html",name = session.get("name") ,email = session.get("email"),city = session.get("city"),room = session.get("room"),phone = session.get("phone") )

@app.route('/changeRoom')
def changeRoom():
    if session.get("stid")==None:
        return render_template("signin.html")
    return render_template("changeRoom.html", name = session.get("name"))

@app.route('/changeRequest')
def changeRequest():
    if session.get("adminid")==None:
        return render_template("signin.html")
    return render_template("changeRequest.html")


@app.route('/studentAtt')
def studentAtt():
    if session.get("stid")==None:
        return render_template("signin.html")
    email = session.get("email")
    date = session.get("date")
    print(email)
    return render_template("studentAtt.html" , email=email, name = session.get("name") , date=date)


@app.route('/showRequest')
def showRequest():
    if session.get("adminid")==None:
        return render_template("adminSignin.html")
    return render_template("showRequest.html")

@app.route('/sendMail')
def sendMail():
    if session.get("adminid")==None:
        return render_template("adminSignin.html")
    return render_template("sendMail.html")

@app.route('/showBookings')
def showBookings():
    if session.get("adminid")==None:
        return render_template("adminSignin.html")
    return render_template("showBookings.html")

@app.route('/attendance')
def attendance():
    if session.get("adminid")==None:
        return render_template("adminSignin.html")
    return render_template("attendance.html")


@app.route('/payment')
def payment():
    if session.get("stid")==None:
        return render_template("signin.html")
    return render_template("payment.html", name = session.get("name"))

@app.route('/showAtt')
def showAtt():
    if session.get("adminid")==None:
        return render_template("adminSignin.html")
    return render_template("showAttendance.html")
@app.route('/updatedetails')
def UpdateDetails():
    if session.get("stid") == None:
        return render_template("signin.html")
    return render_template("updateDetails.html", name=session.get("name"))
@app.route('/showdetails')
def ShowDetails():
    if session.get("stid") == None:
        return render_template("signin.html")
    return render_template("showDetails.html", name=session.get("name"))
@app.route('/showRoom')
def ShowSRoom():
    if session.get("stid") == None:
        return render_template("signin.html")
    return render_template("showStRoom.html", name=session.get("name"))
@app.route('/adminlogout')
def adminlogout():
    session.pop("adminid")
    return render_template("adminSignin.html")



if __name__ == '__main__':
    app.run()


