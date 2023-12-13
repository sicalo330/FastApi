import os
import jsonschema
from main.core.utils.logger import logger_request
from main.core.utils.json_reader import JsonReader


class VerifyResponse:

    def verify_schema(response, schema):
        logger_request.info(f"Validating the response against {schema} schema")
        resources_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "api",
            "resources",
            schema
        )
        template_schema = JsonReader(resources_path).open_json()
        try:
            jsonschema.validate(response, template_schema)
            return True, "Succes"
        except jsonschema.exceptions.ValidationError as error:
            return False, str(error)