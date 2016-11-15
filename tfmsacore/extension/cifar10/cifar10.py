########################################################################
#
# Functions for downloading the CIFAR-10 data-set from the internet
# and loading it into memory.
#
# Implemented in Python 3.5
#
# Usage:
# 1) Set the variable data_path with the desired storage path.
# 2) Call maybe_download_and_extract() to download the data-set
#    if it is not already located in the given data_path.
# 3) Call load_class_names() to get an array of the class-names.
# 4) Call load_training_data() and load_test_data() to get
#    the images, class-numbers and one-hot encoded class-labels
#    for the training-set and test-set.
# 5) Use the returned data in your own program.
#
# Format:
# The images for the training- and test-sets are returned as 4-dim numpy
# arrays each with the shape: [image_number, height, width, channel]
# where the individual pixels are floats between 0.0 and 1.0.
#
########################################################################
#
# This file is part of the TensorFlow Tutorials available at:
#
# https://github.com/Hvass-Labs/TensorFlow-Tutorials
#
# Published under the MIT License. See the file LICENSE for details.
#
# Copyright 2016 by Magnus Erik Hvass Pedersen
#
########################################################################
import numpy as np
import pickle
import os
from tfmsacore.extension.cifar10 import download
from tfmsacore.extension.cifar10 import dataset
import matplotlib.pyplot as plt
import tensorflow as tf
import time
from datetime import timedelta
from sklearn.metrics import confusion_matrix
import requests
from urllib.request import urlopen
from django.conf import settings

# Use PrettyTensor to simplify Neural Network construction.
# pip install prettytensor
import prettytensor as pt
########################################################################
# Directory where you want to download and save the data-set.
# Set this before you start calling any of the functions below.
# donw Load Path
dir = settings.HDFS_EXTENSION_ROOT

# comm_path = dir+"/common/"
save_path = dir +"/trainSave/"
logs_path = dir +"/TBLog/"
curr_path = os.getcwd()+"/"

# print("comm_path:"+str(comm_path))
print("save_path:"+str(save_path))
print("logs_path:"+str(logs_path))
print("curr_path:"+str(curr_path))
########################################################################
# URL for the data-set on the internet.
data_url = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"

# Number of classes.
num_classes = 10

# Width and height of each image.
img_size = 32

# Number of channels in each image, 3 channels: Red, Green, Blue.
num_channels = 3

# Length of an image when flattened to a 1-dim array.
img_size_flat = img_size * img_size * num_channels

img_size_cropped = 24

train_batch_size = 64

# Split the data-set in batches of this size to limit RAM usage.
batch_size = 256

# Number of images for each batch-file in the training-set.
_images_per_file = 10000
########################################################################
# Number of files for the training-set.
_num_files_train = 1
_view_Image = False
########################################################################
def directoryCheck():
    # if not os.path.exists(comm_path):
    #     os.makedirs(comm_path)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    for fileName in os.listdir(curr_path):
        if fileName.find("core.") != -1:
            os.remove(fileName)

    # else:
    #     shutil.rmtree(logs_path)
    #     os.makedirs(logs_path)

    maybe_download_and_extract()
    class_names = load_class_names()
    print("Category:", str(class_names))

# Private functions for downloading, unpacking and loading data-files.
def _get_file_path(filename=""):
    """
    Return the full path of a data-file for the data-set.
    If filename=="" then return the directory of the files.
    """

    return os.path.join(dir, "cifar-10-batches-py/", filename)
########################################################################
def _unpickle(filename):
    """
    Unpickle the given file and return the data.
    Note that the appropriate dir-name is prepended the filename.
    """

    # Create full path for the file.
    file_path = _get_file_path(filename)

    # print("Loading data: " + file_path)

    with open(file_path, mode='rb') as file:
        # In Python 3.X it is important to set the encoding,
        # otherwise an exception is raised here.
        data = pickle.load(file, encoding='bytes')

    return data
########################################################################
def _convert_images(raw):
    """
    Convert images from the CIFAR-10 format and
    return a 4-dim array with shape: [image_number, height, width, channel]
    where the pixels are floats between 0.0 and 1.0.
    """

    # Convert the raw images from the data-files to floating-points.
    raw_float = np.array(raw, dtype=float) / 255.0
    # print("_convert_images raw_float>>>>>",raw_float)
    # print("raw_float.shape:",raw_float.shape)
    # print("num_channels:",num_channels)
    # Reshape the array to 4-dimensions.
    images = raw_float.reshape([-1, num_channels, img_size, img_size])

    # Reorder the indices of the array.
    images = images.transpose([0, 2, 3, 1])

    return images

def get_binary_images(sess, filename_set, type):
    msgText = "S"
    msg = []
    images = []

    for i in range(len(filename_set)):
        filename = str(filename_set[i])
        print("filename>>>>>>>",filename)

        try:
            if type == 'path':
                if not os.path.exists(filename):
                    msgText = "File Not Found Error."

                value = tf.read_file(filename)
            elif type == 'url':
                fHttpFlag1 = filename.find("http://")
                if fHttpFlag1 == -1:
                    filename = "http://"+filename
                req = requests.get(filename)
                req = urlopen(filename)
                value = req.read()

            if msgText == "S":
                decoded_image = tf.image.decode_jpeg(value, channels=3)
                image = sess.run(decoded_image)
                if _view_Image:
                    plot_image(image, None)

                # train image
                resized_image = tf.image.resize_images(decoded_image, img_size, img_size)
                resized_image = tf.cast(resized_image, tf.uint8)

                image = sess.run(resized_image)
                image = np.reshape(image.data, [img_size, img_size, 3])
                image = image.reshape([-1, img_size, img_size, num_channels])

                images.append(image)
                msg.append("S")
            else:
                images.append("E")
                msg.append(msgText)
                msgText = "S"
        except Exception as e:
            if msgText != "S":
                msgText = "get Binary Image Error.........."
            images.append("E")
            msg.append(msgText)

    return images, msg

########################################################################
def _load_data(filename):
    """
    Load a pickled data-file from the CIFAR-10 data-set
    and return the converted images (see above) and the class-number
    for each image.
    """

    # Load the pickled data-file.
    data = _unpickle(filename)
    # print("Data:>>>>>",data)

    # Get the raw images.
    raw_images = data[b'data']
    # print("raw_images:>>>>>",raw_images)
    # Get the class-numbers for each image. Convert to numpy-array.
    cls = np.array(data[b'labels'])
    # plt.imshow(raw_images[0:1,:])#depth
    # plt.show()

    images = _convert_images(raw_images)
    # print("_convert_images After:>>>>>", images)

    return images, cls
########################################################################
# Public functions that you may call to download the data-set from
# the internet and load the data into memory.
def maybe_download_and_extract():
    """
    Download and extract the CIFAR-10 data-set if it doesn't already exist
    in data_path (set this variable first to the desired path).
    """

    download.maybe_download_and_extract(url=data_url, download_dir=dir)
########################################################################
def load_class_names():
    """
    Load the names for the classes in the CIFAR-10 data-set.
    Returns a list with the names. Example: names[3] is the name
    associated with class-number 3.
    """

    # Load the class-names from the pickled file.
    raw = _unpickle(filename="batches.meta")[b'label_names']

    # Convert from binary strings.
    names = [x.decode('utf-8') for x in raw]

    return names
########################################################################
def load_training_data(_num_files_train):
    """
    Load all the training-data for the CIFAR-10 data-set.
    The data-set is split into 5 data-files which are merged here.
    Returns the images, class-numbers and one-hot encoded class-labels.
    """

    # Total number of images in the training-set.
    # This is used to pre-allocate arrays for efficiency.
    # _num_images_train = _num_files_train * _images_per_file
    _num_images_train = _images_per_file

    # Pre-allocate the arrays for the images and class-numbers for efficiency.
    images = np.zeros(shape=[_num_images_train, img_size, img_size, num_channels], dtype=float)
    cls = np.zeros(shape=[_num_images_train], dtype=int)

    # Begin-index for the current batch.
    begin = 0

    # For each data-file.
    # for i in range(_num_files_train):
    # Load the images and class-numbers from the data-file.
    # images_batch, cls_batch = _load_data(filename="data_batch_" + str(i + 1))
    images_batch, cls_batch = _load_data(filename="data_batch_" + str(_num_files_train))

    # Number of images in this batch.
    num_images = len(images_batch)

    # End-index for the current batch.
    end = begin + num_images

    # Store the images into the array.
    images[begin:end, :] = images_batch

    # Store the class-numbers into the array.
    cls[begin:end] = cls_batch

    # The begin-index for the next batch is the current end-index.
    begin = end

    return images, cls, dataset.one_hot_encoded(class_numbers=cls, num_classes=num_classes)
########################################################################
def load_test_data(fileName):
    """
    Load all the test-data for the CIFAR-10 data-set.
    Returns the images, class-numbers and one-hot encoded class-labels.
    """

    images, cls = _load_data(filename=fileName)

    return images, cls, dataset.one_hot_encoded(class_numbers=cls, num_classes=num_classes)
################################################################
################################################################
################################################################
################################################################
################################################################
def plot_images(images, cls_true, img_cls_size, cls_pred=None, smooth=True):
    # assert len(images) == len(cls_true) == (img_cls_sizeY-img_cls_sizeX)

    # Create figure with sub-plots.
    ics_x_tmp = 1
    ics_y_tmp = img_cls_size[1]-img_cls_size[0]

    for i in range(1, ics_y_tmp+1):
        if ics_y_tmp%i == 0:
            if i<= ics_y_tmp/i:
                ics_x = i
                ics_y = int(ics_y_tmp/i)
    # print("img_cls_size>>>>>>>>>>>>>>>>", img_cls_size)
    # print("ics_x, ics_y>>>>>>>>>>>>>>>>", ics_x, ics_y)
    fig, axes = plt.subplots(ics_x, ics_y)

    # Adjust vertical spacing if we need to print ensemble and best-net.
    if cls_pred is None:
        hspace = 0.3
    else:
        hspace = 0.6
    fig.subplots_adjust(hspace=hspace, wspace=0.3)

    if ics_x == 1 and ics_y == 1:
        # # Name of the true class.
        # Interpolation type.
        if smooth:
            interpolation = 'spline16'
        else:
            interpolation = 'nearest'

        # Plot image.
        axes.imshow(images[0, :, :, :], interpolation=interpolation)

        # Name of the true class.
        class_names = load_class_names()
        cls_true_name = class_names[cls_true[0]]

        # Show true and predicted classes.
        if cls_pred is None:
            xlabel = "True: {0}".format(cls_true_name)
        else:
            # Name of the predicted class.
            cls_pred_name = class_names[cls_pred[0]]

            xlabel = "True: {0}\nPred: {1}".format(cls_true_name, cls_pred_name)

        # Show the classes as the label on the x-axis.
        axes.set_xlabel(str(0 + 1) + "." + xlabel)

        # Remove ticks from the plot.
        axes.set_xticks([])
        axes.set_yticks([])
    else:
        for i, ax in enumerate(axes.flat):
            # Interpolation type.
            if smooth:
                interpolation = 'spline16'
            else:
                interpolation = 'nearest'

            # Plot image.
            ax.imshow(images[i, :, :, :],interpolation=interpolation)

            # Name of the true class.
            class_names = load_class_names()
            cls_true_name = class_names[cls_true[i]]

            # Show true and predicted classes.
            if cls_pred is None:
                xlabel = "True: {0}".format(cls_true_name)
            else:
                # Name of the predicted class.
                cls_pred_name = class_names[cls_pred[i]]

                xlabel = "True: {0}\nPred: {1}".format(cls_true_name, cls_pred_name)

            # Show the classes as the label on the x-axis.
            ax.set_xlabel(str(i+1)+"."+xlabel)

            # Remove ticks from the plot.
            ax.set_xticks([])
            ax.set_yticks([])

        # Ensure the plot is shown correctly with multiple plots
        # in a single Notebook cell.
    plt.show()
################################################################
def pre_process_image(image, training):
    # This function takes a single image as input,
    # and a boolean whether to build the training or testing graph.

    if training:
        # For training, add the following to the TensorFlow graph.

        # Randomly crop the input image.
        image = tf.random_crop(image, size=[img_size_cropped, img_size_cropped, num_channels])

        # Randomly flip the image horizontally.
        image = tf.image.random_flip_left_right(image)

        # Randomly adjust hue, contrast and saturation.
        image = tf.image.random_hue(image, max_delta=0.05)
        image = tf.image.random_contrast(image, lower=0.3, upper=1.0)
        image = tf.image.random_brightness(image, max_delta=0.2)
        image = tf.image.random_saturation(image, lower=0.0, upper=2.0)

        # Some of these functions may overflow and result in pixel
        # values beyond the [0, 1] range. It is unclear from the
        # documentation of TensorFlow 0.10.0rc0 whether this is
        # intended. A simple solution is to limit the range.

        # Limit the image pixels between [0, 1] in case of overflow.
        image = tf.minimum(image, 1.0)
        image = tf.maximum(image, 0.0)
    else:
        # For training, add the following to the TensorFlow graph.

        # Crop the input image around the centre so it is the same
        # size as images that are randomly cropped during training.
        image = tf.image.resize_image_with_crop_or_pad(image,
                                                       target_height=img_size_cropped,
                                                       target_width=img_size_cropped)

    return image
################################################################
def pre_process(images, training):
    # Use TensorFlow to loop over all the input images and call
    # the function above which takes a single image as input.
    images = tf.map_fn(lambda image: pre_process_image(image, training), images)

    return images
################################################################
def main_network(images, training, y_true):
    # Wrap the input images as a Pretty Tensor object.
    x_pretty = pt.wrap(images)

    # Pretty Tensor uses special numbers to distinguish between
    # the training and testing phases.
    if training:
        phase = pt.Phase.train
    else:
        phase = pt.Phase.infer

    # Create the convolutional neural network using Pretty Tensor.
    # It is very similar to the previous tutorials, except
    # the use of so-called batch-normalization in the first layer.
    # tensorboard
    with pt.defaults_scope(activation_fn=tf.nn.relu, phase=phase):
        y_pred, loss = x_pretty.\
            conv2d(kernel=5, depth=64, name='layer_conv1', batch_normalize=True).\
            max_pool(kernel=2, stride=2).\
            conv2d(kernel=5, depth=64, name='layer_conv2').\
            max_pool(kernel=2, stride=2).\
            flatten().\
            fully_connected(size=256, name='layer_fc1').\
            fully_connected(size=128, name='layer_fc2').\
            softmax_classifier(class_count=num_classes, labels=y_true)

    return y_pred, loss
################################################################
def create_network(training, images, y_true):
    # Wrap the neural network in the scope named 'network'.
    # Create new variables during training, and re-use during testing.
    # tensorboard

    name = 'network'
    with tf.variable_scope(name, reuse=not training):

        # Create TensorFlow graph for pre-processing.
        images = pre_process(images=images, training=training)

        # Create TensorFlow graph for the main processing.
        y_pred, loss = main_network(images=images, training=training, y_true=y_true)

    return y_pred, loss
################################################################
def plot_confusion_matrix(cls_test, cls_pred):
    # This is called from print_test_accuracy() below.

    # cls_pred is an array of the predicted class-number for
    # all images in the test-set.

    # Get the confusion matrix using sklearn.
    cm = confusion_matrix(y_true=cls_test,  # True class for test-set.
                          y_pred=cls_pred)  # Predicted class.

    # Print the confusion matrix as text.
    class_names = load_class_names()
    for i in range(num_classes):
        # Append the class-name to each line.
        class_name = "({}) {}".format(i, class_names[i])
        print(cm[i, :], class_name)

    # Print the class-numbers for easy reference.
    class_numbers = [" ({0})".format(i) for i in range(num_classes)]
    print("".join(class_numbers))

################################################################
def get_weights_variable(layer_name):
    # Retrieve an existing variable named 'weights' in the scope
    # with the given layer_name.
    # This is awkward because the TensorFlow function was
    # really intended for another purpose.

    with tf.variable_scope("network/" + layer_name, reuse=True):
        variable = tf.get_variable('weights')

    return variable
################################################################
def get_layer_output(layer_name):
    # The name of the last operation of the convolutional layer.
    # This assumes you are using Relu as the activation-function.
    tensor_name = "network/" + layer_name + "/Relu:0"

    # Get the tensor with this name.
    tensor = tf.get_default_graph().get_tensor_by_name(tensor_name)

    return tensor
################################################################
def plot_image(image, cls_true):
    # Create figure with sub-plots.
    fig, axes = plt.subplots(1, 1)
    #
    # # References to the sub-plots.
    # ax0 = axes.flat[0]
    # ax1 = axes.flat[1]
    #
    # # Show raw and smoothened images in sub-plots.
    # ax0.imshow(image, interpolation='nearest')
    # ax1.imshow(image, interpolation='spline16')
    #
    # # Set labels.
    # ax0.set_xlabel('Raw')
    # ax1.set_xlabel('Smooth')
    #
    # # Name of the true class.
    class_names = load_class_names()
    if cls_true != None:
        cls_true_name = class_names[cls_true]
        axes.set_xlabel(cls_true_name)
    axes.imshow(image)

    plt.show()
################################################################
################################################################
################################################################
# Train
def random_batch(images_train, labels_train):
    # Number of images in the training-set.
    num_images = len(images_train)

    # Create a random index.
    idx = np.random.choice(num_images,
                           size=train_batch_size,
                           replace=False)

    # Use the random index to select random images and labels.
    x_batch = images_train[idx, :, :, :]
    y_batch = labels_train[idx, :]

    return x_batch, y_batch
################################################################
def optimize(num_iterations, x, y_true, session, global_step, optimizer, accuracy, saver, images_train, labels_train, writer, merged):
    # Start-time used for printing time-usage below.
    start_time = time.time()

    for i in range(num_iterations):
        # Get a batch of training examples.
        # x_batch now holds a batch of images and
        # y_true_batch are the true labels for those images.
        x_batch, y_true_batch = random_batch(images_train, labels_train)

        # Put the batch into a dict with the proper names
        # for placeholder variables in the TensorFlow graph.
        feed_dict_train = {x: x_batch,
                           y_true: y_true_batch}

        # Run the optimizer using this batch of training data.
        # TensorFlow assigns the variables in feed_dict_train
        # to the placeholder variables and then runs the optimizer.
        # We also want to retrieve the global_step counter.
        i_global, _ = session.run([global_step, optimizer],
                                  feed_dict=feed_dict_train)

        # Print status to screen every 100 iterations (and last).
        if (i_global % 100 == 0) or (i == num_iterations - 1):
            # Calculate the accuracy on the training-batch.
            batch_acc = session.run(accuracy,
                                    feed_dict=feed_dict_train)

            # Print status.
            msg = "Global Step: {0:>6}, Training Batch Accuracy: {1:>6.1%}"
            print(msg.format(i_global, batch_acc))

            # tensorboard
            summary_str = session.run(merged, feed_dict=feed_dict_train)
            writer.add_summary(summary_str, i)

        # Save a checkpoint to disk every 1000 iterations (and last).
        if (i_global % 1000 == 0) or (i == num_iterations - 1):
            # Save all variables of the TensorFlow graph to a
            # checkpoint. Append the global_step counter
            # to the filename so we save the last several checkpoints.
            saver.save(session,
                       save_path=save_path+"check",
                       global_step=global_step)

            print("Saved checkpoint.")

    # Ending time.
    end_time = time.time()

    # Difference between start and end-times.
    time_dif = end_time - start_time

    # Print the time-usage.
    print("Time usage: " + str(timedelta(seconds=int(round(time_dif)))))

################################################################
def predict_cls(images, labels, cls_true, x, y_true, session, y_pred_cls, _img_cls_size):
    # Number of images.
    num_images = len(images)

    # Allocate an array for the predicted classes which
    # will be calculated in batches and filled into this array.
    cls_pred = np.zeros(shape=num_images, dtype=np.int)

    # Now calculate the predicted classes for the batches.
    # We will just iterate through all the batches.
    # There might be a more clever and Pythonic way of doing this.

    # The starting index for the next batch is denoted i.
    i = 0

    while i < num_images:
        # The ending index for the next batch is denoted j.
        j = min(i + batch_size, num_images)

        # Create a feed-dict with the images and labels
        # between index i and j.
        feed_dict = {x: images[i:j, :],
                     y_true: labels[i:j, :]}
        # print("i"+str(i)+" j="+str(j))
        # Calculate the predicted class using TensorFlow.
        cls_pred[i:j] = session.run(y_pred_cls, feed_dict=feed_dict)

        # Set the start-index for the next batch to the
        # end-index of the current batch.
        i = j

    # Create a boolean array whether each image is correctly classified.
    correct = (cls_true == cls_pred)

    # Classification accuracy and the number of correct classifications.
    acc = correct.mean()
    num_correct = correct.sum()

    # Number of images being classified.
    num_images = len(correct)

    # Print the accuracy.
    msg = "Accuracy on Test-Set: {0:.1%} ({1} / {2})"
    print(msg.format(acc, num_correct, num_images))
    ################################################################
    # Plot the confusion matrix, if desired.
    print("Confusion Matrix:")
    plot_confusion_matrix(cls_test=cls_true, cls_pred=cls_pred)
    ################################################################
    # while True:
    # Get the first images from the test-set.
    images = images[_img_cls_size[0]:_img_cls_size[1]]

    # Get the true classes for those images.
    cls_true = cls_true[_img_cls_size[0]:_img_cls_size[1]]

    cls_pred = cls_pred[_img_cls_size[0]:_img_cls_size[1]]
    ###############################################################
    plot_images(images=images,
                        cls_true=cls_true,
                        img_cls_size=_img_cls_size,
                        cls_pred=cls_pred)

    return correct, cls_pred

################################################################
def predict_cls_one(images, labels, x, y_true, session, y_pred_cls, msg):
    # Number of images.
    num_images = len(images)

    # Allocate an array for the predicted classes which
    # will be calculated in batches and filled into this array.
    cls_pred = np.zeros(shape=num_images, dtype=np.int)

    # Now calculate the predicted classes for the batches.
    # We will just iterate through all the batches.
    # There might be a more clever and Pythonic way of doing this.

    # The starting index for the next batch is denoted i.
    i = 0
    cls_true_name = []
    while i < num_images:
        if msg[i] != "S":
            cls_true_name.append(msg[i])
            i = i + 1
            continue

        try:
            # Create a feed-dict with the images and labels
            feed_dict = {x: images[i], y_true: labels}
            # Calculate the predicted class using TensorFlow.
            cls_pred = session.run(y_pred_cls, feed_dict=feed_dict)

            img = images[i][0, :, :, :]
            if _view_Image:
                plot_image(img, cls_pred[0])

            class_names = load_class_names()
            cls_true_name.append(class_names[cls_pred[0]])

            # Set the start-index for the next batch to the
            # end-index of the current batch.
            i = i + 1
        except Exception as e:
            print("Predict Exception Error>>>>>")
            i = i + 1

    return cls_true_name

def get_network_variable():
    ################################################################
    x = tf.placeholder(tf.float32, shape=[None, img_size, img_size, num_channels], name='x')
    y_true = tf.placeholder(tf.float32, shape=[None, num_classes], name='y_true')
    y_true_cls = tf.argmax(y_true, dimension=1)
    # ################################################################
    global_step = tf.Variable(initial_value=10, name='global_step', trainable=False)
    _, loss = create_network(training=True, images=x, y_true=y_true)
    #############################################################
    # Create Neural Network for Test Phase / Inference
    # Now create the neural network for the test-phase.
    # as well as the loss-function to be used during optimization. During testing we only need y_pred.
    y_pred, _ = create_network(training=False, images=x, y_true=y_true)
    y_pred_cls = tf.argmax(y_pred, dimension=1)
    correct_prediction = tf.equal(y_pred_cls, y_true_cls)
    var = tf.cast(correct_prediction, tf.float32)
    accuracy = tf.reduce_mean(var)

    # tensorboard
    with tf.name_scope('Optimizer'):
        optimizer = tf.train.AdamOptimizer(learning_rate=1e-4).minimize(loss, global_step=global_step)

    with tf.name_scope("cost"):
        tf.scalar_summary("cost", loss)

    with tf.name_scope("accuracy"):
        tf.scalar_summary("accuracy", accuracy)

    return x, y_true, global_step, optimizer, accuracy, y_pred_cls



