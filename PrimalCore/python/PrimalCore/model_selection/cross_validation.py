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
   stratified_kfold_cv


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
from sklearn.model_selection  import StratifiedKFold
import numpy as np

# Project
# relative import eg: from .mod import f


def stratified_kfold_cv(model,training_dataset,n_splits=10,random_state=None):
    """

    Parameters
    ----------
    model
    training_dataset
    n_splits
    random_state

    Returns
    -------

    """
    kfold = StratifiedKFold(n_splits=n_splits,random_state=random_state).split(training_dataset.features, training_dataset.target_array)


    cv_score = np.zeros((n_splits))
    for k, (train, test) in enumerate(kfold):
        model.clf.fit(training_dataset.features[train], training_dataset.target_array[train])
        cv_score[k] = model.clf.score(training_dataset.features[test], training_dataset.target_array[test])
        print('fold',k,'score',cv_score[k])


    print('\nCV accuracy: %.3f +/- %.3f' % (np.mean(cv_score), np.std(cv_score)))

    return cv_score, np.mean(cv_score), np.std(cv_score)