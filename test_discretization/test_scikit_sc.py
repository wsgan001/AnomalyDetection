# -*- coding: utf-8 -*-
"""
http://www.astroml.org/sklearn_tutorial/dimensionality_reduction.html
"""
print (__doc__)

import numpy as np
import copy

from sklearn.cluster import KMeans
from sklearn.cluster import k_means
from sklearn.manifold import spectral_embedding
from sklearn.utils import check_random_state

import nslkdd.preprocessing as preprocessing
import sugarbee.reduction as reduction
import sugarbee.distance as distance
import sugarbee.affinity as affinity
import sugarbee.solver as solver

import scipy.sparse as sparse
import scipy.sparse.csgraph as csgraph

#def assign_undirected_weight(W, i, j, v):
#    W[i,j] = W[j,i] = v

if __name__ == '__main__':
    import time
    start = time.time()
    datasize = 1000

    print "preprocessing data..."
    df, headers = preprocessing.get_preprocessed_data(datasize)
    df_train = copy.deepcopy(df)
    df_train.drop('attack',1,inplace=True)
    df_train.drop('difficulty',1,inplace=True)
    print "normal"
    print len(df[df["attack"] == 11])
    print "abnormal"
    print len(df[df["attack"] != 11])

    print "data reduction..."
    proj = reduction.reduction(df_train, n_components=1)

    print "graph generation..."
    A = affinity.get_affinity_matrix(proj, metric_method=distance.gaussian,knn=200)
#    A = affinity.get_affinity_matrix(proj, metric_method=distance.dist, metric_param='euclidean', knn=8)
#    A = affinity.get_affinity_matrix(proj, metric_method=distance.dist, metric_param='manhattan', knn=8)
#    A = affinity.get_affinity_matrix(proj, metric_method=distance.cosdist,knn=8)
    D = affinity.get_degree_matrix(A)
    L = affinity.get_laplacian_matrix(A,D)

    print "data clustering..."
    Abin = None
    if sparse.isspmatrix(L):
        Abin = sparse.csc_matrix(L).sign()
    else:
        Abin = np.sign(L)
    numConn, connMap = csgraph.connected_components(Abin, directed = False)
    numClusters = numConn

    spectral = cluster.SpectralClustering(n_clusters = numClusters,
        affinity = "precomputed")
    y_spectral = spectral.fit_predict(A)
    res = y_spectral
    print "analyzing result..."

    t = df["attack"].values.tolist()
    f = df["difficulty"].values.tolist()
    print res[:10]
    print t[:10]
    print f[:10]

    # t : 11, normal
    # t : otherwise abnormal
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    trueclass = 0
    for i in range(datasize):
        if t[i] == 11 and res[i] == trueclass:
            true_positive = true_positive + 1
        if t[i] != 11 and res[i] == trueclass:
            false_positive = false_positive + 1
        if t[i] != 11 and res[i] != trueclass:
            true_negative = true_negative + 1
        if t[i] == 11 and res[i] != trueclass:
            false_negative = false_negative + 1

    print true_positive
    print true_negative
    print false_positive
    print false_negative

    elapsed = (time.time() - start)
    print "done in %s seconds" % (elapsed)

    tttt = 0
    for zzz in est.labels_:
        if zzz == trueclass :
            tttt = tttt + 1
    print tttt


