# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import tensorflow as tf
from tfmsacore import data
from tfmsacore import netconf
import json, math
import tempfile
from django.conf import settings
from tfmsacore import utils
import pandas as pd
from tfmsacore.netcommon.wdnn_common import WdnnCommonManager
from sklearn.preprocessing import LabelEncoder

class wdnn_predict(WdnnCommonManager):
    def __init__(self):
        utils.tfmsa_logger("Create Wdnn Predict ")
        WdnnCommonManager.__init__(self)

    def wdd_predict(self, nnid, filename=None):
        """
                Wide & Deep Network predict
                :param nnid : network id in tfmsacore_nninfo
                :return: json list with predict value

        """
        try:
            utils.tfmsa_logger("((0.0 Wide & Deep Network Predict Start)) ## " + nnid + "##")
            json_string = WdnnCommonManager.get_all_info_json_by_nnid(self,nnid)
            database = str(json_string['dir'])
            table_name = str(json_string['table'])
            json_string_desc = netconf.load_ori_format(nnid) #Get format json string
            column_format_json_ob = json.loads(json_string_desc)  # Cast json object from string of column formats
            temp_label = column_format_json_ob['label'] #Get label column from data formats
            label_column = list(temp_label.keys())[0]

            #should be change after deciding model directory
            model_dir = str(json_string['query'])
            _label_list = json_string['datasets']
            label_list = eval(_label_list) #Cast a list from string
            utils.tfmsa_logger("((0.0 Wide & Deep Network label List Get)) ## " + str(label_list) + "##")

            wdnn_model = WdnnCommonManager.wdnn_build(self, nnid,model_dir,False)

            if filename == None:
                #Doesn;t need this part now
                limit_no = 100
                print("((2.Get Dataframe from Hbase)) ##Start## (" + database + " , " + table_name + " , " + label_column + ")")
                df = data.DataMaster().query_data(database, table_name, "a", limit_no ,with_label=label_column)
                print("((2.Get Dataframe from Hbase)) ##End## (" + database + " , " + table_name + " , " + label_column + " , " + str(limit_no) + ")")
            else:
                utils.tfmsa_logger("((2.Get Dataframe from CSV)) ##Start##" + nnid + " , " + filename + ")")
                file_path = settings.FILE_ROOT + "/predict/" + nnid + "/" + filename
                utils.tfmsa_logger("((2.Get Dataframe from CSV)) ##filePath###" + file_path + ")")
                df = pd.read_csv(
                     tf.gfile.Open(file_path),
                     # names=COLUMNS,
                     skipinitialspace=True,
                     engine="python")
                df['label'] = df[label_column]

            results=dict() #Make Return Dictionary
            predict_results = wdnn_model.predict(input_fn=lambda: WdnnCommonManager.input_fn(self, df, nnid))
            df['predict_label'] = list(predict_results)
            utils.tfmsa_logger("((3.1 Wide & Deep Network Predict Complete)) ## " + nnid + "##")

            le = LabelEncoder()
            le.fit(label_list)
            lable_decoder_func = lambda x: le.inverse_transform(x)
            df['predict_label'] = df['predict_label'].map(lable_decoder_func).astype("str") #convert label code to label string.

            label_value = list(df['label'].unique())
            label_encode = le.inverse_transform(label_value)
            utils.tfmsa_logger("((3.1 Wide & Deep Network Predict)) ## Label Convert ##" + str(label_value) + "DECODE ---> " + str(label_encode))

            resultList = df.values.tolist()
            resultList.insert(0, df.columns.values.tolist())
            results = json.loads(json.dumps(resultList))
            return results
        except Exception as e:
            print ("Error Message : {0}".format(e))
            raise Exception(e)

