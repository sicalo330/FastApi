import logging
import os

LOGGER = "api_test.log"
absolute_path = os.path.dirname(__file__)
logger_path = os.path.join()

logger_request = logging
logger_request.basicConfig(
    level = logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt = "%d-%m-%Y %H:%M:%S",
    filename = logger_path
)