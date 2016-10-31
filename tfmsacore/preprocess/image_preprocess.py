from PIL import Image, ImageFilter
from django.conf import settings
import os, random, io

class ImagePreprocess:

    def resize_bytes_image(self, byte_arr, x_size = 10, y_size=10):
        im = Image.frombytes('L', [x_size, y_size], byte_arr)
        return list(im.getdata())

    def resize_file_image(self, path):
        """

        """
        im = Image.open(path).convert('L')
        width = float(im.size[0])
        height = float(im.size[1])
        newImage = Image.new('L', (28, 28), (255))


        if width > height:

            nheight = int(round((20.0 / width * height), 0))  # resize height according to ratio width


            img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
            wtop = int(round(((28 - nheight) / 2), 0))  #
            newImage.paste(img, (4, wtop))
        else:

            nwidth = int(round((20.0 / height * width), 0))
            if (nwidth == 0):
                nwidth = 1

            img = im.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
            wleft = int(round(((28 - nwidth) / 2), 0))
            newImage.paste(img, (wleft, 4))

        # newImage.save("sample.png")

        tv = list(newImage.getdata())
        tva = [(255 - x) * 1.0 / 255.0 for x in tv]
        return tva