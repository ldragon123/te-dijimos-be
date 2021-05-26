class Database_Exception(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)