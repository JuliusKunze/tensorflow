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

import numpy as np

from sklearn import datasets
from sklearn.metrics import accuracy_score, mean_squared_error

import tensorflow as tf
from tensorflow.contrib.skflow.python import skflow


class MultiOutputTest(tf.test.TestCase):

    def testMultiRegression(self):
        random.seed(42)
        rng = np.random.RandomState(1)
        X = np.sort(200 * rng.rand(100, 1) - 100, axis=0)
        y = np.array([np.pi * np.sin(X).ravel(), np.pi * np.cos(X).ravel()]).T
        regressor = skflow.TensorFlowLinearRegressor(learning_rate=0.01)
        regressor.fit(X, y)
        score = mean_squared_error(regressor.predict(X), y)
        self.assertLess(score, 10, "Failed with score = {0}".format(score))


if __name__ == "__main__":
    tf.test.main()
