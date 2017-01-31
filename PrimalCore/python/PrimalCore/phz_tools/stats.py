"""
Overview
--------
   
general info about this module



Summary
---------
.. autosummary::
   outliers_score
   eval_z_pred_stats

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

# Project
# relative import eg: from .mod import f




def outliers_score(estimator,X,y,bias=0.15):
    """
    Function for scoring  with signature f(estimator,X,y)
    applies estimator.predict()

    Parameters
    ----------
    estimator
    X : features array
    y : target array
        redshift

    Returns
    -------
    eta_outliers

    """
    z_actual=y
    z_pred=estimator.predict(X)

    delta_z=z_actual-z_pred
    delta_z_norm=delta_z/(1+z_actual)

    outliers=delta_z_norm[np.fabs(delta_z_norm)>bias].size

    eta_outliers=np.float64(outliers)/delta_z_norm.size*100.0

    return 100.0-eta_outliers


def eval_z_pred_stats(z_actual,z_pred):
    """

    Parameters
    ----------
    z_actual
    z_pred

    Returns
    -------

    """
    delta_z=z_actual-z_pred
    delta_z_norm=delta_z/(1+z_actual)

    #bias=delta_z.sum()/np.float(z_pred.size)
    #bias_norm=delta_z_norm.sum()/np.float(z_pred.size)
    #MAD=np.median(np.fabs(delta_z_norm))

    #Normalized MAD
    sigma=1.48*np.median(np.fabs(delta_z_norm))

    bias_JC=np.median(delta_z_norm)
    #bias=delta_z.sum()/np.float(z_pred.size)
    bias_norm=delta_z_norm.sum()/np.float(z_pred.size)
    outliers=delta_z_norm[np.fabs(delta_z_norm)>0.15].size
    outliers_2sig=delta_z_norm[np.fabs(delta_z_norm)>2.0*sigma].size

    eta_outliers=np.float64(outliers)/delta_z_norm.size*100.0
    eta_outliers_2sig=np.float64(outliers_2sig)/delta_z_norm.size*100.0

    #t="bias=%f \n"%bias
    t='$sample size=%d$\n'%z_actual.size
    t+="$bias \ \ (avg.)=%5.5f$\n"%bias_norm
    t+="$bias \ \ (median(\Delta z_{norm})) = %5.5f $\n"%bias_JC
    t+="$MAD = %5.5f$\n"%(sigma/1.48)
    t+="$\sigma \ \ (NMAD) = %5.5f$\n"%sigma
    t+="$\eta \ \ (\Delta z_{norm}>0.15) = %5.2f$ %%\n"%eta_outliers
    t+="$\eta \ \ (\Delta z_{norm}>2.0\sigma )= %5.2f$ %%\n"%eta_outliers_2sig
    #print(t)
    return t,delta_z_norm