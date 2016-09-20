# -*- coding: utf-8 -*-
import json

# json utils
class JsonObject:
  def __init__(self, d):
    self.__dict__ = d

class JsonDataConverter:
    """
        JSON to TensorFlow Learning Data
    """
    #
    @staticmethod
    def convert_json_to_matrix(json_data):
        train_data = []
        train_tag = []
        result_data = []

        for row in json_data:

            temp2 = []
            temp1 = row.tag
            train_tag.append(temp1)

            for line in row.data:
                temp2.append(line)

            train_data.append(temp2)

        result_data.append(train_data)
        result_data.append(train_tag)

        return result_data

    @staticmethod
    def load_obj_json(data):
        """
        return objective json
        :param data:
        :return:
        """
        if(isinstance(data, (str))):
            json_data = json.loads(data, object_hook=JsonObject)
        elif(isinstance(data, (file))):
            json_data = json.loads(data.read(), object_hook=JsonObject)
        elif(isinstance(data, (dict))):
            json_data = json.loads(data, object_hook=JsonObject)
        else:
            raise SyntaxError ("not a right json type")

        return json_data