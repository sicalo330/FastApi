from pytest_bdd import when,parsers
from main.core.utils.logger import logger_request
from main.core.api.request_manager import RequestManager

@when(
    parsers.parse(
        'the user ends "{httpmethod}" request to "{endpoint}" endpoint'
    )

)

def send_request(request,httpmethod,endpoint):
    logger_request.info(request,httpmethod,endpoint)
    req_manager = RequestManager.get_instance()
    try:
        params = request.params
    except AttributeError:
        params = None
    request.response = req_manager.make_request(
        http_method=httpmethod,
        endpoint=endpoint,
        payload=params
    )