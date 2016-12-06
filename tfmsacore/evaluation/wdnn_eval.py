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
from tfmsacore.netcommon.acc_eval_common import AccEvalCommon
from tfmsacore.netcommon.acc_eval_common import AccStaticResult
from sklearn.preprocessing import LabelEncoder


class wdnn_eval(WdnnCommonManager):
    def __init__(self):
        print("############# Create wdnn_eval")
        WdnnCommonManager.__init__(self)

    def wdd_eval(self, nnid, filename=None):
        """
                Wide & Deep Network predict
                :param nnid : network id in tfmsacore_nninfo
                :return: acturacy

        """
        try:
            utils.tfmsa_logger("((3.1 Wide & Deep Network Eval Start)) ## "+ nnid + "##")
            #print(nnid)

            #get network info from postgres
            json_string = WdnnCommonManager.get_all_info_json_by_nnid(self, nnid=nnid)
            #print("WdnnCommonManager.get_json_by_nnid after")
            #print(json_string)
            #print(type(json_string))
            database = json_string['dir']
            table_name = json_string['table']
            #print(database)
            #print(table_name)
            json_string_desc = netconf.load_ori_format(nnid)
            json_ob = json.loads(json_string_desc)  #get datadesc format
            model_dir = str(json_string['query'])
            tt = json_ob['cell_feature']
            #json_ob = json.loads(json_object)
            #t_label = json_ob["label"]
            ##label_column = list(t_label.keys())[0]
            label_column = list(json_ob["label"].keys())[0]

            _label_list = json_string['datasets']
            utils.tfmsa_logger("((3.1 Wide & Deep Network Eval Start)) ## DB : " + database + " TABLE : " + table_name)
            utils.tfmsa_logger("((3.1 Wide & Deep Network Eval Start)) ## Model_Dir : " + model_dir )
            utils.tfmsa_logger("((3.1 Wide & Deep Network Eval Start)) ## Label Column " + label_column + " Label : " + _label_list)

            #print(_label_list)

            label_list = eval(_label_list)
            #print("##########predict label list ########  " + str(label_list))



            wdnn_model = WdnnCommonManager.wdnn_build(self, nnid, model_dir, False)




            if filename == None:
                #limit_no = 100
                #print(
                #    "((2.Get Dataframe from Hbase)) ##Start## (" + database + " , " + table_name + " , " + label_column + ")")
                df, last_key = data.DataMaster().query_data("test_schema_" +  database, table_name, "a", use_df = True, limit_cnt=-1, with_label=label_column)
                utils.tfmsa_logger("((3.1 Wide & Deep Network Eval Start)) ## Get Test Schema Data Count" + str(len(df)) + "LastKey : " + str(last_key))
                #print(
                #    "((2.Get Dataframe from Hbase)) ##End## (" + database + " , " + table_name + " , " + label_column + " , " + str(
                #        limit_no) + ")")
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

            results = {}
            utils.tfmsa_logger("((3.1 Wide & Deep Network Eval Start)) ## Start Predict in Eval Method ##")
            predict_results = wdnn_model.predict(input_fn=lambda: WdnnCommonManager.input_fn(self, df, nnid))
            df['predict_label'] = list(predict_results)

            #print(df['predict_label'] )
            print("make label encorder function ######################")
            #
            #Decode Label(int) to Label(str)
            le = LabelEncoder()
            le.fit(label_list)
            lable_decoder_func = lambda x: le.inverse_transform([x])
            df['predict_label'] = df['predict_label'].map(lable_decoder_func).astype("str")

            #results_acc table manager class create
            acc_result_obj = AccStaticResult()

            for value in df.iterrows():
                print("Inside start row by row")
                print(type(value))
                _row = value[1]
                ori_label = _row[label_column]
                predict_label = str(eval(_row["predict_label"])[0])#str(list(_row["predict_label"])[0])
                #predict_label = le.inverse_transform(_predict_label)
                print(str(ori_label) + "-------> " + str(predict_label))
                acc_result_obj = AccEvalCommon(nnid).set_result(acc_result_obj, ori_label,predict_label)
            return results
        except Exception as e:
            print("Error Message : {0}".format(e))
            raise Exception(e)


