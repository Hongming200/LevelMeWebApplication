class UserProfile:
    count_id = 0

    def __init__(self, first_name, last_name, gender, email, certificates):
        UserProfile.count_id += 1
        self.__profile_id = UserProfile.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__email = email
        self.__certificates = certificates

    def get_profile_id(self):
        return self.__profile_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_email(self):
        return self.__email

    def get_certificates(self):
        return self.__certificates

    def set_profile_id(self, profile_id):
        self.__profile_id = profile_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_email(self, email):
        self.__email = email

    def set_certificates(self, certificates):
        self.__certificates = certificates
