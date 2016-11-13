import requests
import json, os
import tensorflow as tf
import logging
from django.conf import settings
from PIL import Image, ImageFilter
import datetime

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")

def common_nninfo_post():
    resp = requests.post('http://' + url + '/api/v1/type/common/nninfo/',
                         json={
                             "nn_id": net_work_id,
                             "category": "test",
                             "subcate" : "test",
                             "name": "test",
                             "desc" : "test"
                         })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def dataframe_table_post():
    #resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/csvtest/table/titanic/')
    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/'+database+'/table/'+table+'/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))



def dataframe_format_post():
    resp = requests.post('http://' + url + '/api/v1/type/dataframe/base/'+database+'/table/'+table+'/format/'+net_work_id+'/',
                         json={"label":
                                    {"Species": "LABEL"}
                                , "cell_feature":
                                    {"Sepal.Length": {"column_type": "CONTINUOUS"}
                                    , "Sepal.Width": {"column_type": "CONTINUOUS"}
                                    , "Petal.Length": {"column_type": "CONTINUOUS"}
                                    , "Petal.Width": {"column_type": "CONTINUOUS"}
                                    }
                                })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def wdnn_conf_post():
    resp = requests.post('http://' + url + '/api/v1/type/wdnn/conf/'+net_work_id+'/',
                         json={
                                 "layer":[100,50]
                             })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def wdnn_train_post():
    #resp = requests.post('http://' + url + '/api/v1/type/wdnn/train/nn0000011/')
    resp = requests.post('http://' + url + '/api/v1/type/wdnn/train/'+net_work_id+'/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

"""
STEP 1
1. common - nninfo - post
2. dataframe - table - post
"""
def cnn_step1():
    common_nninfo_post()
    dataframe_table_post()

"""
STEP2
3. CSV(use ui http://localhost:8989/view/ftptest)
"""

"""
STEP3
4. dataframe - format - post
5. wdnn - conf - post
6. wdnn - train - post
7. wdnn - predict- post
"""
def cnn_step2():
    dataframe_format_post()
    wdnn_conf_post()
    wdnn_train_post()


net_work_id = "nn0000180"
database = "scm"
table = "nn0000180"

cnn_step2()

