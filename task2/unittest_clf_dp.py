#!/usr/bin/python
# -*- coding: utf-8 -*-
"""TODO: add module docs."""

import os
import unittest
import uuid
import numpy as np
from sklearn import metrics
from clf_dp import ClassifiersDataProcessor


class ClassifierDataProcessorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.empty_csv = str(uuid.uuid4()) + '.csv'
        with open(cls.empty_csv, 'w'):
            pass

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.empty_csv)

    def testCheckFile_notExists(self):
        clf = ClassifiersDataProcessor()
        clf.is_data_ok = True
        fname = str(uuid.uuid4())
        self.assertTupleEqual(
                (clf.check_file(fname), clf.is_data_ok),
                (None, False), "%s not exists" % fname)

    def testCheckFile_notFile(self):
        clf = ClassifiersDataProcessor()
        clf.is_data_ok = True
        self.assertTupleEqual(
                (clf.check_file(os.curdir), clf.is_data_ok),
                (None, False), "%s not a file" % os.curdir)

    def testCheckFile_noCsv(self):
        clf = ClassifiersDataProcessor()
        clf.is_data_ok = True
        self.assertTupleEqual(
                (clf.check_file(__file__), clf.is_data_ok),
                (None, False), "%s is not a csv file" % __file__)

    def testCheckFile_goodFile(self):
        clf = ClassifiersDataProcessor()
        clf.is_data_ok = True
        self.assertTupleEqual(
                (clf.check_file(self.empty_csv), clf.is_data_ok),
                (os.path.abspath(self.empty_csv), True),
                "%s exists and has properly extension" % self.empty_csv)

    def testIsCsv_notCsv(self):
        clf = ClassifiersDataProcessor()
        self.assertEqual(
                clf.is_csv(__file__),
                False, "%s is not a CSV" % __file__)

    def testIsCsv_isCsv(self):
        clf = ClassifiersDataProcessor()
        self.assertEqual(
                clf.is_csv(self.empty_csv),
                True, "%s is a CSV" % self.empty_csv)

    def testParseAnswers_positive(self):
        clf = ClassifiersDataProcessor()
        arr = np.array([0, 1])
        self.assertEqual(
                clf.parse_answers(arr),
                True, "%s contains only 0 and 1" % arr)

    def testParseAnswers_negative(self):
        clf = ClassifiersDataProcessor()
        arr = np.array([0, 1, 3])
        print clf.parse_answers(arr)
        self.assertEqual(
                clf.parse_answers(arr),
                False, "%s doesn't contain {0, 1} only" % arr)

    def testIsClassesDisbalance_positive(self):
        clf = ClassifiersDataProcessor()
        arr = np.array([1] * 96)
        arr = np.append(arr, [0] * 4)
        clf.answer_array = arr
        self.assertEqual(
                clf.is_classes_disbalance(),
                True, "'0' amount < 5%% from all data in %s" % arr)

    def testIsClassesDisbalance_negative(self):
        clf = ClassifiersDataProcessor()
        arr = np.array([1] * 95)
        arr = np.append(arr, [0] * 5)
        clf.answer_array = arr
        self.assertEqual(
                clf.is_classes_disbalance(),
                False, "'0' amount = 5%% from all data in %s" % arr)

    def testSetQualityFunc_withDisbalance(self):
        clf = ClassifiersDataProcessor()
        arr = np.array([1] * 96)
        arr = np.append(arr, [0] * 4)
        clf.answer_array = arr
        clf.set_quality_func()
        self.assertEqual(clf.quality_func.__name__, clf.prc_auc_score.__name__, "prc_auc_score must be selected with classes disbalance")

    def testSetQualityFunc_noDisbalance(self):
        clf = ClassifiersDataProcessor()
        arr = np.array([1] * 95)
        arr = np.append(arr, [0] * 5)
        clf.answer_array = arr
        clf.set_quality_func()
        self.assertEqual(clf.quality_func.__name__, clf.roc_auc_score.__name__, "roc_auc_score must be selected without classes disbalance")

    def testPrcAucScore(self):
        clf = ClassifiersDataProcessor()
        clf.answer_array = np.array([0, 0, 1, 1])
        clf_array = np.array([0.1, 0.4, 0.35, 0.8])
        precision, recall, _ = metrics.precision_recall_curve(clf.answer_array, clf_array)
        self.assertEqual(metrics.auc(recall, precision), clf.prc_auc_score(clf_array), "scores don't match")

    def testRocAucScore(self):
        clf = ClassifiersDataProcessor()
        clf.answer_array = np.array([0, 0, 1, 1])
        clf_array = np.array([0.1, 0.4, 0.35, 0.8])
        self.assertEqual(metrics.roc_auc_score(clf.answer_array, clf_array), clf.roc_auc_score(clf_array), "scores don't match")

    def testMeasureClfQuality_diffArrLen(self):
        clf = ClassifiersDataProcessor()
        clf.answer_array = np.array([0, 0, 1])
        clf_array = np.array([0.1, 0.4, 0.35, 0.8])
        self.assertEqual(clf.measure_clf_quality(clf_array), None, "lenght for %s and %s don't match" % (clf.answer_array, clf_array))

    def testMeasureClfQuality(self):
        clf = ClassifiersDataProcessor()
        clf.answer_array = np.array([0, 0, 1, 1])
        clf_array = np.array([0.1, 0.4, 0.35, 0.8])
        self.assertEqual(clf.measure_clf_quality(clf_array), 0.75, "error in quality measurement")

    def testGetBestQuality_badData(self):
        clf = ClassifiersDataProcessor()
        clf.quality = [1, 2, 3]
        clf.is_data_ok = False
        self.assertEqual(clf.get_best_quality(), None, "No ability to determine best quality with bad data")

    def testGetBestQuality(self):
        clf = ClassifiersDataProcessor()
        clf.quality = [1, 2, 3]
        clf.is_data_ok = True
        self.assertEqual(clf.get_best_quality(), max(clf.quality), "Wrong quality calculation")

    def testGetBestClassifier_badData(self):
        clf = ClassifiersDataProcessor()
        clf.quality = [1, 2, 3]
        clf.files = ['not_best1', 'not_best2', 'best']
        clf.is_data_ok = False
        self.assertEqual(clf.get_best_classifier(), None, "No ability to determine best classifier with bad data")

    def testGetBestClassifier(self):
        clf = ClassifiersDataProcessor()
        clf.quality = [1, 2, 3]
        clf.files = ['not_best1', 'not_best2', 'best']
        clf.is_data_ok = True
        self.assertEqual(clf.get_best_classifier(), clf.files[-1], "Error in best classifier determination")

if __name__ == '__main__':
    unittest.main(verbosity=2)
