import requests
import json
import tensorflow as tf
import logging
from django.conf import settings

# Reference
#https://realpython.com/blog/python/api-integration-in-python/
#http://www.slideshare.net/Byungwook/rest-api-60505484

url = "8ea172cae00f:8989"


####################################################################################
# Common - nninfo
####################################################################################

def common_nninfo_post():
    resp = requests.post('http://' + url + '/api/v1/type/common/nninfo/',
                         json={
                             "nn_id": "nn0000009",
                             "category": "cate1",
                             "subcate" : "subcate1",
                             "name": "test",
                             "desc" : "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                         })

    data = json.loads(resp.json())
    print("test result : {0}".format(data))


def common_nninfo_get():
    #resp = requests.get('http://' + url + '/api/v1/type/common/nninfo/nn0000009/category/cate1/subcate/subcate1/')
    #resp = requests.get('http://' + url + '/api/v1/type/common/nninfo//category//subcate/subcate1/')
    resp = requests.get('http://' + url + '/api/v1/type/common/nninfo//category//subcate//')
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def common_nninfo_put():
    resp = requests.put('http://' + url + '/api/v1/type/common/nninfo/',
                         json={
                             "nn_id": "nn0000008",
                             "category": "cate1",
                             "subcate" : "subcate1",
                             "name": "test",
                             "desc" : "sssssssssssssssssssssss"
                         })
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def common_nninfo_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/common/nninfo/',
                         json=['nn0000008', 'nn0000009'])
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

####################################################################################
# DataFrame - database
####################################################################################

def dataframe_base_post():
    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/testschema/',)
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def dataframe_base_get():
    resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/',)
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def dataframe_base_put():
    resp = requests.put('http://' + url + '/api/v1/type/dataframe/base/',
                        json={"origin" : "test1" , "modify" : "xxxxx"})
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def dataframe_base_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/dataframe/base/test2/')
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

####################################################################################
# DataFrame - table
####################################################################################
def dataframe_table_post():
    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/testschema/table/ddd/')
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def dataframe_table_get():
    resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/testschema/table/')
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def dataframe_table_put():
    resp = requests.put('http://' + url + '/api/v1/type/dataframe/base/testschema/table/',
                        json={"origin" : "ddd" , "modify" : "zzz"})
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def dataframe_table_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/dataframe/base/testschema/table/ddd/')
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

####################################################################################
# DataFrame - format
####################################################################################

def dataframe_format_post():
    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/testschema/table/ddd/format/nn0000009/',
                         json={"name":"none", "univ":"rank", "org" : "cate" , "eng" : "cont", "grade" : "tag",
                               "gender" :"cate" , "age" : "cont"})
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def dataframe_format_get():
    resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/testschema/table/ddd/format/nn0000009/')
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def dataframe_format_put():
    resp = requests.put('http://' + url + '/api/v1/type/dataframe/base/testschema/table/ddd/format/nn0000009/',
                        json={"name": "none", "univ": "rank", "org": "cate", "eng": "cont", "grade": "tag",
                                          "gender": "cate", "age": "cont"})
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def dataframe_format_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/dataframe/base/testschema/table/ddd/format/nn0000009/')
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

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
    print("test result : {0}".format(data))

def dataframe_data_get():
    """
    col type (None) : not gonna use on the model
    col type (cont) : continuous data can be used without modification
    col type (cate) : categorical data needs to be modified
    :return:
    """

    resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/testschema/table/ddd/data/')

    data = json.loads(resp.json())
    print("test result : {0}".format(data))

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
    print("test result : {0}".format(data))

####################################################################################
# DataFrame - preprocess
####################################################################################
def dataframe_pre_post():
    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/testschema/table/ddd/pre/nn0000009/')
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def dataframe_pre_get():
    resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/testschema/table/ddd/pre/nn0000009/')
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def dataframe_pre_put():
    resp = requests.put('http://' + url + '/api/v1/type/dataframe/base/testschema/table/ddd/pre/nn0000009/')
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def dataframe_pre_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/dataframe/base/testschema/table/ddd/pre/nn0000009/')
    data = json.loads(resp.json())
    print("test result : {0}".format(data))


####################################################################################
# CNN - Config
####################################################################################
def cnn_conf_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/conf/nn0000009/',
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
    print("test result : {0}".format(data))

def cnn_conf_get():
    resp = requests.get('http://' + url + '/api/v1/type/cnn/conf/nn0000009/')
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

def cnn_conf_put():
    resp = requests.put('http://' + url + '/api/v1/type/cnn/conf/nn0000009/',
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
    print("test result : {0}".format(data))

def cnn_conf_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/cnn/conf/nn0000009/')
    data = json.loads(resp.json())
    print("test result : {0}".format(data))


####################################################################################
# CNN - Train
####################################################################################

def cnn_train_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/train/nn0000009/',
                         json= {
                             "epoch" : "50",
                             "testset" : "10"
                         })
    data = json.loads(resp.json())
    print("test result : {0}".format(data))


####################################################################################
# CNN - Predict
####################################################################################

def cnn_predict_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/predict/nn0000009/',
                         json= [{'name':'Andy', 'univ':'a', 'org' : '1', 'eng' : '800' , 'gender' : 'female', 'age' : '50'}]
                         )
    data = json.loads(resp.json())
    print("test result : {0}".format(data))


####################################################################################
# TEST - TEST - TEST
####################################################################################

#common, dataframe, cnn
category1 = "cnn"
# checker, predict, stat, test, train, conf, nnfino, base, data, format, table, pre
category2 = "predict"
# post, get, put, delete
request = "post"


locals()["{0}_{1}_{2}".format(category1, category2, request)]()
