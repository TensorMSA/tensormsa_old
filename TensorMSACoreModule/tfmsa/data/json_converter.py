# JSON Object 변수에 직접 접근할 수 있도록 합니다
class JsonObject:
  def __init__(self, d):
    self.__dict__ = d

class JsonDataConverter:
    """
        JSON to TensorFlow Learning Data
    """

    # 테스트를 위해 1차적으로 개발
    def convert_json_to_matrix(self, data):
        train_data = []
        train_tag = []
        result_data = []
        # result_data.append(train_data, train_tag)

        json_data = json.loads(data, object_hook=JsonObject)

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