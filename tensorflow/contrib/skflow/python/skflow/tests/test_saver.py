#  Copyright 2015-present The Scikit Flow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import division, print_function, absolute_import

import os
import random

from sklearn import datasets
from sklearn.metrics import accuracy_score, mean_squared_error, log_loss

import tensorflow as tf
from tensorflow.contrib.skflow.python import skflow


class SaverTest(tf.test.TestCase):

    def testIris(self):
        path = tf.test.get_temp_dir() + '/tmp.saver'
        random.seed(42)
        iris = datasets.load_iris()
        classifier = skflow.TensorFlowLinearClassifier(n_classes=3)
        classifier.fit(iris.data, iris.target)
        classifier.save(path)
        new_classifier = skflow.TensorFlowEstimator.restore(path)
        self.assertEqual(type(new_classifier), type(classifier))
        score = accuracy_score(iris.target, new_classifier.predict(iris.data))
        self.assertGreater(score, 0.5, "Failed with score = {0}".format(score))

    def testCustomModel(self):
        path = tf.test.get_temp_dir() + '/tmp.saver2'
        random.seed(42)
        iris = datasets.load_iris()
        def custom_model(X, y):
            return skflow.models.logistic_regression(X, y)
        classifier = skflow.TensorFlowEstimator(model_fn=custom_model,
            n_classes=3)
        classifier.fit(iris.data, iris.target)
        classifier.save(path)
        new_classifier = skflow.TensorFlowEstimator.restore(path)
        self.assertEqual(type(new_classifier), type(classifier))
        score = accuracy_score(iris.target, new_classifier.predict(iris.data))
        self.assertGreater(score, 0.5, "Failed with score = {0}".format(score))
    
    def testDNN(self):
        path = tf.test.get_temp_dir() + '/tmp_saver3'
        random.seed(42)
        iris = datasets.load_iris()
        classifier = skflow.TensorFlowDNNClassifier(hidden_units=[10, 20, 10], n_classes=3)
        classifier.fit(iris.data, iris.target)
        classifier.save(path)
        new_classifier = skflow.TensorFlowEstimator.restore(path)
        self.assertEqual(type(new_classifier), type(classifier))
        score = accuracy_score(iris.target, new_classifier.predict(iris.data))
        self.assertGreater(score, 0.5, "Failed with score = {0}".format(score))

    def testNoFolder(self):
        with self.assertRaises(ValueError):
            skflow.TensorFlowEstimator.restore('no_model_path')

    def testNoCheckpoints(self):
        path = tf.test.get_temp_dir() + '/tmp/tmp.saver4'
        random.seed(42)
        iris = datasets.load_iris()
        classifier = skflow.TensorFlowDNNClassifier(hidden_units=[10, 20, 10], n_classes=3)
        classifier.fit(iris.data, iris.target)
        classifier.save(path)
        os.remove(os.path.join(path, 'checkpoint'))
        with self.assertRaises(ValueError):
            skflow.TensorFlowEstimator.restore(path)
        

if __name__ == "__main__":
    tf.test.main()
