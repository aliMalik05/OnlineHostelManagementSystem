from .resources import  addAdmin,mypayments,roomApi,updateRoomApi,attendanceget,availRoom,sendpayreq,change,bookApi,updateRequest,student,StudentApi,attendanceAPi,getstudent,attendanceUpdateApi,paymentShow

def initialize_routes(api):
    api.add_resource(addAdmin, '/api/addadmin')
    api.add_resource(roomApi, '/api/room')
    api.add_resource(updateRoomApi, '/api/room/<roomNo>')
    api.add_resource(availRoom, '/api/availRoom')
    api.add_resource(bookApi, '/api/bookApi')
    api.add_resource(updateRequest, '/api/updateRequest/<sid>')
    api.add_resource(student, '/api/students')
    api.add_resource(StudentApi, '/api/studentlogin/<email>')
    api.add_resource(attendanceAPi, '/api/attendance/<date>')
    api.add_resource(attendanceget, '/api/attendance')
    api.add_resource(attendanceUpdateApi, '/api/attendance/<date>/<email>')
    api.add_resource(paymentShow, '/api/payment')
    api.add_resource(sendpayreq, '/api/sendpayrequest')
    api.add_resource(mypayments, '/api/mypayments/<id>')
    api.add_resource(getstudent, '/api/getstudent/<email>')
    api.add_resource(change, '/api/changeroom')


