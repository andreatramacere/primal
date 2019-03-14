#  
# Copyright (C) 2012-2020 Euclid Science Ground Segment      
#    
# This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General    
# Public License as published by the Free Software Foundation; either version 3.0 of the License, or (at your option)    
# any later version.    
#    
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied    
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more    
# details.    
#    
# You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to    
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA    
#

"""
Overview
--------

general info about this module


Summary
---------
.. autosummary::
   rec_feat_rem
   rec_feat_rem_cv
   get_names_list

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
from sklearn.feature_selection import RFECV,RFE

# Project
# relative import eg: from .mod import f
from ..homogeneous_table.dataset_handler import *


@decorator.decorator
def check_has_feat_imp(func,model,*args, **kwargs):
    if hasattr(model.clf, 'feature_importances_') or hasattr(model.clf, 'coef_'):
        return func(model,*args, **kwargs)
    else:
        raise RuntimeError('''model has not 'feature_importances_' or 'coef_' attribute''')


@check_has_feat_imp
def rec_feat_rem(model, training_set, filter=True, step=1, test_set=None,n_features_to_select=None):
    """
    Performs a Feature ranking with recursive feature elimination using the `sklearn.feature_selection.RFE`

    Parameters
    ----------
    model :
    train : training.set
    filter : bool
        if True the features are removed from the model
    step : int or float, optional (default=1)
        If greater than or equal to 1, then step corresponds to the (integer) number of features to
        remove at each iteration. If within (0.0, 1.0), then step corresponds to the percentage (rounded down)
        of features to remove at each iteration.
    test :
    n_features_to_select

    Returns
    -------

    """
    rfe = RFE(estimator=model.clf, step=step,n_features_to_select=n_features_to_select)
    rfe.fit(training_set.features, training_set.target_array)
    print("Optimal number of features : %d" % rfe.n_features_)

    if filter == True:
        training_set.columns_mask = rfe.support_
        if test_set is not None:
            training_set.columns_mask = rfe.support_

    return rfe.support_,rfe.n_features_

@check_has_feat_imp
def rec_feat_rem_cv(model, training_set, cv=10, filter=True, test_set=None, scoring=None):
    """
    Performs a Feature ranking with recursive feature elimination using the `sklearn.feature_selection.RFECV`

    Parameters
    ----------
    model
    training_set
    cv
    filter
    test_set
    scoring

    Returns
    -------

    """

    rfecv = RFECV(estimator=model.clf, step=1, cv=cv, scoring=scoring)
    rfecv.fit(training_set.features, training_set.target_array)

    print("Optimal number of features : %d" % rfecv.n_features_)

    if filter == True:
        training_set.columns_mask=rfecv.support_
        if test_set is not None:
            training_set.columns_mask = rfecv.support_

    return rfecv.support_,rfecv.n_features_,rfecv.grid_scores_,rfecv.ranking_



def get_names_list(features_names,support_):
    return [name for ID,name in enumerate(features_names) if support_[ID]==True]

