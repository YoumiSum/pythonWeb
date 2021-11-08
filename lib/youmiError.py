class SameParamsError(Exception):
    def __str__(self):
        return "you cann't set same param name in request"
