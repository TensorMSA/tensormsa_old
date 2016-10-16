import requests
import json
import tensorflow as tf
import logging
from django.conf import settings

# Reference
#https://realpython.com/blog/python/api-integration-in-python/
#http://www.slideshare.net/Byungwook/rest-api-60505484

url = "2fd17f7a6b09:8989"


####################################################################################
# Common - nninfo
####################################################################################

def common_nninfo_post():
    # resp = requests.post('http://' + url + '/api/v1/type/common/nninfo/',
    #                      json={
    #                          "nn_id": "nn0000011",
    #                          "category": "evaluation",
    #                          "subcate" : "csv",
    #                          "name": "evaluation",
    #                          "desc" : "wdnn_protoType"
    #                      })
    resp = requests.post('http://' + url + '/api/v1/type/common/nninfo/',
                         json={
                             "nn_id": "nn0000012",
                             "category": "evaluation",
                             "subcate" : "csv",
                             "name": "evaluation",
                             "desc" : "wdnn_protoType"
                         })


    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


def common_nninfo_get():
    #resp = requests.get('http://' + url + '/api/v1/type/common/nninfo/nn0000009/category/cate1/subcate/subcate1/')
    #resp = requests.get('http://' + url + '/api/v1/type/common/nninfo//category//subcate/subcate1/')
    resp = requests.get('http://' + url + '/api/v1/type/common/nninfo//category//subcate//')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def common_nninfo_put():
    resp = requests.put('http://' + url + '/api/v1/type/common/nninfo/',
                         json={
                             "nn_id": "nn0000010",
                             "category": "evaluation",
                             "subcate" : "csv",
                             "name": "evaluation",
                             "desc" : "sssssssssssssssssssssss"
                         })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def common_nninfo_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/common/nninfo/',
                         json=['nn0000008', 'nn0000009'])
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

####################################################################################
# DataFrame - database
####################################################################################

def dataframe_base_post():
    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/csvtest/',)
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_base_get():
    resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/',)
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_base_put():
    resp = requests.put('http://' + url + '/api/v1/type/dataframe/base/',
                        json={"origin" : "test1" , "modify" : "xxxxx"})
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_base_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/dataframe/base/csvtest/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

####################################################################################
# DataFrame - table
####################################################################################
def dataframe_table_post():
    #resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/titanic/')
    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/scm/table/tb_test_incomedata_wdnn3/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_table_get():
    resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_table_put():
    resp = requests.put('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/',
                        json={"origin" : "ddd" , "modify" : "zzz"})
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_table_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/titanic/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

####################################################################################
# DataFrame - format
##########################################################5e5b6cb099aa##########################

def dataframe_format_post():
    # resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/titanic/format/nn0000010/',
    #                      json={"pclass":"cate",
    #                            "survived":"tag",
    #                            "name" : "none" ,
    #                            "sex" : "cate",
    #                            "age" : "cont",
    #                            "embarked": "cate",
    #                            "boat": "cate"
    #                            })
    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/scm/table/tb_test_incomedata_wdnn3/format/nn0000012/',
                         json={ "cross_cell":
                                    {
                                      "col12": {"column2_0": "native_country", "column2_1": "occupation"},
                                      "col1": {"column_1": "occupation", "column_0": "education"}
                                    },
                                  "cell_feature":
                                    {
                                      "hours_per_week": "CONTINUOUS_COLUMNS",
                                      "native_country": "CATEGORICAL",
                                      "relationship": "CATEGORICAL",
                                      "gender": "CATEGORICAL",
                                      "age": "CONTINUOUS_COLUMNS",
                                      "marital_status": "CATEGORICAL",
                                      "race": "CATEGORICAL",
                                      "capital_gain": "CONTINUOUS_COLUMNS",
                                      "workclass": "CATEGORICAL",
                                      "capital_loss": "CONTINUOUS_COLUMNS",
                                      "education": "CATEGORICAL",
                                      "education_num": "CONTINUOUS_COLUMNS",
                                      "occupation": "CATEGORICAL"
                                    },
                                  "label":
                                    {
                                       "income_bracket" : "LABEL"
                                    }
                               })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_format_get():
    resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/titanic/format/nn0000010/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_format_put():
    resp = requests.put('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/titanic/format/nn0000010/',
                        json={"pclass":"cate",
                               "survived":"tag",
                               "name" : "none" ,
                               "sex" : "cate",
                               "age" : "cont",
                               "embarked": "cate",
                               "boat": "cate"
                               })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_format_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/ddd/format/nn0000010/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

####################################################################################
# DataFrame - data
####################################################################################


def dataframe_data_post():
    """
    col type (None) : not gonna use on the model
    col type (cont) : continuous data can be used without modification
    col type (cate) : categorical data needs to be modified
    :return:
    """

    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/testschema/table/ddd/data/JSON/',
                        json= {
                                "data":[{'name':'Andy', 'univ':'SKKU', 'org' : '1', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '50'},
                                        {'name':'Kim', 'univ':'SKKU', 'org' : '2', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '35'},
                                        {'name':'Kim', 'univ':'SKKU', 'org' : '3', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '65'},
                                        {'name':'Kim', 'univ':'SKKU', 'org' : '4', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '70'},
                                        {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'},
                                        {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'},
                                        {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'}]
                        })

    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_data_get():
    """
    col type (None) : not gonna use on the model
    col type (cont) : continuous data can be used without modification
    col type (cate) : categorical data needs to be modified
    :return:
    """
    resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/scm/table/tb_test_incomedata_wdnn3/data/a')
    #resp = requests.get('http://' + url + '/api/v1/type/dataframe/scm/table/tb_test_imcomedata_wdnn/data/a')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_data_put():
    """
    col type (None) : not gonna use on the model
    col type (cont) : continuous data can be used without modification
    col type (cate) : categorical data needs to be modified
    :return:
    """

    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/testschema/table/ddd/data/JSON/',
                        json= {
                                "data":[{'name':'Andy', 'univ':'SKKU', 'org' : '1', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '50'},
                                        {'name':'Kim', 'univ':'SKKU', 'org' : '2', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '35'},
                                        {'name':'Kim', 'univ':'SKKU', 'org' : '3', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '65'},
                                        {'name':'Kim', 'univ':'xxxx', 'org' : '4', 'eng' : '800' , 'grade' : 'B', 'gender' : 'female', 'age' : '70'},
                                        {'name':'Kim', 'univ':'xxxx', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'},
                                        {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'},
                                        {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'}]
                        })

    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

####################################################################################
# DataFrame - preprocess
####################################################################################
def dataframe_pre_post():
    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/titanic/pre/nn0000010/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_pre_get():
    resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/titanic/pre/nn0000010/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_pre_put():
    resp = requests.put('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/titanic/pre/nn0000010/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_pre_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/titanic/pre/nn0000010/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


####################################################################################
# WDNN - Config
####################################################################################
def wdnn_conf_post():
    resp = requests.post('http://' + url + '/api/v1/type/wdnn/conf/nn0000012/',
                         json={
                                 "layer":[100,50,20]
                             })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def wdnn_train_post():
    #resp = requests.post('http://' + url + '/api/v1/type/wdnn/train/nn0000011/')
    resp = requests.post('http://' + url + '/api/v1/type/wdnn/train/nn0000012/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


def wdnn_predict_post():
    #resp = requests.post('http://' + url + '/api/v1/type/wdnn/predict/nn0000011/')
    resp = requests.post('http://' + url + '/api/v1/type/wdnn/predict/nn0000012/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

####################################################################################
# CNN - Config
####################################################################################
def cnn_conf_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/conf/nn0000010/',
                         json={
                                 "data":
                                     {
                                         "datalen": 96,
                                         "taglen": 2,
                                         "matrix": [12, 8],
                                         "learnrate": 0.01,
                                         "epoch": 10
                                     },
                                 "layer":
                                     [
                                         {
                                             "type": "input",
                                             "active": "relu",
                                             "cnnfilter": [2, 2],
                                             "cnnstride": [1, 1],
                                             "maxpoolmatrix": [2, 2],
                                             "maxpoolstride": [1, 1],
                                             "node_in_out": [1, 16],
                                             "regualizer": "",
                                             "padding": "SAME",
                                             "droprate": ""
                                         },
                                         {
                                             "type": "out",
                                             "active": "softmax",
                                             "cnnfilter": "",
                                             "cnnstride": "",
                                             "maxpoolmatrix": "",
                                             "maxpoolstride": "",
                                             "node_in_out": [64, 2],
                                             "regualizer": "",
                                             "padding": "SAME",
                                             "droprate": ""
                                         }
                                     ]
                             })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def cnn_conf_get():
    resp = requests.get('http://' + url + '/api/v1/type/cnn/conf/nn0000010/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def cnn_conf_put():
    resp = requests.put('http://' + url + '/api/v1/type/cnn/conf/nn0000010/',
                         json={
                                 "data":
                                     {
                                         "datalen": 96,
                                         "taglen": 2,
                                         "matrix": [12, 8],
                                         "learnrate": 0.01,
                                         "epoch": 10
                                     },
                                 "layer":
                                     [
                                         {
                                             "type": "input",
                                             "active": "relu",
                                             "cnnfilter": [2, 2],
                                             "cnnstride": [1, 1],
                                             "maxpoolmatrix": [2, 2],
                                             "maxpoolstride": [1, 1],
                                             "node_in_out": [1, 16],
                                             "regualizer": "",
                                             "padding": "SAME",
                                             "droprate": ""
                                         },
                                         {
                                             "type": "out",
                                             "active": "softmax",
                                             "cnnfilter": "",
                                             "cnnstride": "",
                                             "maxpoolmatrix": "",
                                             "maxpoolstride": "",
                                             "node_in_out": [64, 2],
                                             "regualizer": "",
                                             "padding": "SAME",
                                             "droprate": ""
                                         }
                                     ]
                             })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def cnn_conf_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/cnn/conf/nn0000010/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


####################################################################################
# CNN - Train
####################################################################################

def cnn_train_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/train/nn0000010/',
                         json= {
                             "epoch" : "10",
                             "testset" : "10"
                         })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


####################################################################################
# CNN - Predict
####################################################################################

def cnn_predict_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/predict/nn0000010/',
                         json= [
                             {"pclass": "1st",
                              "survived": "tag",
                              "sex": "female",
                              "age": "30",
                              "embarked": "Southampton",
                              "boat": "2"
                              }]
                         )
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))



####################################################################################
# Common task manager
####################################################################################

#datetime(2013, 6, 5, 23, 59, 59, 999999)
def common_job_post():
    resp = requests.post('http://' + url + '/api/v1/type/common/job/nn0000009/',
                         json= {'year':2013, 'month':6, 'day' :5, 'hour' :23 , 'min' : 59, 'sec' : 59}
                         )
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


def common_job_get():
    resp = requests.get('http://' + url + '/api/v1/type/common/job/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


def common_job_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/common/job/nn0000009/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

####################################################################################
# common server setting
####################################################################################

def common_env_post():
    resp = requests.post('http://' + url + '/api/v1/type/common/env/',
                         json= {'state': 'A',
                                'store_type': '1',
                                'fw_capa' : '1',
                                'livy_host' : '8ea172cae00f:8998' ,
                                'livy_sess' : '1',
                                'spark_host' : '8ea172cae00f:7077',
                                'spark_core': '1',
                                'spark_memory': '1G',
                                'hdfs_host': '587ed1df9441:9000',
                                'hdfs_root': '/tensormsa',
                                's3_host': '',
                                's3_access': '',
                                's3_sess': '',
                                's3_bucket': '',
                                }
                         )
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


def common_env_get():
    resp = requests.get('http://' + url + '/api/v1/type/common/env/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


####################################################################################
# Livy Session
####################################################################################

def common_livy_post():
    resp = requests.post('http://' + url + '/api/v1/type/common/livy/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def common_livy_get():
    resp = requests.get('http://' + url + '/api/v1/type/common/livy/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def common_livy_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/common/livy/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

####################################################################################
# cnn - checker - post
####################################################################################

def cnn_checker_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/checker/nn0000010/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


####################################################################################
# cnn - eval - post
####################################################################################

def cnn_eval_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/eval/nn0000010/',
                         json={'samplenum': 0.1, 'samplemethod' : '1'})
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def cnn_eval_get():
    resp = requests.get('http://' + url + '/api/v1/type/cnn/eval/nn0000010/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


####################################################################################
# TEST - TEST - TEST
####################################################################################

"""
Test Sequence !!
1. common - env - post
2. common - nninfo - post
3. dataframe - base - post
    3.1 Hbase does not need it
4. dataframe - table - post

5. JSON(dataframe - data - post)
    5.1 Json devolop for next time
5. CSV(use ui http://localhost:8989/view/ftptest)

6. dataframe - format - post
7. dataframe - pre - post
   7.1 doesn't need it for wdnnb
8. cnn - conf - post
9. cnn - checker - post
10. cnn - train - post
11. cnn - predict- post
"""


"""
Wdnn Test Sequence !!

2. common - nninfo - post

4. dataframe - table - post

5. CSV(use ui http://localhost:8989/view/ftptest)

6. dataframe - format - post

8.wdnn - conf - post
10. wdnn - train - post
11. wdnn - predict- post
"""
#common, dataframe, cnn, wdnn
category1 = "wdnn"
# checker, predict, stat, evaluation, train, conf, nnfino, base, data, format, table, pre
category2 = "predict"
# post, get, put, delete
request = "post"


locals()["{0}_{1}_{2}".format(category1, category2, request)]()
