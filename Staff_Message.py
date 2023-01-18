class Staff_Message:
    message_count_id = 0

    def __init__(self, message_name, message_email, message):
        Staff_Message.message_count_id +=1
        self.__message_id = Staff_Message.message_count_id
        self.__message_name = message_name
        self.__message_email = message_email
        self.__message = message

    def get_message_count_id(self):
        return self.__message_id
    def get_message_name(self):
        return self.__message_name
    def get_message_email(self):
        return self.__message_email
    def get_message(self):
        return self.__message

    def set_message_count_id(self, message_count_id):
        self.__message_id = message_count_id
    def set_message_name(self, message_name):
        self.__message_name = message_name
    def set_message_email(self, message_email):
        self.__message_email = message_email
    def set_message(self, message):
        self.__message = message

