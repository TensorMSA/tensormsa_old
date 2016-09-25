import requests
import json
import tensorflow as tf
import logging

# Reference
#https://realpython.com/blog/python/api-integration-in-python/
#http://www.slideshare.net/Byungwook/rest-api-60505484

url = "481bf68ee6d9:8989"


# test-predict
def test_nn_cnn_service_predict():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/predict/' ,
                        json={ "nn_id": "nn0000009" ,
                               "nn_type" : "cnn",
                               "run_type" : "local",
                               "epoch" : "",
                               "testset" : "" ,
                               "predict_data":[{'name':'Andy', 'univ':'a', 'org' : '1', 'eng' : '800' , 'gender' : 'female', 'age' : '50'}]})

    data = json.loads(resp.json())
    print("test result : {0}".format(data))

# test-train
def test_nn_cnn_service_train():
    #requests.post(url, data, json, arg )
    #nn_type, run_type, nn_id
    resp = requests.post('http://' + url + '/api/v1/type/cnn/train/',
                        json={ "nn_id": "nn0000009" , "nn_type" : "cnn",
                               "run_type" : "local", "epoch" : 5, "testset" : 10 ,"predict_data":""})

    data = json.loads(resp.json())
    print("test result : {0}".format(data))

# create new network test
def test_nn_cnn_config_insert_conf():
    resp = requests.post('http://' + url + '/api/v1/type/cnn/config/',
                        json={
                            "nn_info" : { "nn_id": "nn0000007",
                                          "category":"test",
                                          "name" : "test",
                                          "type" : "cnn",
                                          "acc" : "",
                                          "train" : "",
                                          "config" : "Y",
                                          "table" : "TEST2",
                                          "query" : "select * from TEST1",
                                          "datadesc":"{'name':'none', 'univ':'rank', 'org' : 'cate' , 'eng' : 'cont', 'grade' : 'tag', 'gender' :'cate' , 'age' : 'cont'}",
                                          "datasets":"",
                                          "dir" : "default"},
                            "nn_conf" : {
                                        "data":
                                            {
                                                "datalen": 96,
                                                "taglen": 2,
                                                "matrix": [12, 8],
                                                "learnrate": 0.01,
                                                "epoch":10
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
                                    }
                        })
    print(resp.url)
    data = json.loads(resp.json())
    print("test result : {0}".format(data))

# insert network configuration
def test_nn_cnn_config_update_conf():
    resp = requests.put('http://' + url + '/api/v1/type/cnn/config/',
                         json={
                             "nn_info": {"nn_id": "nn0000009",
                                         "category": "test",
                                         "name": "test",
                                         "type": "cnn",
                                         "acc": "",
                                         "train": "",
                                         "config": "Y",
                                         "table": "TEST2",
                                         "query": "select * from TEST1",
                                         "datadesc": "{'name':'none', 'univ':'rank', 'org' : 'cate' , 'eng' : 'cont', 'grade' : 'tag', 'gender' :'cate' , 'age' : 'cont'}",
                                         "datasets": "",
                                         "dir": "default"},
                             "nn_conf": {
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
                             }
                         })

    data = json.loads(resp.json())
    print("test result : {0}".format(data))


# insert network configuration
def test_nn_cnn_config_search_conf():

    resp = requests.get('http://' + url + '/api/v1/type/cnn/config/nn0000009/' )

    data = json.loads(resp.json())
    print("test result : {0}".format(data))


# create new table on spark
def test_nn_cnn_data_post():
    """
    col type (None) : not gonna use on the model
    col type (cont) : continuous data can be used without modification
    col type (cate) : categorical data needs to be modified
    :return:
    """

    resp = requests.post('http://' + url + '/api/v1/type/cnn/data/',
                        json= { "nn_id": "nn0000009",
                                "table": "TEST2",
                                "data":"[{'name':'Andy', 'univ':'SKKU', 'org' : '1', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '50'}," \
                                       " {'name':'Kim', 'univ':'SKKU', 'org' : '2', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '35'}," \
                                       " {'name':'Kim', 'univ':'SKKU', 'org' : '3', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '65'}," \
                                       " {'name':'Kim', 'univ':'SKKU', 'org' : '4', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '70'}," \
                                       " {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'SKKU', 'org' : '5', 'eng' : '800' , 'grade' : 'A', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'d', 'org' : '4', 'eng' : '800' , 'grade' : 'B', 'gender' : 'female', 'age' : '70'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'d', 'org' : '4', 'eng' : '800' , 'grade' : 'B', 'gender' : 'female', 'age' : '70'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'d', 'org' : '4', 'eng' : '800' , 'grade' : 'B', 'gender' : 'female', 'age' : '70'}," \
                                       "]",
                                "query": ""
                        })

    data = json.loads(resp.json())
    print("test result : {0}".format(data))

# append data on spark
def test_nn_cnn_data_put():

    resp = requests.put('http://' + url + '/api/v1/type/cnn/data/',
                        json= { "nn_id": "nn0000009",
                                "table": "TEST2",
                                "data":"[{'name':'Andy', 'univ':'a', 'org' : '1', 'eng' : '800' , 'grade' : 'A', 'gender' : 'female', 'age' : '50'}," \
                                       " {'name':'Kim', 'univ':'b', 'org' : '2', 'eng' : '800' , 'grade' : 'B', 'gender' : 'female', 'age' : '35'}," \
                                       " {'name':'Kim', 'univ':'YcSU', 'org' : '3', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '65'}," \
                                       " {'name':'Kim', 'univ':'d', 'org' : '4', 'eng' : '800' , 'grade' : 'B', 'gender' : 'female', 'age' : '70'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}," \
                                       " {'name':'Kim', 'univ':'e', 'org' : '5', 'eng' : '800' , 'grade' : 'B', 'gender' : 'male', 'age' : '25'}" \
                                       "]",
                                "query" : ""
                        })

    data = json.loads(resp.json())
    print("test result : {0}".format(data))




# select data from table
def test_nn_cnn_data_get():

    resp = requests.get('http://' + url + '/api/v1/type/cnn/data/TEST2/')

    data = json.loads(resp.json())
    temp = json.loads(data["result"])
    print(len(temp))
    print(temp[0]["grade"])
    print(temp[0]["univ"])


# select data from table
def test_nn_common_config_get():

    resp = requests.get('http://' + url + '/config/nn/common/',
                        json={   "nn_id": "",
                                 "category": "",
                                 "name": "",
                                 "type": "",
                                 "acc": "",
                                 "train": "",
                                 "config": "",
                                 "table": "",
                                 "query": "",
                                 "datadesc": "",
                                 "datasets": "",
                                 "dir": ""

                        })

    data = json.loads(resp.json())
    print("test result : {0}".format(data))

# test each rest apis
def main(case):
    # try:
    #     import http.client as http_client
    # except ImportError:
    #     # Python 2
    #     import httplib as http_client
    # http_client.HTTPConnection.debuglevel = 1
    #
    # # You must initialize logging, otherwise you'll not see debug output.
    # logging.basicConfig()
    # logging.getLogger().setLevel(logging.DEBUG)
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True

    case = 2
    if(case == 1):
        # set conf for neural network
        #test_nn_cnn_config_insert_conf()
        #test_nn_cnn_config_update_conf()
        test_nn_cnn_config_search_conf()
        #test_nn_common_config_get()
    elif(case ==2):
        # set data for train
        #test_nn_cnn_data_post()
        test_nn_cnn_data_get()
        #test_nn_cnn_data_put()
        #test_nn_cnn_data_get()
    elif (case == 3):
        # start train
        test_nn_cnn_service_train()
    elif (case == 4):
        #predict result
        test_nn_cnn_service_predict()

if __name__ == '__main__':
    tf.app.run()
