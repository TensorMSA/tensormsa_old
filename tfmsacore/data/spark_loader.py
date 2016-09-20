from tfmsacore import netconf


class JsonObject:
    """
    json object hooker class
    """
    def __init__(self, d):
        self.__dict__ = d

    def __getitem__(self, item):
        return self.__dict__[item]


class SparkLoader:
    def __init__(self):
        print("init")
        # TO-DO :

    def get_train_data(self, nn_id):
        """
        load livy config from file
        :return: None
        """
        try :
            print("!!")
            result = netconf.get_network_config(nn_id)
            print(result)
        except IOError as e:
            return e

