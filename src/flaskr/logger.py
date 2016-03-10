import datetime
__author__ = 'sam_l'


class Logger:
    log = []

    def __init__(self, name = ""):
        self.name = name

    def add_log(self,message):
        Logger.log.append(datetime.datetime.today().strftime("%M:%S:%f -- ")[:-3] + self.name + " -- " + message)

    def get_log(self):
        string = ""
        for m in Logger.log:
            string += str(m) + "<br>"
        self.reset_logger()
        return string

    def reset_logger(self):
        Logger.log = []