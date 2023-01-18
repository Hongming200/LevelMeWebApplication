from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask import request

from Forms import CreateUserForm, CreateAdminFormTask, CreateAdminProfile, CreateStaffMessage, EmailSubscription
from Forms import RegistrationForm, LoginForm, UpdateForm, DeleteAccountForm, ChangePasswordForm, Accept, Delete, IndividualForm, UpdateGroupForm, DeleteTimeTableForm, ContactUsForm, UpdateTicket, ResolvedForm, ReviewForm, DeleteOnlyForm, UpdateReviewForm, UpdatePictureForm
from random import randint
import os
import shelve, Task, AdminProfile, User, Staff_Message, Email_Subscription

#hongming
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from database import cursor, db
from flask_mail import Mail, Message
from Forms import AuthenticationForm

#hoyjtun
import hashlib


app = Flask(__name__)
#Advance logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler('log.txt')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

fail_login_dict = {}

#rate limiting
limiter = Limiter(app, key_func=get_remote_address)

#ayaka for now
import sys
import shelve
import User, pyotp
from Forms import FeedbackForm, UpdateFeedbackForm, feedbackfilter, CreateTaskFormCS, taskfiltercs, CreateProfileCS, RetrieveTicket, MessageTCS, ForgetPasswordForm, VerifyOTPForm, ResetPasswordForm
from datetime import date, datetime
#ayaka end for now

#justin for now
from Forms import CreateStudentRequestForm
from Forms import CreateUserInterestForm
from Forms import CreateUserProfileForm
from flask import sessions
import StudentRequest
import UserInterest
import UserProfile

#justin end for now



app = Flask(__name__)
# To add more HTML pages, you cannot directly link a html file in the content
# you will need to write @app.route(refer below) to tell this python file to read the html file

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

from flask_wtf import CSRFProtect
app.config['SECRET_KEY'] = 'SECRET'  #protect against modifying cookies and crosssite request forgery attacks
csrf = CSRFProtect(app)

#app.config["WTF_CSRF_CHECK_DEFAULT"] = False


app.config["RECAPTCHA_PUBLIC_KEY"] = "6Ldw4PMbAAAAAJNqBkfWzaINVFTlTwi6ARPcpCWq"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6Ldw4PMbAAAAAMKXBBB6tI45FQSb1JY_sXqWSHX3"

import uuid
import gc
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            print(session)
            return func(*args, **kwargs)
        else:
            flash('Please login.')
            print('session empty')
            return redirect(url_for("login"))
    return wrap

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit('10/minute', error_message=logger.info("[ALERT] [Source IP: 122.11.229.171] [Result: Failure] User exceeded rate limit of 10 per minute."))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db = shelve.open('storage.db', 'r')
        users_dict = db['Teachers']
        db.close()

        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)

        for obj in users_list:
            if form.email.data == obj.get_email() and check_hash(form.password.data, obj.get_salt()) == obj.get_hash():
                otp = randint(000000, 999999)
                msg = Message('Your OTP for Level Me is : {}'.format(otp),
                              recipients=['{}'.format(form.email.data)])  # recipient is copied from temp mail
                mail.send(msg)
                id = obj.get_user_id()
                logger.info(
                    "[Source IP: 122.11.229.171] [Result: Success] Successful login of by user. Email: {},".format(form.email.data))
                add_log("INFO", "122.11.229.171", "Success", "Successful login of by user. Email: {}".format(form.email.data))
                flash('Enter OTP!', 'success')
                session['logged_in'] = 'teacher'
                return redirect(url_for('authentication', id=id))
            else:
                add_log("INFO", "122.11.229.171", "Failure","Unsuccessful login. Attempt - Email: {},".format(form.email.data))
                fail_login_list = list(fail_login_dict.keys())
                if form.email.data in fail_login_list:
                    fail_login_dict[form.email.data] += 1
                    if fail_login_dict[form.email.data] == 3:
                        add_log("WARNING", "122.11.229.171", "Failure","3 Unsuccessful login attempt. Email: {}".format(form.email.data))
                        fail_login_dict[form.email.data] = 0
                else:
                    fail_login_dict[form.email.data] = 1


        if form.email.data == "admin@gmail.com" and form.password.data == "admin":
            session['logged_in'] = 'admin'
            return redirect(url_for("admin_dashboard"))
        elif form.email.data == "customerservice@gmail.com" and form.password.data == "customerservice":
            session['logged_in'] = 'cs'
            return redirect(url_for("manage_feedback"))
        elif form.email.data == "student@gmail.com" and form.password.data == "student":
            session['logged_in'] = 'student'
            return redirect(url_for("create_profile"))

    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash('You have logged out')
    gc.collect()
    return redirect(url_for("home"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    add_log("INFO", "122.11.229.171", "Success", "User have successfully accessed the register page.")
    form = RegistrationForm()
    if form.validate_on_submit():
        users_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            users_dict = db['Teachers']
        except:
            print("Error in retrieving Users from storage.db.")


        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)

        email_list = []
        for obj in users_list:
            email = obj.get_email()
            email_list.append(email)

        if form.email.data not in email_list:
            hash = hashpassword(form.password.data)
            hash2 = check_hash(form.password.data, hash[1])
            user = User.Teacher(form.first_name.data, form.last_name.data, form.email.data, hash[0], hash[1])
            users_dict[user.get_user_id()] = user
            db['Teachers'] = users_dict
            add_log("INFO", "122.11.229.171", "Success", "User have successfully registered an account. First name: {}, Last name: {}, Email: {}.".format(user.get_first_name(), user.get_last_name(), user.get_email()))
            #flash('Your account has been created! You are now able to log in.', 'success')
            return redirect(url_for('register_2fa'))
        else:
            flash('The email that you used is already taken!', 'danger')

        db.close()

    return render_template('register.html', form=form)

def save_picture(form_picture):
    random = str(randint(0,10000000))  #prevent the image from colliding with one another
    _, f_ext = os.path.splitext(form_picture.filename)  #retrieve the extension
    picture_fn = random + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

@app.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    if session['logged_in'] == 'teacher':
        form = UpdatePictureForm()
        db = shelve.open('storage.db', 'r')
        users_dict = db['Teachers']
        user = users_dict.get(id)
        db.close()
        if form.validate_on_submit():
            users_dict = {}
            db = shelve.open('storage.db', 'w')
            users_dict = db['Teachers']
            user = users_dict.get(id)
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                user.set_picture(picture_file)
                flash("You have successfully updated your profile picture!", "success")
            db['Teachers'] = users_dict
            db.close()

        image_file = url_for('static', filename='profile_pics/' + user.get_picture())
        return render_template('profile.html', user=user, id=id, form=form, image_file=image_file)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/updateprofile/<int:id>',  methods=['GET', 'POST'])
@login_required
def update_profile(id):
    if session['logged_in'] == 'teacher':
        form1 = UpdateForm()
        if form1.validate_on_submit():
            users_dict = {}
            db = shelve.open('storage.db', 'w')
            users_dict = db['Teachers']
            user = users_dict.get(id)

            first_name = form1.first_name.data
            last_name = form1.last_name.data
            occupation = form1.occupation.data
            experience = form1.experience.data
            education = form1.education.data
            skills = form1.skills.data
            mobile_phone = form1.mobile_phone.data
            email = form1.email.data
            link = form1.link.data
            social_media = form1.social_media.data
            birthdate = form1.birthdate.data
            gender = form1.gender.data
            language = form1.language.data
            location = form1.location.data

            user.set_first_name(first_name)
            user.set_last_name(last_name)
            user.set_occupation(occupation)
            user.set_experience(experience)
            user.set_education(education)
            user.set_skills(skills)
            user.set_mobile_phone(mobile_phone)
            user.set_email(email)
            user.set_link(link)
            user.set_social_media(social_media)
            user.set_birthdate(birthdate)
            user.set_gender(gender)
            user.set_language(language)
            user.set_location(location)

            db['Teachers'] = users_dict
            db.close()
            add_log("INFO", "122.11.229.171", "Success","Successful update of account.")
            flash('You have successfully updated your profile!', 'success')
            return redirect(url_for('profile', id=id))

        else: #display data so that user do not have to re-enter
            users_dict = {}
            db = shelve.open('storage.db', 'r')
            users_dict = db['Teachers']
            user = users_dict.get(id)
            db.close()

            form1.first_name.data = user.get_first_name()
            form1.last_name.data = user.get_last_name()
            form1.occupation.data = user.get_occupation()
            form1.experience.data = user.get_experience()
            form1.education.data = user.get_education()
            form1.skills.data = user.get_skills()
            form1.mobile_phone.data = user.get_mobile_phone()
            form1.email.data = user.get_email()
            form1.link.data = user.get_link()
            form1.social_media.data = user.get_social_media()
            form1.birthdate.data = user.get_birthdate()
            form1.gender.data = user.get_gender()
            form1.language.data = user.get_language()
            form1.location.data = user.get_location()

        return render_template('updateprofile.html', form1=form1, id=id)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/updatepassword/<int:id>',  methods=['GET', 'POST'])
@login_required
def update_password(id):
    if session['logged_in'] == 'teacher':
        form = ChangePasswordForm()
        if form.validate_on_submit():

            users_dict = {}
            db = shelve.open('storage.db', 'w')
            users_dict = db['Teachers']
            user = users_dict.get(id)

            hash = hashpassword(form.new_password.data)
            user.set_hash(hash[0])
            user.set_salt(hash[1])

            db['Teachers'] = users_dict
            db.close()
            flash('You have successfully changed your password!!', 'success')
            add_log("INFO", "122.11.229.171", "Success","Successful update of password of user Email: {}".format(user.get_email()))
            return redirect(url_for('login'))
        return render_template('updatepassword.html', form=form, id=id)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/deleteprofile/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_profile(id):
    if session['logged_in'] == 'teacher':
        form = DeleteAccountForm()
        if form.validate_on_submit():
            users_dict = {}
            db = shelve.open('storage.db', 'w')
            users_dict = db['Teachers']
            user = users_dict.get(id)

            email = user.get_email()
            if form.email.data == email:
                del users_dict[id]
                add_log("INFO", "122.11.229.171", "Success","Successful deletion of account. Email: {}".format(user.get_email()))
                flash('You have successfully deleted your account. See you soon. :(', 'success')

            else:
                flash("The email you entered does not match this account!", "danger")

            db['Teachers'] = users_dict
            db.close()

        return render_template('deleteprofile.html', form=form, id=id)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/contactus/<int:id>', methods=['GET', 'POST'])
def contact_us(id):
    if session['logged_in'] == 'teacher':
        form = ContactUsForm()
        if form.validate_on_submit():
            users_dict = {}
            db = shelve.open('storage.db', 'w')
            users_dict = db['Teachers']
            user = users_dict.get(id)

            if user.get_email() == form.email.data:
                feedback = [form.issue.data, form.feedback.data]
                user.set_ticket(feedback)
                redirect(url_for("ticket", id=id))
                flash("You have successfully sent a feedback to us.", "success")

            else:
                flash("The email you entered does not match this account.", "danger")

            db['Teachers'] = users_dict
            db.close()

        else:
            storagedb = shelve.open('storage.db', 'r')
            users_dict = storagedb['Teachers']
            user = users_dict.get(id)
            storagedb.close()

            form.email.data = user.get_email()

        return render_template('contactus.html', form=form,  id=id)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def ticket(id):
    if session['logged_in'] == 'teacher':
        form = ResolvedForm()

        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Teachers']
        user = users_dict.get(id)

        if form.validate_on_submit():
            user.remove_ticket()
            flash("You have successfully deleted your support ticket!", "success")

        db['Teachers'] = users_dict
        db.close()

        return render_template('ticket.html', id=id, form=form, user=user)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/updateticket/<int:id>', methods=['GET', 'POST'])
@login_required
def update_ticket(id):
    if session['logged_in'] == 'teacher':
        form = UpdateTicket()
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Teachers']
        user = users_dict.get(id)

        ticket = user.get_ticket()
        if form.validate_on_submit():
            if form.choice.data == 'Issue':
                ticket[0] = form.update.data
                user.set_ticket(ticket)

            else:  #feedback
                ticket[1] = form.update.data
                user.set_ticket(ticket)

            flash("You have successfully updated your support ticket!", "success")

        db['Teachers'] = users_dict
        db.close()


        return render_template('updateticket.html', form=form, id=id)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/retrieveticket', methods=['GET', 'POST'])
@login_required
def retrieveticket():
    if session['logged_in'] == 'teacher':
        form = RetrieveTicket()
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Teachers']


        db['Teachers'] = users_dict
        db.close()

        user_list = []
        for key in users_dict:
            user_list.append(users_dict[key])

        issue_dict = {} #issue:feedback
        for obj in user_list:
            issue_dict[obj.get_email()] = [obj.get_ticket()[0],obj.get_ticket()[1]]

        return render_template('retrieveticket.html', form=form, issue_dict=issue_dict)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/requestz/<int:id>', methods=['GET', 'POST'])
@login_required
def requestz(id):
    if session['logged_in'] == 'teacher':
        studentrequests_dict = {}
        db = shelve.open('storageStudentRequest.db', 'r')
        studentrequests_dict = db['StudentRequests']
        db.close()

        stud_list = []
        for key in studentrequests_dict:
            studentrequest = studentrequests_dict.get(key)
            stud_list.append(studentrequest)


        # obj = users_dict.get(id)
        # stud_list = obj.get_students_request()

        return render_template('requestz.html', id=id, stud_list=stud_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/manage/<int:id>', methods=['GET','POST'])
@login_required
def manage(id):
    if session['logged_in'] == 'teacher':
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Teachers']
        db.close()

        obj = users_dict.get(id)
        stud_list = obj.get_students()

        return render_template('manage.html', id=id, stud_list=stud_list)
    else:
        return redirect(url_for('logout'))

@app.route('/updaterequestz/<int:id>', methods=['GET', 'POST'])
@login_required
def update_requestz(id):
    if session['logged_in'] == 'teacher':
        form = Accept()

        if form.validate_on_submit():
            studentrequests_dict = {}
            db = shelve.open('storageStudentRequest.db', 'w')
            studentrequests_dict = db['StudentRequests']

            stud_list = [] #get obj
            for key in studentrequests_dict:
                studentrequest = studentrequests_dict.get(key)
                stud_list.append(studentrequest)

            stud_name = [] #get full names
            for obj in stud_list:
                first = obj.get_first_name()
                last = obj.get_last_name()
                fullname = first + ' ' + last
                stud_name.append(fullname)

            if form.student.data in stud_name: #if input is in list
                for obj in stud_list:
                    fullname = obj.get_first_name() + ' ' + obj.get_last_name()
                    if form.student.data == fullname:
                        req_info = [fullname, obj.get_email(), obj.get_size(), obj.get_timeslot()]

                        for key in studentrequests_dict:  #delete from db according to fullname
                            name = studentrequests_dict[key].get_first_name() + " " + studentrequests_dict[key].get_last_name()
                            if name == fullname:
                                studentrequests_dict.pop(key)
                                break

                        users_dict = {}
                        dbstorage = shelve.open('storage.db', 'w')
                        users_dict = dbstorage['Teachers']
                        user = users_dict.get(id)

                        user.add_students(req_info)
                        dbstorage['Teachers'] = users_dict
                        dbstorage.close()
                        flash("You have successfully accepted a student's request! Go to 'View Students' to see.", "success")

            else:
                flash("The student request you are trying to accept cannot be found!", "danger")

            db['StudentRequests'] = studentrequests_dict
            db.close()
            # studentrequests_dict = db['StudentRequests']
            # db.close()
            #
            # users_dict = {}
            # db = shelve.open('storage.db', 'w')
            # users_dict = db['Teachers']
            # user = users_dict.get(id)
            #
            # req_list = user.get_students_request()
            # name_list = []
            # for student_info in req_list:
            #     name_list.append(student_info[0])
            #
            # if form.student.data in name_list:
            #     req_info = user.remove_students_request(form.student.data)  #returns the stud info that is deleted
            #     user.add_students(req_info)
            #     flash("You have successfully accepted a student's request! Go to 'View Students' to see.", "success")
            #
            # else:
            #     flash("The student request you are trying to accept cannot be found!", "danger")

            # list = user.get_students_request()         #memoryerror
            #
            # req_list = []
            # for req_info in list:
            #     list.append(req_info[0])
            #
            # if form.student.data in req_list:
            #     new_list = []
            #     for req_info in list:
            #         if req_info[0] != form.student.data:
            #             new_list.append(req_info)
            #         else:  #if accepted
            #             req = req_info
            #
            #     user.set_students_request(new_list)  #updating obj's req list
            #
            #     stud_list = user.get_students()
            #     stud_list.append(req)
            #     user.set_students(stud_list)
            #     flash('You have successfully accepted a student, view the student in "View Students"', 'primary')
            #
            # else:
            #     flash('The name of the student you are trying to accept is not found', 'danger')

            # db['Teachers'] = users_dict
            # db.close()


        return render_template('updaterequestz.html', form=form, id=id)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/updatemanage/<int:id>', methods=['GET', 'POST'])
@login_required
def update_manage(id):
    if session['logged_in'] == 'teacher':
        form = Delete()
        if form.validate_on_submit():
            users_dict = {}
            db = shelve.open('storage.db', 'w')
            users_dict = db['Teachers']
            user = users_dict.get(id)

            list = user.get_students()

            student = []
            for student_info in list:  #remove this when there is stud obj(during inte)
                student.append(student_info[0])

            if form.student.data in student:
                new_list = []
                for student in list:
                    if student[0] != form.student.data:
                        new_list.append(student)
                flash('You have successfully deleted a student!', 'success')

                user.set_students(new_list)
            else:
                flash('The student you are trying to delete is not found!', 'danger')

            db['Teachers'] = users_dict
            db.close()


        return render_template('updatemanage.html',form=form, id=id)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/individualtimetable/<int:id>', methods=['GET', 'POST'])
@login_required
def individual_timetable(id):
    if session['logged_in'] == 'teacher':
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Teachers']
        db.close()

        obj = users_dict.get(id)
        ind_list = obj.get_individual_timetable()

        return render_template('individualtimetable.html', id=id, ind_list=ind_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/grouptimetable/<int:id>', methods=['GET', 'POST'])
@login_required
def group_timetable(id):
    if session['logged_in'] == 'teacher':
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Teachers']
        db.close()

        obj = users_dict.get(id)
        group_list = obj.get_group_timetable()

        return render_template('grouptimetable.html', id=id, group_list=group_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/updateindividualtimetable/<int:id>', methods=['GET', 'POST'])
@login_required
def update_individual_timetable(id):
    if session['logged_in'] == 'teacher':
        form = IndividualForm()

        if form.validate_on_submit():
            users_dict = {}
            db = shelve.open('storage.db', 'w')
            users_dict = db['Teachers']
            user = users_dict.get(id)

            info = [form.date.data, form.time.data, form.name.data, form.email.data]
            user.add_individual_timetable(info)

            db['Teachers'] = users_dict
            db.close()

            flash('You have successfully update your timetable!', 'success')

        return render_template('updateindividualtimetable.html', id=id, form=form)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/updategrouptimetable/<int:id>', methods=['GET', 'POST'])
@login_required
def update_group_timetable(id):
    if session['logged_in'] == 'teacher':
        form = UpdateGroupForm()
        if form.validate_on_submit():
            users_dict = {}
            db = shelve.open('storage.db', 'w')
            users_dict = db['Teachers']
            user = users_dict.get(id)

            info = [form.date.data, form.time.data, form.group_no.data]
            user.add_group_timetable(info)

            db['Teachers'] = users_dict
            db.close()
            flash('You have successfully update your timetable!', 'success')

        return render_template('updategrouptimetable.html', id=id, form=form)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/deletetimeslot/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_timeslot(id):
    if session['logged_in'] == 'teacher':
        form = DeleteTimeTableForm()
        if form.validate_on_submit():
            users_dict = {}
            db = shelve.open('storage.db', 'w')
            users_dict = db['Teachers']
            user = users_dict.get(id)

            if form.choice.data == 'Individual':
                ind_timeslot = []
                for timeslot in user.get_individual_timetable():
                    ind_timeslot.append(timeslot[1])

                if form.time.data in ind_timeslot:
                    user.remove_individual_timeslot(form.time.data)
                    flash('You have successfully deleted a timeslot!', 'success')

                else:
                    flash("The timeslot you are trying to delete is not found!", "danger")

            else:   #group
                group_timeslot = []
                for timeslot in user.get_group_timetable():
                    group_timeslot.append(timeslot[1])

                if form.time.data in group_timeslot:
                    user.remove_group_timeslot(form.time.data)
                    flash('You have successfully deleted a timeslot!', 'success')

                else:
                    flash("The timeslot you are trying to delete is not found!", "danger")

            db['Teachers'] = users_dict
            db.close()


        return render_template('deletetimeslot.html', id=id, form=form)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/review/<int:id>', methods=['GET', 'POST'])
@login_required
def review(id):
    if session['logged_in'] == 'teacher':
        storagedb = shelve.open('storage.db', 'r')
        users_dict = storagedb['Teachers']
        storagedb.close()

        user = users_dict.get(id)#main user

        reviewdb = shelve.open('review.db', 'r')
        users_dict = reviewdb['UserReview']
        reviewdb.close()

        image_file = url_for('static', filename='profile_pics/' + user.get_picture())

        info_list = []
        good = 0
        avg = 0
        bad = 0
        for key in users_dict:
            info_list.append(users_dict[key])
            if users_dict[key][1] == 'Very Good':
                good += 10  #percentage per review
            elif users_dict[key][1] == 'Very Bad':
                bad += 10
            elif users_dict[key][1] == 'Average':
                avg += 10


        form = DeleteOnlyForm()
        if form.validate_on_submit():
            users_dict = {}
            db = shelve.open('storage.db', 'w')
            users_dict = db['Teachers']
            user = users_dict.get(id)

            user.set_rating('')
            user.set_review('')

            db['Teachers'] = users_dict
            db.close()

            users_review = {}
            reviewdb = shelve.open('review.db', 'w')
            users_review = reviewdb['UserReview']
            del users_review[id]

            reviewdb['UserReview'] = users_review
            reviewdb.close()
            flash('You have Successfully deleted your review!', 'success')

        return render_template('review.html', id=id, user=user, info_list=info_list, form=form, good=good, avg=avg, bad=bad, image_file=image_file)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/createreview/<int:id>', methods=['GET', 'POST'])
@login_required
def create_review(id):
    if session['logged_in'] == 'teacher':
        form = ReviewForm()
        if form.validate_on_submit():
            storagedb = shelve.open('storage.db', 'w')
            users_dict = storagedb['Teachers']
            user = users_dict.get(id)

            user.set_rating(form.rating.data)
            user.set_review(form.review.data)

            name = user.get_first_name() + ' ' + user.get_last_name()

            users_review = {}
            reviewdb = shelve.open('review.db', 'c')

            try:
                users_review = reviewdb['UserReview']
            except:
                print("Error in retrieving Users from storage.db.")

            users_review[id] = [name, form.rating.data, form.review.data]

            storagedb['Teachers'] = users_dict
            storagedb.close()
            reviewdb['UserReview'] = users_review
            reviewdb.close()

            flash('You have Successfully created your review!', 'success')

        return render_template('createreview.html', form=form, id=id)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/updatereview/<int:id>', methods=['GET', 'POST'])
@login_required
def update_review(id):
    if session['logged_in'] == 'teacher':
        form = UpdateReviewForm()
        if form.validate_on_submit():
            storagedb = shelve.open('storage.db', 'w')
            users_dict = storagedb['Teachers']
            user = users_dict.get(id)

            user.set_review(form.review.data)

            storagedb['Teachers'] = users_dict
            storagedb.close()


            reviewdb = shelve.open('review.db', 'w')
            users_review = reviewdb['UserReview']

            users_review[id][2] = form.review.data

            reviewdb['UserReview'] = users_review
            reviewdb.close()
            flash('You have Successfully updated your review!', 'success')

        else:
            storagedb = shelve.open('storage.db', 'r')
            users_dict = storagedb['Teachers']
            user = users_dict.get(id)
            storagedb.close()

            form.review.data = user.get_review()
        return render_template('updatereview.html', form=form, id=id)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/teacher_messagetcs', methods=['GET', 'POST'])
@login_required
def teacher_messagetcs():
    if session['logged_in'] == 'teacher':
        messagetcs_dict = {}
        db = shelve.open('messagetcs.db', 'r')
        messagetcs_dict = db['MessageTCS']
        db.close()

        messagetcs_list = []
        for key in messagetcs_dict:
            messagetcs = messagetcs_dict.get(key)
            messagetcs_list.append(messagetcs)

        return render_template('teacher_messagetcs.html', count=len(messagetcs_list), messagetcs_list=messagetcs_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

#database log
def add_log(level, ip, result ,event):
    sql = ("INSERT INTO logs(level, ip, result, event) VALUES (%s, %s, %s, %s)")
    cursor.execute(sql, (level, ip, result, event,))
    db.commit()
    log_id = cursor.lastrowid
    print("Added log {}".format(log_id))

def get_all_logs():
    sql = ("SELECT * FROM logs ORDER BY created DESC")
    cursor.execute(sql)
    result = cursor.fetchall()

    for row in result:
        print(row)

def get_level_logs(level):
    sql = ("SELECT * FROM logs WHERE level = %s")
    cursor.execute(sql, (level,))
    result = cursor.fetchall()

    for row in result:
        print(row)

def delete_log(id):
    sql = ("DELETE FROM logs WHERE id = %s")
    cursor.execute(sql, (id,))
    db.commit()
    print("Log id {} removed".format(id))

def delete_log_less(id):
    sql = ("DELETE FROM logs WHERE id < %s")
    cursor.execute(sql, (id,))
    db.commit()
    print("Log id < {} is removed".format(id))

#captcha
app.config["RECAPTCHA_PUBLIC_KEY"] = "6Ld4iJ8bAAAAAE5R2gy7V9y81SAmpADlZwBtepGB"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6Ld4iJ8bAAAAAL70tUcuTAZx8YzGUTYvZh5hp16h"

#2fa for email
# app.config['DEBUG'] = True
# app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'flaskwebapp8@gmail.com'
app.config['MAIL_PASSWORD'] = 'flaskuser34!'
app.config['MAIL_DEFAULT_SENDER'] = 'flaskwebapp8@gmail.com'
# app.config['MAIL_MAX_EMAILS'] = None
#app.config['MAIL_SUPPRESS_SEND'] = False
# app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

@app.route('/authentication/<int:id>', methods=['GET', 'POST'])
def authentication(id):
    form = AuthenticationForm()
    if form.validate_on_submit():
        # if form.otp.data == otp:
        #     return redirect(url_for('profile', id=id))
        # else:
        #     return redirect(url_for('login'))
        return redirect(url_for('profile', id=id))
    return render_template('authentication.html', id=id, form=form)

#hongming end

#ayaka start
@app.route("/createFeedback", methods=['GET', 'POST'])
@login_required
def createFeedback():
    if session['logged_in'] == 'cs':
        feedbackForm = FeedbackForm(request.form)
        if request.method == 'POST' and feedbackForm.validate():
            feedDict = {}
            db = shelve.open('feedback.db', 'c')

            try:
                feedDict = db['Feedback']

            except:
                print("Error in retrieving Feedback from feedback.db.")

            # id = 0
            # for i in feedDict:
            #     if int(i) > id:
            #         id = int(i)
            # if recentcount >= 0:
            #    id = recentcount

            id = uuid.uuid1()
            print(id)

            feed = User.Feedback(id, feedbackForm.firstName.data, feedbackForm.email.data, feedbackForm.type.data,
                                     feedbackForm.category.data, feedbackForm.remarks.data, feedbackForm.status.data, date = date.today())

            feedDict[feed.get_feedID()] = feed
            db['Feedback'] = feedDict

            db.close()

            return redirect(url_for('manage_feedback'))
        return render_template("createfeedback.html", form=feedbackForm)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/manage_feedback', methods=['GET', 'POST'])
@login_required
def manage_feedback():
    if session['logged_in'] == 'cs':
        filterform = feedbackfilter(request.form)
        feedDict = {}
        db = shelve.open('feedback.db', 'r')
        feedDict = db['Feedback']
        db.close()

        feedList = []
        Pendinglist = []
        Resolvedlist = []
        for key in feedDict:
            feed = feedDict.get(key)
            feedList.append(feed)
            if feed.get_status() == "Pending":
                Pendinglist.append(feed)
            elif feed.get_status() == "Resolved":
                Resolvedlist.append(feed)

        if request.method == "POST" and filterform.validate():
            varfilter = filterform.filter.data
            if varfilter == "":
                return redirect(url_for('manage_feedback'))
            elif varfilter == "Pending":
                return redirect(url_for('PendingFeedback'))
            elif varfilter == "Resolved":
                return redirect(url_for('ResolvedFeedback'))

        #retrieveticketstart

        form = RetrieveTicket()
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Teachers']


        db['Teachers'] = users_dict
        db.close()

        user_list = []
        for key in users_dict:
            user_list.append(users_dict[key])

        issue_dict = {} #issue:feedback
        for obj in user_list:

            issue_dict[obj.get_email()] = [obj.get_ticket()[0],obj.get_ticket()[1]]

        #retrieveticketend



        return render_template('manage_feedback.html', feedList=feedList, count=len(feedList), form = filterform, issue_dict=issue_dict)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)
    #retrieveticketstart
   # form = RetrieveTicket()
  #  users_dict = {}
   # db = shelve.open('storage.db', 'w')
   # users_dict = db['Teachers']


   # db['Teachers'] = users_dict
   # db.close()

   # user_list = []
   # for key in users_dict:
   #     user_list.append(users_dict[key])

   # issue_dict = {} #issue:feedback
    #for obj in user_list:
     #   issue_dict[obj.get_email()] = [obj.get_ticket()[0],obj.get_ticket()[1]]

    #retrieveticketend





@app.route('/updateFeedback/<uuid:id>/', methods=['GET', 'POST'])
@login_required
def updateFeedback(id):
    if session['logged_in'] == 'cs':
        updateFeedbackForm = UpdateFeedbackForm(request.form)
        if request.method == 'POST' and updateFeedbackForm.validate():
            feedDict = {}
            db = shelve.open('feedback.db', 'w')
            feedDict = db['Feedback']
            feed = feedDict.get(id)
            feed.set_status(updateFeedbackForm.status.data)
            db['Feedback'] = feedDict
            db.close()

            return redirect(url_for('manage_feedback'))

        else:
            feedDict = {}
            db = shelve.open('feedback.db', 'r')
            feedDict = db['Feedback']
            db.close()

            feed = feedDict.get(id)
            updateFeedbackForm.firstName.data = feed.get_firstName()
            updateFeedbackForm.email.data = feed.get_email()
            updateFeedbackForm.category.data = feed.get_category()
            updateFeedbackForm.type.data = feed.get_type()
            updateFeedbackForm.remarks.data = feed.get_remarks()
            updateFeedbackForm.status.data = feed.get_status()
            return render_template('updateFeedback.html', form=updateFeedbackForm)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/deletefeedback/<uuid:id>', methods=['POST'])
@login_required
def deletefeedback(id):
    if session['logged_in'] == 'cs':
        feedback_dict = {}
        db = shelve.open('feedback.db', 'w')
        feedback_dict = db['Feedback']

        # feedback_dict.clear()
        feedback_dict.pop(id)

        db['Feedback'] = feedback_dict
        db.close()

        return redirect(url_for('manage_feedback'))
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/pendingFeedback', methods=['GET', 'POST'])
@login_required
def PendingFeedback():
    if session['logged_in'] == 'cs':
        filterform = feedbackfilter(request.form)
        feedDict = {}
        db = shelve.open('feedback.db', 'r')
        feedDict = db['Feedback']
        db.close()

        feedList = []
        Pendinglist = []
        for key in feedDict:
            feed = feedDict.get(key)
            feedList.append(feed)
            if feed.get_status() == "P":
                Pendinglist.append(feed)

        if request.method == "POST" and filterform.validate():
            varfilter = filterform.filter.data
            if varfilter == "":
                return redirect(url_for('manage_feedback'))
            elif varfilter == "Pending":
                return redirect(url_for('PendingFeedback'))
            elif varfilter == "Resolved":
                return redirect(url_for('ResolvedFeedback'))

        return render_template('Pendingfilter.html', feedList=feedList, count=len(feedList), form = filterform, Pendinglist = Pendinglist)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)
@app.route('/resolvedFeedback', methods=['GET', 'POST'])
@login_required
def ResolvedFeedback():
    if session['logged_in'] == 'cs':
        filterform = feedbackfilter(request.form)
        feedDict = {}
        db = shelve.open('feedback.db', 'r')
        feedDict = db['Feedback']
        db.close()

        feedList = []
        Resolvedlist = []
        for key in feedDict:
            feed = feedDict.get(key)
            feedList.append(feed)
            if feed.get_status() == "R":
                Resolvedlist.append(feed)

        if request.method == "POST" and filterform.validate():
            varfilter = filterform.filter.data
            if varfilter == "":
                return redirect(url_for('manage_feedback'))
            elif varfilter == "Pending":
                return redirect(url_for('PendingFeedback'))
            elif varfilter == "Resolved":
                return redirect(url_for('ResolvedFeedback'))

        return render_template('Resolvedfilter.html', feedList=feedList, count=len(feedList), form = filterform, Resolvedlist = Resolvedlist)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)
#create Task CS
@app.route('/createtaskcs', methods=['GET', 'POST'])
@login_required
def createtaskcs():
    if session['logged_in'] == 'cs':
        createtaskcs = CreateTaskFormCS(request.form)
        if request.method == 'POST' and createtaskcs.validate():

            taskcs_dict = {}
            db = shelve.open('task.db', 'c')

            try:
                taskcs_dict = db['Tasks']
            except:
                print("Error in retrieving Task from task.db.")

            current_id = 0
            for id in taskcs_dict:
                if id >= current_id and id < sys.maxsize:
                    current_id = id

                else:
                    current_id = 0

            User.Taskcs.count_id = current_id
            taskcs = User.Taskcs(
                             createtaskcs.urgency.data,
                             createtaskcs.remarks.data)
            taskcs_dict[taskcs.get_task_idcs()] = taskcs
            db['Tasks'] = taskcs_dict

            db.close()

            return redirect(url_for('retrievetaskcs'))

        return render_template('createtaskcs.html', form=createtaskcs)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/retrievetaskcs', methods=['GET', 'POST'])
@login_required
def retrievetaskcs():
    if session['logged_in'] == 'cs':
        filtertaskcs = taskfiltercs(request.form)
        taskcs_dict = {}
        db = shelve.open('task.db', 'r')
        taskcs_dict = db['Tasks']
        db.close()

        taskcs_list = []
        urgenttaskcs_list = []
        nutaskcs_list = []
        for key in taskcs_dict:
            taskcs = taskcs_dict.get(key)
            taskcs_list.append(taskcs)
            if taskcs.get_urgency() == "Urgent":
                urgenttaskcs_list.append(taskcs)
            elif taskcs.get_urgency() == "Not Urgent":
                nutaskcs_list.append(taskcs)

        if request.method == "POST" and filtertaskcs.validate():
            varfilter = filtertaskcs.filter.data
            if varfilter == "":
                return redirect(url_for('retrievetaskcs'))
            elif varfilter == "Urgent":
                return redirect(url_for('urgenttaskcs'))
            elif varfilter == "Not Urgent":
                return redirect(url_for('nutaskcs'))

        return render_template('retrievetaskcs.html', taskcs_list=taskcs_list, count=len(taskcs_list), form = filtertaskcs)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/updatetaskcs/<int:id>/', methods=['GET', 'POST'])
@login_required
def updatetaskcs(id):
    if session['logged_in'] == 'cs':
        update_task_form_cs = CreateTaskFormCS(request.form)
        if request.method == 'POST' and update_task_form_cs.validate():
            taskcs_dict = {}
            db = shelve.open('task.db', 'w')
            taskcs_dict = db['Tasks']

            taskcs = taskcs_dict.get(id)
            taskcs.set_urgency(update_task_form_cs.urgency.data)
            taskcs.set_remarks(update_task_form_cs.remarks.data)

            db['Tasks'] = taskcs_dict
            db.close()

            return redirect(url_for('retrievetaskcs'))
        else:
            taskcs_dict = {}
            db = shelve.open('task.db', 'r')
            taskcs_dict = db['Tasks']
            db.close()

            taskcs = taskcs_dict.get(id)
            update_task_form_cs.urgency.data = taskcs.get_urgency()
            update_task_form_cs.remarks.data = taskcs.get_remarks()

            return render_template('updatetaskcs.html', form=update_task_form_cs)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/deletetaskcs/<int:id>', methods=['POST'])
@login_required
def deletetaskcs(id):
    if session['logged_in'] == 'cs':
        taskcs_dict = {}
        db = shelve.open('task.db', 'w')
        taskcs_dict = db['Tasks']

        taskcs=taskcs_dict.pop(id)

        db['Tasks'] = taskcs_dict
        db.close()

        return redirect(url_for('retrievetaskcs'))
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/urgenttaskcs', methods=['GET', 'POST'])
@login_required
def urgenttaskcs():
    if session['logged_in'] == 'cs':
        filtertaskcs = taskfiltercs(request.form)
        taskcs_dict = {}
        db = shelve.open('task.db', 'r')
        taskcs_dict = db['Tasks']
        db.close()

        taskcs_list = []
        urgenttaskcs_list = []
        for key in taskcs_dict:
            taskcs = taskcs_dict.get(key)
            taskcs_list.append(taskcs)
            if taskcs.get_urgency() == "U":
                urgenttaskcs_list.append(taskcs)

        if request.method == "POST" and filtertaskcs.validate():
            varfilter = filtertaskcs.filter.data
            if varfilter == "":
                return redirect(url_for('retrievetaskcs'))
            elif varfilter == "Urgent":
                return redirect(url_for('urgenttaskcs'))
            elif varfilter == "Not Urgent":
                return redirect(url_for('nutaskcs'))

        return render_template('urgenttaskcs.html', taskcs_list=taskcs_list, count=len(taskcs_list), form = filtertaskcs, urgenttaskcs_list = urgenttaskcs_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/nutaskcs', methods=['GET', 'POST'])
@login_required
def nutaskcs():
    if session['logged_in'] == 'cs':
        filtertaskcs = taskfiltercs(request.form)
        taskcs_dict = {}
        db = shelve.open('task.db', 'r')
        taskcs_dict = db['Tasks']
        db.close()

        taskcs_list = []
        nutaskcs_list = []
        for key in taskcs_dict:
            taskcs = taskcs_dict.get(key)
            taskcs_list.append(taskcs)
            if taskcs.get_urgency() == "N":
                nutaskcs_list.append(taskcs)

        if request.method == "POST" and filtertaskcs.validate():
            varfilter = filtertaskcs.filter.data
            if varfilter == "":
                return redirect(url_for('retrievetaskcs'))
            elif varfilter == "Urgent":
                return redirect(url_for('urgenttaskcs'))
            elif varfilter == "Not Urgent":
                return redirect(url_for('nutaskcs'))

        return render_template('nutaskcs.html', taskcs_list=taskcs_list, count=len(taskcs_list), form = filtertaskcs, nutaskcs_list = nutaskcs_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

#Create Profile for CS/Staff
@app.route('/createprofilecs', methods=['GET', 'POST'])
@login_required
def createprofilecs():
    if session['logged_in'] == 'cs':
        create_profile_cs = CreateProfileCS(request.form)
        if request.method == 'POST' and create_profile_cs.validate():

            cs_dict = {}
            db = shelve.open('cs.db', 'c')

            try:
                cs_dict = db['CS']
            except:
                print("Error in retrieving CS from cs.db.")

            cs = User.CService(create_profile_cs.first_name.data, create_profile_cs.last_name.data,
                             create_profile_cs.gender.data, create_profile_cs.email.data, create_profile_cs.category.data,
                             create_profile_cs.remarks.data)
            cs_dict[cs.get_cs_id()] = cs
            db['CS'] = cs_dict

            db.close()
            return redirect(url_for('retrieveprofilecs'))

        return render_template('createprofilecs.html', form=create_profile_cs)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/retrieveprofilecs', methods=['GET', 'POST'])
@login_required
def retrieveprofilecs():
    if session['logged_in'] == 'cs':
        cs_dict = {}
        db = shelve.open('cs.db', 'r')
        cs_dict = db['CS']
        db.close()

        cs_list = []
        for key in cs_dict:
            cs = cs_dict.get(key)
            cs_list.append(cs)

        return render_template('retrieveprofilecs.html', count=len(cs_list), cs_list=cs_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/updateprofilecs/<int:id>/', methods=['GET', 'POST'])
@login_required
def updateprofilecs(id):
    if session['logged_in'] == 'cs':
        updateprofilecs = CreateProfileCS(request.form)
        if request.method == 'POST' and updateprofilecs.validate():
            cs_dict = {}
            db = shelve.open('cs.db', 'w')
            cs_dict = db['CS']

            cs = cs_dict.get(id)
            cs.set_first_name(updateprofilecs.first_name.data)
            cs.set_last_name(updateprofilecs.last_name.data)
            cs.set_gender(updateprofilecs.gender.data)
            cs.set_email(updateprofilecs.email.data)
            cs.set_category(updateprofilecs.category.data)
            cs.set_remarks(updateprofilecs.remarks.data)

            db['CS'] = cs_dict
            db.close()

            return redirect(url_for('retrieveprofilecs'))
        else:
            cs_dict = {}
            db = shelve.open('cs.db', 'r')
            cs_dict = db['CS']
            db.close()

            cs = cs_dict.get(id)
            updateprofilecs.first_name.data = cs.get_first_name()
            updateprofilecs.last_name.data = cs.get_last_name()
            updateprofilecs.gender.data = cs.get_gender()
            updateprofilecs.email.data = cs.get_email()
            updateprofilecs.category.data = cs.get_category()
            updateprofilecs.remarks.data = cs.get_remarks()

            return render_template('updateprofilecs.html', form=updateprofilecs)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/deleteprofilecs/<int:id>', methods=['POST'])
@login_required
def deleteprofilecs(id):
    if session['logged_in'] == 'cs':
        cs_dict = {}
        db = shelve.open('cs.db', 'w')
        cs_dict = db['CS']

        cs=cs_dict.pop(id)

        db['CS'] = cs_dict
        db.close()

        return redirect(url_for('retrieveprofilecs'))
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/createmessagetcs', methods=['GET', 'POST'])
@login_required
def createmessagetcs():
    if session['logged_in'] == 'cs':
        createmessagetcs = MessageTCS(request.form)
        if request.method == 'POST' and createmessagetcs.validate():

            messagetcs_dict = {}
            db = shelve.open('messagetcs.db', 'c')

            try:
                messagetcs_dict = db['MessageTCS']
            except:
                print("Error in retrieving Message from messagetcs.db.")

            current_id = 0
            for id in messagetcs_dict:
                if id >= current_id and id < sys.maxsize:
                    current_id = id

                else:
                    current_id = 0

            User.MessageTCS.count_id = current_id

            messagetcs = User.MessageTCS(createmessagetcs.name.data, createmessagetcs.message.data)
            messagetcs_dict[messagetcs.get_message_idtcs()] = messagetcs
            db['MessageTCS'] = messagetcs_dict

            db.close()
            return redirect(url_for('retrievemessagetcs'))

        return render_template('createmessagetcs.html', form=createmessagetcs)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/retrievemessagetcs', methods=['GET', 'POST'])
@login_required
def retrievemessagetcs():
    if session['logged_in'] == 'cs':
        messagetcs_dict = {}
        db = shelve.open('messagetcs.db', 'r')
        messagetcs_dict = db['MessageTCS']
        db.close()

        messagetcs_list = []
        for key in messagetcs_dict:
            messagetcs = messagetcs_dict.get(key)
            messagetcs_list.append(messagetcs)

        return render_template('retrievemessagetcs.html', count=len(messagetcs_list), messagetcs_list=messagetcs_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/updatemessagetcs/<int:id>/', methods=['GET', 'POST'])
@login_required
def updatemessagetcs(id):
    if session['logged_in'] == 'cs':
        updatemessagetcs = MessageTCS(request.form)
        if request.method == 'POST' and updatemessagetcs.validate():
            messagetcs_dict = {}
            db = shelve.open('messagetcs.db', 'w')
            messagetcs_dict = db['MessageTCS']

            messagetcs = messagetcs_dict.get(id)
            messagetcs.set_name(updatemessagetcs.name.data)
            messagetcs.set_message(updatemessagetcs.message.data)

            db['MessageTCS'] = messagetcs_dict
            db.close()

            return redirect(url_for('retrievemessagetcs'))
        else:
            messagetcs_dict = {}
            db = shelve.open('messagetcs.db', 'r')
            messagetcs_dict = db['MessageTCS']
            db.close()

            messagetcs = messagetcs_dict.get(id)
            updatemessagetcs.name.data = messagetcs.get_name()
            updatemessagetcs.message.data = messagetcs.get_message()

            return render_template('updatemessagetcs.html', form=updatemessagetcs)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/deletemessagetcs/<int:id>', methods=['POST'])
@login_required
def deletemessagetcs(id):
    if session['logged_in'] == 'cs':
        messagetcs_dict = {}
        db = shelve.open('messagetcs.db', 'w')
        messagetcs_dict = db['MessageTCS']

        messagetcs=messagetcs_dict.pop(id)

        db['MessageTCS'] = messagetcs_dict
        db.close()

        return redirect(url_for('retrievemessagetcs'))
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/forgetpassword', methods=['GET', 'POST'])
def forgetpassword():

    form = ForgetPasswordForm()
    if form.validate_on_submit():
        db = shelve.open('storage.db', 'r')
        users_dict = db['Teachers']
        db.close()

        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)

        for obj in users_list:

            if form.email.data == obj.get_email():
                id = obj.get_user_id()
                flash('OTP sent to your email. Please check your email.')
                return redirect(url_for('verifyOTP',id=id))

            else:
                flash('Please enter the correct email','danger')

    return render_template('forget_password.html',form=form)

@app.route('/verifyOTP/<int:id>', methods=['GET', 'POST'])
def verifyOTP(id):
    form = VerifyOTPForm()
    if form.validate_on_submit():
        # digits="0123456789"
        # OTP=""
        # for i in range(6):
        #     OTP +=digits[math.floor(random.random()*10)]
        # otp = OTP + " is your OTP"
        # msg= otp
        # flash(msg)
        if int(form.email.data) == 123456:
            flash('Verified','success')
            return redirect(url_for('reset_password',id=id))

        else:
            flash('Please enter the correct OTP','danger')

    return render_template('verifyOTP.html',form=form)

@app.route('/reset_password/<int:id>', methods=['GET', 'POST'])
def reset_password(id):
    form = ResetPasswordForm()
    if form.validate_on_submit():

        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Teachers']
        user = users_dict.get(id)

        hash = hashpassword(form.new_password.data)
        user.set_hash(hash[0])
        user.set_salt(hash[1])
        db['Teachers'] = users_dict
        db.close()
        flash('You have successfully reset your password!!', 'success')
        return redirect(url_for('login',id=id))

    return render_template('reset_password.html', form=form, id=id)

@app.route("/register/2fa/")
def register_2fa():
    # generating random secret key for authentication
    secret = pyotp.random_base32()
    return render_template("register_2FA.html", secret=secret)

@app.route("/register/2fa/", methods=["POST"])
def register_2fa_form():
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        # inform users if OTP is valid
        flash("The TOTP 2FA token is valid", "success")
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for("login"))

    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("register_2fa"))

#ayaka end

#justin start

@app.route("/student_feedback", methods=['GET', 'POST'])
@login_required
def student_feedback():
    if session['logged_in'] == 'student':
        feedDict = {}
        db = shelve.open('feedback.db', 'r')
        feedDict = db['Feedback']
        db.close()

        feedList = []
        for key in feedDict:
            feed = feedDict.get(key)
            feedList.append(feed)

        return render_template('student_feedback.html', feedList=feedList, count=len(feedList))
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)




@app.route("/student_create_feedback", methods=['GET', 'POST'])
@login_required
def student_create_feedback():
    if session['logged_in'] == 'student':
        feedbackForm = FeedbackForm(request.form)
        if request.method == 'POST' and feedbackForm.validate():
            feedDict = {}
            db = shelve.open('feedback.db', 'c')

            try:
                feedDict = db['Feedback']

            except:
                print("Error in retrieving Feedback from feedback.db.")

            # id = 0
            # for i in feedDict:
            #     if int(i) > id:
            #         id = int(i)
            # if recentcount >= 0:
            #    id = recentcount

            id = uuid.uuid1()
            print(id)

            feed = User.Feedback(id, feedbackForm.firstName.data, feedbackForm.email.data, feedbackForm.type.data,
                                     feedbackForm.category.data, feedbackForm.remarks.data, feedbackForm.status.data, date = date.today())

            feedDict[feed.get_feedID()] = feed
            db['Feedback'] = feedDict

            db.close()

            return redirect(url_for('student_feedback'))
        return render_template("student_create_feedback.html", form=feedbackForm)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)



#justin stat

@app.route('/createProfile', methods=['GET', 'POST'])
@login_required
def create_profile():
    if session['logged_in'] == 'student':
        create_profile_form = CreateUserProfileForm(request.form)
        if request.method == 'POST' and create_profile_form.validate():
            profiles_dict = {}
            db = shelve.open('storageUserProfile.db', 'c')

            try:
                profiles_dict = db['Profiles']
            except:
                print("Error in retrieving Profiles from storageUserProfile.db.")

            profile = UserProfile.UserProfile(create_profile_form.first_name.data, create_profile_form.last_name.data,
                                              create_profile_form.gender.data, create_profile_form.email.data,
                                              create_profile_form.certificates.data)
            profiles_dict[profile.get_profile_id()] = profile
            db['Profiles'] = profiles_dict

            db.close()

            session['profile_created'] = profile.get_first_name() + ' ' + profile.get_last_name()

            return redirect(url_for('final_profile'))
        return render_template('createUserProfile.html', form=create_profile_form)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/retrieveProfiles')
@login_required
def retrieve_profiles():
    if session['logged_in'] == 'student':
        profiles_dict = {}
        db = shelve.open('storageUserProfile.db', 'r')
        profiles_dict = db['Profiles']
        db.close()

        profiles_list = []
        for key in profiles_dict:
            profile = profiles_dict.get(key)
            profiles_list.append(profile)

        return render_template('retrieveUserProfiles.html', count=len(profiles_list), profiles_list=profiles_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/updateProfileStudent/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_profile_student(id):
    if session['logged_in'] == 'student':
        update_profile_form = CreateUserProfileForm(request.form)
        if request.method == 'POST' and update_profile_form.validate():
            profiles_dict = {}
            db = shelve.open('storageUserProfile.db', 'w')
            profiles_dict = db['Profiles']

            profile = profiles_dict.get(id)
            profile.set_first_name(update_profile_form.first_name.data)
            profile.set_last_name(update_profile_form.last_name.data)
            profile.set_gender(update_profile_form.gender.data)
            profile.set_email(update_profile_form.email.data)
            profile.set_certificates(update_profile_form.certificates.data)

            db['Profiles'] = profiles_dict
            db.close()

            session['profile_updated'] = profile.get_first_name() + ' ' + profile.get_last_name()

            return redirect(url_for('final_profile'))
        else:
            profiles_dict = {}
            db = shelve.open('storageUserProfile.db', 'r')
            profiles_dict = db['Profiles']
            db.close()

            profile = profiles_dict.get(id)
            update_profile_form.first_name.data = profile.get_first_name()
            update_profile_form.last_name.data = profile.get_last_name()
            update_profile_form.gender.data = profile.get_gender()
            update_profile_form.email.data = profile.get_email()
            update_profile_form.certificates.data = profile.get_certificates()

            return render_template('updateUserProfile.html', form=update_profile_form)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/deleteProfileStudent/<int:id>', methods=['POST'])
@login_required
def delete_profile_student(id):
    if session['logged_in'] == 'student':
        profiles_dict = {}
        db = shelve.open('storageUserProfile.db', 'w')
        profiles_dict = db['Profiles']

        profile = profiles_dict.pop(id)

        db['Profiles'] = profiles_dict
        db.close()

        session['profile_deleted'] = profile.get_first_name() + ' ' + profile.get_last_name()

        return redirect(url_for('retrieve_profiles'))
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/final_profile')
@login_required
def final_profile():
    if session['logged_in'] == 'student':
        profiles_dict = {}
        db = shelve.open('storageUserProfile.db', 'r')
        profiles_dict = db['Profiles']
        db.close()

        profiles_list = []
        for key in profiles_dict:
            profile = profiles_dict.get(key)
            profiles_list.append(profile)

        interests_dict = {}
        db = shelve.open('storageUserInterest.db', 'r')
        interests_dict = db['Interests']
        db.close()

        interests_list = []
        for key in interests_dict:
            interest = interests_dict.get(key)
            interests_list.append(interest)

        return render_template('finalprofile.html', profiles_list=profiles_list, interests_list=interests_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/createInterest', methods=['GET', 'POST'])
@login_required
def create_interest():
    if session['logged_in'] == 'student':
        create_interest_form = CreateUserInterestForm(request.form)
        if request.method == 'POST' and create_interest_form.validate():
            interests_dict = {}
            db = shelve.open('storageUserInterest.db', 'c')

            try:
                interests_dict = db['Interests']
            except:
                print('Error in retrieving Interests from storageUserInterest.db.')

            interest = UserInterest.UserInterest(create_interest_form.fav.data, create_interest_form.hate.data)
            interests_dict[interest.get_interest_id()] = interest
            db['Interests'] = interests_dict

            db.close()

            return redirect(url_for('final_profile'))
        return render_template('createUserInterest.html', form=create_interest_form)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/retrieveInterest')
@login_required
def retrieve_interests():
    if session['logged_in'] == 'student':
        interests_dict = {}
        db = shelve.open('storageUserInterest.db', 'r')
        interests_dict = db['Interests']
        db.close()

        interests_list = []
        for key in interests_dict:
            interest = interests_dict.get(key)
            interests_list.append(interest)

        return render_template('retrieveUserInterest.html', count=len(interests_list), interests_list=interests_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/updateInterest/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_interest(id):
    if session['logged_in'] == 'student':
        update_interest_form = CreateUserInterestForm(request.form)
        if request.method == 'POST' and update_interest_form.validate():
            interests_dict = {}
            db = shelve.open('storageUserInterest.db', 'w')
            interests_dict = db['Interests']

            interest = interests_dict.get(id)
            interest.set_fav(update_interest_form.fav.data)
            interest.set_hate(update_interest_form.hate.data)

            db['Interests'] = interests_dict
            db.close()


            return redirect(url_for('retrieve_interests'))
        else:
            interests_dict = {}
            db = shelve.open('storageUserInterest.db', 'r')
            interests_dict = db['Interests']
            db.close()

            interest = interests_dict.get(id)
            update_interest_form.fav.data = interest.get_fav()
            update_interest_form.hate.data = interest.get_hate()

            return render_template('updateUserInterest.html', form=update_interest_form)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/deleteInterest/<int:id>', methods=['POST'])
@login_required
def delete_interest(id):
    if session['logged_in'] == 'student':
        interests_dict = {}
        db = shelve.open('storageUserInterest.db', 'w')
        interests_dict = db['Interests']

        interest = interests_dict.pop(id)

        db['Interests'] = interests_dict
        db.close()


        return redirect(url_for('retrieve_interests'))
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/createStudentRequest', methods=['GET', 'POST'])
@login_required
def create_studentrequest():
    if session['logged_in'] == 'student':
        create_studentrequest_form = CreateStudentRequestForm(request.form)
        if request.method == 'POST' and create_studentrequest_form.validate():
            studentrequests_dict = {}
            db = shelve.open('storageStudentRequest.db', 'c')

            try:
                studentrequests_dict = db['StudentRequests']
            except:
                print("Error in retrieving StudentRequests from storageStudentRequest.db.")

            studentrequest = StudentRequest.StudentRequest(create_studentrequest_form.first_name.data,
                                                           create_studentrequest_form.last_name.data,
                                                           create_studentrequest_form.gender.data,
                                                           create_studentrequest_form.email.data,
                                                           create_studentrequest_form.size.data,
                                                           create_studentrequest_form.day.data,
                                                           create_studentrequest_form.timeslot.data)
            studentrequests_dict[studentrequest.get_studentrequest_id()] = studentrequest
            db['StudentRequests'] = studentrequests_dict

            db.close()

            session['studentrequest_created'] = studentrequest.get_first_name() + ' ' + studentrequest.get_last_name()

            return redirect(url_for('retrieve_studentrequests'))
        return render_template('createStudentRequest.html', form=create_studentrequest_form)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/retrieveStudentRequests')
@login_required
def retrieve_studentrequests():
    if session['logged_in'] == 'student':
        studentrequests_dict = {}
        db = shelve.open('storageStudentRequest.db', 'r')
        studentrequests_dict = db['StudentRequests']
        db.close()

        studentrequests_list = []
        for key in studentrequests_dict:
            studentrequest = studentrequests_dict.get(key)
            studentrequests_list.append(studentrequest)

        return render_template('retrieveStudentRequest.html', count=len(studentrequests_list),
                               studentrequests_list=studentrequests_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/updateStudentRequest/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_studentrequest(id):
    if session['logged_in'] == 'student':
        update_studentrequest_form = CreateStudentRequestForm(request.form)
        if request.method == 'POST' and update_studentrequest_form.validate():
            studentrequests_dict = {}
            db = shelve.open('storageStudentRequest.db', 'w')
            studentrequests_dict = db['StudentRequests']

            studentrequest = studentrequests_dict.get(id)
            studentrequest.set_first_name(update_studentrequest_form.first_name.data)
            studentrequest.set_last_name(update_studentrequest_form.last_name.data)
            studentrequest.set_gender(update_studentrequest_form.gender.data)
            studentrequest.set_email(update_studentrequest_form.email.data)
            studentrequest.set_size(update_studentrequest_form.size.data)
            studentrequest.set_day(update_studentrequest_form.day.data)
            studentrequest.set_timeslot(update_studentrequest_form.timeslot.data)

            db['StudentRequests'] = studentrequests_dict
            db.close()

            session['studentrequest_updated'] = studentrequest.get_first_name() + ' ' + studentrequest.get_last_name()

            return redirect(url_for('retrieve_studentrequests'))
        else:
            studentrequests_dict = {}
            db = shelve.open('storageStudentRequest.db', 'r')
            studentrequests_dict = db['StudentRequests']
            db.close()

            studentrequest = studentrequests_dict.get(id)
            update_studentrequest_form.first_name.data = studentrequest.get_first_name()
            update_studentrequest_form.last_name.data = studentrequest.get_last_name()
            update_studentrequest_form.gender.data = studentrequest.get_gender()
            update_studentrequest_form.email.data = studentrequest.get_email()
            update_studentrequest_form.size.data = studentrequest.get_size()
            update_studentrequest_form.day.data = studentrequest.get_day()
            update_studentrequest_form.timeslot.data = studentrequest.get_timeslot()

            return render_template('updateStudentRequest.html', form=update_studentrequest_form)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)


@app.route('/deleteStudentRequest/<int:id>', methods=['POST'])
@login_required
def delete_studentrequest(id):
    if session['logged_in'] == 'student':
        studentrequests_dict = {}
        db = shelve.open('storageStudentRequest.db', 'w')
        studentrequests_dict = db['StudentRequests']

        studentrequest = studentrequests_dict.pop(id)

        db['StudentRequests'] = studentrequests_dict
        db.close()

        session['studentrequest_deleted'] = studentrequest.get_first_name() + ' ' + studentrequest.get_last_name()

        return redirect(url_for('retrieve_studentrequests'))
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

#justin end



#weilun
@app.route('/', methods=['GET', 'POST'])
def home():
    session.clear()
    print(session)

    create_email_subscription_form = EmailSubscription(request.form)
    if request.method == 'POST' and create_email_subscription_form.validate():
        email_subscription_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            email_subscription_dict = db['Email_Subscription']
        except:
            print("Error in retrieving Users from storage.db.")

        email_subscription = Email_Subscription.Email_Subscription(create_email_subscription_form.emailsubscription_name.data, create_email_subscription_form.emailsubscription_email.data)
        email_subscription_dict[email_subscription.get_email_subscription_id()] = email_subscription
        db['Email_Subscription'] = email_subscription_dict

        db.close()
        print(email_subscription_dict[1])

        return redirect(url_for('home'))
    return render_template('home.html', form=create_email_subscription_form)



@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if session['logged_in'] == 'admin':
        #retrieve tasks
        task_dict = {}
        try:
            db = shelve.open('storage.db', 'r')
            task_dict = db['Tasks']
            db.close()
        except:
            print("Storage DB not found")

        task_list = []
        for key in task_dict:
            task = task_dict.get(key)
            task_list.append(task)

        #retreieve user account
        users_dict = {}
        try:
            db = shelve.open('storage.db', 'r')
            users_dict = db['Users']
            db.close()
        except:
            print("Storage DB not found")
        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)
        return render_template('admin_dashboard.html', task_list=task_list, users_list=users_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/admin_dashboard_update_list')
@login_required
def admin_dashboard_update_list():
    if session['logged_in'] == 'admin':
        task_dict = {}
        try:
            db = shelve.open('storage.db', 'r')
            task_dict = db['Tasks']
            db.close()
        except:
            print("Storage DB not found")

        task_list = []
        for key in task_dict:
            task = task_dict.get(key)
            task_list.append(task)

        print("admin_dashboard: ", task_dict)
        return render_template('admin_dashboard_update_list.html', task_list=task_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/admin_profile')
@login_required
def admin_profile():
    if session['logged_in'] == 'admin':
        admin_profile_dict = {}
        try:
            db = shelve.open('storage.db', 'r')
            admin_profile_dict = db['Admin_Profile']
            db.close()
        except:
            print("Admin Profile not found in storage DB.")
        admin_profile_list = []
        for key in admin_profile_dict:
            admin_profile = admin_profile_dict.get(key)
            admin_profile_list.append(admin_profile)

        return render_template('admin_profile.html', admin_profile_list=admin_profile_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/admin_profile_create', methods=['GET', 'POST'])
@login_required
def admin_profile_create():
    if session['logged_in'] == 'admin':
        create_admin_profile = CreateAdminProfile(request.form)
        if request.method == 'POST' and create_admin_profile.validate():
            admin_profile_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                admin_profile_dict = db['Admin_Profile']
            except:
                print("Error in retrieving Admin Profile from storage.db.")
            admin_profile = AdminProfile.AdminProfile(create_admin_profile.company.data, create_admin_profile.username.data, create_admin_profile.admin_email.data,
                             create_admin_profile.admin_first_name.data, create_admin_profile.admin_last_name.data, create_admin_profile.address.data, create_admin_profile.city.data,
                            create_admin_profile.country.data, create_admin_profile.postal_code.data)
            admin_profile_dict[admin_profile.get_admin_profile_id()] = admin_profile
            db['Admin_Profile'] = admin_profile_dict
            db.close()


            return redirect(url_for('admin_profile'))

        return render_template('admin_profile_create.html', form=create_admin_profile)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/admin_profile_update/<int:id>/', methods=['GET', 'POST'])
@login_required
def admin_profile_update(id):
    if session['logged_in'] == 'admin':
        update_admin_profile = CreateAdminProfile(request.form)
        if request.method == 'POST' and update_admin_profile.validate():

            db = shelve.open('storage.db', 'w')
            admin_profile_dict = db['Admin_Profile']

            admin_profile = admin_profile_dict.get(id)
            admin_profile.set_company(update_admin_profile.company.data)
            admin_profile.set_username(update_admin_profile.username.data)
            admin_profile.set_admin_email(update_admin_profile.admin_email.data)
            admin_profile.set_admin_first_name(update_admin_profile.admin_first_name.data)
            admin_profile.set_admin_last_name(update_admin_profile.admin_last_name.data)
            admin_profile.set_address(update_admin_profile.address.data)
            admin_profile.set_city(update_admin_profile.city.data)
            admin_profile.set_country(update_admin_profile.country.data)
            admin_profile.set_postal_code(update_admin_profile.postal_code.data)

            db['Admin_Profile'] = admin_profile_dict
            db.close()


            return redirect(url_for('admin_profile'))
        else:
            admin_profile_dict = {}
            db = shelve.open('storage.db', 'r')
            admin_profile_dict = db['Admin_Profile']
            db.close()

            admin_profile = admin_profile_dict.get(id)
            update_admin_profile.company.data = admin_profile.get_company()
            update_admin_profile.username.data = admin_profile.get_username()
            update_admin_profile.admin_email.data = admin_profile.get_admin_email()
            update_admin_profile.admin_first_name.data = admin_profile.get_admin_first_name()
            update_admin_profile.admin_last_name.data = admin_profile.get_admin_last_name()
            update_admin_profile.address.data = admin_profile.get_address()
            update_admin_profile.city.data = admin_profile.get_city()
            update_admin_profile.country.data = admin_profile.get_country()
            update_admin_profile.postal_code.data = admin_profile.get_postal_code()

            return render_template('admin_profile_update.html', form=update_admin_profile)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/DeleteAdminProfile/<int:id>', methods=['POST'])
@login_required
def admin_profile_delete(id):
    if session['logged_in'] == 'admin':
        admin_profile_dict = {}
        db = shelve.open('storage.db', 'w')
        admin_profile_dict = db['Admin_Profile']

        admin_profile_dict.pop(id)

        db['Admin_Profile'] = admin_profile_dict
        db.close()

        return redirect(url_for('admin_profile'))
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/cs_message')
@login_required
def cs_message():
    if session['logged_in'] == 'admin':
        staff_message_dict = {}
        try:
            db = shelve.open('storage.db', 'r')
            staff_message_dict = db['Staff_Message']
            db.close()
        except:
            print("staff message not found")

        staff_message_list = []
        for key in staff_message_dict:
            staff_message = staff_message_dict.get(key)
            staff_message_list.append(staff_message)


        return render_template('cs_message.html', staff_message_list=staff_message_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/cs_message_create', methods=['GET', 'POST'])
@login_required
def cs_message_create():
    if session['logged_in'] == 'admin':
        create_staff_message_form = CreateStaffMessage(request.form)
        if request.method == 'POST' and create_staff_message_form.validate():

            staff_message_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                staff_message_dict = db['Staff_Message']
            except:
                print("Error in retrieving Users from storage.db.")

            staff_message = Staff_Message.Staff_Message(create_staff_message_form.message_name.data, create_staff_message_form.message_email.data, create_staff_message_form.message.data)
            staff_message_dict[staff_message.get_message_count_id()] = staff_message
            db['Staff_Message'] = staff_message_dict

            db.close()


            return redirect(url_for('cs_message'))
        return render_template('cs_message_create.html', form=create_staff_message_form)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/cs_message_update/<int:id>/', methods=['GET', 'POST'])
@login_required
def cs_message_update(id):
    if session['logged_in'] == 'admin':
        update_staff_message_form = CreateStaffMessage(request.form)
        if request.method == 'POST' and update_staff_message_form.validate():
            staff_message_dict = {}
            db = shelve.open('storage.db', 'w')
            staff_message_dict = db['Staff_Message']

            staff_message = staff_message_dict.get(id)
            staff_message.set_message_name(update_staff_message_form.message_name.data)
            staff_message.set_message_email(update_staff_message_form.message_email.data)
            staff_message.set_message(update_staff_message_form.message.data)
            db['Staff_Message'] = staff_message_dict
            db.close()



            return redirect(url_for('cs_message'))
        else:
            staff_message_dict = {}
            db = shelve.open('storage.db', 'r')
            staff_message_dict = db['Staff_Message']
            db.close()

            staff_message = staff_message_dict.get(id)
            update_staff_message_form.message_name.data = staff_message.get_message_name()
            update_staff_message_form.message_email.data = staff_message.get_message_email()
            update_staff_message_form.message.data = staff_message.get_message()


            return render_template('cs_message_update.html', form=update_staff_message_form)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/delete_cs_message/<int:id>', methods=['POST'])
@login_required
def cs_message_delete(id):
    if session['logged_in'] == 'admin':
        staff_message_dict = {}
        db = shelve.open('storage.db', 'w')
        staff_message_dict = db['Staff_Message']

        staff_message_dict.pop(id)

        db['Staff_Message'] = staff_message_dict
        db.close()

        return redirect(url_for('cs_message'))
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/cs_email_subscription_retrieve')
@login_required
def cs_email_subscription_retrieve():
    if session['logged_in'] == 'admin':
        email_subscription_dict = {}
        try:
            db = shelve.open('storage.db', 'r')
            email_subscription_dict = db['Email_Subscription']
            db.close()
        except:
            print("email subscription not found")

        email_subscription_list = []
        for key in email_subscription_dict:
            email_subscription = email_subscription_dict.get(key)
            email_subscription_list.append(email_subscription)


        return render_template('cs_email_subscription_retrieve.html', email_subscription_list=email_subscription_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/staff_message')
@login_required
def staff_message():
    if session['logged_in'] == 'admin':
        staff_message_dict = {}
        try:
            db = shelve.open('storage.db', 'r')
            staff_message_dict = db['Staff_Message']
            db.close()
        except:
            print("staff message not found")

        staff_message_list = []
        for key in staff_message_dict:
            staff_message = staff_message_dict.get(key)
            staff_message_list.append(staff_message)


        return render_template('staff_message.html', staff_message_list=staff_message_list)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/staff_message_create', methods=['GET', 'POST'])
@login_required
def staff_message_create():
    if session['logged_in'] == 'admin':
        create_staff_message_form = CreateStaffMessage(request.form)
        if request.method == 'POST' and create_staff_message_form.validate():

            staff_message_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                staff_message_dict = db['Staff_Message']
            except:
                print("Error in retrieving Users from storage.db.")

            staff_message = Staff_Message.Staff_Message(create_staff_message_form.message_name.data, create_staff_message_form.message_email.data, create_staff_message_form.message.data)
            staff_message_dict[staff_message.get_message_count_id()] = staff_message
            db['Staff_Message'] = staff_message_dict

            db.close()


            return redirect(url_for('staff_message'))
        return render_template('staff_message_create.html', form=create_staff_message_form)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/staff_message_update/<int:id>/', methods=['GET', 'POST'])
@login_required
def staff_message_update(id):
    if session['logged_in'] == 'admin':
        update_staff_message_form = CreateStaffMessage(request.form)
        if request.method == 'POST' and update_staff_message_form.validate():
            staff_message_dict = {}
            db = shelve.open('storage.db', 'w')
            staff_message_dict = db['Staff_Message']

            staff_message = staff_message_dict.get(id)
            staff_message.set_message_name(update_staff_message_form.message_name.data)
            staff_message.set_message_email(update_staff_message_form.message_email.data)
            staff_message.set_message(update_staff_message_form.message.data)
            db['Staff_Message'] = staff_message_dict
            db.close()



            return redirect(url_for('staff_message'))
        else:
            staff_message_dict = {}
            db = shelve.open('storage.db', 'r')
            staff_message_dict = db['Staff_Message']
            db.close()

            staff_message = staff_message_dict.get(id)
            update_staff_message_form.message_name.data = staff_message.get_message_name()
            update_staff_message_form.message_email.data = staff_message.get_message_email()
            update_staff_message_form.message.data = staff_message.get_message()


            return render_template('staff_message_update.html', form=update_staff_message_form)
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

@app.route('/delete_staff_message/<int:id>', methods=['POST'])
@login_required
def staff_message_delete(id):
    if session['logged_in'] == 'admin':
        staff_message_dict = {}
        db = shelve.open('storage.db', 'w')
        staff_message_dict = db['Staff_Message']

        staff_message_dict.pop(id)

        db['Staff_Message'] = staff_message_dict
        db.close()

        return redirect(url_for('staff_message'))
    else:
        role = session['logged_in']
        return render_template('unauthorisedaccess.html', role=role)

# retrieveuser
@app.route('/manage_user')
@login_required
def manage_user():
    users_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
    except:
        print("Storage DB not found")
    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    cs_dict = {}
    try:
        db = shelve.open('cs.db', 'r')
        cs_dict = db['CS']
        db.close()
    except:
        print("Storage DB not found")
    cs_list = []
    for key in cs_dict:
        cs = cs_dict.get(key)
        cs_list.append(cs)

    try:
        db = shelve.open('storage.db', 'r')
        users_dict = db['Teachers']
        db.close()
    except:
        print("error in retrieving teachers")
    user_list = []
    for key in users_dict:
        obj = users_dict[key]
        user_list.append(obj)


    return render_template('manage_user.html', count=len(users_list), users_list=users_list, countcs=len(cs_list), cs_list=cs_list, user_list=user_list)


# updateuser
@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_email(update_user_form.email.data)
        user.set_gender(update_user_form.gender.data)
        user.set_role(update_user_form.role.data)
        user.set_remarks(update_user_form.remarks.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('manage_user'))
    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.role.data = user.get_role()
        update_user_form.remarks.data = user.get_remarks()

        return render_template('updateUser.html', form=update_user_form)


# create user
@app.route('/createUser', methods=['GET', 'POST'])
@login_required
def createUser():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        user = User.User(create_user_form.first_name.data, create_user_form.last_name.data, create_user_form.email.data,
                         create_user_form.gender.data, create_user_form.role.data, create_user_form.remarks.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        # Test codes
        users_dict = db['Users']
        user = users_dict[user.get_user_id()]
        print(user.get_first_name(), user.get_last_name(), "was stored in storage.db successfully with user_id ==",
              user.get_user_id())

        db.close()

        return redirect(url_for('manage_user'))
    return render_template('createUser.html', form=create_user_form)


# ----- end of create user

# createuser
@app.route('/deleteUser/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    users_dict = {}
    db = shelve.open('storage.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('manage_user'))


@app.route('/test1/')
def test1():
    return render_template('test1.html')


@app.route('/createTask', methods=['GET', 'POST'])
@login_required
def create_Task():
    create_admin_form_task = CreateAdminFormTask(request.form)

    if request.method == 'POST' and create_admin_form_task.validate():
        task_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            task_dict = db['Tasks']
            print(db["Tasks"])
        except:
            print("Error in retrieving Users from storage.db.")

        task = Task.Task(create_admin_form_task.task.data, create_admin_form_task.done_by.data)
        task_dict[task.get_task_id()] = task
        db['Tasks'] = task_dict
        db.close()

        print("create_Task: ", task_dict)
        return redirect(url_for('admin_dashboard'))
    return render_template('createTask.html', form=create_admin_form_task)

@app.route('/updateTask/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_task(id):
    update_task_form = CreateAdminFormTask(request.form)
    if request.method == 'POST' and update_task_form.validate():
        task_dict = {}
        db = shelve.open('storage.db', 'w')
        task_dict = db['Tasks']

        task = task_dict.get(id)
        task.set_task(update_task_form.task.data)
        task.set_done_by(update_task_form.done_by.data)


        db['Tasks'] = task_dict
        db.close()

        return redirect(url_for('admin_dashboard_update_list'))
    else:
        task_dict = {}
        db = shelve.open('storage.db', 'r')
        task_dict = db['Tasks']
        db.close()

        task = task_dict.get(id)
        update_task_form.task.data = task.get_task()
        update_task_form.done_by.data = task.get_done_by()

        return render_template('updateTask.html', form=update_task_form)

@app.route('/deleteTask/<int:id>', methods=['POST'])
@login_required
def delete_task(id):
    task_dict = {}
    db = shelve.open('storage.db', 'w')
    task_dict = db['Tasks']

    task_dict.pop(id)

    db['Tasks'] = task_dict
    db.close()

    return redirect(url_for('admin_dashboard_update_list'))

@app.route('/email_subscription_retrieve')
@login_required
def email_subscription_retrieve():
    email_subscription_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        email_subscription_dict = db['Email_Subscription']
        db.close()
    except:
        print("email subscription not found")

    email_subscription_list = []
    for key in email_subscription_dict:
        email_subscription = email_subscription_dict.get(key)
        email_subscription_list.append(email_subscription)


    return render_template('email_subscription_retrieve.html', email_subscription_list=email_subscription_list)

@app.route('/email_subscription_update/<int:id>/', methods=['GET', 'POST'])
@login_required
def email_subscription_update(id):
    update_email_subscription_form = EmailSubscription(request.form)
    if request.method == 'POST' and update_email_subscription_form.validate():
        email_subscription_dict = {}
        db = shelve.open('storage.db', 'w')
        email_subscription_dict = db['Email_Subscription']

        email_subscription = email_subscription_dict.get(id)
        email_subscription.set_email_subscription_name(update_email_subscription_form.emailsubscription_name.data)
        email_subscription.set_email_subscription_email(update_email_subscription_form.emailsubscription_email.data)


        db['Email_Subscription'] = email_subscription_dict
        db.close()



        return redirect(url_for('email_subscription_retrieve'))
    else:
        email_subscription_dict = {}
        db = shelve.open('storage.db', 'r')
        email_subscription_dict = db['Email_Subscription']
        db.close()

        email_subscription = email_subscription_dict.get(id)
        update_email_subscription_form.emailsubscription_name.data = email_subscription.get_email_subscription_name()
        update_email_subscription_form.emailsubscription_email.data = email_subscription.get_email_subscription_email()
        return render_template('email_subscription_update.html', form=update_email_subscription_form)

@app.route('/email_subscription_delete/<int:id>', methods=['POST'])
@login_required
def email_subscription_delete(id):
    email_subscription_dict = {}
    db = shelve.open('storage.db', 'w')
    email_subscription_dict = db['Email_Subscription']

    email_subscription_dict.pop(id)

    db['Email_Subscription'] = email_subscription_dict
    db.close()

    return redirect(url_for('email_subscription_retrieve'))

@app.route('/admin_update_profile_cs/<int:id>/', methods=['GET', 'POST'])
@login_required
def admin_update_profile_cs(id):
    updateprofilecs = CreateProfileCS(request.form)
    if request.method == 'POST' and updateprofilecs.validate():
        cs_dict = {}
        db = shelve.open('cs.db', 'w')
        cs_dict = db['CS']

        cs = cs_dict.get(id)
        cs.set_first_name(updateprofilecs.first_name.data)
        cs.set_last_name(updateprofilecs.last_name.data)
        cs.set_gender(updateprofilecs.gender.data)
        cs.set_email(updateprofilecs.email.data)
        cs.set_category(updateprofilecs.category.data)
        cs.set_remarks(updateprofilecs.remarks.data)

        db['CS'] = cs_dict
        db.close()

        return redirect(url_for('manage_user'))
    else:
        cs_dict = {}
        db = shelve.open('cs.db', 'r')
        cs_dict = db['CS']
        db.close()

        cs = cs_dict.get(id)
        updateprofilecs.first_name.data = cs.get_first_name()
        updateprofilecs.last_name.data = cs.get_last_name()
        updateprofilecs.gender.data = cs.get_gender()
        updateprofilecs.email.data = cs.get_email()
        updateprofilecs.category.data = cs.get_category()
        updateprofilecs.remarks.data = cs.get_remarks()

        return render_template('admin_update_profile_cs.html', form=updateprofilecs)

@app.route('/admin_delete_profile_cs/<int:id>', methods=['POST'])
@login_required
def admin_delete_profile_cs(id):
    cs_dict = {}
    db = shelve.open('cs.db', 'w')
    cs_dict = db['CS']

    cs=cs_dict.pop(id)

    db['CS'] = cs_dict
    db.close()

    return redirect(url_for('manage_user'))

#hoyjtun start
def hashpassword(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    return hashed_password, salt


def check_hash(password, salt):
    password = (password + salt).encode('utf-8')
    hash2 = hashlib.sha512(password).hexdigest()
    return hash2


#hoyjtun end


if __name__ == '__main__':
    app.run(ssl_context="adhoc")
