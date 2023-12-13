from pytest_bdd import then, parsers
from main.core.utils.logger import logger_request
from main.core.utils.verify_response import VerifyResponse

@then(
    parsers.parse('then the response status code should be "{statuscode}" ')
)
def validate_status_code(request, statuscode):
    logger_request.info("Validating the status code" +
                        f"it should be {statuscode} and the real status code" +
                        f"is {request.response.statuscode}" )
    assert request.response.status_code == int(statuscode)

@then(
    parsers.parse(
        'the response body should be have "{number}" elements'
    )
)
def validate_number_elements(request,number):
    logger_request.info(f"Validating the response has {number} elements")
    assert len(request.response.json() == int(number))

@then(
    parsers.parse('the response should fit the following schema "{schema}"')
)
def validate_schema(request,schema):
    logger_request.info(f"Validating the response against {schema} schema")
    schema_rep = request.response.json()
    veredict, msg = VerifyResponse.verify_schema(
        response = schema_rep,
        schema = schema
    )
    logger_request.info(f"The veredict: {veredict} with the message: {msg}")
    assert veredict