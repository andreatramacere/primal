"""
Overview
--------

general info about this module




Module API
----------
"""

from __future__ import absolute_import, division, print_function

from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object, map, zip)

__author__ = "Andrea Tramacere"

# Standard library
# eg copy
# absolute import rg:from copy import deepcopy

# Dependencies
# eg numpy
# absolute import eg: import numpy as np
import matplotlib.pyplot as plt
import numpy as np
# Project
# relative import eg: from .mod import f
from PrimalCore.phz_tools.stats import eval_z_pred_stats


class PrimalPlot(object):

    def __init__(self,ax=None):
        if ax is None:
            self.fig, self.ax = plt.subplots()
        else:
            self.fig = None
            self.ax= ax

    def save_plot(self, file_name=None):

        if self.fig is None:
            self.ax.figure.savefig(file_name)
        else:
            self.fig.savefig(file_name)


def plot_learning_curve(train_sizes, train_scores, test_scores,ax=None,fig=None,title='learning curve',plot=False):
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    p=PrimalPlot(ax)


    p.ax.set_title(title)
    p.ax.grid()
    p.ax.set_xlabel("Training examples")
    p.ax.set_ylabel("Score")

    p.ax.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    p.ax.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    p.ax.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    p.ax.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    p.ax.legend(loc="best")

    plt.tight_layout()
    y1,y2=p.ax.get_ylim()
    p.ax.set_ylim(y1-y1*0.1,y2+y2*0.1)
    if plot == True:
        plt.show()

    return p

def plot_features_imp(feature_importances,feature_names=None,ax=None,title='feature importance',plot=False,max_plot=None):
    p = PrimalPlot(ax)

    p.ax.set_title(title)

    if feature_names is None:
        feature_names = [ID for ID in np.arange(feature_importances.size)]

    feature_importances = 100.0 * (feature_importances / feature_importances.max())

    sorted_idx = np.argsort(feature_importances)

    if max_plot is not None:
        sorted_idx = sorted_idx[-max_plot:]

    pos = np.arange(sorted_idx.shape[0]) + .5

    p.ax.barh(pos, feature_importances[sorted_idx], align='center')
    p.ax.set_yticks(pos)
    p.ax.set_yticklabels(np.array(feature_names)[sorted_idx],fontsize='x-small')
    p.ax.set_xlabel('Relative Importance',fontsize=20)
    if max_plot is not None:
        p.ax.set_title('Top  %d feature Importance'%(max_plot),fontsize=20)
    else:
        p.ax.set_title('Feature Importances', fontsize=20)
    for label in (p.ax.get_xticklabels() + p.ax.get_yticklabels()):
        label.set_fontsize(13)

    plt.tight_layout()

    if plot == True:
        plt.show()

    return p




def plot_z_spec_vs_z_phot(z_spec,z_phot,ax=None,title='',bias=0.15,plot=False,point_size=1.0):
    p = PrimalPlot(ax)

    p.ax.set_title(title)

    x = np.linspace(z_spec.min(), z_spec.max(), 100)
    p.ax.plot(x, x, '-', color='red', lw=1.5)
    p.ax.plot(x, x + bias * (1 + x), '--', lw=1.5, color='red')
    p.ax.plot(x, x - bias * (1 + x), '--', lw=1.5, color='red')

    z_min=min(z_spec.min(),z_phot.min())
    z_max=min(z_spec.max(),z_phot.max())
    p.ax.set_xlim([z_min-0.5, z_max+1.0])
    p.ax.set_ylim([z_min-0.5, z_max+1.0])

    stats_text, delta_z_norm = eval_z_pred_stats(z_spec, z_phot)
    p.ax.plot(z_spec, z_phot, '.', color='blue',ms=point_size,label=stats_text)

    p.ax.set_ylabel("z_phot", fontsize=20)
    p.ax.set_xlabel("z_spec", fontsize=20)
    for label in (p.ax.get_xticklabels() + p.ax.get_yticklabels()):
        label.set_fontsize(13)

    p.ax.legend(loc='best', fontsize=10)

    plt.axis('equal')
    plt.tight_layout()
    if plot==True:
        plt.show()

    return p



def plot_z_spec_vs_z_phot_kde(z_spec,z_phot,ax=None,title='',n_levels=20,plot=False,gridsize=100):
    p = PrimalPlot(ax)

    p.ax.set_title(title)


    try:
        import seaborn as sns
        sns.set_style('white')
        sns.despine()
        sns.kdeplot(z_spec, z_phot, ax=p.ax, shade=True, n_levels=n_levels, cmap='Blues', shade_lowest=False,gridsize=gridsize)



    except:

        from scipy import stats

        x = z_spec
        y = z_phot
        xmin, xmax = x.min(), x.max()
        ymin, ymax = y.min(), y.max()
        xx, yy = np.mgrid[xmin:xmax:np.complex(gridsize), ymin:ymax:np.complex(gridsize)]
        positions = np.vstack([xx.ravel(), yy.ravel()])
        values = np.vstack([x, y])
        kernel = stats.gaussian_kde(values)
        f = np.reshape(kernel(positions).T, xx.shape)
        cset=p.ax.contourf(xx, yy, f, n_levels, cmap='Blues')
        cset.collections[0].set_alpha(0)

    p.ax.plot(z_spec, z_phot, '.', color='black',ms=1.0)

    z_min = min(z_spec.min(), z_phot.min())
    z_max = min(z_spec.max(), z_phot.max())
    p.ax.set_xlim([z_min - 0.5, z_max + 1.0])
    p.ax.set_ylim([z_min - 0.5, z_max + 1.0])

    plt.axis('equal')
    p.ax.set_xlabel('z spec', {'size': 20})
    p.ax.set_ylabel('z phot', {'size': 20})
    plt.tight_layout()

    return p


def binned_trend_scatter_plot(x,y,title='',ax=None,label=None,color=None,x_label='x',y_label='y',plot=False,n_bins=10):
    p = PrimalPlot(ax)

    p.ax.set_title(title)

    p.ax.plot(x, y, '.', label=label, c=color, ms=1, zorder=-1)

    hist, bin_edges = np.histogram(x, n_bins)
    x_bin = np.zeros(hist.size)
    y_bin = np.zeros(hist.size)
    dy_bin = np.zeros(hist.size)

    bin_popuation = np.searchsorted(bin_edges, x, side='right')
    bin_popuation[bin_popuation == bin_edges.size] = bin_edges.size - 1
    bin_popuation[bin_popuation == 0] = 1

    for id in np.arange(hist.size):
        x_bin[id] = (bin_edges[id + 1] + bin_edges[id]) * 0.5
        y_bin[id] = np.mean(y[bin_popuation == id + 1])
        dy_bin[id] = np.std(y[bin_popuation == id + 1])

        p.ax.errorbar(x_bin, y_bin, yerr=dy_bin, xerr=(bin_edges[id + 1] - bin_edges[id]) * 0.5, fmt='o', color='black', zorder=1)

    p.ax.set_xlabel(x_label, {'size': 18})
    p.ax.set_ylabel(y_label, {'size': 18})
    p.ax.legend()

    #plt.axis('equal')
    if plot == True:
        plt.show()

    return p

def plot_feature_imp_trend(scores,ax=None,title='feature_imp_trend',plot=False):
    p = PrimalPlot(ax)

    p.ax.set_title(title)
    p.ax.plot(np.arange(scores.size) + 1, scores)
    p.ax.set_xlabel('n features',{'size': 20})
    p.ax.set_ylabel('cv score',{'size': 20})

    plt.tight_layout()
    if plot == True:
        plt.show()

    return p


def plot_PIT_histogram(pit,ax=None,title='PIT',plot=False,bins=20,normed=True):
    p = PrimalPlot(ax)

    p.ax.set_title(title)

    p.ax.hist(pit,bins,normed=normed)
    p.ax.set_ylabel("norm. counts", fontsize=18)
    plt.tight_layout()
    if plot == True:
        plt.show()

    return p


def plot_CRPS_histogram(crps, ax=None, title='CRPS', plot=False, bins=20,normed=True):
    p = PrimalPlot(ax)

    p.ax.set_title(title+' %3.3f'%np.mean(crps))

    p.ax.hist(crps, bins,normed=normed)
    p.ax.set_ylabel("norm. counts", fontsize=18)
    plt.tight_layout()
    if plot == True:
        plt.show()

    return p


def plot_pdf(pdf_array,ID,ax=None,plot=False,normed=True,bins=20):
    p = PrimalPlot(ax)


    p.ax.set_title('estimate of z_phot pdf')

    p.ax.hist(pdf_array[ID]['z_phot_values'],label='pdf,',bins=bins,normed=normed)

    y=p.ax.get_ylim()
    p.ax.plot([pdf_array[ID]['z_spec'],pdf_array[ID]['z_spec']],y,label='z_spec')
    p.ax.plot([pdf_array[ID]['z_phot'], pdf_array[ID]['z_phot']], y, label='z_phot')
    p.ax.plot(pdf_array['z_phot_pdf_grid'][ID], pdf_array['z_phot_pdf'][ID], '-', label='gmm pdf', color='black')
    p.ax.set_xlabel("z_phot",fontsize=22)
    p.ax.legend(loc='best',fontsize=22)

def test_plot(x,y,ax=None):
    from scipy import stats
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig =None
    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    values = np.vstack([x, y])
    kernel = stats.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, xx.shape)


    ax = fig.gca()
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # Contourf plot
    cfset = ax.contourf(xx, yy, f, cmap='Blues')
    cfset.collections[0].set_alpha(0)
    ## Or kernel density estimate plot instead of the contourf plot
    # ax.imshow(np.rot90(f), cmap='Blues', extent=[xmin, xmax, ymin, ymax])
    # Contour plot
    #cset = ax.contour(xx, yy, f, colors='k')
    # Label plot
    #ax.clabel(cset, inline=1, fontsize=10)
    ax.plot(x, y, '.', color='black', ms=1.0)
    plt.axis('equal')
    ax.set_xlabel('z spec', {'size': 20})
    ax.set_ylabel('z phot', {'size': 20})

    if fig is not None:
        return fig, ax
    else:
        return None



