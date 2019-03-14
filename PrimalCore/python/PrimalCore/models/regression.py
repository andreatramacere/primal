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



Classes and Inheritance Structure
----------------------------------------------
.. inheritance-diagram::
    Regressor

Summary
---------
.. autosummary::
   Regressor

Module API
----------


.. _sklearn: http://scikit-learn.org/stable/documentation.html
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

from sklearn.ensemble import GradientBoostingRegressor,RandomForestRegressor,AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor

from sklearn.neighbors import KNeighborsRegressor,BallTree

from sklearn.svm import SVR
# Project
# relative import eg: from .mod import f
from .base import BaseModel




class Regressor(BaseModel):
    """
    This class implements a :class:`~PrimalCore.models.base.BaseModel` derived class
    specialized for  skelearn Regressors  :class:`sklearn.base.RegressorMixin`

    It  implements  class methods to build some predefined Regressors`

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

        super(Regressor,self).__init__(clf,par_grid_dict=par_grid_dict,add_scorer=add_scorer,name=name)

    @classmethod
    def RFRegressor(cls, n_estimators=100,name='random_forest'):
        """
        A class factory wrapping  :class:`~sklearn.ensemble.RandomForestRegressor`

        Parameters
        ----------
        n_estimators : int
            number of estimators in  :class:`~sklearn.ensemble.RandomForestRegressor`

        Returns
        -------
        cls : :class:`Regressor` object
        """
        n_estimators_range = np.arange(10, 260, 30)
        param_grid = {'n_estimators': n_estimators_range}

        return cls(RandomForestRegressor(n_estimators=n_estimators), par_grid_dict=param_grid,name=name)

    @classmethod
    def GBRegressor(cls, learning_rate=0.1,n_estimators=100,name='gradient_boosting'):
        """
        A class factory wrapping  :class:`~sklearn.ensemble.GradientBoostingRegressor`

        Parameters
        ----------
        n_estimators : int
            number of estimators in  :class:`~sklearn.ensemble.GradientBoostingRegressor`

        learning_rate : float
            the learning_rate parameter in the  :class:`~sklearn.ensemble.GradientBoostingRegressor`


        Returns
        -------
        cls : :class:`Regressor` object

        """
        n_estimators_range = np.arange(50, 500, 50)
        param_grid = {'n_estimators': n_estimators_range}

        return cls(GradientBoostingRegressor(n_estimators=n_estimators,
                                             learning_rate=learning_rate,
                                             loss='huber',
                                             alpha=0.01,
                                             subsample=0.8,
                                             min_samples_leaf=10,
                                             min_samples_split=10),par_grid_dict=param_grid,name=name)

    @classmethod
    def ABRegressor(cls, n_estimators=100,name='ada_boost'):
        """
        A class factory wrapping  :class:`~sklearn.ensemble.AdaBoostRegressor`

        Parameters
        ----------
        n_estimators : int
            number of estimators in  :class:`~sklearn.ensemble.AdaBoostRegressor`

        Returns
        -------
        cls : :class:`Regressor` object

        """
        n_estimators_range = np.arange(10, 260, 30)
        param_grid = {'n_estimators': n_estimators_range}
        return cls(AdaBoostRegressor(DecisionTreeRegressor(),n_estimators=n_estimators), par_grid_dict=param_grid,name=name)

    @classmethod
    def KNRegressor(cls, n_neighbors=5,name=''):
        """
        A class factory wrapping  :class:`~sklearn.neighbors.KNeighborsRegressor`

        Parameters
        ----------
        n_neighbors : int
            number of neighbors in  :class:`~sklearn.neighbors.KNeighborsRegressor`

        Returns
        -------
        cls : :class:`Regressor` object

        """

        n_estimators_range=np.linspace(1, 50, 20).astype(np.int32)
        param_grid = {'n_neighbors':n_estimators_range}
        clf=KNeighborsRegressor(n_neighbors=n_neighbors,weights='distance',algorithm='ball_tree',p=2,leaf_size=200)
        return cls(clf, par_grid_dict=param_grid,name='KN')

    @classmethod
    def SVKRegressor(cls,kernel= 'rbf'):
        """
        A class factory wrapping  :class:`~sklearn.svm.SVR`

        Parameters
        ----------
        kernel : string
            the kernel parameter in  :class:`~sklearn.svm.SVR`

        Returns
        -------
        cls : :class:`Regressor` object

        """


        C_range = np.logspace(-2, 10, 13)
        param_grid = {'C': C_range}
        gamma_range = np.logspace(-9, 3, 13)
        param_grid['gamma'] = gamma_range
        svc = SVR(kernel='rbf')


        return cls(svc, par_grid_dict=param_grid)
