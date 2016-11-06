import unittest, requests, os, json,random
from tfmsacore.utils.logger import tfmsa_logger
from django.core.files.uploadedfile import TemporaryUploadedFile
from tfmsacore.data import ImageManager
from PIL import Image, ImageFilter

class TestImagePredictProcess(unittest.TestCase):
    """
    ./manage.py jenkins ./tests/functions --enable-coverage
    ./manage.py jenkins ./tests/functions
    """
    rand_name = str(random.randrange(1,99999))

    def test_image_predict(self):
        host_name = "{0}:{1}".format(os.environ['HOSTNAME'], "8989")

        tfmsa_logger("[1] Image file format update")
        resp = requests.post('http://' + host_name + '/api/v1/type/imagefile/base/mes/table/testtable2/format/nn0000090/',
                             json={"x_size": 32,"y_size": 32 })
        if(json.loads(resp.json())['status'] != "200"):
            raise Exception ("RESI Service Fail")


        tfmsa_logger("[2] Network info update")
        resp = requests.post('http://' + host_name + '/api/v1/type/common/nninfo/',
                             json={
                                 "nn_id": "nn0000090",
                                 "category": "SCM",
                                 "subcate": "csv",
                                 "name": "CENSUS_INCOME",
                                 "desc": "INCOME PREDICT"
                             })
        if (json.loads(resp.json())['status'] != "200"):
            raise Exception("RESI Service Fail")

        tfmsa_logger("[3] Predict Neural Network")
        img = self.simple_resize("/home/dev/TensorMSA/tfmsacore/resources/test.png", 32, 32)
        resp = requests.put('http://' + host_name + '/api/v1/type/cnn/predict/nn0000090/',
                             json=[img]
                             )
        if (json.loads(resp.json())['status'] != "200"):
            raise Exception("RESI Service Fail")

        tfmsa_logger("[4] PASS TEST")

    def simple_resize(self, path, x_size, y_size):
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