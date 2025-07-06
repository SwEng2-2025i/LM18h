import logging
import os
import traceback
class DuplicadorSalida:
    def __init__(self, *destinos):
        self.destinos = destinos
    def write(self, texto):
        for d in self.destinos:
            d.write(texto)
    def flush(self):
        for d in self.destinos:
            d.flush()
class Logger():

    def __init__(self):
        self.logger = self.__set_logger()
        
    def __set_logger(self):
        # log_directory = 'Logs'
        # log_filename = 'app.log'
        base_dir = os.path.dirname(os.path.abspath(__file__))  # => .../1000256311/Test

        # Ruta a la carpeta Logs dentro de Test
        log_directory = os.path.join(base_dir, "Logs")
        log_filename = "app.log"
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        log_path = os.path.join(log_directory, log_filename)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)

        if (logger.hasHandlers()):
            logger.handlers.clear()

        logger.addHandler(file_handler)

        return logger
    @classmethod
    def add_to_log(cls,level,message):
        try:
            logger = cls.__set_logger(cls)
            if (level == "critical"):
                logger.critical(message)
            elif (level == "debug"):
                logger.debug(message)
            elif (level == "error"):
                logger.error(message)
            elif (level == "warn"):
                logger.warning(message)
            elif (level == "info"):
                logger.info(message)

        except Exception as ex:
            print(traceback.format_exc())
            print(ex)
