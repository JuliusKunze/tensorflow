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

import tensorflow as tf

import random

from sklearn import datasets, metrics
from sklearn.cross_validation import train_test_split

from tensorflow.contrib.skflow.python import skflow


class EarlyStoppingTest(tf.test.TestCase):

    def testIrisES(self):
        random.seed(42)

        iris = datasets.load_iris()
        X_train, X_test, y_train, y_test = train_test_split(iris.data,
                                                            iris.target,
                                                            test_size=0.2,
                                                            random_state=42)

        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2)
        val_monitor = skflow.monitors.ValidationMonitor(X_val, y_val, n_classes=3)

        # classifier without early stopping - overfitting
        classifier1 = skflow.TensorFlowDNNClassifier(hidden_units=[10, 20, 10],
                                                     n_classes=3, steps=1000)
        classifier1.fit(X_train, y_train)
        score1 = metrics.accuracy_score(y_test, classifier1.predict(X_test))

        # classifier with early stopping - improved accuracy on testing set
        classifier2 = skflow.TensorFlowDNNClassifier(hidden_units=[10, 20, 10],
                                                     n_classes=3, steps=1000)

        classifier2.fit(X_train, y_train, val_monitor)
        score2 = metrics.accuracy_score(y_test, classifier2.predict(X_test))

        # self.assertGreater(score2, score1, "No improvement using early stopping.")

if __name__ == "__main__":
    tf.test.main()
