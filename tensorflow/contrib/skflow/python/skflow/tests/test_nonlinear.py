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

import random

from sklearn import datasets
from sklearn.metrics import accuracy_score, mean_squared_error

import tensorflow as tf
from tensorflow.contrib.skflow.python import skflow


class NonLinearTest(tf.test.TestCase):

    def testIrisDNN(self):
        random.seed(42)
        iris = datasets.load_iris()
        classifier = skflow.TensorFlowDNNClassifier(
            hidden_units=[10, 20, 10], n_classes=3)
        classifier.fit(iris.data, iris.target)
        score = accuracy_score(iris.target, classifier.predict(iris.data))
        self.assertGreater(score, 0.5, "Failed with score = {0}".format(score))
        weights = classifier.weights_
        self.assertEqual(weights[0].shape, (4, 10))
        self.assertEqual(weights[1].shape, (10, 20))
        self.assertEqual(weights[2].shape, (20, 10))
        self.assertEqual(weights[3].shape, (10, 3))
        biases = classifier.bias_
        self.assertEqual(len(biases), 4)

    def testBostonDNN(self):
        random.seed(42)
        boston = datasets.load_boston()
        regressor = skflow.TensorFlowDNNRegressor(
            hidden_units=[10, 20, 10], n_classes=0,
            batch_size=boston.data.shape[0],
            steps=200, learning_rate=0.001)
        regressor.fit(boston.data, boston.target)
        score = mean_squared_error(
            boston.target, regressor.predict(boston.data))
        self.assertLess(score, 100, "Failed with score = {0}".format(score))
        weights = regressor.weights_
        self.assertEqual(weights[0].shape, (13, 10))
        self.assertEqual(weights[1].shape, (10, 20))
        self.assertEqual(weights[2].shape, (20, 10))
        self.assertEqual(weights[3].shape, (10, 1))
        biases = regressor.bias_
        self.assertEqual(len(biases), 4)

    def testRNN(self):
        random.seed(42)
        import numpy as np
        data = np.array(list([[2, 1, 2, 2, 3],
                              [2, 2, 3, 4, 5],
                              [3, 3, 1, 2, 1],
                              [2, 4, 5, 4, 1]]), dtype=np.float32)
        # labels for classification
        labels = np.array(list([1, 0, 1, 0]), dtype=np.float32)
        # targets for regression
        targets = np.array(list([10, 16, 10, 16]), dtype=np.float32)
        test_data = np.array(list([[1, 3, 3, 2, 1], [2, 3, 4, 5, 6]]))
        def input_fn(X):
            return tf.split(1, 5, X)

        # Classification
        classifier = skflow.TensorFlowRNNClassifier(
            rnn_size=2, cell_type='lstm', n_classes=2, input_op_fn=input_fn)
        classifier.fit(data, labels)
        classifier.weights_
        classifier.bias_
        predictions = classifier.predict(test_data)
        self.assertAllClose(predictions, np.array([1, 0]))
        
        classifier = skflow.TensorFlowRNNClassifier(
            rnn_size=2, cell_type='rnn', n_classes=2,
            input_op_fn=input_fn, num_layers=2)
        classifier.fit(data, labels)
        classifier = skflow.TensorFlowRNNClassifier(
            rnn_size=2, cell_type='invalid_cell_type', n_classes=2,
            input_op_fn=input_fn, num_layers=2)
        with self.assertRaises(ValueError):
            classifier.fit(data, labels)

        # Regression
        regressor = skflow.TensorFlowRNNRegressor(
            rnn_size=2, cell_type='gru', input_op_fn=input_fn)
        regressor.fit(data, targets)
        regressor.weights_
        regressor.bias_
        predictions = regressor.predict(test_data)
    
    def testBidirectionalRNN(self):
        random.seed(42)
        import numpy as np
        data = np.array(list([[2, 1, 2, 2, 3],
                              [2, 2, 3, 4, 5],
                              [3, 3, 1, 2, 1],
                              [2, 4, 5, 4, 1]]), dtype=np.float32)
        labels = np.array(list([1, 0, 1, 0]), dtype=np.float32)
        def input_fn(X):
            return tf.split(1, 5, X)

        # Classification
        classifier = skflow.TensorFlowRNNClassifier(
            rnn_size=2, cell_type='lstm', n_classes=2, input_op_fn=input_fn,
            bidirectional=True)
        classifier.fit(data, labels)
        predictions = classifier.predict(np.array(list([[1, 3, 3, 2, 1],
                                                        [2, 3, 4, 5, 6]])))
        self.assertAllClose(predictions, np.array([1, 0]))
        

if __name__ == "__main__":
    tf.test.main()
