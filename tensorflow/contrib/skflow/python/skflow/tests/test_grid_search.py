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
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score, mean_squared_error

import tensorflow as tf

from tensorflow.contrib.skflow.python import skflow


class GridSearchTest(tf.test.TestCase):

    def testIrisDNN(self):
        random.seed(42)
        iris = datasets.load_iris()
        classifier = skflow.TensorFlowDNNClassifier(
            hidden_units=[10, 20, 10], n_classes=3, steps=50)
        grid_search = GridSearchCV(classifier,
            {'hidden_units': [[5, 5], [10, 10]],
             'learning_rate': [0.1, 0.01]})
        grid_search.fit(iris.data, iris.target)
        score = accuracy_score(iris.target, grid_search.predict(iris.data))
        self.assertGreater(score, 0.5, "Failed with score = {0}".format(score))


if __name__ == "__main__":
    tf.test.main()
