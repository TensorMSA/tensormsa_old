from tfmsacore import netconf
from tfmsacore.utils import JsonDataConverter, tfmsa_logger
from tfmsarest import livy
from tfmsacore.data.spark_loader import SparkManager



class DFPreProcessor:
    def __init__(self):
        print("init SparkLoader")
        self.m_train = []
        self.m_tag = []
        self.train_len = None
        self.tag_len = None

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
            tfmsa_logger("modifying Train start!")
            # (1) get data configuration info
            net_conf = netconf.get_network_config(nn_id)
            datadesc = JsonDataConverter().load_obj_json(net_conf['datadesc'])
            datasets = JsonDataConverter().load_obj_json(net_conf['datasets'])

            # (2) get user seleceted data from spark
            sql_stmt = self.get_sql_state(datadesc , net_conf['table'])
            livy_client = livy.LivyDfClientManager()
            livy_client.create_session()
            origin_data = livy_client.query_data(net_conf['dir'], net_conf['table'], sql_stmt)

            # (3) modify train data for 'categorical data'
            self.m_train[:] = []
            self.m_tag[:] = []
            self.m_train, self.m_tag = self.reform_train_data(JsonDataConverter().load_obj_json(origin_data), \
                                                              datasets, datadesc)
            # (4) caculate size of arrays need for neural networks
            self.train_len = len(next(iter(self.m_train), None))
            self.tag_len = len(next(iter(self.m_tag), None))

            tfmsa_logger("modifying Train End!")
            return self

        except IOError as e:
            return e


    def get_predict_data(self, nn_id, predict_data):
        """
        (1) get net column descritions
        (2) modify predict data for 'categorical data'
        (3) caculate size of arrays need for neural networks
        :param nn_id:neural network id want to train
        :return: Train Data Sets
        """
        try :
            tfmsa_logger("modifying predict start!")
            # (1) get data configuration info
            net_conf = netconf.get_network_config(nn_id)
            datadesc = JsonDataConverter().load_obj_json(net_conf['datadesc'])
            datasets = JsonDataConverter().load_obj_json(net_conf['datasets'])

            # (2) modify train data for 'categorical data'
            self.m_train[:] = []
            self.m_tag[:] = []
            self.m_train, self.m_tag = self.reform_train_data(predict_data, datasets, datadesc)

            # (3) caculate size of arrays need for neural networks
            self.train_len = len(next(iter(self.m_train), None))

            tfmsa_logger("modified predict data : {0} ".format(self.m_train))
            return self

        except Exception as e:
            print ("Exception {0} , {1}".format(self.__class__, e))
            raise Exception(e)

    def reform_train_data(self, origin_data, data_cate, data_desc):
        """
        reform train data fit for neural network input  &
        calculate and update necessary configurations
        :param origin_data : original data need to be modified
        :param data_cate : category data
        :return : ready to train data & update net conf data
        """
        modified_train_data = []
        modified_train_row = []
        modified_tag_data = []
        modified_tag_row = []

        for data in origin_data:
            modified_train_row[:] = []
            modified_tag_row[:] = []
            for col_key in data.keys():

                if(col_key in data_desc.keys()):

                    if(data_desc[col_key] == 'cate'):
                        modified_train_row = self.set_cate_row(col_key, data_cate, data, \
                                                               modified_train_row)
                    elif (data_desc[col_key] == 'tag'):
                        modified_tag_row = self.set_cate_row(col_key, data_cate, data, \
                                                             modified_tag_row)
                        modified_tag_data.append(modified_tag_row)
                    elif (data_desc[col_key] == 'rank'):
                        modified_train_row = self.set_rank_row(col_key, data_cate, data, \
                                                               modified_train_row)
                    elif (data_desc[col_key] == 'cont'):
                        if(str(data_desc[col_key]).isdigit()):
                            modified_train_row.append(str(data[col_key]))
                        else:
                            modified_train_row.append("0")

            # padding
            while(range(0, len(modified_train_row) % 2)):
                modified_train_row.append("0")

            modified_train_data.append(modified_train_row)

        #tfmsa_logger ("modified train data : {0} ".format(modified_train_data))
        #tfmsa_logger ("modified tah data : {0} ".format(modified_tag_data))

        return modified_train_data, modified_tag_data

    def set_cate_row(self, col_key, data_cate, data, modified_train_row):
        """
        convert data form to categorical list array
        :param col_key:row - col key name
        :param data_cate: category list for each col key
        :param data: data set for tarining
        :param modified_train_row: on processing trainging list data
        :return: modified tarin row data
        """
        for cate_key in data_cate[col_key]:
            if (str(cate_key) == str(data[col_key]).encode("UTF-8")):
                modified_train_row.append("1")
            else:
                modified_train_row.append("0")

        return modified_train_row


    def set_rank_row(self, col_key, data_cate, data, modified_train_row):
        """
        convert data form to rank type integer
        :param col_key:row - col key name
        :param data_cate: category list for each col key
        :param data: data set for tarining
        :param modified_train_row: on processing trainging list data
        :return: modified tarin row data
        """

        if(data[col_key] in data_cate[col_key]):
            modified_train_row.append(data_cate[col_key].index(data[col_key]))
        else :
            modified_train_row.append(0)
        return modified_train_row


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
            if(datadesc[x] != 'none'):
                sql_stmt.append(str(x))
                sql_stmt.append(",")

        sql_stmt = sql_stmt[ : -1]
        sql_stmt.append(" from ")
        sql_stmt.append(str(table))

        return ''.join(sql_stmt)




