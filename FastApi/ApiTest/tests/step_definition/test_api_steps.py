import os
from pytest_bdd import scenarios
from main.core.utils.logger import logger_request
from common_action_steps import *
from common_verificiation_steps import *

logger_request.info("Executing the selected features")

feature_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "features"
)

scenarios(feature_path)
