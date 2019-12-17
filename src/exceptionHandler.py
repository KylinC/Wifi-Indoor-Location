class AP_NOT_EXIST(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('AP NOT EXIST!')