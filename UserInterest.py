class UserInterest:
    count_id = 0

    def __init__(self, fav, hate):
        UserInterest.count_id += 1
        self.__interest_id = UserInterest.count_id
        self.__fav = fav
        self.__hate = hate

    def get_interest_id(self):
        return self.__interest_id


    def get_fav(self):
        return self.__fav

    def get_hate(self):
        return self.__hate

    def set_interest_id(self, interest_id):
        self.__interest_id = interest_id



    def set_fav(self, fav):
        self.__fav = fav

    def set_hate(self, hate):
        self.__hate = hate
