import os
import requests
from main.core.utils.json_reader import JsonReader
from main.core.utils.logger import logger_request

class RequestManager:
    __instance = None

    def __init__(self, config_file:str="") -> None:
        root_path = os.path.join(
            os.path.dirname(__file__),#Estamos en el directorio de FastApi(creo)
            "..",
            "..",
            ".."
            #lo de arriba es el quivalente a ../../../, esto puede ser algo malo ya que algunos sistemas operativos pueden no enteneder esa nomenclatura
        )
        if(config_file == ""):
            self.__config = JsonReader(
                os.path.join(root_path,"configuration.json")
            ).open_json
        else:
            self.__config = JsonReader(config_file).open_json()
        env_selected = self.__config.get("environment","testing")
        logger_request.debug(f"the selected env: {env_selected} ")
        __environment = (
            JsonReader(
                os.path.join(root_path,"environment.json")
            ).open_json().get(env_selected)
        )

        self.url = __environment.get("url")
        self.headers = __environment.get("headers")
        self.params = None
        self.response = {}

#usaremos get instance para hacer un singleton(ver patron de diseño)

    @staticmethod
    def get_instance():
        if(RequestManager.__instance is None):
            RequestManager.__instance = RequestManager()
        return RequestManager.__instance

    def make_request(self, http_method, endpoint, payload = None):
        logger_request.debug(
            f"Request {http_method} to {self.url}{endpoint} "
        )
        self.response = requests.request(
            method=http_method,
            url = f"{self.url}{endpoint}",
            #headers = self.headers,
            params=payload,
            timeout=(15)
        )