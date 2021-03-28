import logging
import datetime

# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')
# logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
class Logger:
    def __init__(self):
        now = datetime.datetime.now()
        filename = now.strftime("%Y-%m-%d")
        logging.basicConfig(filename=filename + '.log', level=logging.DEBUG)

    def _debug(self, msg):
        logging.debug(msg)
    
    def _info(self, msg):
        logging.info(msg)

    def _warning(self, msg):
        logging.warning(msg)
    
    def _error(self, msg):
        logging.error(msg)

    @staticmethod
    def Debug(msg):
        logger = Logger()
        logger._debug(msg)
    
    @staticmethod
    def Info(msg):
        logger = Logger()
        logger._info(msg)

    @staticmethod
    def Warning(msg):
        logger = Logger()
        logger._warning(msg)

    @staticmethod
    def Error(msg):
        logger = Logger()
        logger._error(msg)