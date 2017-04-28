#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Module provide methods for classifiers data.

It allow to determine quality function
and find classifier with best quality.
"""

import os
import numpy as np
from sklearn import metrics


class ClassifiersDataProcessor:
    """Process classifiers data."""

    def __init__(self, *args):
        """Initialize class instance."""
        self.files = []
        self.quality = []
        self.answer_array = None
        self.quality_func = None
        self.is_data_ok = True
        if len(args) < 2:
            self.is_data_ok = False
            print("Not enough files")
        else:
            for f in args:
                self.files.append(self.check_file(f))

        if self.is_data_ok:
            self.answer_array = np.genfromtxt(self.files[-1], delimiter=',')
            if not self.parse_answers(self.answer_array):
                self.is_data_ok = False
                print("'%s' file contains some values which are not in {0, 1}. \
Are you sure that it is a file with answers?" % self.files[-1])

    def is_csv(self, filename):
        """Check that file has 'csv' extension."""
        f_name = os.path.basename(filename)
        return f_name.split('.')[-1].lower() == 'csv'

    def check_file(self, filename):
        """Simple check that path exists and it is file."""
        f = os.path.abspath(filename)
        if not os.path.exists(f):
            self.is_data_ok = False
            print("Looks like that '%s' is not exist. \
Please check input parameters" % filename)
            return None
        if not os.path.isfile(f):
            self.is_data_ok = False
            print("'%s' is not a file" % filename)
            return None
        if not self.is_csv(f):
            self.is_data_ok = False
            print("'%s' is not a CSV file" % filename)
            return None
        return f

    def parse_answers(self, answers_array):
        """Check that array contains only 0 and 1."""
        for x in answers_array:
            if x not in (0, 1):
                return False
        return True

    def is_classes_disbalance(self):
        """
        Check classes for disbalance.

        Return True if amount of data for one class < 5%
        from all data amount.
        """
        data_amount = float(len(self.answer_array))
        f_class = sum(self.answer_array)
        z_class = data_amount - f_class
        return min(f_class / data_amount, z_class / data_amount) < 0.05

    def prc_auc_score(self, clf_array):
        """Calculate area under curve for precision-recall curve."""
        precision, recall, _ = metrics.precision_recall_curve(
                self.answer_array,
                clf_array)
        return metrics.auc(recall, precision)

    def roc_auc_score(self, clf_array):
        """Calculate area under ROC curve."""
        return metrics.roc_auc_score(self.answer_array, clf_array)

    def set_quality_func(self):
        """Determine classifiers quality functions."""
        if self.is_classes_disbalance():
            self.quality_func = self.prc_auc_score
        else:
            self.quality_func = self.roc_auc_score

    def measure_clf_quality(self, clf_array):
        """Calculate quality for specified classifier."""
        self.set_quality_func()
        if len(clf_array) != len(self.answer_array):
            return None
        return self.quality_func(clf_array)

    def calculate_quality(self):
        """Calculate quality for all classifiers."""
        if self.is_data_ok:
            for f in self.files[:-1]:
                clf_array = np.genfromtxt(f, delimiter=',')
                clf_quality = self.measure_clf_quality(clf_array)
                self.quality.append(clf_quality)
            if not any(self.quality):
                self.is_data_ok = False
                print("Can't calculate a quality for any classifier. \
Data lenght in classifiers and answers files don't match")
        else:
            print("Wrong data files, Please see output above.")

    def get_best_quality(self):
        """Return best quality."""
        if self.is_data_ok:
            return max(self.quality)
        else:
            return None

    def get_best_classifier(self):
        """Return classifier data file with best quality."""
        if self.is_data_ok:
            return self.files[self.quality.index(self.get_best_quality())]
        else:
            return None

if __name__ == '__main__':
    import sys
    cdp = ClassifiersDataProcessor(*sys.argv[1:])
    cdp.calculate_quality()
    if cdp.is_data_ok:
        if len(cdp.files) > 2:
            print("Classifier with data in '%s' shows best quality: %s" % (
                cdp.get_best_classifier(),
                cdp.get_best_quality()))
        else:
            print("Classifier with data in '%s' has next quality: %s" % (
                cdp.get_best_classifier(),
                cdp.get_best_quality()))

    else:
        print("Can't calculate a quality. Wrong data. See output above")
