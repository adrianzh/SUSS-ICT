from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models.courses import Course, HoleUploadInfo
from models.hole import Hole
from models.booking import Booking
from models.users import User
import csv, io, datetime

course = Blueprint('courses', __name__)

@course.route('/courses', methods=['GET','POST'])
@login_required
def render_course():
    if request.method == 'POST':
        choiceFlow = request.form.get('type')
        courseSelectedName = request.form.get('courseType')

        return redirect(url_for('courses.render_course_detail', aCourse=courseSelectedName))
    choiceFlow = request.args.get('type')
    if choiceFlow == 'courseBook':
        return render_template('courses.html', aUser=current_user.name, courses=Course.objects(), type=choiceFlow)

    return render_template('courses.html', aUser=current_user.name, courses=Course.objects(), type=choiceFlow)

@course.route('/courseDetail', methods=['GET','POST'])
@login_required
def render_course_detail():
    if request.method == 'POST':
        courseSelectedName = request.form.get('courseType')
        choiceFlow = request.form.get('type')
        tee_time = request.form.get('tee_time')
        courseSelected = Course.objects(name=courseSelectedName).first()
        aUser = User.objects(name=current_user.name).first()
        bookingSelected = Booking.objects(name=aUser, courseName=courseSelected).first()
        new_tee_time = bookingSelected['tee_time']
        tee_time = tee_time.replace("-","/").replace("T"," ")
        tee_time_DT = datetime.datetime.strptime(tee_time,"%Y/%m/%d %H:%M")
        tee_time_DT = [str(tee_time_DT.strftime("%d/%m/%Y %I:%M:%S %p"))]
        new_tee_time.append(tee_time_DT)
        bookingSelected.update(__raw__={'$set': {'tee_time': new_tee_time}})
        return redirect(url_for('courses.render_course', aUser=current_user.name, courses=Course.objects(), type=choiceFlow))
    courseName = request.args.get('aCourse')
    aCourse = Course.objects(name=courseName).first()
    return render_template('courseDetail.html', aUser=current_user.name, aCourse=aCourse, aCourseName=courseName)

@course.route("/upload", methods=['GET','POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template("upload.html", aUser=current_user.name)
    elif request.method == 'POST':        
        type = request.form.get('type')
        file = request.files.get('file')                    
        data = file.read().decode('utf-8')
        dict_reader = csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"')
        file.close()
        #after upload successfully - maybe can show some message
        if type == 'booking':
            prev_item_name = None

            #ECA
            prev_name = None

            tee_time_list = []
            for item in list(dict_reader):
                name = User.objects(email=item['user']).first()
                courseName = Course.objects(name=item['course_name']).first()
                tee_time = item['check_in_time'].strip('"').split(", ")
                if prev_item_name is None: 
                    prev_item_name = item['course_name']

                    #ECA
                    prev_name = item['user']

                    tee_time_list.append(tee_time)
                else:

                    #TMA
                    #if prev_item_name == item['course_name']:
                    #ECA - to resolve some bug
                    if prev_item_name == item['course_name'] and prev_name == item['user']:

                        tee_time_list.append(tee_time)
                    else:
                        #as long as diff from prev item, add to DB
                        courseNamePrev = Course.objects(name=prev_item_name).first()

                        #TMA
                        #aBookingUpload = Booking(name=name,courseName=courseNamePrev,tee_time=tee_time_list).save()
                        #prev_item_name = item['course_name']
                        #ECA - to resolve some bug
                        namePrev = User.objects(email=prev_name).first()
                        aBookingUpload = Booking(name=namePrev,courseName=courseNamePrev,tee_time=tee_time_list).save()
                        prev_item_name = item['course_name']
                        prev_name = item['user']

                        tee_time_list = []
                        tee_time_list.append(tee_time)
            #This is to add to booking DB if last two item is the same
            aBookingUpload = Booking(name=name,courseName=courseName,tee_time=tee_time_list).save()
                
        elif type == 'course':
            for item in list(dict_reader):
                name = item['course']
                indexUpload = item['index'].strip("[]").split(", ")
                parUpload = item['par'].strip("[]").split(", ")
                distUpload = item['dist'].strip("[]").split(", ")

                #TMA
                #holesDetail = HoleUploadInfo(index=indexUpload,par=parUpload,dist=distUpload).save()
                #ECA
                uploadBatch = []
                for row, value in enumerate(indexUpload): 
                    uploadItem = Hole(index=indexUpload[row],par=parUpload[row],dist=distUpload[row]).save()
                    uploadBatch.append(uploadItem)

                image = item['image_url']
                description = item['description']
                aCourseUpload = Course(name=name, holesDetail=uploadBatch, image=image, description=description).save()
        
        return render_template("upload.html", aUser=current_user.name)
