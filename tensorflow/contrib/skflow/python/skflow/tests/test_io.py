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
from sklearn.metrics import accuracy_score

import tensorflow as tf

from tensorflow.contrib.skflow.python import skflow
from tensorflow.contrib.skflow.python.skflow.io import *


class IOTest(tf.test.TestCase):

    def test_pandas_dataframe(self):
        if HAS_PANDAS:
            random.seed(42)
            iris = datasets.load_iris()
            data = pd.DataFrame(iris.data)
            labels = pd.DataFrame(iris.target)
            classifier = skflow.TensorFlowLinearClassifier(n_classes=3)
            classifier.fit(data, labels)
            score = accuracy_score(labels, classifier.predict(data))
            self.assertGreater(score, 0.5, "Failed with score = {0}".format(score))
        else:
            print("No pandas installed. pandas-related tests are skipped.")

    def test_pandas_series(self):
        if HAS_PANDAS:
            random.seed(42)
            iris = datasets.load_iris()
            data = pd.DataFrame(iris.data)
            labels = pd.Series(iris.target)
            classifier = skflow.TensorFlowLinearClassifier(n_classes=3)
            classifier.fit(data, labels)
            score = accuracy_score(labels, classifier.predict(data))
            self.assertGreater(score, 0.5, "Failed with score = {0}".format(score))

    def test_string_data_formats(self):
        if HAS_PANDAS:
            with self.assertRaises(ValueError):
                skflow.io.extract_pandas_data(pd.DataFrame({"Test": ["A", "B"]}))
            with self.assertRaises(ValueError):
                skflow.io.extract_pandas_labels(pd.DataFrame({"Test": ["A", "B"]}))
   
    def test_dask_io(self):
        if HAS_DASK and HAS_PANDAS:
            # test dask.dataframe
            df = pd.DataFrame(dict(a=list('aabbcc'), b=list(range(6))),
                              index=pd.date_range(start='20100101', periods=6))
            ddf = dd.from_pandas(df, npartitions=3)
            extracted_ddf = extract_dask_data(ddf)
            self.assertEqual(extracted_ddf.divisions, (0, 2, 4, 6),
                             "Failed with divisions = {0}".format(extracted_ddf.divisions))
            self.assertEqual(extracted_ddf.columns.tolist(), ['a', 'b'],
                             "Failed with columns = {0}".format(extracted_ddf.columns))
            # test dask.series
            labels = ddf['a']
            extracted_labels = extract_dask_labels(labels)
            self.assertEqual(extracted_labels.divisions, (0, 2, 4, 6),
                             "Failed with divisions = {0}".format(extracted_labels.divisions))
            # labels should only have one column
            with self.assertRaises(ValueError):
                extract_dask_labels(ddf)
        else:
            print("No dask installed. dask-related tests are skipped.")

    def test_dask_iris_classification(self):
        if HAS_DASK and HAS_PANDAS:
            random.seed(42)
            iris = datasets.load_iris()
            data = pd.DataFrame(iris.data)
            data = dd.from_pandas(data, npartitions=2)
            labels = pd.DataFrame(iris.target)
            labels = dd.from_pandas(labels, npartitions=2)
            classifier = skflow.TensorFlowLinearClassifier(n_classes=3)
            classifier.fit(data, labels)
            predictions = data.map_partitions(classifier.predict).compute()
            score = accuracy_score(labels.compute(), predictions)
            self.assertGreater(score, 0.5, "Failed with score = {0}".format(score))

if __name__ == '__main__':
    tf.test.main()
