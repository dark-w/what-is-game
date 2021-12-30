import logging
from logging import handlers
import threading
import server_env

class logger:
    def __init__(self, log_level='DEBUG'):
        filename = "{}/server.log".format(server_env.GAME_SERVER_LOG_HOME)
        print(filename)
        self.fmt = '%(asctime)s %(levelname)s %(message)s'

        logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=log_level, filemode='w')

        self.__log = logging.getLogger("game_server")
        self.th = handlers.TimedRotatingFileHandler(filename=filename, when='H', backupCount=24,
                                                    encoding='utf-8')

        self.format_obj = logging.Formatter(self.fmt)
        self.th.setFormatter(self.format_obj)
        self.__log.propagate = False
        self.__log.addHandler(self.th)

    def get_log(self) -> logging.Logger:
        return self.__log

    def debug(self, str):
        self.__log.debug("[{}]: {}".format(
            threading.current_thread().name, str))

    def info(self, str):
        self.__log.info("[{}]: {}".format(
            threading.current_thread().name, str))

    def warning(self, str):
        self.__log.warning("[{}]: {}".format(
            threading.current_thread().name, str))

    def error(self, str):
        self.__log.error("[{}]: {}".format(
            threading.current_thread().name, str))

    def critical(self, str):
        self.__log.critical("[{}]: {}".format(
            threading.current_thread().name, str))

    def log_file_name_set(self, name: str):
        self.__log.removeHandler(self.th)
        self.th = handlers.TimedRotatingFileHandler(filename=name, when='H', backupCount=24,
                                                    encoding='utf-8')

        self.th.setFormatter(self.format_obj)
        self.__log.addHandler(self.th)


log = logger()
