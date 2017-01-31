"""
Overview
--------
   
general info about this module

Summary
---------
.. autosummary::
   eval_pit
   eval_pdf_gmm

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
import  numpy as np
from sklearn.mixture import GaussianMixture
import properscoring as ps
from scipy.stats import norm

# Project
# relative import eg: from .mod import f





def eval_pit(z_values,z_true):
    z_true=np.atleast_1d(z_true)
    z_sort=np.sort(np.atleast_2d(z_values))
    pit=np.zeros(z_true.size)
    for ID,z in enumerate(z_true):
        pit[ID]= np.float(np.where(z_sort[ID]<=z_true[ID])[0].size)/np.float(z_sort[ID].size)

    return pit


def eval_crps(z_values,z_true):
    z_values=np.atleast_2d(z_values)
    cprs = np.zeros(z_values.shape[0])
    for ID,z in enumerate(z_values):

        cprs[ID]= ps.crps_ensemble(z_true[ID], z)

    return cprs



def eval_pdf_gmm(z_values,n_components=2,grid_size=100):
    models=[GaussianMixture(n_components=n).fit(z_values.reshape(z_values.size,1)) for n in xrange(1,n_components+1)]

    BICs = [m.bic(z_values.reshape(z_values.size,1)) for m in models]

    t=np.linspace(z_values.min(),z_values.max(),grid_size)
    logprob=models[np.argmin(BICs)].score_samples(t.reshape(t.size,1))

    return t, np.exp(logprob)




