# -*- coding: utf-8 -*-
import json

# JSON Object 변수에 직접 접근할 수 있도록 합니다
class JsonObject:
  def __init__(self, d):
    self.__dict__ = d

class JsonDataConverter:
    """
        JSON to TensorFlow Learning Data
    """
    # 테스트를 위해 1차적으로 개발
    def convert_json_to_matrix(self, json_data):
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


    def load_obj_json(self, data):
        """
        return objective json
        :param data:
        :return:
        """
        json_data = json.loads(data.read(), object_hook=JsonObject)

        return json_data