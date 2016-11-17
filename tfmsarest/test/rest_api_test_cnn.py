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

def image_table_post():
    resp = requests.post('http://' + url + '/api/v1/type/imagefile/base/' + database + '/table/' + table + '/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def image_format_post():
    resp = requests.post('http://' + url + '/api/v1/type/imagefile/base/' + database + '/table/' + table + '/format/' + net_work_id + '/',
                         json={"x_size": 32,
                               "y_size": 32
                               })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def cnn_conf_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/conf/' + net_work_id + '/',
                         json={
                                 "data":
                                     {
                                         "datalen": 10000,
                                         "taglen": 2,
                                         "matrix": [100, 100],
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

def cnn_train_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/train/' + net_work_id + '/',
                         json= {
                             "epoch" : "10",
                             "testset" : "10"
                         })
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))


def cnn_eval_post():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/eval/' + net_work_id +'/',
                         json={'samplenum': 0.1, 'samplemethod' : '1'})
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

def cnn_eval_get():
    resp = requests.get('http://' + url + '/api/v1/type/cnn/eval/' + net_work_id +'/')
    data = json.loads(resp.json())
    print("evaluation result : {0}".format(data))

"""
STEP1
1. common - env - post
2. common - nninfo - post
3. image - table - post
4. image - format - post
"""

def cnn_step1():
    common_nninfo_post()
    image_table_post()
    image_format_post()

"""
STEP2
Upload File
http://IP:8989
>>data>image>upload
"""

"""
STEP3
6. cnn - conf - post
7. cnn - checker - post
8. cnn - train - post
"""
def cnn_step2():
    cnn_conf_post()
    cnn_train_post()

"""
STEP4
9. cnn - predict- put (local test)
9. cnn - predict- post (file upload)
10. cnn - eval - post
"""
def cnn_step3():
    cnn_eval_post()
    cnn_eval_get()


net_work_id = "nn0000090"
database = "mes"
table = "nn0000090"

cnn_step3()