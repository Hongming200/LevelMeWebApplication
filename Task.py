class Task:
    count_id = 0

    def __init__(self, task, done_by):
        Task.count_id += 1
        self.__task_id = Task.count_id
        self.__task = task
        self.__done_by = done_by

    def get_task_id(self):
        return self.__task_id
    def get_task(self):
        return self.__task
    def get_done_by(self):
        return self.__done_by

    def set_task_id(self, task_id):
        self.__task_id = task_id
    def set_task(self, task):
        self.__task = task
    def set_done_by(self, done_by):
        self.__done_by = done_by
