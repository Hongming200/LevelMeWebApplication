class AdminProfile:
    count_id = 0

    def __init__(self, company, username, admin_email, admin_first_name, admin_last_name, address, city, country, postal_code):
        AdminProfile.count_id += 1
        self.__admin_profile_id = AdminProfile.count_id
        self.__company = company
        self.__username = username
        self.__admin_email = admin_email
        self.__admin_first_name = admin_first_name
        self.__admin_last_name = admin_last_name
        self.__address = address
        self.__city = city
        self.__country = country
        self.__postal_code = postal_code

    def get_admin_profile_id(self):
        return self.__admin_profile_id
    def get_company(self):
        return self.__company
    def get_username(self):
        return self.__username
    def get_admin_email(self):
        return self.__admin_email
    def get_admin_first_name(self):
        return self.__admin_first_name
    def get_admin_last_name(self):
        return self.__admin_last_name
    def get_address(self):
        return self.__address
    def get_city(self):
        return self.__city
    def get_country(self):
        return self.__country
    def get_postal_code(self):
        return self.__postal_code

    def set_admin_profile_id(self, admin_profile_id):
        self.__admin_profile_id = admin_profile_id
    def set_company(self, company):
        self.__company = company
    def set_username(self, username):
        self.__username = username
    def set_admin_email(self, admin_email):
        self.__admin_email = admin_email
    def set_admin_first_name(self, admin_first_name):
        self.__admin_first_name = admin_first_name
    def set_admin_last_name(self, admin_last_name):
        self.__admin_last_name = admin_last_name
    def set_address(self, address):
        self.__address = address
    def set_city(self, city):
        self.__city = city
    def set_country(self, country):
        self.__country = country
    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code


