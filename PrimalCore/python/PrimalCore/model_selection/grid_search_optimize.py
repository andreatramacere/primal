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
   grid_search_stratified_kfold_cv


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
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection  import StratifiedKFold

# Project
# relative import eg: from .mod import f



def grid_search_stratified_kfold_cv(model,training_dataset,par_grid_dict=None):
    kfold = StratifiedKFold(n_splits=10, random_state=1).split(training_dataset.features, training_dataset.target_array)
    if par_grid_dict is None:
        param_grid=model.par_grid_dict
    g_search = GridSearchCV(model.clf, param_grid=param_grid, cv=kfold)
    g_search.fit(training_dataset.features,  training_dataset.target_array)
    print("best parameters are %s with a CV score  of %0.2f" % (g_search.best_params_, g_search.best_score_))
    return g_search.best_params_, g_search.best_score_,g_search.best_estimator_


# MT kfold:
'''
shuffle=True;
fetures-->features;
add: param_grid=par_grid_dict
add: scoring
%0.2f --> %0.4f
'''

def grid_search_stratified_kfold_cv_para(model,training_dataset,par_grid_dict=None,scoring=None):
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=1).split(training_dataset.features, training_dataset.target_array)
    if par_grid_dict is None:
        param_grid=model.par_grid_dict
    else:
        param_grid=par_grid_dict
    g_search = GridSearchCV(model.clf, param_grid=param_grid, cv=kfold, scoring=scoring)
    g_search.fit(training_dataset.features,  training_dataset.target_array)
    print("best parameters are %s with a CV score  of %0.4f" % (g_search.best_params_, g_search.best_score_))
    return g_search.best_params_, g_search.best_score_,g_search.best_estimator_
