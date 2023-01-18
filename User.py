class Teacher:
    count_id = 0

    def __init__(self, first_name, last_name, email, hash, salt):
        Teacher.count_id += 1
        self.__user_id = Teacher.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__experience = ''
        self.__education = ''
        self.__skills = ''
        self.__mobile_phone = ''
        self.__link = ''
        self.__social_media = ''
        self.__birthdate = ''
        self.__gender = ''
        self.__language = ''
        self.__location = ''
        self.__occupation = ''
        self.__students = [] #store obj(no nested list, and change the display on the html), when integrate use obj.get_name() ...(also change the mutator method)
        self.__students_request = [['Req1', 'req1@gmail.com', 'Group', '2pm-3pm'], ['Req2', 'req2@gmail.com', 'Individual', '4pm-5pm'], ['Req3', 'req3@gmail.com', 'Group', '5pm-6pm']] #store obj(no nested list, and change the display on the html), when integrate use obj.get_name() ...(also change the mutator method)
        self.__individual_timetable = [["2020-12-30", "0200-0300", "John", "John@email.com"], ["2020-12-31", "0300-0400", "Sam", "Sam@email.com"]]
        self.__group_timetable = [["2020-12-30", '0200-0300', '2'], ["2020-12-31", '0300-0400', '3']]
        self.__ticket = []
        self.__rating = ''
        self.__review = ''
        self.__picture = 'default.jpg'
        self.__hash = hash
        self.__salt = salt
#Accessor Methods

    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email


    def get_experience(self):
        return self.__experience

    def get_education(self):
        return self.__education

    def get_skills(self):
        return self.__skills

    def get_mobile_phone(self):
        return self.__mobile_phone

    def get_experience(self):
        return self.__experience

    def get_link(self):
        return self.__link

    def get_social_media(self):
        return self.__social_media

    def get_birthdate(self):
        return self.__birthdate

    def get_gender(self):
        return self.__gender

    def get_language(self):
        return self.__language

    def get_location(self):
        return self.__location

    def get_occupation(self):
        return self.__occupation

    def get_students(self):
        return self.__students

    def get_students_request(self):
        return self.__students_request

    def get_individual_timetable(self):
        return self.__individual_timetable

    def get_group_timetable(self):
        return self.__group_timetable

    def get_ticket(self):
        return self.__ticket

    def get_rating(self):
        return self.__rating

    def get_review(self):
        return self.__review
    def get_picture(self):
        return self.__picture
    def get_hash(self):
        return self.__hash
    def get_salt(self):
        return self.__salt
#Mutator Methods

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email


    def set_experience(self, experience):
        self.__experience = experience

    def set_education(self, education):
        self.__education = education

    def set_skills(self, skills):
        self.__skills = skills

    def set_mobile_phone(self, mobile_phone):
        self.__mobile_phone = mobile_phone

    def set_link(self, link):
        self.__link = link

    def set_social_media(self, social_media):
        self.__social_media = social_media

    def set_birthdate(self, birthdate):
        self.__birthdate = birthdate

    def set_gender(self, gender):
        self.__gender = gender

    def set_language(self, language):
        self.__language = language

    def set_location(self, location):
        self.__location = location

    def set_occupation(self, occupation):
        self.__occupation = occupation

    def set_students(self, students):
        self.__students = students

    def set_students_request(self, students_request):
        self.__students_request = students_request

    def set_individual_timetable(self, individual_timetable):
        self.__individual_timetable = individual_timetable

    def set_gourp_timetable(self, group_timetable):
        self.__group_timetable = group_timetable

    def set_ticket(self, ticket):
        self.__ticket = ticket

    def set_rating(self, rating):
        self.__rating = rating

    def set_review(self, review):
        self.__review = review
    def set_picture(self, picture):
        self.__picture = picture

    def set_hash(self, hash):
        self.__hash = hash
    def set_salt(self, salt):
        self.__salt = salt
#Methods

    def add_students(self, student):
        self.__students.append(student)

    def add_students_request(self, student):
        self.__students_request.append(student)

    def remove_students_request(self, student):
        for req_info in self.__students_request:
            if student in req_info:
                self.__students_request.remove(req_info)
                return req_info


    def add_individual_timetable(self, timeslot):
        self.__individual_timetable.append(timeslot)

    def add_group_timetable(self, timeslot):
        self.__group_timetable.append(timeslot)

    def remove_individual_timeslot(self, timeslot):
        for slot in self.__individual_timetable:
            if timeslot == slot[1]:
                self.__individual_timetable.remove(slot)

    def remove_group_timeslot(self, timeslot):
        for slot in self.__group_timetable:
            if timeslot == slot[1]:
                self.__group_timetable.remove(slot)

    def remove_ticket(self):
        self.__ticket = []

    def remove(self, users_dict, id):
        users_dict.pop(id)
        return users_dict


    def __str__(self):
        return 'Hi {} {} nice to meet you!'.format(self.__first_name, self.__last_name)





class User:
    count_id = 0

    def __init__(self, first_name, last_name, email, gender, role, remarks):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__gender = gender
        self.__role = role
        self.__remarks = remarks

    def get_user_id(self):
        return self.__user_id
    def get_first_name(self):
        return self.__first_name
    def get_last_name(self):
        return self.__last_name
    def get_email(self):
        return self.__email
    def get_gender(self):
        return self.__gender
    def get_role(self):
        return self.__role
    def get_remarks(self):
        return self.__remarks

    def set_user_id(self, user_id):
        self.__user_id = user_id
    def set_first_name(self, first_name):
        self.__first_name = first_name
    def set_last_name(self, last_name):
        self.__last_name = last_name
    def set_email(self, email):
        self.__email = email
    def set_gender(self, gender):
        self.__gender = gender
    def set_role(self, role):
        self.__role = role
    def set_remarks(self, remarks):
        self.__remarks = remarks

class Feedback:

    def __init__(self, feedid, firstName, email, type, category, remarks, status, date):
        self.__feedID = feedid
        self.__firstName = firstName
        self.__type = type
        self.__email = email
        self.__category = category
        self.__remarks = remarks
        self.__status = status
        self.__date = date

    def get_feedID(self):
        return self.__feedID

    def get_firstName(self):
        return self.__firstName

    def get_type(self):
        return self.__type

    def get_email(self):
        return self.__email

    def get_category(self):
        return self.__category

    def get_remarks(self):
        return self.__remarks

    def get_status(self):
        return self.__status

    def get_date(self):
        return self.__date

    def set_feedID(self, feedID):
        self.__feedID = feedID

    def set_firstName(self, firstName):
        self.__firstName = firstName

    def set_email(self, email):
        self.__email = email

    def set_type(self, type):
        self.__type = type

    def set_category(self, category):
        self.__category = category

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_status(self, status):
        self.__status = status

    def set_date(self, date):
        self.__status = date


class Taskcs:
    count_id = 0
    def __init__(self,urgency,remarks):
        Taskcs.count_id +=1
        self.__task_idcs = Taskcs.count_id
        self.__urgency = urgency
        self.__remarks = remarks
    def get_task_idcs(self):
        return self.__task_idcs
    def get_urgency(self):
        return self.__urgency
    def get_remarks(self):
        return self.__remarks
    def set_user_id(self,task_idcs):
        self.__task_idcs = task_idcs
    def set_urgency(self,urgency):
        self.__urgency=urgency
    def set_remarks(self,remarks):
        self.__remarks=remarks

class CService:
    count_id = 0
    def __init__(self,first_name,last_name,gender,email,category,remarks):
        CService.count_id +=1
        self.__cs_id = CService.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__email = email
        self.__category = category
        self.__remarks = remarks
    def get_cs_id(self):
        return self.__cs_id
    def get_first_name(self):
        return self.__first_name
    def get_last_name(self):
        return self.__last_name
    def get_gender(self):
        return self.__gender
    def get_email(self):
        return self.__email
    def get_category(self):
        return self.__category
    def get_remarks(self):
        return self.__remarks
    def set_cs_id(self,cs_id):
        self.__cs_id = cs_id
    def set_first_name(self, first_name):
        self.__first_name=first_name
    def set_last_name(self, last_name):
        self.__last_name=last_name
    def set_gender(self,gender):
        self.__gender=gender
    def set_email(self,email):
        self.__email=email
    def set_category(self,category):
        self.__category=category
    def set_remarks(self,remarks):
        self.__remarks=remarks

class MessageTCS:
    count_id = 0
    def __init__(self,name,message):
        MessageTCS.count_id +=1
        self.__message_idtcs = MessageTCS.count_id
        self.__name = name
        self.__message = message
    def get_message_idtcs(self):
        return self.__message_idtcs
    def get_name(self):
        return self.__name
    def get_message(self):
        return self.__message
    def set_message_idtcs(self,message_idtcs):
        self.__message_idtcs = message_idtcs
    def set_name(self,name):
        self.__name=name
    def set_message(self,message):
        self.__message=message
