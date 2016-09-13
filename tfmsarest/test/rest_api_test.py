import requests
import json
import tensorflow as tf

# Reference
#https://realpython.com/blog/python/api-integration-in-python/
#http://www.slideshare.net/Byungwook/rest-api-60505484

url = "192.168.0.3:8989"

# test-predict
def test_nn_cnn_service_predict():
    req_data = """[ 0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
                   0 , 0 , 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]"""
    resp = requests.get('http://' + url + '/service/nn/cnn/' ,
                        json={ "nn_id": "sample" , "nn_type" : "cnn",
                               "run_type" : "local", "epoch" : "", "testset" : "" , "predict_data":req_data})
    if resp.status_code != 200:
        raise SyntaxError('GET /tasks/ {}'.format(resp.status_code))

    data = json.loads(resp.json())
    print("test result : {0}".format(data))

# test-train
def test_nn_cnn_service_train():
    #requests.post(url, data, json, arg )
    #nn_type, run_type, nn_id
    resp = requests.post('http://' + url + '/service/nn/cnn/',
                        json={ "nn_id": "sample" , "nn_type" : "cnn",
                               "run_type" : "local", "epoch" : 50, "testset" : 10 ,"predict_data":""})
    if resp.status_code != 200:
        raise SyntaxError('GET /tasks/ {}'.format(resp.status_code))

    data = json.loads(resp.json())
    print("test result : {0}".format(data))

# create new network test
def test_nn_cnn_config_insert_conf():
    req_data = """{
            "data":
                {
                    "datalen": 96,
                    "taglen": 2,
                    "matrix": [12, 8],
                    "learnrate": 0.01,
                    "epoch":50
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
                        "type": "cnn",
                        "active": "relu",
                        "cnnfilter": [2, 2],
                        "cnnstride": [1, 1],
                        "maxpoolmatrix": [2, 2],
                        "maxpoolstride": [1, 1],
                        "node_in_out": [16, 32],
                        "regualizer": "",
                        "padding": "SAME",
                        "droprate": ""
                    },

                    {
                        "type": "drop",
                        "active": "relu",
                        "cnnfilter": "",
                        "cnnstride": "",
                        "maxpoolmatrix": "",
                        "maxpoolstride": "",
                        "node_in_out": [192, 100],
                        "regualizer": "",
                        "padding": "SAME",
                        "droprate": 0.5
                    },
                    {
                        "type": "out",
                        "active": "softmax",
                        "cnnfilter": "",
                        "cnnstride": "",
                        "maxpoolmatrix": "",
                        "maxpoolstride": "",
                        "node_in_out": [100, 2],
                        "regualizer": "",
                        "padding": "SAME",
                        "droprate": ""
                    }
                ]
        }"""

    nn_info = """
         { "nnid": "sample",
           "category":"test",
           "name" : "test",
           "type" : "cnn",
           "acc" : "",
           "train" : "",
           "config" : "",
           "dir" : "default"}
         """
    resp = requests.post('http://' + url + '/config/nn/cnn/',
                        json={
                            "nn_info" : nn_info,
                            "nn_conf" : ""
                        })
    if resp.status_code != 200:
        raise SyntaxError('GET /tasks/ {}'.format(resp.status_code))
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

# insert network configuration
def test_nn_cnn_config_update_conf():
    req_data = """{
        "data":
            {
                "datalen": 96,
                "taglen": 2,
                "matrix": [12, 8],
                "learnrate": 0.01,
                "epoch":50
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
                    "type": "cnn",
                    "active": "relu",
                    "cnnfilter": [2, 2],
                    "cnnstride": [1, 1],
                    "maxpoolmatrix": [2, 2],
                    "maxpoolstride": [1, 1],
                    "node_in_out": [16, 32],
                    "regualizer": "",
                    "padding": "SAME",
                    "droprate": ""
                },

                {
                    "type": "drop",
                    "active": "relu",
                    "cnnfilter": "",
                    "cnnstride": "",
                    "maxpoolmatrix": "",
                    "maxpoolstride": "",
                    "node_in_out": [192, 100],
                    "regualizer": "",
                    "padding": "SAME",
                    "droprate": 0.5
                },
                {
                    "type": "out",
                    "active": "softmax",
                    "cnnfilter": "",
                    "cnnstride": "",
                    "maxpoolmatrix": "",
                    "maxpoolstride": "",
                    "node_in_out": [100, 2],
                    "regualizer": "",
                    "padding": "SAME",
                    "droprate": ""
                }
            ]
    }"""
    nn_info = """
         { "nnid": "nn0000001",
           "category":"test",
           "name" : "test",
           "type" : "cnn",
           "acc" : "",
           "train" : "",
           "config" : "",
           "dir" : "default"}
         """

    resp = requests.put('http://' + url + '/config/nn/cnn/',
                        json={
                            "nn_info" : nn_info,
                            "nn_conf" : req_data
                        })
    if resp.status_code != 200:
        raise SyntaxError('GET /tasks/ {}'.format(resp.status_code))
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

# insert network configuration
def test_nn_cnn_config_search_conf():

    nn_info = """
         { "nnid": "nn0000001",
           "category":"",
           "name" : "",
           "type" : "",
           "acc" : "",
           "train" : "",
           "config" : "",
           "dir" : "default"}
         """

    resp = requests.get('http://' + url + '/config/nn/cnn/',
                        json={
                            "nn_info" : nn_info,
                            "nn_conf" : ""
                        })
    if resp.status_code != 200:
        raise SyntaxError('GET /tasks/ {}'.format(resp.status_code))
    data = json.loads(resp.json())
    print("test result : {0}".format(data))


# test each rest apis
def main(case):
    case = 2
    if(case == 1):
        test_nn_cnn_service_predict()
    elif(case ==2):
        test_nn_cnn_service_train()
    elif (case == 3):
        test_nn_cnn_config_insert_conf()
    elif (case == 4):
        test_nn_cnn_config_update_conf()
    elif (case == 5):
        test_nn_cnn_config_search_conf()

if __name__ == '__main__':
    tf.app.run()
