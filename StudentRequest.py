class StudentRequest:
    count_id = 0

    def __init__(self, first_name, last_name, gender, email, size, day, timeslot):
        StudentRequest.count_id += 1
        self.__studentrequest_id = StudentRequest.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__email = email
        self.__size = size
        self.__day = day
        self.__timeslot = timeslot



    def get_studentrequest_id(self):
        return self.__studentrequest_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_email(self):
        return self.__email

    def get_size(self):
        return self.__size

    def get_day(self):
        return self.__day

    def get_timeslot(self):
        return self.__timeslot


    def set_studentrequest_id(self, studentrequest_id):
        self.__studentrequest_id = studentrequest_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_email(self, email):
        self.__email = email

    def set_size(self, size):
        self.__size = size

    def set_day(self, day):
        self.__day = day

    def set_timeslot(self, timeslot):
        self.__timeslot = timeslot
