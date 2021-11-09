import conf.log_dict_config as logging

class SameParamsError(Exception):
    def __str__(self):
        logging.logger.error("you cann't set same param name in request")
        return "you cann't set same param name in request"


