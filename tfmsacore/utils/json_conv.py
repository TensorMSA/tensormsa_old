# -*- coding: utf-8 -*-
import json

# json utils
class JsonObject:

    def __init__(self, d):
        self.__dict__ = d

    def __getitem__(self, item):
        return self.__dict__[item]

    def keys(self):
        return self.__dict__.keys()

    def get_dict(self):
        return self.__dict__

    def dumps(self):
        # only for the simple
        return self.__dict__

class CusJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, JsonObject):
            return super(CusJsonEncoder, self).default(obj)
        return obj.__dict__

class JsonDataConverter:
    """
        JSON to TensorFlow Learning Data
    """
    @staticmethod
    def load_obj_json(data):
        """
        return objective json
        :param data:
        :return:
        """

        def comma_converter(data):
            """
            TO-DO :need to find a samrter way on write and read json on db and spark
            :param data:
            :return:
            """
            if(data == "") :
                data = "{}"

            if ("'" in data and "\"" in data):
                if (data.index("'") < data.index("\"")):
                    data = data.encode("utf-8")
                    data = data.replace("'", "\"")
            elif ("'" in data and "\"" not in data):
                data = data.encode("utf-8")
                data = data.replace("'", "\"")
            else:
                data = data.encode("utf-8")
            return data

        try :

            if(isinstance(data, (str))):
                json_data = json.loads(comma_converter(data), object_hook=JsonObject)
            elif(isinstance(data, (file))):
                json_data = json.loads(data.read(), object_hook=JsonObject)
            elif(isinstance(data, (dict))):
                json_data = json.loads(data, object_hook=JsonObject)
            elif(isinstance(data, (unicode))):
                json_data = json.loads(comma_converter(data), object_hook=JsonObject)
            elif (isinstance(data, (JsonObject))):
                return data
            else:
                raise SyntaxError ("not a right json type")

            return json_data
        except Exception as e:
            raise Exception(e)


