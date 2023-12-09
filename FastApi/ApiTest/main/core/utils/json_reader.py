import json

class JsonReader:

    def __init__(self, path:str) -> None:
        self.path = path
        self.json = None

    def open_json(self,encoding:str = "utf-8"):#Esto es para leer, 'r' (read)
        with open(self.path,'r',encoding = encoding) as json_file:
            self.json = json.load(json_file)
        return self.json

    def save_json(self, data:dict | list, encoding):#Esto es para escribir 'w' (writte)
        with open(self.path,'w',encoding=encoding) as json_file:
            json.dump(data,json_file,indent=4)
