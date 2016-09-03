# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from sklearn import cross_validation
from sklearn import metrics
import tensorflow as tf
import numpy as np
from tensorflow.contrib import learn
import os


# commit account test
# delete the accoutn but still using a wrong account
# contribution count test
# somting is little bit starnge
# god damn my another git accoutn confued
class TensorIris():

    score = None
    predict = None

    def iris_simple(self):
        # Load dataset.
        iris = learn.datasets.load_dataset('iris')
        x_train, x_test, y_train, y_test = cross_validation.train_test_split(
          iris.data, iris.target, test_size=0.2, random_state=42)

        # Build 3 layer DNN with 10, 20, 10 units respectively.
        feature_columns = learn.infer_real_valued_columns_from_input(x_train)
        classifier = learn.DNNClassifier(
          feature_columns=feature_columns, hidden_units=[10, 20, 10], n_classes=3)

        # Fit and predict.
        classifier.fit(x_train, y_train, steps=200)
        score = metrics.accuracy_score(y_test, classifier.predict(x_test))
        print('Accuracy: {0:f}'.format(score))

        self.score = format(score)

    @property
    def score(self):
        return self.score


    def iris_train_save(self):

        print(os.path.dirname(__file__))

        # Data sets
        IRIS_TRAINING = os.path.dirname(__file__) + "/iris_training.csv"
        IRIS_TEST = os.path.dirname(__file__) + "/iris_test.csv"

        # Load datasets.
        training_set = tf.contrib.learn.datasets.base.load_csv(filename=IRIS_TRAINING,
                                                               target_dtype=np.int)
        test_set = tf.contrib.learn.datasets.base.load_csv(filename=IRIS_TEST,
                                                           target_dtype=np.int)



        # Build 3 layer DNN with 10, 20, 10 units respectively.
        classifier = tf.contrib.learn.DNNClassifier(hidden_units=[10, 20, 10],
                                                    n_classes=3,
                                                    model_dir="/tmp/iris_model")

        # Fit model.
        classifier.fit(x=training_set.data,
                       y=training_set.target,
                       steps=2000)

        # Evaluate accuracy.
        accuracy_score = classifier.evaluate(x=test_set.data,
                                             y=test_set.target)["accuracy"]
        print('Accuracy: {0:f}'.format(accuracy_score))

        self.score = accuracy_score

    @property
    def predict(self):
        return self.predict


    def iris_predict(self):

        classifier = tf.contrib.learn.DNNClassifier(hidden_units=[10, 20, 10],
                                                    n_classes=3,
                                                    model_dir="/tmp/iris_model")

        # Classify two new flower samples.
        new_samples = np.array(
            [[6.4, 3.2, 4.5, 1.5], [5.8, 3.1, 5.0, 1.7]], dtype=float)
        y = classifier.predict(new_samples)
        print('Predictions: {}'.format(str(y)))

        self.predict = str(y)
