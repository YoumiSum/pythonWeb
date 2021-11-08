class HttpRequest(object):

    def __init__(self):
        self.__cookie = None

    """
        About manager cookie's function see bellow.
    """
    def setCookie(self, cookie):
        self.__cookie = cookie

    def getCookie(self):
        return self.__cookie

    cookie = property(getCookie, setCookie)
