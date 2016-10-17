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

def wdd_train(nnid):
    """
            Wide & Deep Network Training
            :param nnid : network id in tfmsacore_nninfo
            :return: acturacy
    """

    #make wide & deep model
    wdnn_model = wdnn_build(nnid)

    #get json from postgres by nnid
    json_string = get_json_by_nnid(nnid)
    #parse database, table_name for select data from hbase
    database = str(json_string['dir'])
    table_name = str(json_string['table'])

    #Make NetworkConfiguration Json Objct
    json_ob = json.loads(json_string['datadesc'])
    #print(json_ob)

    #get label column from hbase nn config json
    t_label = json_ob['label']
    #for key, value in t_label.iteritems():
    #    print("label key   " , key)
    label_key =   t_label.keys()
    label_column = label_key[0]
    #print(label_key[0])
    #key, value = t_label[0]
    #print(key)
    print("((2.Get Dataframe from Hbase)) ##Start## (" + database+ " , "+ table_name + " , " + label_column + ")")
    #dataframe, tablename
    limit_no = 3000
    df = data.DataMaster().query_data(database, table_name, "a", limit_no,with_label=label_column)

    print("((2.Get Dataframe from Hbase)) ##End## (" + database +" , " + table_name + " , " + label_column + " , "+  str(limit_no) + ")")

    #cols , label = input_fn(df,nnid)
    #print("a")
    #print(cols)

    print("((3.Wide & Deep Network Train )) ##Start##  (" + nnid + ")")
    wdnn_model.fit(input_fn=lambda: input_fn(df, nnid), steps=200)
    print("((3.Wide & Deep Network Train )) ##End##  (" + nnid + ")")

    #conf dir need

    results = wdnn_model.evaluate(input_fn=lambda: input_fn(df, nnid), steps=1)

    for key in sorted(results):
        print("((4.Wide & Deep Network Accurary)) %s: %s" % (key, results[key]))


def wdd_predict(nnid):
    """
            Wide & Deep Network predict
            :param nnid : network id in tfmsacore_nninfo
            :return: acturacy

    """
    try:
        json_string = get_json_by_nnid(nnid)
        database = str(json_string['dir'])
        table_name = str(json_string['table'])
        json_object = json_string['datadesc']
        model_dir = str(json_string['datasets'])
        json_ob = json.loads(json_object)
        #json_label = json_object["label"]
        #print(database)
        #print(table_name)
        tt = json_ob['cell_feature']
        #print(json_ob)
        #print(tt)
        #print("database    ", database)
        #print("table_name    ", table_name)

        wdnn_model = wdnn_build(nnid,model_dir,False)

        t_label = json_ob['label']

        for key, value in t_label.iteritems():
            print("label key   " , key)

        label_key =   t_label.keys()
        label_column = label_key[0]
        #print(label_key[0])
        #key, value = t_label[0]
        #print(key)
        limit_no = 100
        print("((2.Get Dataframe from Hbase)) ##Start## (" + database + " , " + table_name + " , " + label_column + ")")
        df = data.DataMaster().query_data(database, table_name, "a", limit_no ,with_label=label_column)
        print("((2.Get Dataframe from Hbase)) ##End## (" + database + " , " + table_name + " , " + label_column + " , " + str(limit_no) + ")")

        #cols , label = input_fn(df,nnid)
        #print("a")
        #print(cols)

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

    print("((3.1 Wide & Deep Network Make Tensor)) ## START ##")
    #print("input fn start")
    CONTINUOUS_COLUMNS = []
    CATEGORICAL_COLUMNS = []

    json_string = get_json_by_nnid(nnid)
    json_object_temp = json_string['datadesc']
    json_object = json.loads(json_object_temp)
    # get all feature colums from json
    j_feature = json_object['cell_feature']

    for cn, c_value in j_feature.iteritems():
      #print(c_value)
      if c_value == "CATEGORICAL":
          CATEGORICAL_COLUMNS.append(cn)
      elif c_value == "CONTINUOUS_COLUMNS":
          CONTINUOUS_COLUMNS.append(cn)

    print("((3.1 Wide & Deep Network Make Tensor)) ## SPARSE TENSOR ##", CATEGORICAL_COLUMNS)
    print("((3.1 Wide & Deep Network Make Tensor)) ## REAL VALUE TENSOR ##", CONTINUOUS_COLUMNS)

    continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
    # Creates a dictionary mapping from each categorical feature column name (k)
    # to the values of that column stored in a tf.SparseTensor.
    categorical_cols = {k: tf.SparseTensor(
      indices=[[i, 0] for i in range(df[k].size)],
      values=df[k].values,
      shape=[df[k].size, 1])
                      for k in CATEGORICAL_COLUMNS}
    # Merges the two dictionaries into one.
    feature_cols = dict(continuous_cols)
    feature_cols.update(categorical_cols)
    # Converts the label column into a constant Tensor.
    label = tf.constant(df["label"].values)
    print("((3.1 Wide & Deep Network Make Tensor)) ## END ##")
    # Returns the feature columns and the label.
    return feature_cols, label

def get_json_by_nnid(nnid):
    """get network config json
    :param nnid
    :return: json string """

    result = netconf.get_network_config(nnid)
    return result

def wdnn_build(nnid, model_dir = "No", train=True):
    """ wide & deep netowork builder
        :param nnid
        :param model_dir : directory of chkpoint of wdnn model
        :param train : train or predict
        :return: tensorflow network model """

    # need json, model_dir
    print("((1.Make WDN Network Build)) start wddd build (" + nnid + ")")
    json_string = get_json_by_nnid(nnid)
    json_object = json.loads(json_string['datadesc'])

    #hidden_layers = json_string['datasize']
    hidden_layers = json.loads(json_string['datasize'])  # should change columns after alter table
    hidden_layers_value = hidden_layers["layer"]
    #h = type(hidden_layers_value)
    print("((1.Make WDN Network Build)) set up Hidden Layers ("+ str(hidden_layers_value) + ")")

    if(train):
        model_dir = settings.HDFS_MODEL_ROOT + "/"+nnid + "/"+tempfile.mkdtemp().split("/")[2]
    else:
        if(model_dir <> "No"):
            model_dir = model_dir
    print("((1.Make WDN Network Build)) set up WDNN directory("+nnid +") ---> " + model_dir)

    #json_object = json.loads(jsonFile)filename
    featureColumnCategorical = {}
    featureColumnContinuous = {}

    j_feature = json_object["cell_feature"]

    for cn, c_value in j_feature.iteritems():
        #print(c_value)
        if c_value == "CATEGORICAL":
            featureColumnCategorical[cn] = tf.contrib.layers.sparse_column_with_hash_bucket(
                cn, hash_bucket_size=1000)
        elif c_value == "CONTINUOUS_COLUMNS":
            featureColumnContinuous[cn] = tf.contrib.layers.real_valued_column(cn)

    wide_columns = []
    for sparseTensor in featureColumnCategorical:
        wide_columns.append(featureColumnCategorical[sparseTensor])

    j_cross = json_object["cross_cell"]

    cross_col1 = []
    #cross_feature = []
    for jc, values in j_cross.iteritems():
        print("((1.Make WDN Network Build)) Cross rows " + str(values))
        for c_key, c_value in values.iteritems():
            cross_col1.append(featureColumnCategorical[c_value])
            #print("((1.Make WDN Network Build)) Cross Colume " + str(c_value))
        wide_columns.append(tf.contrib.layers.crossed_column(cross_col1,hash_bucket_size=int(1e4)))

    deep_columns = []
    for realTensor in featureColumnContinuous:
        deep_columns.append(featureColumnContinuous[realTensor])

    m = tf.contrib.learn.DNNLinearCombinedClassifier(
        model_dir=model_dir,
        linear_feature_columns=wide_columns,
        dnn_feature_columns=deep_columns,
        dnn_hidden_units=hidden_layers_value)

    rv = network_update(nnid,model_dir)
    print("((1.Make WDN Network Build)) wdnn directory info update sucess")
    return m

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
    finally:
        return return_data

def main(_):
    wdd_train()
