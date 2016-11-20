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

    def resize_file_image(self, path, net_info, format_info, file_name, label):
        """
        load uploaded image and resize
        :param path:
        :return:
        """
        x_size = int(format_info['x_size'])
        y_size = int(format_info['y_size'])
        dataframe = net_info['dir']
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
        self.save_preview_image(newImage, dataframe, table, file_name, label)
        return newImage.getdata(), width, height

    def simple_resize(self, path, x_size, y_size):
        """
        simply resize image and return array
        :param path:
        :return:
        """
        x_size = int(x_size)
        y_size = int(y_size)
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

    def save_preview_image(self, newImage, dataframe, table, file_name, label):
        """
        save preview image for UI
        :return:
        """
        preview_path = "{0}/{1}".format(settings.PREVIEW_IMG_PATH, "preview")
        preview_database = "{0}/{1}/{2}".format(settings.PREVIEW_IMG_PATH, "preview", dataframe)
        preview_table = "{0}/{1}/{2}/{3}".format(settings.PREVIEW_IMG_PATH, "preview", dataframe, table)
        preview_label = "{0}/{1}/{2}/{3}/{4}".format(settings.PREVIEW_IMG_PATH, "preview", dataframe, table, label)
        preview_img_file = "{0}/{1}/{2}/{3}/{4}/{5}".format(
            settings.PREVIEW_IMG_PATH, "preview", dataframe, table, label, file_name)

        # create preview path
        if not os.path.exists(preview_path):
            os.mkdir(preview_path)

        # create database path
        if not os.path.exists(preview_database):
            os.mkdir(preview_database)

        # create table path
        if not os.path.exists(preview_table):
            os.mkdir(preview_table)

        # create label path
        if not os.path.exists(preview_label):
            os.mkdir(preview_label)

        # check preview image number
        if(len([name for name in os.listdir(preview_label)  \
                if os.path.isfile(os.path.join(preview_label, name))]) < 8) :
            newImage.save(preview_img_file)
