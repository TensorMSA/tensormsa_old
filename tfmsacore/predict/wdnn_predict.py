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
from sklearn.preprocessing import LabelEncoder

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
            print("############# Wdnn Predict ########")
            json_string = WdnnCommonManager.get_all_info_json_by_nnid(self,nnid)
            database = str(json_string['dir'])
            table_name = str(json_string['table'])
            json_object = json_string['datadesc']

            json_string_desc = netconf.load_ori_format(nnid)
            json_ob = json.loads(json_string_desc)  # get datadesc format

            #should be change
            model_dir = str(json_string['query'])
            #json_ob = json.loads(json_object)\
            _label_list = json_string['datasets']
            print(_label_list)

            label_list = eval(_label_list)
            print("##########predict label list ########  " + str(label_list))
            tt = json_ob['cell_feature']

            wdnn_model = WdnnCommonManager.wdnn_build(self, nnid,model_dir,False)

            t_label = json_ob['label']
            label_column = list(t_label.keys())[0]
            print(label_column)

            # for key, value in t_label.items():
            #     print("label key   " , key)
            #
            # label_key =   list(t_label.keys())
            # label_column = label_key[0]

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
                # multi class
                df['label'] = df[label_column]
                #lable_list = df[label_column].unique()
                #label_list
                print("##########predict label list ########  " + str(label_list))




                #df['label'] = (df[label_column].apply(lambda x: "Y" in x)).astype(int)

            print("((3.Wide & Deep Network Predict )) ##Start## ")
            predicts = wdnn_model.evaluate(input_fn=lambda: WdnnCommonManager.input_fn(self, df, nnid), steps=1)
            print("((3.Wide & Deep Network Predict )) ##End## ")
            results={}

            #add df column
            

            predict_results = wdnn_model.predict(input_fn=lambda: WdnnCommonManager.input_fn(self, df, nnid))
            df['predict_label'] = list(predict_results)


            le = LabelEncoder()
            # lable_list_sorted = sorted(list(lable_list))
            print("make sorted lable######################")
            le.fit(label_list)
            print("make label encorder function ######################")
            lable_decoder_func = lambda x: le.inverse_transform([x])

            print("make label mapping start")
            df['predict_label'] = df['predict_label'].map(lable_decoder_func).astype("str")
            print(df['predict_label'])
            #print(type(df['label']))
            print("make label maping end")

            #print("Df file save")
            #csv = df.to_csv('/home/dev/test_predict2.csv', sep='\t', encoding='utf-8')



            # wdnn_model.predict(i)
            print("##########predict cokes###############")
            print(predict_results)

            # resultList.append(df.columns.values.tolist().append(df.values.tolist()))
            resultList = df.values.tolist()
            resultList.insert(0, df.columns.values.tolist())
            results = json.loads(json.dumps(resultList))

            #thefile = open('/home/dev/test_predict2.txt', 'w')
            #for item in predict_results:
            #    thefile.write("%s\n" % item)

            #for key in sorted(predicts):
            #    print("((4.Wide & Deep Network Accurary)) %s: %s" % (key, predicts[key]))
            #    results[key]= str(predicts[key])

            return results
        except Exception as e:
            print ("Error Message : {0}".format(e))
            raise Exception(e)

