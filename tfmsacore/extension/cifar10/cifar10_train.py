import tensorflow as tf
import numpy as np
from tfmsacore.extension.cifar10 import cifar10
from tfmsacore.extension.cifar10.cifar10 import img_size, num_channels, num_classes
from tfmsacore.extension.cifar10 import dataset
################################################################
################################################################
################################################################
################################################################
def m_train(_train_cnt):
    _train_cnt = int(_train_cnt)
    cifar10.directoryCheck()
    print("Loading Tranin Data.....")
    images_train, cls_train, labels_train = cifar10.load_training_data(cifar10._num_files_train)
    print("- Size of: Training-set:\t\t{}".format(len(images_train)))

    x, y_true, global_step, optimizer, accuracy, y_pred_cls  = cifar10.get_network_variable()

    saver = tf.train.Saver()
    with tf.Session() as sess:
        try:
            print("Trying to restore last checkpoint SavePath : "+str(cifar10.save_path))
            # Use TensorFlow to find the latest checkpoint - if any.
            last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=cifar10.save_path)
            print("Try and load the data in the checkpoint: : "+str(last_chk_path))
            # Try and load the data in the checkpoint.
            saver.restore(sess, save_path=last_chk_path)
            # If we get to this point, the checkpoint was successfully loaded.
            print("Restored checkpoint from:", last_chk_path)
        except:
            # If the above failed for some reason, simply
            # initialize all the variables for the TensorFlow graph.
            print("None to restore checkpoint. Initializing variables instead.")
            sess.run(tf.initialize_all_variables())

        # tensorboard
        writer = tf.train.SummaryWriter(cifar10.logs_path, graph=tf.get_default_graph())
        merged = tf.merge_all_summaries()
        ################################################################
        print("Train Optimize Call:",_train_cnt)
        cifar10.optimize(num_iterations=_train_cnt
                         , x=x
                         , y_true=y_true
                         , session=sess
                         , global_step=global_step
                         , optimizer=optimizer
                         , accuracy=accuracy
                         , saver=saver
                         , images_train=images_train
                         , labels_train=labels_train
                         , writer=writer
                         , merged=merged)

def m_predict(_predict_start, _predict_cnt):
    cifar10.directoryCheck()
    _predict_start = int(_predict_start)
    if _predict_start < 1:
        _predict_start = 1
    _predict_cnt = int(_predict_cnt)
    if _predict_cnt < 1:
        _predict_cnt = 1

    _img_cls_size = [1,1]
    _img_cls_size[0] = _predict_start - 1

    if _predict_start - 1 + _predict_cnt > int(cifar10._images_per_file):
        _img_cls_size[1] = int(cifar10._images_per_file)
    else:
        _img_cls_size[1] = _predict_start - 1 + _predict_cnt

    print("Loading Test Data....._img_cls_size:"+str(_img_cls_size))
    images_test, cls_test, labels_test = cifar10.load_test_data("test_batch")
    print("- Size of: Test-set:\t\t{}".format(len(images_test)))

    x, y_true, global_step, optimizer, accuracy, y_pred_cls = cifar10.get_network_variable()

    saver = tf.train.Saver()
    with tf.Session() as sess:
        try:
            print("Trying to restore last checkpoint SavePath : "+str(cifar10.save_path))
            # Use TensorFlow to find the latest checkpoint - if any.
            last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=cifar10.save_path)
            print("Try and load the data in the checkpoint: : "+str(last_chk_path))
            # Try and load the data in the checkpoint.
            saver.restore(sess, save_path=last_chk_path)
            # If we get to this point, the checkpoint was successfully loaded.
            print("Restored checkpoint from:", last_chk_path)
        except:
            # If the above failed for some reason, simply
            # initialize all the variables for the TensorFlow graph.
            print("None to restore checkpoint. Initializing variables instead.")
            sess.run(tf.initialize_all_variables())

        # For all the images in the test-set,
        # calculate the predicted classes and whether they are correct.
        correct, cls_pred = cifar10.predict_cls(images=images_test
                                                , labels=labels_test
                                                , cls_true=cls_test
                                                , x=x
                                                , y_true=y_true
                                                , session=sess
                                                , y_pred_cls=y_pred_cls
                                                , _img_cls_size=_img_cls_size)
# fileType : path, url
def s_predict_file(_fileName, fileType):
    cifar10.directoryCheck()
    x, y_true, global_step, optimizer, accuracy, y_pred_cls = cifar10.get_network_variable()

    saver = tf.train.Saver()
    with tf.Session() as sess:
        try:
            print("Trying to restore last checkpoint SavePath : "+str(cifar10.save_path))
            # Use TensorFlow to find the latest checkpoint - if any.
            last_chk_path = tf.train.latest_checkpoint(checkpoint_dir=cifar10.save_path)
            print("Try and load the data in the checkpoint: : "+str(last_chk_path))
            # Try and load the data in the checkpoint.
            saver.restore(sess, save_path=last_chk_path)
            # If we get to this point, the checkpoint was successfully loaded.
            print("Restored checkpoint from:", last_chk_path)
        except:
            # If the above failed for some reason, simply
            # initialize all the variables for the TensorFlow graph.
            print("None to restore checkpoint. Initializing variables instead.")
            sess.run(tf.initialize_all_variables())

        images_test, msg = cifar10.get_binary_images(sess, _fileName, fileType)
        cls_test = [0]
        labels_test = dataset.one_hot_encoded(class_numbers=cls_test, num_classes=cifar10.num_classes)

        cls_true_name = cifar10.predict_cls_one(images=images_test
                                           , labels=labels_test
                                           , x=x
                                           , y_true=y_true
                                           , session=sess
                                           , y_pred_cls=y_pred_cls
                                           , msg=msg)

        print("Predict Class Name>>>>>", cls_true_name)

        return cls_true_name

def main(argv = None):
    select_menu = input("1:Multy Train, 2:Multy Predict, 3:Single Predict fileName, 4.Single Predict fileURL :")
    if select_menu == "1":
        _train_cnt = input("How Many Train 1 ~ 200000 or exit : ")

        m_train(_train_cnt)
    elif select_menu == "2":
        start_cnt = input("Start Predict Number 1 ~ "+str(cifar10._images_per_file)+" or exit : ")
        image_cnt = input("How Many Image(Max 100) or exit : ")

        m_predict(start_cnt, image_cnt)
    elif select_menu == "3":
        # while True:
        #     fileName = input("FileName or exit : ")
        #     if fileName == "exit":
        #         break
        _fileName = []
        _fileName.append("/home/dev/tensorflowEx/cifar10Ex/data/common/car1.jpg")
        _fileName.append("/home/dev/tensorflowEx/cifar10Ex/data/common/car3faefaefae.jpg")
        _fileName.append("/home/dev/tensorflowEx/cifar10Ex/data/common/car3.jpg")
        s_predict_file(_fileName, "path")
    elif select_menu == "4":
        # while True:
        #     fileName = input("FileURL or exit : ")
        #     if fileName == "exit":
        #         break
        _fileName = []
        _fileName.append("http://farm4.static.flickr.com/3269/2563134338_6b904bebc2.jpg")
        _fileName.append("http://farm4.static.flickr.com/3269/2563134338_6b904bebc2.jpg")
        s_predict_file(_fileName, "url")
    else:
        print("End.")

    print("tensorboard --logdir="+str(cifar10.curr_path)+str(cifar10.logs_path))


    # # while True:
    # gloval_fileName("car1.jpg")
    # gloval_fileName("car3.jpg")
    # train_predict(sess, "sp_predict")

    # fileName = "car1.jpg"
    # gloval_fileName(fileName)
    # train_predict(sess, "sp_predict")
    #
    # gloval_fileName("http://farm4.static.flickr.com/3228/2604849157_fb055b5bde.jpg")
    # gloval_fileName("http://farm4.static.flickr.com/3269/2563134338_6b904bebc2.jpg")
    # gloval_fileName("http://farm3.static.flickr.com/2272/2112334051_fddb6ff69f.jpg")
    #
    # gloval_fileName("farm1.static.flickr.com/230/496213162_4b72ef3d67.jpg")
    # train_predict(sess, "su_predict")

if __name__ == '__main__':
    tf.app.run()




