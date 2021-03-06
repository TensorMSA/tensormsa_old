import requests
import json, os
import tensorflow as tf
import logging
from django.conf import settings
from PIL import Image, ImageFilter
#from tfmsacore import netconf
#from tfmsacore.utils.json_conv import JsonDataConverter as jc
import datetime

# Reference
#https://realpython.com/blog/python/api-integration-in-python/
#http://www.slideshare.net/Byungwook/rest-api-60505484

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")
#url = "52.78.19.96:8989"

####################################################################################
# Common - nninfo
####################################################################################
def simple_resize(path, x_size, y_size):
    """
    simply resize image and return array
    :param path:
    :return:
    """

    im = Image.open(path).convert('L')
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (x_size, y_size), (255))

    if width > height:
        nheight = int(round((x_size / width * height), 0))
        img = im.resize((x_size, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((y_size - nheight) / 2), 0))
        newImage.paste(img, (4, wtop))
    else:
        nwidth = int(round((x_size / height * width), 0))
        if (nwidth == 0):
            nwidth = 1

        img = im.resize((nwidth, y_size), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((y_size - nwidth) / 2), 0))
        newImage.paste(img, (wleft, 4))

    return list(newImage.getdata())

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
                             "nn_id": "nn0000045",
                             "category": "MES",
                             "subcate" : "csv",
                             "name": "CENSUS_INCOME",
                             "desc" : "INCOME PREDICT"
                         })


    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


def common_nninfo_get():
    #resp = requests.get('http://' + url + '/api/v1/type/common/nninfo/nn0000009/category/cate1/subcate/subcate1/')
    #resp = requests.get('http://' + url + '/api/v1/type/common/nninfo//category//subcate/subcate1/')
    resp = requests.get('http://' + url + '/api/v1/type/common/nninfo/scm_default_wdnn_66039/category//subcate//')
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
    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/scm/table/tb_census_data01/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_table_get():
    #resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/')
    resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/scm/table/')
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
    #
    # resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/scm/table/tb_data_cokes/format/nn0000020/',
    #                      json={"label":
    #                                 {"COKE_Q_DI150_Class": "LABEL"}
    #                             , "cell_feature":
    #                                 {"ASH": {"column_type": "CONTINUOUS"} # u'ASH': <tf.Tensor 'Const_1:0' shape=(1000,) dtype=float64>
    #                                 , "VM": {"column_type": "CONTINUOUS"} #u'VM': <tf.Tensor 'Const_3:0' shape=(1000,) dtype=float64>
    #                                 , "TS": {"column_type": "CONTINUOUS"} # u'TS': <tf.Tensor 'Const_4:0' shape=(1000,) dtype=float64>
    #                                 , "TD": {"column_type": "CONTINUOUS"} # u'TD': <tf.Tensor 'Const_10:0' shape=(1000,) dtype=int64>
    #                                 , "L_MF": {"column_type": "CONTINUOUS"} # u'L_MF': <tf.Tensor 'Const_7:0' shape=(1000,) dtype=float64>
    #                                 , "SI": {"column_type": "CONTINUOUS"} #u'SI': <tf.Tensor 'Const_6:0' shape=(1000,) dtype=float64>
    #                                 , "ERD": {"column_type": "CONTINUOUS"} # u'ERD': <tf.Tensor 'Const_5:0' shape=(1000,) dtype=float64>
    #                                 , "CBI": {"column_type": "CONTINUOUS"} #u'CBI': <tf.Tensor 'Const_2:0' shape=(1000,) dtype=float64>
    #                                 , "A_O": {"column_type": "CONTINUOUS"}#u'A_O': <tf.Tensor 'Const_9:0' shape=(1000,) dtype=float64>
    #                                 , "G_F": {"column_type": "CONTINUOUS"} #u'G_F': <tf.Tensor 'Const_11:0' shape=(1000,) dtype=float64>
    #                                 , "HGI": {"column_type": "CONTINUOUS"} #u'HGI': <tf.Tensor 'Const_8:0' shape=(1000,) dtype=float64>
    #                                 , "CMCP_OUT_MON": {"column_type": "CONTINUOUS"} # u'CMCP_OUT_MON': <tf.Tensor 'Const:0' shape=(1000,) dtype=float64>
    #                                 }
    #                             })


    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/scm/table/tb_census_data01/format/nn0000100/',
                         json={"label":
                                    {"income_bracket": "LABEL"}
                                , "Transformations":
                                    {"col1": {"boundaries": [18, 25, 30, 35, 40, 45, 50, 55, 60, 65], "column_name": "age"}}
                                , "cross_cell": {"col12": {"column2_0": "native_country", "column2_1": "occupation"}
                                        , "col1": {"column_1": "occupation", "column_0": "education"}}
                                , "cell_feature":
                                    {"hours_per_week": {"column_type": "CONTINUOUS"}
                                    , "capital_loss": {"column_type": "CONTINUOUS"}
                                    , "age": {"column_type": "CONTINUOUS"}
                                    , "capital_gain": {"column_type": "CONTINUOUS"}
                                    ,"education_num": {"column_type": "CONTINUOUS"}
                                    , "education": {"column_type": "CATEGORICAL"}
                                    , "occupation": {"column_type": "CATEGORICAL"}
                                    , "workclass": {"column_type": "CATEGORICAL"}
                                    , "gender": {"keys": ["female", "male"]
                                    , "column_type": "CATEGORICAL_KEY"}
                                    , "native_country": {"column_type": "CATEGORICAL"}
                                    ,"relationship": {"column_type": "CATEGORICAL"}
                                    , "marital_status": {"column_type": "CATEGORICAL"}
                                    , "race": {"column_type": "CATEGORICAL"}

                                    }
                                })
    #eep_columns = [
  # tf.contrib.layers.embedding_column(workclass, dimension=8),
  # tf.contrib.layers.embedding_column(education, dimension=8),
  # tf.contrib.layers.embedding_column(marital_status, dimension=8),
  # tf.contrib.layers.embedding_column(gender, dimension=8),
  # tf.contrib.layers.embedding_column(relationship, dimension=8),
  # tf.contrib.layers.embedding_column(race, dimension=8),
  # tf.contrib.layers.embedding_column(native_country, dimension=8),
  # tf.contrib.layers.embedding_column(occupation, dimension=8),
  # age, education_num, capital_gain, capital_loss, hours_per_week]
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_format_get():

    #resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/titanic/format//',json = {"type":"cell_feature"})
                                           #/api/v1/type/dataframe/base/csvtest/table/titanic/format/nn0000102 /
    resp = requests.get('http://' + url + '/api/v1/type/dataframe/format/mes_m30_wdnn_99023/type/labels/')
    #resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/titanic/format/scm_default_wdnn_66039/type/all/')

    #resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/titanic/format/nn0000102/',json = {"type":"cell_feature"})
    #                                       #/api/v1/type/dataframe/base/csvtest/table/titanic/format/nn0000102 /
    #resp = requests.get('http://' + url + '/api/v1/type/dataframe/format/nn0000102/type/cell_feature/')
    #resp = requests.get('http://' + url + '/api/v1/type/dataframe/format/nn0000102/type/label/')
    #resp = requests.get('http://' + url + '/api/v1/type/dataframe/format/nn0000102/type/all/')

    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))
    #/api/v1/type/dataframe/base/csvtest/table/titanic/format/nn0000102/ [object % 20Object]



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
# DataFrame - data33333333333333333
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

    #resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/scm/table/tb_data_cokes/data/')
    resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/frame_pre_scm_default/table/test111/data/'
                        , json= {
                             "limits" : "0"
                                }
                        )
    #resp = requests.get('http://' + url + '/api/v1/type/dataframe/base/scm/table/tb_test_incomedata_wdnn3/data/a')
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
    resp = requests.post('http://' + url + '/api/v1/type/wdnn/conf/nn0000102/',
                         json={
                                 "layer":[100,50]
                             })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def wdnn_train_post():
    #resp = requests.post('http://' + url + '/api/v1/type/wdnn/train/nn0000011/')
    resp = requests.post('http://' + url + '/api/v1/type/wdnn/train/nn0000102/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


def wdnn_predict_post():
    #resp = requests.post('http://' + url + '/api/v1/type/wdnn/predict/nn0000011/')
    resp = requests.post('http://' + url + '/api/v1/type/wdnn/predict/nn0000102/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


def wdnn_eval_post():
    #resp = requests.post('http://' + url + '/api/v1/type/wdnn/predict/nn0000011/')
    resp = requests.post('http://' + url + '/api/v1/type/wdnn/eval/nn0000102/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


####################################################################################
# CNN - Config
####################################################################################
def cnn_conf_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/conf/nn0000091/',
                         json={
                                 "data":
                                     {
                                         "datalen": 1024,
                                         "taglen": 4,
                                         "matrix": [32, 32],
                                         "learnrate": 0.01,
                                         "epoch": 10
                                     },
                                 "layer":
                                     [
                                         {
                                             "type": "cnn",
                                             "active": "relu",
                                             "cnnfilter": [2, 2],
                                             "cnnstride": [2, 2],
                                             "maxpoolmatrix": [2, 2],
                                             "maxpoolstride": [2, 2],
                                             "node_in_out": [1, 16],
                                             "regualizer": "",
                                             "padding": "SAME",
                                             "droprate": ""
                                         },
                                         {
                                             "type": "cnn",
                                             "active": "relu",
                                             "cnnfilter": [2, 2],
                                             "cnnstride": [2, 2],
                                             "maxpoolmatrix": [2, 2],
                                             "maxpoolstride": [2, 2],
                                             "node_in_out": [16, 32],
                                             "regualizer": "",
                                             "padding": "SAME",
                                             "droprate": ""
                                         },
                                         {
                                             "type": "reshape",
                                         },
                                         {
                                             "type": "drop",
                                             "active": "relu",
                                             "regualizer": "",
                                             "droprate": "0.5"
                                         },
                                         {
                                             "type": "out",
                                             "active": "softmax",
                                             "cnnfilter": "",
                                             "cnnstride": "",
                                             "maxpoolmatrix": "",
                                             "maxpoolstride": "",
                                             "node_in_out": [32, 4],
                                             "regualizer": "",
                                             "padding": "SAME",
                                             "droprate": ""
                                         }
                                     ]
                             })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def cnn_conf_get():
    resp = requests.get('http://' + url + '/api/v1/type/cnn/conf/nn0000091/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def cnn_conf_put():
    resp = requests.put('http://' + url + '/api/v1/type/cnn/conf/nn0000091/',
                        json={
                            "data":
                                {
                                    "datalen": 1024,
                                    "taglen": 4,
                                    "matrix": [32, 32],
                                    "learnrate": 0.01,
                                    "epoch": 10
                                },
                            "layer":
                                [
                                    {
                                        "type": "cnn",
                                        "active": "relu",
                                        "cnnfilter": [2, 2],
                                        "cnnstride": [2, 2],
                                        "maxpoolmatrix": [2, 2],
                                        "maxpoolstride": [2, 2],
                                        "node_in_out": [1, 16],
                                        "regualizer": "",
                                        "padding": "SAME",
                                        "droprate": ""
                                    },
                                    {
                                        "type": "cnn",
                                        "active": "relu",
                                        "cnnfilter": [2, 2],
                                        "cnnstride": [2, 2],
                                        "maxpoolmatrix": [2, 2],
                                        "maxpoolstride": [2, 2],
                                        "node_in_out": [16, 32],
                                        "regualizer": "",
                                        "padding": "SAME",
                                        "droprate": ""
                                    },
                                    {
                                        "type": "reshape",
                                    },
                                    {
                                        "type": "drop",
                                        "active": "relu",
                                        "regualizer": "",
                                        "droprate": "0.5"
                                    },
                                    {
                                        "type": "out",
                                        "active": "softmax",
                                        "cnnfilter": "",
                                        "cnnstride": "",
                                        "maxpoolmatrix": "",
                                        "maxpoolstride": "",
                                        "node_in_out": [32, 4],
                                        "regualizer": "",
                                        "padding": "SAME",
                                        "droprate": ""
                                    }
                                ]
                        })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def cnn_conf_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/cnn/conf/nn0000091/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


####################################################################################
# CNN - Train
####################################################################################

def cnn_train_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/train/nn0000045/',
                         json= {
                             "epoch" : "10",
                             "testset" : "10"
                         })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


####################################################################################
# CNN - Predict
####################################################################################

def cnn_predict_put():
    img = simple_resize("/home/dev/TensorMSA/tfmsacore/resources/test.png", 32, 32 )
    resp = requests.put('http://' + url + '/api/v1/type/cnn/predict/nn0000045/',
                         json= [img]
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
    resp = requests.get('http://' + url + '/api/v1/type/common/job/mes_m30_wdnn_84110/')
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
    resp = requests.post('http://' + url + '/api/v1/type/cnn/checker/nn0000090/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


####################################################################################
# cnn - eval - post

####################################################################################

def cnn_eval_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/eval/nn0000090/',
                         json={'sampcnn_predictlenum': 0.1, 'samplemethod' : '1'})
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def cnn_eval_get():
    resp = requests.get('http://' + url + '/api/v1/type/cnn/eval/nn0000090/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

####################################################################################
# image - format
####################################################################################
def image_format_post():
    resp = requests.post('http://' + url + '/api/v1/type/imagefile/base/mes/table/test10/format/nn0000091/',
                         json={"x_size": 32,
                               "y_size": 32
                               })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def image_format_get():
    resp = requests.get('http://' + url + '/api/v1/type/imagefile/base/mes/table/testtable3/format/nn0000091/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def image_table_post():
    resp = requests.post('http://' + url + '/api/v1/type/imagefile/base/mes/table/test10/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def image_table_get():
    resp = requests.get('http://' + url + '/api/v1/type/imagefile/base/mes/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def image_table_get():
    resp = requests.get('http://' + url + '/api/v1/type/imagefile/base/mes/table/testtable3/label/mario/data/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def image_data_put():
    resp = requests.put('http://' + url + '/api/v1/type/imagefile/base/mes/table/testtable3/label/mario/data/',
                        json=["1","10"])
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))
def image_table_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/imagefile/base/mes/table/nn0000045/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def image_preview_get():
    resp = requests.get('http://' + url + '/api/v1/type/imgpreview/nnid/nn0000091/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def image_preview_delete():
    resp = requests.delete('http://' + url + '/api/v1/type/imgpreview/nnid/nn0000091/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def image_label_post():
    resp = requests.post('http://' + url + '/api/v1/type/imagefile/label/xxx/nnid/nn0000091/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def image_label_get():
    resp = requests.get('http://' + url + '/api/v1/type/imagefile/label/nn0000091/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


def log_insert_test():
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
                             "nn_id": "nn0000100",
                             "loss": "0.001",
                             "step": "100",
                             "max_step": "1000",
                             "trainDate": "2013-01-29",
                             "testsets": "1"
                         })

    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def common_stat_get():
    resp = requests.get('http://' + url + '/api/v1/type/common/stat/nn0000045/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


####################################################################################
# TEST - TEST - TEST
####################################################################################

"""
CNN TEST Sequence
1. common - env - post
2. common - nninfo - post
3. image - table - post
4. image - format - post
5. Image Upload (use ui http://localhost:8989/view/ftptest)
6. cnn - conf - post
7. cnn - checker - post
8. cnn - train - post
9. cnn - predict- put (local test)
9. cnn - predict- post (file upload)
10. cnn - eval - post
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
"""
data setup  screen
4. dataframe - table - post
<<<<<<< HEAD
5. dataframe - table - get
5. dataframe - data - get
5. dataframe - format - post
8.wdnn - conf - conf
dataframe_base_get

"""
#common, dataframe, cnn, wdnn

category1 = "dataframe"
# checker, predict, stat, evaluation, train, conf, nnfino, base, data, format, table, pre
category2 = "format"
#dataframe_table_get
# post, get, put, delete
request = "get"


locals()["{0}_{1}_{2}".format(category1, category2, request)]()
