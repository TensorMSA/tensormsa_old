import unittest, requests, os, json,random
from tfmsacore.utils.logger import tfmsa_logger
from django.core.files.uploadedfile import TemporaryUploadedFile
from tfmsacore.data import ImageManager

class TestImageStoreProcess(unittest.TestCase):
    """
    ./manage.py jenkins ./tests/functions --enable-coverage
    ./manage.py jenkins ./tests/functions
    """
    rand_name = str(random.randrange(1,99999))

    def test_upload_file(self):
        host_name = "{0}:{1}".format(os.environ['HOSTNAME'], "8989")
        resp = requests.post('http://' + host_name + '/api/v1/type/imagefile/base/mes' \
                             + '/table/' + self.__class__.rand_name + '/label/1/')

        temp_file = TemporaryUploadedFile("img_test_data", "byte", 66666, "xxxxxxxxxxxxxxxxxxxxxxxxxx")
        self.assertEqual(ImageManager().put_data("mes", self.__class__.rand_name.join , "1" , [temp_file]), 1)
        tfmsa_logger("==========PASS==========")

    def test_create_format(self):
        host_name = "{0}:{1}".format(os.environ['HOSTNAME'], "8989")
        resp = requests.post('http://' + host_name + '/api/v1/type/common/nninfo/',
                             json={
                                 "nn_id": self.__class__.rand_name,
                                 "category": "img",
                                 "subcate": "img_test",
                                 "name": "img_cnn",
                                 "desc": "img_cnn"
                             })
        resp = requests.post(
            'http://' + host_name + '/api/v1/type/imagefile/base/mes/table/'  \
            + self.__class__.rand_name + '/format/' + self.__class__.rand_name + '/',
            json={"x_size": 100,
                  "y_size": 100
                  })
        data = json.loads(resp.json())

        if (data['status'] == "200"):
            tfmsa_logger("==========PASS==========")
        else:
            raise Exception(data['result'])