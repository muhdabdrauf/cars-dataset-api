import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging(level=logging.INFO):
    logger = logging.getLogger()
    logger.handlers = []  # Clear existing handlers
    logger.setLevel(level)

    logHandler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s %(module)s %(funcName)s %(lineno)d' 
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)