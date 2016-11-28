# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import numpy as np
import tensorflow as tf
from tfmsacore import data
from tfmsacore import netconf
from tfmsacore.netcommon.wdnn_common import WdnnCommonManager
from tfmsacore.utils.json_conv import JsonDataConverter as jc
import json, math
import tempfile
from django.conf import settings
from tfmsacore import utils
from rest_framework.response import Response
from tfmsacore.netcommon import monitors_common as Monitors

# flags = tf.app.flags
# FLAGS = flags.FLAGS
# flags.DEFINE_string("model_type", "wide_n_deep",
#                     "Valid model types: {'wide', 'deep', 'wide_n_deep'}.")
# flags.DEFINE_integer("train_steps", 10000, "Number of training steps.")

class wdnn_train(WdnnCommonManager):
    def __init__(self):
        print("############# Create wdnn_train ")
        WdnnCommonManager.__init__(self)

    def run_wdd_train(self, nnid):
        """
                Wide & Deep Network Training
                :param nnid : network id in tfmsacore_nninfo
                :return: acturacy
        """
        try:
            print("start run wdd_Train " + nnid)
            #make wide & deep model
            wdnn_model = WdnnCommonManager.wdnn_build(self, nnid = nnid)

            #get json from postgres by nnid
            json_string = WdnnCommonManager.get_all_info_json_by_nnid(self, nnid=nnid)
            print("############# get json string")
            #print(json_string)
            #parse database, table_name for select data from hbase
            database = json_string["dir"]
            print("############# get database from json string")
            table_name = json_string["table"]

            #Make NetworkConfiguration Json Objct

            json_string = netconf.load_ori_format(nnid)
            json_ob = json.loads(json_string)
            print("####################print")
            print(json_ob)
            print(type(json_ob))

            #json_ob = json.loads(json_string["datadesc"],'utf-8')

            #get label column from hbase nn config json
            t_label = json_ob["label"]

            #for key, value in t_label.iteritems():
            #    print("label key   " , key)
            #label_key =   list(t_label.keys()) #3.5
            #label_column = label_key[0]
            label_column = list(t_label.keys())[0]
            #t_label[]

            print("((2.Get Dataframe from Hbase)) ##Start## (" + database+ " , "+ table_name + " , " + label_column + ")")

            limit_no = 3000 #limit number for hbase cnt
            df = data.DataMaster().query_data(database, table_name, "a", use_df=True,limit_cnt=limit_no,with_label=label_column)
            df_eval = df.copy()
            print("what is df type")
            print(type(df))
            print("((2.Get Dataframe from Hbase)) ##End## (" + database +" , " + table_name + " , " + label_column + " , "+  str(limit_no) + ")")

            ##MAKE MONITOR
            print("###################make monitors ##############")
            model_lint_cnt = 10000
            customsMonitor = Monitors.MonitorCommon(p_nn_id = nnid, p_max_steps=model_lint_cnt, p_every_n_steps=1000)

            print("((3.Wide & Deep Network Train )) ##Start##  (" + nnid + ")")
            wdnn_model.fit(input_fn=lambda: WdnnCommonManager.input_fn(self, df, nnid), steps=model_lint_cnt, monitors=[customsMonitor])
            print("((3.Wide & Deep Network Train )) ##End##  (" + nnid + ")")

            #conf dir need
            results = wdnn_model.evaluate(input_fn=lambda: WdnnCommonManager.input_fn(self, df_eval, nnid), steps=1)

            #predict_results = wdnn_model.predict(input_fn=lambda: WdnnCommonManager.input_fn(self, df, nnid))
            #wdnn_model.predict(i)
            print("##########predict cokes###############")
            #print(predict_results)

            #thefile = open('/home/dev/test_predict.txt', 'w')
            #for item in predict_results:
            #    thefile.write("%s\n" % item)

            #for predict_y in predict_results:
            #    print(predict_y)

            for key in sorted(results):
                print("((4.Wide & Deep Network Accurary)) %s: %s" % (key, results[key]))

            return nnid
        except Exception as e:
            print ("Error Message : {0}".format(e))
            raise Exception(e)

