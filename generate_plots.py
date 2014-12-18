# -*- coding: utf-8 -*-
"""
http://www.astroml.org/sklearn_tutorial/dimensionality_reduction.html
"""
print (__doc__)

import numpy as np
import copy
import cPickle as pickle

import matplotlib
import matplotlib.mlab
import matplotlib.pyplot as plt
from matplotlib import gridspec

import nslkdd.preprocessing as preprocessing
import nslkdd.data.model as model
from nslkdd.get_kdd_dataframe import attack_types
from nslkdd.get_kdd_dataframe import df_by_attack_type

import colorhex
import util

today = util.make_today_folder('./results')
plot_lim_max = 30
plot_lim_min = -30

def plot_true_labels(ax, data_per_true_labels, title="", highlight_point = None):
    ax.set_title("True labels")
    for i, p in enumerate(data_per_true_labels) :
        x = np.array([t[0] for t in p])
        y = np.array([t[1] for t in p])
        if i == model.attack_normal:
            colors = ['g'] * len(x)
            ax.scatter(x, y, c=colors)
        elif i != model.attack_normal and i != highlight_point:
            colors = ['r'] * len(x)
            ax.scatter(x, y, c=colors)

    if highlight_point != None :
        p = data_per_true_labels[highlight_point]
        x = np.array([t[0] for t in p])
        y = np.array([t[1] for t in p])
        colors = ['b'] * len(x)
        ax.scatter(x, y, c=colors)

def plot_normal_label(ax, data_per_true_labels, title=""):
    ax.set_title(title)
    for i, p in enumerate(data_per_true_labels) :
        x = [t[0] for t in p]
        y = [t[1] for t in p]
        x = np.array(x)
        y = np.array(y)
        if i == model.attack_normal:
            ax.scatter(x, y, c='g')

def plot_abnormal_label(ax, data_per_true_labels, title=""):
    ax.set_title(title)
    for i, p in enumerate(data_per_true_labels) :
        x = [t[0] for t in p]
        y = [t[1] for t in p]
        x = np.array(x)
        y = np.array(y)
        if i != model.attack_normal:
            ax.scatter(x, y, c='r')

def get_data(title):
    with open(today+'/'+title+'_cproj.pkl','rb') as input:
        cproj = pickle.load(input)
    with open(today+'/'+title+'_res.pkl','rb') as input:
        res = pickle.load(input)
    with open(today+'/'+title+'_df.pkl','rb') as input:
        df = pickle.load(input)
    with open(today+'/'+title+'_highlight_point.pkl','rb') as input:
        highlight_point = pickle.load(input)
    return cproj, res, df, highlight_point

def gen_plot(cproj, res, df, highlight_point):
    # figure setting
    fig, axarr = plt.subplots(4, 4, sharex='col', sharey='row')
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.xlim(plot_lim_min, plot_lim_max)
    plt.ylim(plot_lim_min, plot_lim_max)

    data_per_true_labels = []
    for i in range( len(attacks) ):
        data_per_true_labels.append([])

    true_attack_types = df["attack"].values.tolist()
    for i, d in enumerate(cproj):
        data_per_true_labels[true_attack_types[i]].append(d)

    k = 10
    clusters = [0] * k
    for i, p in enumerate(cproj):
        true_label = true_attack_types[i]
        if true_label == model.attack_normal :
            clusters[ res[i] ] = clusters[ res[i] ] + 1
        else :
            clusters[ res[i] ] = clusters[ res[i] ] - 1

    ax1 = axarr[0, 0]
    ax2 = axarr[0, 1]
    ax3 = axarr[0, 2]
    ax4 = axarr[0, 3]
    ax5 = axarr[1, 0]
    ax6 = axarr[1, 1]
    ax7 = axarr[1, 2]
    ax8 = axarr[1, 3]
    ax9 = axarr[2, 0]
    ax10 = axarr[2, 1]
    ax11 = axarr[2, 2]
    ax12 = axarr[2, 3]
    ax13 = axarr[3, 0]
    ax14 = axarr[3, 1]
    ax15 = axarr[3, 2]
    ax16 = axarr[3, 3]

    plot_true_labels(ax1, data_per_true_labels, "True labels", highlight_point)
    plot_normal_label(ax2, data_per_true_labels, "True normals")
    plot_abnormal_label(ax3, data_per_true_labels, "True abnormal")

    ax4.set_title("k-means")
    for i, p in enumerate(cproj):
        ax4.scatter(p[0], p[1], c=colorhex.codes[ res[i] ])
    ##############################################################
    ax5.set_title("Normal res")
    for i, p in enumerate(cproj):
        if clusters[ res[i] ] >= 0 :
            ax5.scatter(p[0], p[1], c='g')
    ##############################################################
    ax6.set_title("Abnormal res")
    for i, p in enumerate(cproj):
        if clusters[ res[i] ] < 0 :
            ax6.scatter(p[0], p[1], c='r')

    ##############################################################
    ax7.set_title("Cluster 1")
    for i, p in enumerate(cproj):
        if res[i] == 0 :
            ax7.scatter(p[0], p[1], c='g')
    ##############################################################
    ax8.set_title("Cluster 2")
    for i, p in enumerate(cproj):
        if res[i] == 1 :
            ax8.scatter(p[0], p[1], c='g')
    ##############################################################
    ax9.set_title("Cluster 3")
    for i, p in enumerate(cproj):
        if res[i] == 2 :
            ax9.scatter(p[0], p[1], c='g')
    ##############################################################
    ax10.set_title("Cluster 4")
    for i, p in enumerate(cproj):
        if res[i] == 3 :
            ax10.scatter(p[0], p[1], c='g')
    ##############################################################
    ax11.set_title("Cluster 5")
    for i, p in enumerate(cproj):
        if res[i] == 4 :
            ax11.scatter(p[0], p[1], c='g')
    ##############################################################
    ax12.set_title("Cluster 6")
    for i, p in enumerate(cproj):
        if res[i] == 5 :
            ax12.scatter(p[0], p[1], c='g')
    ##############################################################
    ax13.set_title("Cluster 7")
    for i, p in enumerate(cproj):
        if res[i] == 6 :
            ax13.scatter(p[0], p[1], c='g')
    ##############################################################
    ax14.set_title("Cluster 8")
    for i, p in enumerate(cproj):
        if res[i] == 7 :
            ax14.scatter(p[0], p[1], c='g')
    ##############################################################
    ax15.set_title("Cluster 9")
    for i, p in enumerate(cproj):
        if res[i] == 8 :
            ax15.scatter(p[0], p[1], c='g')
    ##############################################################
    ax16.set_title("Cluster 10")
    for i, p in enumerate(cproj):
        if res[i] == 9 :
            ax16.scatter(p[0], p[1], c='g')
    ##############################################################

    print title + " has been saved"
    fig.savefig(today + "/" + title + ".png")
    plt.close()

if __name__ == '__main__':
    """ Anomaly detection with spectral clustering algorithm.
    First training set only, to see what would happen with only known classes
    Next with test set, to see what would happen with only unknown classes
    """
    import time
    start = time.time()

    headers, attacks = preprocessing.get_header_data()

    dataset_description = "training20_only"
    title = dataset_description
    cproj, res, df, highlight_point = get_data(title)
    gen_plot(cproj, res, df, highlight_point)

    dataset_description = "training20_test20"
    for attack_type_index, attack_type in enumerate(model.attack_types) :
        if attack_type_index <= model.attack_normal : # why <= instead of !=
            continue
        title = dataset_description + "_" + attack_type
        cproj, res, df, highlight_point = get_data(title)
        gen_plot(cproj, res, df, highlight_point)

    elapsed = (time.time() - start)
    print "done in %s seconds" % (elapsed)
