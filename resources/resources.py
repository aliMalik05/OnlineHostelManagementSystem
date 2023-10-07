from flask import request, Response, jsonify
from flask import Flask, jsonify,request, render_template,session
from flask_restful import Resource
from database.models import Admin,Room,bookRequest,studentBooking,StudentLogin,attend,roomChange
import os
from datetime import datetime
class addAdmin(Resource):
    def post(self):
        print("In Add Admin")
        body=request.get_json()
        veh=Admin(**body).save()
        id=veh.id
        return {'id':str(id)},200

class availRoom(Resource):
    def get(self):
        rooms = Room.objects(remainingSeats__gte="1").to_json()
        return Response(rooms, mimetype="application/json", status=200)
class roomApi(Resource):
    def post(self):
        roomNo = request.form["roomNo"]
        roomRent = request.form["roomRent"]
        seatRent = request.form["seatRent"]
        seator = request.form["seator"]
        img = request.files["img"]
        if roomNo=="" or roomRent == "" or seatRent == "" or seator == "" or img.filename == "":
            return Response(render_template("addRoom.html", msg ="ENTER ALL DETAILS") )
        obj = Room.objects()
        for i in obj:
            if roomNo == i.roomNo:
                return Response(render_template("addRoom.html", msg="ROOM ALREADY EXIST"))
        print(roomNo, roomRent, seatRent, seator)
        img.save(os.path.join("C:\\Users\\Muhammad Ali\\PycharmProjects\\OnlineHostelManagement\\static\\img", img.filename))
        print(roomNo, roomRent, seatRent, seator, img.filename)
        obj = Room(roomNo=roomNo,roomRent=roomRent,seatRent=seatRent,seator=seator,img=img.filename,livingStudents="0",remainingSeats=seator).save()
        return Response(render_template("addRoom.html" , msg="ROOM ADDED SUCCESSFULLY"))

    def get(self):
        rooms = Room.objects().to_json()
        return Response(rooms, mimetype="application/json", status=200)
class updateRoomApi(Resource):
    def put(self,roomNo):
        body=request.get_json()
        obj=Room.objects.get(roomNo = roomNo)
        obj.update(**body)
        id=obj.id
        return {'id':str(id)},200

    def get(self , roomNo):
        rooms = Room.objects(roomNo=roomNo).to_json()
        return Response(rooms, mimetype="application/json", status=200)

    def delete(self, roomNo):
        reqdata = request.get_json()
        obj = Room.objects.get(roomNo=roomNo)
        if int(obj.livingStudents)==0:
            obj.delete()
            return "Deleted"
        raise Exception("error")


class StudentApi(Resource):
    def delete(self,email):
        reqdata = request.get_json()
        obj = studentBooking.objects.get(email=email)
        roomNo = obj.roomNo
        roomObj = Room.objects.get(roomNo=roomNo)
        rem = str(int(roomObj.remainingSeats)+1)
        stdLiv = str(int(roomObj.livingStudents)-1)
        roomObj.update(remainingSeats=rem,livingStudents=stdLiv)
        obj.delete()
        obj1 =StudentLogin.objects.get(email1=email).delete()
    def put(self,email):
        reqdata = request.get_json()
        obj = studentBooking.objects.get(email=email)
        if reqdata["roomNo"] =="" and reqdata["food"]  != "":
            reqdata["roomNo"] = obj.roomNo
        if reqdata["roomNo"] =="" and reqdata["food"]  == "":
            reqdata["food"] = obj.food
            reqdata["roomNo"] = obj.roomNo
            studentBooking.objects.get(email=email).update(**reqdata)
            return "updated"
        if reqdata["food"]  == "" and reqdata["roomNo"] !="":
            reqdata["food"] = obj.food
        prevRoom = obj.roomNo
        newRoom = reqdata["roomNo"]
        obj1 = Room.objects.get(roomNo=prevRoom)
        obj2 = Room.objects.get(roomNo=newRoom)
        rem1 = int(obj1.remainingSeats)
        stdliv1 = int(obj1.livingStudents)
        rem2 = int(obj2.remainingSeats)
        stdliv2 = int(obj2.livingStudents)
        obj1.update(remainingSeats=str(rem1+1),livingStudents=str(stdliv1-1))
        obj2.update(remainingSeats=str(rem2 - 1), livingStudents=str(stdliv2 + 1))
        if obj.food == "" or obj.food == "no" and reqdata["food"] =="yes":
            s1=int(obj.remainRent)+3000
            studentBooking.objects.get(email=email).update(remainRent=str(s1))
        studentBooking.objects.get(email=email).update(**reqdata)
        return "updated"
class bookApi(Resource):
    def post(self):
        body = request.get_json()

        book = bookRequest.objects()
        std = studentBooking.objects()
        for i in book:
            if i.email == body["email"]:
                raise Exception("error")
        for i in std:
            if i.email == body["email"]:
                raise Exception("error")
        obj = studentBooking(**body).save()
        session["status"] = "pending"
        obj3 = StudentLogin.objects(id = session.get("stid")).update(email1 = obj.email , status="pending")

        obj2  = bookRequest(sid = str(obj.id) ,name= obj.name , email = obj.email , paymentid = obj.paymentid , roomNo = obj.roomNo, type="booking").save()
        return {'id':str(id)},200
    def get(self):
        obj = bookRequest.objects().to_json()
        return Response(obj, mimetype="application/json", status=200)

class updateRequest(Resource):
    def delete(self , sid):
        StudentLogin.objects.get(email1=sid).update(status="false")
        bookRequest.objects.get(email=sid).delete()
        return "Request deleted"

    def put(self, sid):
        book = bookRequest.objects.get(email=sid)
        if book.type == "monthly":
            studentBooking.objects.get(email=sid).update(remainRent="0")
            bookRequest.objects.get(email=sid).delete()
            return "Request Confirmed"
        today = datetime.now()
        datestr = str(today.day) + "-" + str(today.month) + "-" + str(today.year)
        StudentLogin.objects.get(email1=sid).update(status = "true")
        studentBooking.objects.get(email=sid).update(status = "true")
        studentBooking.objects.get(email=sid).update(remainRent = "0",date=datestr)
        obj = studentBooking.objects.get(email=sid)
        roomNo = obj.roomNo
        room = Room.objects.get(roomNo=roomNo)
        remSeat = int(room.remainingSeats)-1
        stds = int(room.livingStudents)+1
        obj1 = studentBooking.objects.get(email=obj.email)
        session["city"] = obj1.city
        session["room"] = obj1.roomNo
        session["phone"] = obj1.phone
        session["date"] = datestr
        session["status"] = obj1.status
        Room.objects.get(roomNo=roomNo).update(livingStudents=str(stds),remainingSeats=str(remSeat))
        bookRequest.objects.get(email=sid).delete()
        return "Request Confirmed"


class student(Resource):
    def get(self):
        obj = studentBooking.objects(status="true").to_json()
        return Response(obj, mimetype="application/json", status=200)
    def post(self):
        body = request.get_json()
        veh = studentBooking(**body).save()
        id = veh.id
        return {'id': str(id)}, 200
    def put(self):
        reqdata = request.get_json()
        a = reqdata['id']
        studentBooking.objects.get(id=a).update(**reqdata)
        return {'id': str(id)}, 200

class attendanceAPi(Resource):
    def post(self,date):
        att = attend.objects()
        status = False
        for i in att:
            if i.date == date:
                status = True
        if status == False:
            obj = attend(date=date).save()
            return "added"
        else:
            raise Exception("error")

    def get(self,date):
        try:
            obj = attend.objects.get(date=date).to_json()
        except Exception as e:
            return "error"
        return Response(obj, mimetype="application/json" ,status=200 )

class attendanceUpdateApi(Resource):
    def put(self,date,email):
        obj = attend.objects.get(date=date)
        status = False
        for i in obj.attendance:
            if i == email:
                status = True
        status2 = True
        obj1 = studentBooking.objects()
        for i in obj1:
            if i.email == email:
                status2 = False
        if status == False and status2==False:
            list = obj.attendance
            list.append(email)
            obj.update(attendance = list)
            return "updated"
        else:
            raise Exception("error")

class mypayments(Resource):
    def get(self,id):
        obj = studentBooking.objects.get(email=session.get("email"))
        obj1 = bookRequest.objects()
        for i in obj1:
            if i.email == obj.email:
                raise Exception("error")
        obj2 = bookRequest(sid=str(obj.id), name=obj.name, email=obj.email, paymentid=id,roomNo=obj.roomNo, type="monthly").save()
        return {'id': str(id)}, 200


class paymentShow(Resource):
    def get(self):
        obj = studentBooking.objects(email = session.get("email")).to_json()
        return Response(obj, mimetype="application/json", status=200)
class sendpayreq(Resource):
    def get(self):
        obj = studentBooking.objects()
        for obj1 in obj:
            roomnbr=obj1.roomNo
            roomobj=Room.objects.get(roomNo=roomnbr)
            seatrent=int(roomobj.seatRent)
            foodstat=obj1.food
            if foodstat=="yes":
                seatrent=seatrent+3000
            print(seatrent)
            obj1.update(remainRent=str(seatrent))
        return {"msg":"Sented"}

class getstudent(Resource):
    def get(self,email):
        obj = studentBooking.objects.get(email=email).to_json()
        return Response(obj,mimetype="application/json", status=200)

class attendanceget(Resource):
    def get(self):
        obj = attend.objects().to_json()
        return Response(obj,mimetype="application/json", status=200)

class change(Resource):
    def post(self,):
        body = request.get_json()
        obj = studentBooking.objects.get(email=session.get("email"))
        roomChange(newRoom = body["new"] , prevRoom = body["prev"] , email = session.get("email") , sid = str(obj.id)).save()
        obj.update(roomNo = body["new"])
        return "Successfull"
    def get(self):
        obj = roomChange.objects().to_json()
        return Response(obj, mimetype="application/json", status=200)

    def delete(self):
        body = request.get_json()
        obj = roomChange.objects.get(sid = body["id"]).delete()
        return "deleted"

    def put(self):
        body = request.get_json()
        obj = roomChange.objects.get(sid = body["id"])
        prevRoom = obj.prevRoom
        newRoom = obj.newRoom
        obj1 = Room.objects.get(roomNo=prevRoom)
        obj2 = Room.objects.get(roomNo=newRoom)
        rem1 = int(obj1.remainingSeats)
        stdliv1 = int(obj1.livingStudents)
        rem2 = int(obj2.remainingSeats)
        stdliv2 = int(obj2.livingStudents)
        session["room"] = newRoom
        obj1.update(remainingSeats=str(rem1 + 1), livingStudents=str(stdliv1 - 1))
        obj2.update(remainingSeats=str(rem2 - 1), livingStudents=str(stdliv2 + 1))
        obj.delete()
        return "updated"
