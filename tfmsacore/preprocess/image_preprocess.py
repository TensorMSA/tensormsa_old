from PIL import Image, ImageFilter
from django.conf import settings
import os, random, io
import numpy as np

class ImagePreprocess:

    def resize_bytes_image(self, data, conf, net_info):
        """

        :param data: data object contain image data
        :param conf: data manipulation conf data
        :return:
        """
        byte_obj = data['bt']
        ext = str(data['decoder'] ,'utf-8')
        width = str(data['width'], 'utf-8')
        height = str(data['height'], 'utf-8')
        table = net_info['table']
        byte_arr = bytearray(byte_obj)

        # mode : F , L , P , 1 , I, RGB, RGBA
        im = Image.frombytes('L', [int(width), int(height)], byte_obj, self.decoder_type(ext))
        tv = list(im.getdata())
        train_arr = [(255 - x) * 1.0 / 255.0 for x in tv]
        return train_arr

    def decoder_type(self, ext_type):
        if(ext_type == 'jpg' or ext_type == 'jpeg'):
            return 'JPEG'
        elif(ext_type == 'zip'):
            return 'zip'
        elif (ext_type == 'png'):
            return 'png'
        elif (ext_type == 'bmp'):
            return 'raw'
        else:
            return ext_type

    def resize_file_image(self, path, net_info, format_info, file_name):
        """
        load uploaded image and resize
        :param path:
        :return:
        """
        x_size = format_info['x_size']
        y_size = format_info['y_size']
        table = net_info['table']

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
        width, height = newImage.size

        #save preview on jango static folder
        self.save_preview_image(newImage, table, file_name)
        return newImage.getdata(), width, height

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

        return newImage.getdata()

    def save_preview_image(self, newImage, table, file_name):
        """
        save preview image for UI
        :return:
        """
        preview_path = "{0}/{1}".format(settings.STATIC_ROOT, "preview")
        preview_img_path = "{0}/{1}/{2}".format(settings.STATIC_ROOT, "preview", table)
        preview_img_file = "{0}/{1}/{2}/{3}".format(settings.STATIC_ROOT, "preview", table, file_name)

        # create preview image
        if not os.path.exists(preview_path):
            os.mkdir(preview_path)

        # create preview image
        if not os.path.exists(preview_img_path):
            os.mkdir(preview_img_path)

        # check preview image number
        if(len([name for name in os.listdir(preview_img_path)  \
                if os.path.isfile(os.path.join(preview_img_path, name))]) < 10) :
            newImage.save(preview_img_file)
