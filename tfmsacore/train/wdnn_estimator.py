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

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string("model_type", "wide_n_deep",
                    "Valid model types: {'wide', 'deep', 'wide_n_deep'}.")
flags.DEFINE_integer("train_steps", 10000, "Number of training steps.")

def wdd_train(nnid):
    """
            Wide & Deep Network Training
            :param nnid : network id in tfmsacore_nninfo
            :return: acturacy
    """
    try:
        #make wide & deep model
        wdnn_model = wdnn_build(nnid)

        #get json from postgres by nnid
        json_string = get_json_by_nnid(nnid)
        print("############# get json string")
        #print(json_string)
        #parse database, table_name for select data from hbase
        database = json_string["dir"]
        print("############# get database from json string")
        table_name = json_string["table"]

        #Make NetworkConfiguration Json Objct
        json_ob = json.loads(json_string["datadesc"],'utf-8')

        #get label column from hbase nn config json
        t_label = json_ob["label"]
        #for key, value in t_label.iteritems():
        #    print("label key   " , key)
        label_key =   list(t_label.keys()) #3.5
        label_column = label_key[0]

        print("((2.Get Dataframe from Hbase)) ##Start## (" + database+ " , "+ table_name + " , " + label_column + ")")

        limit_no = 2000 #limit number for hbase cnt
        df = data.DataMaster().query_data(database, table_name, "a", use_df=True,limit_cnt=limit_no,with_label=label_column)
        print("what is df type")
        print(type(df))
        print("((2.Get Dataframe from Hbase)) ##End## (" + database +" , " + table_name + " , " + label_column + " , "+  str(limit_no) + ")")

        print("((3.Wide & Deep Network Train )) ##Start##  (" + nnid + ")")
        wdnn_model.fit(input_fn=lambda: input_fn(df, nnid), steps=FLAGS.train_steps)
        print("((3.Wide & Deep Network Train )) ##End##  (" + nnid + ")")

        #conf dir need
        results = wdnn_model.evaluate(input_fn=lambda: input_fn(df, nnid), steps=1)

        for key in sorted(results):
            print("((4.Wide & Deep Network Accurary)) %s: %s" % (key, results[key]))
    except Exception as e:
        print ("Error Message : {0}".format(e))
        raise Exception(e)


def wdd_predict(nnid):
    """
            Wide & Deep Network predict
            :param nnid : network id in tfmsacore_nninfo
            :return: acturacy

    """
    try:
        json_string = get_json_by_nnid(nnid)
        database = str(json_string['dir'],'utf-8')
        table_name = str(json_string['table'],'utf-8')
        json_object = json_string['datadesc']
        model_dir = str(json_string['datasets'],'utf-8')
        json_ob = json.loads(json_object)

        tt = json_ob['cell_feature']

        wdnn_model = wdnn_build(nnid,model_dir,False)

        t_label = json_ob['label']

        for key, value in t_label.items():
            print("label key   " , key)

        label_key =   t_label.keys()
        label_column = label_key[0]
        limit_no = 100
        print("((2.Get Dataframe from Hbase)) ##Start## (" + database + " , " + table_name + " , " + label_column + ")")
        df = data.DataMaster().query_data(database, table_name, "a", limit_no ,with_label=label_column)
        print("((2.Get Dataframe from Hbase)) ##End## (" + database + " , " + table_name + " , " + label_column + " , " + str(limit_no,'utf-8') + ")")

        print("((3.Wide & Deep Network Predict )) ##Start## ")
        results = wdnn_model.evaluate(input_fn=lambda: input_fn(df, nnid), steps=1)
        print("((3.Wide & Deep Network Predict )) ##End## ")

        for key in sorted(results):
            print("((4.Wide & Deep Network Accurary)) %s: %s" % (key, results[key]))
    except Exception as e:
        print ("Error Message : {0}".format(e))
        raise Exception(e)




def input_fn(df, nnid):
    """Wide & Deep Network input tensor maker
            :param df : dataframe from hbase
            :param nnid
            :return: tensor sparse, constraint """
    try:
        print("((3.1 Wide & Deep Network Make Tensor)) ## START ##")
        #print("input fn start")
        CONTINUOUS_COLUMNS = []
        CATEGORICAL_COLUMNS = []

        json_string = get_json_by_nnid(nnid)
        json_object_temp = json_string['datadesc']
        json_object = json.loads(json_object_temp)
        # get all feature colums from json
        j_feature = json_object['cell_feature']

        for cn, c_value in j_feature.items():
          #print(c_value)

          # if c_value["column_type"] == "CATEGORICAL":
          #
          #     featureColumnCategorical[cn] = tf.contrib.layers.sparse_column_with_hash_bucket(
          #         cn, hash_bucket_size=1000)
          # elif c_value["column_type"] == "CATEGORICAL_KEY":
          #     print("((1.Make WDN Network Build)) categorical_key add ")
          #     print(str(c_value["keys"]))
          #     featureColumnContinuous[cn] = tf.contrib.layers.sparse_column_with_keys(column_name=cn,
          #                                                                             keys=c_value["keys"])
          #     print("((1.Make WDN Network Build)) categorical_key add end ")
          #     #
          #     # gender = tf.contrib.layers.sparse_column_with_keys(column_name="gender",
          #     #                                                    keys=["female", "male"])
          # elif c_value["column_type"] == "CONTINUOUS":
          #     featureColumnContinuous[cn] = tf.contrib.layers.real_valued_column(cn)
          if c_value["column_type"] == "CATEGORICAL":
              CATEGORICAL_COLUMNS.append(cn)
          elif c_value["column_type"] == "CONTINUOUS":
              CONTINUOUS_COLUMNS.append(cn)
          elif c_value["column_type"] =="CATEGORICAL_KEY":
              CATEGORICAL_COLUMNS.append(cn)

        print("((3.1 Wide & Deep Network Make Tensor)) ## SPARSE TENSOR ##", CATEGORICAL_COLUMNS)
        print("((3.1 Wide & Deep Network Make Tensor)) ## REAL VALUE TENSOR ##", CONTINUOUS_COLUMNS)
        # Check Continuous Column from json is exsist?
        if len(CONTINUOUS_COLUMNS)>0 :
            print(CONTINUOUS_COLUMNS)
            print("((3.1 Wide & Deep Network Make Tensor)) ## IF CONTINUES")
            for k in CONTINUOUS_COLUMNS:
                print(k)
                print(type(df))
                print(df[k].values)

            print("df should ne wrong?")

            continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}

        # Check Categorical Column from json is exsist?
        if len(CATEGORICAL_COLUMNS) > 0 :
            print("((3.1 Wide & Deep Network Make Tensor)) ## IF CATEGORICAL")
            print()
            for k in CATEGORICAL_COLUMNS:
                print(k)
                print("df should ne wrong?")
                print(df[k].size)

            categorical_cols = {k: tf.SparseTensor(
              indices=[[i, 0] for i in range(df[k].size)],
              values=df[k].values,
              shape=[df[k].size, 1])
                              for k in CATEGORICAL_COLUMNS}
            # Merges the two dictionaries into one.
        print("((3.1 Wide & Deep Network Make Tensor)) ## SAPRSE TENSOR INPUT ##")
        if(len(CONTINUOUS_COLUMNS)>0):
            print("((3.1 Wide & Deep Network Make Tensor)) ## IF CONTINUE ADD LIST")
            feature_cols = dict(continuous_cols)
        if len(CATEGORICAL_COLUMNS) > 0:
            print("((3.1 Wide & Deep Network Make Tensor)) ## IF CATEGORICAL ADD LIST")
            feature_cols.update(categorical_cols)
        # Converts the label column into a constant Tensor.
        #label={'label':tf.constant(df["label"].values)}
        label = tf.constant(df["label"].values)
        print("((3.1 Wide & Deep Network Make Tensor)) ## END ##")
        # Returns the feature columns and the label.
        #print(feature_cols)
        print("((3.1 Wide & Deep Network Make Tensor LABEL)) ## START##")
        #print(label)
        #print(df["label"].values)
        return feature_cols, label
    except Exception as e:
        print("Error Message : {0}".format(e))
        raise Exception(e)

def get_json_by_nnid(nnid):
    """get network config json
    :param nnid
    :return: json string """
    print("get_json_networkid########")
    result = netconf.get_network_config(nnid)
    print(result)
    return result

def wdnn_build(nnid, model_dir = "No", train=True):
    """ wide & deep netowork builder
        :param nnid
        :param model_dir : directory of chkpoint of wdnn model
        :param train : train or predict
        :return: tensorflow network model """
    try:
        # need json, model_dir
        print("((1.Make WDN Network Build)) start wddd build (" + nnid + ")")
        json_string = get_json_by_nnid(nnid)
        print("get json string in wdnn builder ####")
        print(json_string)

        #json_object = json.loads(json.dumps(json_string["datadesc"])) #3.5 fixed 16.11.02
        json_object = json.loads(json_string["datadesc"])
        print("get json string in wdnn builder ####")
        # load NN conf form db
        utils.tfmsa_logger("[4]load net conf form db")
        conf = netconf.load_conf(nnid)
        hidden_layers_value = conf.layer
        #hidden_layers_value2 = conf["layer"]
        #print("((1.Make WDN Network Build)) config load " + str(hidden_layers_value2))
        print("((1.Make WDN Network Build)) set up Hidden Layers ("+ str(hidden_layers_value),'utf-8' + ")")

        if(train):
            model_dir = settings.HDFS_MODEL_ROOT + "/"+nnid + "/"+tempfile.mkdtemp().split("/")[2]
        else:
            if(model_dir != "No"):
                model_dir = model_dir
        print("((1.Make WDN Network Build)) set up WDNN directory("+nnid +") ---> " + model_dir)

        # continuous, categorical and embeddingforCategorical(deep) list
        featureColumnCategorical = {}
        featureColumnContinuous = {}
        featureDeepEmbedding={}
        #print("before json convert")
        #print(json_object) #cross_cell
        print("before Cell feature")
        j_feature = json_object["cell_feature"]
        print(j_feature)
        print("after Cell feature")
        print("((1.Make WDN Network Build)) set up Hidden Layers (" + str(hidden_layers_value), 'utf-8' + ")")
        for cn, c_value in j_feature.items(): #change 3.5python
            print("((1.Make WDN Network Build)) first get feature columns " + str(c_value["column_type"]),'utf-8')

            if c_value["column_type"] == "CATEGORICAL":
                featureColumnCategorical[cn] = tf.contrib.layers.sparse_column_with_hash_bucket(
                    cn, hash_bucket_size=1000)
            elif c_value["column_type"] == "CATEGORICAL_KEY":
                print("((1.Make WDN Network Build)) categorical_key add ")
                print(c_value["keys"])
                featureColumnCategorical[cn] = tf.contrib.layers.sparse_column_with_keys(column_name=cn,keys=c_value["keys"])
                print("((1.Make WDN Network Build)) categorical_key add end ")
            elif c_value["column_type"] == "CONTINUOUS": #CONTINUOUS
                print("((1.Make WDN Network Build)) CONTINUOUS add ")
                featureColumnContinuous[cn] = tf.contrib.layers.real_valued_column(cn)
        # embedding column add
        for key, value in featureColumnCategorical.items(): #3.5python
            print("((1.Make WDN Network Build)) Categorical Embedding add ")
            featureDeepEmbedding[key] = tf.contrib.layers.embedding_column(value, dimension=8)

        wide_columns = []
        for sparseTensor in featureColumnCategorical:
            wide_columns.append(featureColumnCategorical[sparseTensor])

        # cross_cell checks null
        cross_col1 = []
        if 'cross_cell' in json_object: #json_object.has_key('cross_cell'):
            j_cross = json_object["cross_cell"]
            for jc, values in j_cross.items():
                print("((1.Make WDN Network Build)) Cross rows " + str(values) )
                for c_key, c_value in values.items(): #3.5python
                    cross_col1.append(featureColumnCategorical[c_value])
                wide_columns.append(tf.contrib.layers.crossed_column(cross_col1,hash_bucket_size=int(1e4)))

        ##Transformations column for wide
        transfomation_col= {}
        if 'Transformations' in json_object: #json_object.has_key('Transformations'):
            j_boundaries = json_object["Transformations"]
            for jc, values in j_boundaries.items(): #3.5python
                print("((1-1.Make WDN Network Build)) TransForm Columns " + str(values))
                trans_col_name = values["column_name"]
                trans_boundaries = values["boundaries"]
                print("((1-1 get age columns  )) ")
                print(type(featureColumnContinuous[trans_col_name]))
                rvc = featureColumnContinuous[trans_col_name]

                #print("((1-1 transform cell parameters )) key : " + str(jc) +" --->  "+ trans_col_name + ":" + trans_boundaries)
                transfomation_col[jc] = tf.contrib.layers.bucketized_column(featureColumnContinuous[trans_col_name],trans_boundaries)
                wide_columns.append(tf.contrib.layers.bucketized_column(featureColumnContinuous[trans_col_name],trans_boundaries))
                print("((1-1 transform tensor insert))")

        deep_columns = []
        for realTensor in featureColumnContinuous:
            deep_columns.append(featureColumnContinuous[realTensor])

        # categorucal colums change to embedTensor for Deep
        for embeddingTensor in featureDeepEmbedding:
            deep_columns.append(featureDeepEmbedding[embeddingTensor])
#'wide', 'deep', 'wide_n_deep'
        network_type = flags.DEFINE_string
        if FLAGS.model_type == "wide_n_deep":
            print("###################wide and deep network##############")
            m = tf.contrib.learn.DNNLinearCombinedClassifier(
                model_dir=model_dir,
                linear_feature_columns=wide_columns,
                dnn_feature_columns=deep_columns,
                dnn_hidden_units=hidden_layers_value)
        elif FLAGS.model_type == "wide":
            print("###################wide network#######################")
            m = tf.contrib.learn.LinearClassifier(model_dir=model_dir,
                                                  feature_columns=wide_columns
                                                  ,enable_centered_bias = True)
            print("wide network end")
        elif FLAGS.model_type =="deep":
            print("###################deep###############################")
            print(deep_columns)
            m = tf.contrib.learn.DNNClassifier(model_dir=model_dir,
                                                   feature_columns=deep_columns,
                                                   n_classes = 3, #0.11 bug
                                                   hidden_units=hidden_layers_value)

        rv = network_update(nnid,model_dir)
        print("((1.Make WDN Network Build)) wdnn directory info update sucess")
        return m
    except Exception as e:
        print("Error Message : {0}".format(e))
        raise Exception(e)


def network_update(nnid, model_dir):
    """ Wide Deep Network Info directory sae
        :param nnid
        :param model_dir : directory of chkpoint of wdnn model
    """
    try:
        jd = jc.load_obj_json("{}")
        #temporaly use dataset.
        jd.datasets = model_dir
        jd.nn_id = nnid
        netconf.update_network(jd)
        return_data = {"status": "200", "result": nnid}

    except Exception as e:
        return_data = {"status": "404", "result": str(e)}
        print("Error Message : {0}".format(e))
        raise Exception(e)
    finally:
        return return_data

def main(_):
    wdd_train()
