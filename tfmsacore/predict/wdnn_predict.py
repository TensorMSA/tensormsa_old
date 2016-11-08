# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import numpy as np
import tensorflow as tf
from tfmsacore import data
from tfmsacore import netconf
from tfmsacore.utils.json_conv import JsonDataConverter as jc
import json, math
import tempfile
from django.conf import settings
from tfmsacore import utils
from rest_framework.response import Response
import pandas as pd
from tfmsacore.netcommon.wdnn_common import WdnnCommonManager



class wdnn_predict(WdnnCommonManager):
    def __init__(self):
        print("############# Create wdnn_predict")
        WdnnCommonManager.__init__(self)

    def wdd_predict(self, nnid, filename=None):
        """
                Wide & Deep Network predict
                :param nnid : network id in tfmsacore_nninfo
                :return: acturacy

        """
        try:
            json_string = WdnnCommonManager.get_json_by_nnid(self,nnid)
            database = str(json_string['dir'])
            table_name = str(json_string['table'])
            json_object = json_string['datadesc']
            #should be change
            model_dir = str(json_string['datasets'])
            json_ob = json.loads(json_object)

            tt = json_ob['cell_feature']

            wdnn_model = WdnnCommonManager.wdnn_build(self, nnid,model_dir,False)

            t_label = json_ob['label']

            for key, value in t_label.items():
                print("label key   " , key)

            label_key =   list(t_label.keys())
            label_column = label_key[0]

            if filename == None:
                limit_no = 100
                print("((2.Get Dataframe from Hbase)) ##Start## (" + database + " , " + table_name + " , " + label_column + ")")
                df = data.DataMaster().query_data(database, table_name, "a", limit_no ,with_label=label_column)
                print("((2.Get Dataframe from Hbase)) ##End## (" + database + " , " + table_name + " , " + label_column + " , " + str(limit_no) + ")")
            else:
                print("((2.Get Dataframe from CSV)) ##Start## (" + nnid + " , " + filename + ")")
                file_path = settings.FILE_ROOT + "/predict/" + nnid + "/" + filename
                print("((2.Get Dataframe from CSV)) ##filePath## (" + file_path + ")")
                print(file_path)
                df = pd.read_csv(
                     tf.gfile.Open(file_path),
                     # names=COLUMNS,
                     skipinitialspace=True,
                     engine="python")
                # add label feature for wdnn netowrk
                df['label'] = (df[label_column].apply(lambda x: "Y" in x)).astype(int)

            print("((3.Wide & Deep Network Predict )) ##Start## ")
            predicts = wdnn_model.evaluate(input_fn=lambda: WdnnCommonManager.input_fn(self, df, nnid), steps=1)
            print("((3.Wide & Deep Network Predict )) ##End## ")
            results={}

            #add df column
            

            predict_results = wdnn_model.predict(input_fn=lambda: WdnnCommonManager.input_fn(self, df, nnid))
            df['predict_label'] = list(predict_results)
            
            print("Df file save")
            csv = df.to_csv('/home/dev/test_predict2.csv', sep='\t', encoding='utf-8')



            # wdnn_model.predict(i)
            print("##########predict cokes###############")
            print(predict_results)

            thefile = open('/home/dev/test_predict2.txt', 'w')
            for item in predict_results:
                thefile.write("%s\n" % item)

            for key in sorted(predicts):
                print("((4.Wide & Deep Network Accurary)) %s: %s" % (key, predicts[key]))
                results[key]= str(predicts[key])

            return results
        except Exception as e:
            print ("Error Message : {0}".format(e))
            raise Exception(e)

