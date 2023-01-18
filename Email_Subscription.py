class Email_Subscription:
    count_id = 0

    def __init__(self, email_subscription_name, email_subscription_email):
        Email_Subscription.count_id += 1
        self.__email_subscription_id = Email_Subscription.count_id
        self.__email_subscription_name = email_subscription_name
        self.__email_subscription_email = email_subscription_email

    def get_email_subscription_id(self):
        return self.__email_subscription_id
    def get_email_subscription_name(self):
        return self.__email_subscription_name
    def get_email_subscription_email(self):
        return self.__email_subscription_email

    def set_email_subscription_id(self, email_subscription_id):
        self.__email_subscription_id = email_subscription_id
    def set_email_subscription_name(self, email_subscription_name):
        self.__email_subscription_name = email_subscription_name
    def set_email_subscription_email(self, email_subscription_email):
        self.__email_subscription_email = email_subscription_email

