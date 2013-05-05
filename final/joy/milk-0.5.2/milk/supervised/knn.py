# -*- coding: utf-8 -*-
# Copyright (C) 2008-2012, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# License: MIT. See COPYING.MIT file in the milk distribution

from __future__ import division
from collections import defaultdict
from milk.utils import get_nprandom
import numpy as np
from .base import supervised_model

__all__ = [
    'kNN',
    'knn_learner',
    'approximate_knn_learner',
    ]

def _plurality(xs):
    from collections import defaultdict
    counts = defaultdict(int)
    for x in xs: counts[x] += 1
    best,_ = max(counts.iteritems(), key=(lambda k_v: k_v[1]))
    return best

class kNN(object):
    '''
    k-Nearest Neighbour Classifier

    Naive implementation of a k-nearest neighbour classifier.

    C = kNN(k)

    Attributes:
    -----------
    k : integer
        number of neighbours to consider
    '''


    def __init__(self, k=1):
        self.k = k

    def train(self, features, labels, normalisedlabels=False, copy_features=False):
        features = np.asanyarray(features)
        labels = np.asanyarray(labels)
        if copy_features:
            features = features.copy()
            labels = labels.copy()
        features2 = np.sum(features**2, axis=1)
        return kNN_model(self.k, features, features2, labels)

knn_learner = kNN

class kNN_model(supervised_model):
    def __init__(self, k, features, features2, labels):
        self.k = k
        self.features = features
        self.f2 = features2
        self.labels = labels

    def apply(self, features):
        features = np.asanyarray(features)
        diff2 = np.dot(self.features, (-2.)*features)
        diff2 += self.f2
        neighbours = diff2.argsort()[:self.k]
        labels = self.labels[neighbours]
        return _plurality(labels)


class approximate_knn_model(supervised_model):
    def __init__(self, k, X, projected):
        self.k = k
        self.X = X
        self.projected = projected
        self.p2 = np.array([np.dot(p,p) for p in projected])

    def apply(self, t):
        tx = np.dot(self.X.T, t)
        d = np.dot(self.projected,tx)
        d *= -2
        d += self.p2
        if self.k == 1:
            return np.array([d.argmin()])
        d = d.argsort()
        return d[:self.k]

class approximate_knn_classification_model(supervised_model):
    def __init__(self, k, X, projected, labels):
        self.base = approximate_knn_model(k, X, projected)
        self.labels = labels

    def apply(self, f):
        idxs = self.base.apply(f)
        return _plurality(self.labels[idxs])

class approximate_knn_learner(object):
    '''
    approximate_knn_learner

    Learns a k-nearest neighbour classifier, where the proximity is approximate
    as it is computed on a small dimensional subspace (random subspace
    projection). For many datasets, this is acceptable.
    '''

    def __init__(self, k, ndims=8):
        self.k = k
        self.ndims = ndims
    def train(self, features, labels, **kwargs):
        labels = np.asanyarray(labels)
        R = get_nprandom(kwargs.get('R'))
        _, n_features = features.shape
        X = R.random_sample((n_features, self.ndims))
        projected = np.dot(features, X)
        return approximate_knn_classification_model(self.k, X, projected, labels.copy())

