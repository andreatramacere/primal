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
   model_learning_curve


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
from sklearn.model_selection import learning_curve
import numpy as np
# Project
# relative import eg: from .mod import f


def model_learning_curve(model,training_test,cv=5,n_jobs=1,train_sizes=np.linspace(0.1,0.9,9),scoring=None):

    train_sizes, train_scores, test_scores = learning_curve(model.clf,
                                                            training_test.features,
                                                            training_test.target_array,
                                                            cv=cv,
                                                            n_jobs=n_jobs,
                                                            train_sizes=train_sizes,
                                                            scoring=scoring)


    return train_sizes, train_scores, test_scores