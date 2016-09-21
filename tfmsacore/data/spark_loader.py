from tfmsacore import netconf
from tfmsacore.utils import JsonDataConverter
from tfmsarest import livy


class SparkLoader:
    def __init__(self):
        print("init")
        # TO-DO :

    def get_train_data(self, nn_id):
        """
        (1) get net column descritions
        (2) get user selected data , exclude user check None
        (3) modify train data for 'categorical data'
        (4) caculate size of arrays need for neural networks
        (5) change neural network configurioatns automtically
        :param nn_id:neural network id want to train
        :return: Train Data Sets
        """
        try :

            # (1) get data configuration info
            net_conf = netconf.get_network_config(nn_id)
            datadesc = JsonDataConverter().load_obj_json(net_conf['datadesc'])
            datasets = JsonDataConverter().load_obj_json(net_conf['datasets'])

            # (2) get user seleceted data from spark
            sql_stmt = self.get_sql_state(datadesc , net_conf['table'])
            livy_client = livy.LivyDfClientManager(2)
            livy_client.create_session()
            livy_client.query_data(net_conf['table'], sql_stmt)

            # (3) modify train data for 'categorical data'
            """
                think it is better to be done on spark
            """

            """
            TO-DO :
                    (3) modify train data for 'categorical data'
                    (4) caculate size of arrays need for neural networks
                    (5) change neural network configurioatns automtically
            """
        except IOError as e:
            return e

    def get_sql_state(self, datadesc, table):
        """
        create sql statement for spark
        TO-DO : need to prepare for lage set data
        :param datadesc:declation os data types
        :param table:target table want to get data
        :return: complete sql statements
        """
        sql_stmt = []
        sql_stmt.append("select ")

        for x in datadesc.keys():
            if(datadesc[x] != 'None'):
                sql_stmt.append(str(x))
                sql_stmt.append(",")

        sql_stmt = sql_stmt[ : -1]
        sql_stmt.append(" from ")
        sql_stmt.append(str(table))

        return ''.join(sql_stmt)

    def get_predict_data(self, nn_id, predict_data):
        """
        (1) get net column descritions
        (2) modify predict data for 'categorical data'
        :param nn_id:neural network id want to train
        :return: Train Data Sets
        """
        """
        TO-DO :
            (1) get net column descritions
            (2) modify predict data for 'categorical data'
        """

        return True