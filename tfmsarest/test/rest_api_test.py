import requests
import json
import tensorflow as tf

# Reference
#https://realpython.com/blog/python/api-integration-in-python/
#http://www.slideshare.net/Byungwook/rest-api-60505484

# test-predict
def test_nn_cnn_service_predict():
    req_data = """[ 0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
                   0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
                   0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
                   0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
                   0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
                   0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
                   0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ,
                   0 , 1 , 0, 1 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 1 ]"""
    resp = requests.get('http://localhost:8989/nn/cnn/service/' ,json=req_data)
    if resp.status_code != 200:
        raise SyntaxError('GET /tasks/ {}'.format(resp.status_code))

    data = json.loads(resp.json())
    print("test result : {0}".format(data))

# test-train
def test_nn_cnn_service_train():
    #requests.post(url, data, json, arg )
    resp = requests.post('http://localhost:8989/nn/cnn/service/',
                        json={ "nn_id": "sample"})
    if resp.status_code != 200:
        raise SyntaxError('GET /tasks/ {}'.format(resp.status_code))

    data = json.loads(resp.json())
    print("test result : {0}".format(data))


def main(case):
    case = 1
    if(case == 1):
        test_nn_cnn_service_predict()
    elif(case ==2):
        test_nn_cnn_service_train()

if __name__ == '__main__':
    tf.app.run()
