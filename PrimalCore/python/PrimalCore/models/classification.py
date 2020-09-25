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
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.ensemble import GradientBoostingClassifier as GB
from sklearn.ensemble import AdaBoostClassifier as AB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier

import numpy as np

# Project
# relative import eg: from .mod import f


from .base import BaseModel



class Classifier(BaseModel):
    """
    This class implements a :class:`~PrimalCore.models.base.BaseModel` derived class
    specialized for  skelearn Classifiers  :class:`sklearn.base.ClassifierMixin`

    It  implements  class methods to build some predefined Classifiers

    Parameters
    ----------
     clf : :class:`~sklearn.base.RegressorMixin` or :class:`~sklearn.base.ClassifierMixin` derived object
        the skelarn model wrapped in the class

     par_grid_dict : dictionary
        the dictionary of `clf` that we want to use for regularziation

     add_scorer : function  with a signature f(object, features, targe)
        a function to evaluate a specific score, that can be used as alternative
        to the `clf` one, having the same signature.
        It is useful to use in the case of :mod:`PrimalCore.models.pipeline`
    """
    def __init__(self,clf,par_grid_dict=None,add_scorer=None,name=None):

        super(Classifier,self).__init__(clf,par_grid_dict=par_grid_dict,add_scorer=add_scorer,name=name)



    @classmethod
    def LDAClassifier(cls, ):
        tol_range = np.logspace(-10, 0, 100)
        param_grid = {'tol': tol_range}

        n_components_range = np.arange(1, 100, 10)
        param_grid['n_components'] = n_components_range

        return cls(LDA(), par_grid_dict=param_grid)

    @classmethod
    def RFCClassifier(cls, ):
        n_estimators_range = np.arange(10, 260, 30)
        param_grid = {'n_estimators': n_estimators_range}

        return cls(RFC(n_estimators=100), par_grid_dict=param_grid)

    @classmethod
    def GBClassifier(cls, ):
        n_estimators_range = np.arange(50, 500, 50)
        param_grid = {'n_estimators': n_estimators_range}

        # learning_rate_range=np.array([0.1])
        # param_grid['learning_rate']=learning_rate_range

        return cls(GB(learning_rate=0.1), par_grid_dict=param_grid)

    # MT: add inputs: n_estimators parameter; base estimator parameters
    @classmethod
    def ABClassifier(cls, ):
        n_estimators_range = np.arange(10, 260, 30)
        param_grid = {'n_estimators': n_estimators_range}

        return cls(AB(n_estimators=100), par_grid_dict=param_grid)

    @classmethod
    def SVLClassifier(cls, ):
        C_range = np.logspace(-2, 10, 13)
        param_grid = {'C': C_range}
        svc = svm.LinearSVC()

        return cls(svc, par_grid_dict=param_grid)

    @classmethod
    def SVKClassifier(cls, ):
        C_range = np.logspace(-2, 10, 13)
        param_grid = {'C': C_range}
        gamma_range = np.logspace(-9, 3, 13)
        param_grid['gamma'] = gamma_range

        return cls(svm.SVC(kernel='rbf'), par_grid_dict=param_grid)

    # NEW
    # MT: add parameters: n_estimators, max_depth, max_features, min_samples_split
    @classmethod
    def RFCClassifierPara(cls, n_estimators=100, max_depth=None, max_features='auto', min_samples_split=2):
        n_estimators_range = np.arange(10, 260, 30)
        param_grid = {'n_estimators': n_estimators_range}

        return cls(RFC(n_estimators=n_estimators,
                       max_depth=max_depth,
                       max_features=max_features,
                       min_samples_split=min_samples_split),
                   par_grid_dict=param_grid)

    # MT: add inputs: n_estimators parameter; base estimator parameters
    @classmethod
    def ABClassifierPara(cls, n_estimators=100, max_depth=None, max_features=None, min_samples_split=2):
        n_estimators_range = np.arange(10, 260, 30)
        param_grid = {'n_estimators': n_estimators_range}

        ABclf = AB(base_estimator=DecisionTreeClassifier(max_depth=max_depth,
                                                         max_features=max_features,
                                                         min_samples_split=min_samples_split),
                   n_estimators=n_estimators)
        return cls(ABclf, par_grid_dict=param_grid)
