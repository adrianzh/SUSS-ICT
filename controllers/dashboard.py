from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models.courses import Course, HoleUploadInfo
from models.booking import Booking
from models.users import User
from datetime import datetime, timedelta

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard', methods=['GET','POST'])
@login_required
def render_dashboard():
    #ECA
    getUserBookingName = request.values.get('userByBooking')
    getUserLoginObject = User.objects(name=getUserBookingName).first()
    filterUser = request.values.get('filterUser')

    checkCourse = request.form.get("courseSelect")
    if checkCourse is not None:
        courseSelectName = checkCourse
        courseSelect = Course.objects(name=courseSelectName).first()
        courseList = Course.objects()

        #TMA
        #courseBooking = Booking.objects(courseName=courseSelect)
        #ECA
        if filterUser == "":
            courseBooking = Booking.objects(courseName=courseSelect)
        else:
            courseBooking = Booking.objects(courseName=courseSelect,name=getUserLoginObject)

        #to check if there are any booking against the selection
        if len(courseBooking) > 0:
            holes_duration = []
            #just to calculate the holes duration for the course
            for i in courseList: 
                if i['name'] == courseSelectName:
                    duration = 0

                    #TMA
                    #for x in range(len(i['holesDetail']['index'])):
                    #    index = int(i['holesDetail']['index'][x])
                    #    par = int(i['holesDetail']['par'][x])
                    #    dist = int(i['holesDetail']['dist'][x])
                    #ECA
                    for row, hole in enumerate(i['holesDetail']):
                        index = int(hole['index'])
                        par = int(hole['par'])
                        dist = int(hole['dist'])

                        if index <= 6: setupTime = par*180
                        elif index <= 12: setupTime = par*150
                        else: setupTime = par*120
                        #set multipler as Play Time is 60s times X
                        multipler = dist//100 + 1
                        if dist > 500: multipler = 6
                        elif dist%100 == 0: multipler+1
                        playTime = 60*multipler
                        holes_duration.append(playTime+setupTime)
            accumulated_duration = [0]
            #To calculate duration per hole in total
            for i, t in enumerate(holes_duration):
                accumulated_duration.append(accumulated_duration[i] + t)
            #to run though all aviliable booking
            hole_start_time = []
            dict_id = 1
            courseBookingID = {}
            for o in courseBooking:
                tee_time = o['tee_time']
                for a in tee_time:
                    tee_time_date = datetime.strptime(a[0],'%d/%m/%Y %I:%M:%S %p')
                    #To add the start time per hole
                    for t in accumulated_duration:
                        hole_start_time.append(tee_time_date + timedelta(seconds = t))  
                    courseBookingID["Booking_"+str(dict_id)] = hole_start_time
                    hole_start_time = []
                    dict_id += 1
            charts = courseBookingID
            hole_labels = [f'Hole {i}' for i in range(1, len(accumulated_duration))] 
            hole_labels.insert(0, 'Start time')  
        else: return render_template('dashboard.html', aUser=current_user.name, sidebar=1, courses=Course.objects())
        if request.method == "GET":
                return render_template("dashboard.html", aUser=current_user.name, sidebar=1, courses=Course.objects(), chartData = jsonify({'charts': charts, 'labels': hole_labels}))
        elif request.method == "POST":
                return jsonify({'charts': charts, 'labels': hole_labels})

    #ECA
    if getUserBookingName is not None:
        user_booked_course = []
        user_booked_course_name = []
        for row, value in enumerate(Booking.objects()):
            if getUserBookingName == value['name']['name']:
                user_booked_course_name.append(value['courseName']['name'])
        for row, value in enumerate(Course.objects()):
            if value['name'] in user_booked_course_name:
                user_booked_course.append(Course.objects()[row])
        return render_template('dashboard.html', aUser=current_user.name, sidebar=1, courses=user_booked_course, filterByUser=1)            

    return render_template('dashboard.html', aUser=current_user.name, sidebar=1, courses=Course.objects())