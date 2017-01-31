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
   handle_missing_values
   std_features
   dataset_train_test_split
   drop_bad_values
   drop_nan_inf



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
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler
from  sklearn.model_selection import StratifiedShuffleSplit,ShuffleSplit



# Project
# relative import eg: from .mod import f

from ..homogeneous_table.dataset_handler import *



#------------------------------------
# sklearn based
#------------------------------------
@check_dataset_decorate
def handle_missing_values(dataset, missing_values='NaN', strategy='mean', axis=0):
    """
    Replace missing values using the :class:`sklearn.preprocessing.Imputer class`

    Parameters
    ----------
    missing_values
    strategy
    axis

    Returns
    -------

    """

    imp = Imputer(missing_values=missing_values, strategy=strategy, axis=axis)
    dataset._features = imp.fit_transform(dataset._features)

@check_dataset_decorate
def std_features(dataset, test=None):
    """
    standardize features using the :class:`sklearn.preprocessing.data.StandardScaler`
    Parameters
    ----------
    dataset
    test

    Returns
    -------

    """
    stdsc = StandardScaler()
    dataset._features = stdsc.fit_transform(dataset._features)


@check_dataset_decorate
def dataset_train_test_split(dataset,train_ratio=None,stratify=True,random_state=None):
    """

    Splits a dataset in train and  test using StratifiedShuffleSplit or ShuffleSplit from `sklearn.model_selection` package

    Parameters
    ----------
    dataset :  :class:`.dataset.MLDataSet` object

    train_ratio : float
        the fraction of split for the training set

    stratify : bool
        if stratify==True, then ShuffleSplit is used
        if stratify==False, then StratifiedShuffleSplit

    random_state=  int or RandomState
        Pseudo-random number generator state used for random sampling.

    Returns
    -------
    train_dataset :  :class:`.dataset.MLDataSet` object
    test_dataset :  :class:`.dataset.MLDataSet` object
    """

    N_split_train = np.int(dataset.features_N_rows * train_ratio)

    if N_split_train == dataset.features_N_rows or N_split_train == 0:
        raise RuntimeError("Splitting ratio produced train set size or test set size ==0")

    if stratify ==True :
        gen = StratifiedShuffleSplit(n_splits=1,test_size=1.0-train_ratio,random_state=random_state).split(dataset.features,dataset.stratifying_array)
    else:
        gen = ShuffleSplit(n_splits=1,test_size=1.0-train_ratio,random_state=random_state).split(dataset.features)

    train_IDs, test_IDs=gen.next()
    train_dataset=new_from_rows(dataset,train_IDs)
    test_dataset=new_from_rows(dataset,test_IDs)

    return train_dataset,test_dataset





#------------------------------------
# cleaning
#------------------------------------
@check_dataset_decorate
def drop_bad_values(dataset, bad_value):
    """
    Removes bad values.

    Removes a whole column if all the entries have a bad_value
    Removes a row if any of the entry in the row has a bad_value


    Parameters
    ----------
    dataset :  :class:`.dataset.MLDataSet` object
    bad_value :

    Returns
    -------

    """



    print("| features cleaning for bad_value=", bad_value)
    print("| features initial Rows,Cols=", dataset.features_N_rows, dataset.features_N_cols)
    # removes a whole column is all the elements in the are
    # all== inf or
    # all== nan or
    # all== inf or nan
    black_list = []
    use_IDs_list = np.arange(dataset.features.shape[1])
    for ID, name in enumerate(dataset._features_names):

        bad_column = ~np.all(dataset.features[:, ID] == bad_value)

        if bad_column is True:
            use_IDs_list.remove(ID)
            black_list.append(name)

    print("| removed columns", black_list)

    drop_features(dataset,black_list)

    # removes a row if any of the entry in the row is == bad_value
    masked = np.zeros(dataset.features_N_rows, dtype=np.bool)
    for ID in xrange(dataset.features_N_rows):
        masked[ID] = np.any(dataset.features[ID] == bad_value)
    print(dataset.features[masked])
    keep_rows(dataset, ~masked)
    print("|removed rows", np.sum(masked),masked.shape)
    print("| features cleaned Rows,Cols=", dataset.features_N_rows, dataset.features_N_cols)
    print("")

@check_dataset_decorate
def drop_nan_inf(dataset):
    """
    Removes a whole column if all the entries in the columns are NaN or Inf
    Removes a row if  any of the entry in the row are NaN or Inf

    Parameters
    ----------
    dataset :  :class:`.dataset.MLDataSet` object

    Returns
    -------

    """

    print("| features cleaning for nan/inf")
    print("| features initial Rows,Cols=", dataset.features_N_rows, dataset.features_N_cols)

    # removes a whole column is all the elements in the are
    # all== inf or
    # all== nan or
    # all== inf or nan
    black_list = []
    for ID, name in enumerate(dataset._features_names):

        # we skip strings

        bad_column = ~np.all(np.logical_or(np.isnan(dataset.features[:, ID]), np.isinf(dataset.features[:, ID])))

        if bad_column is True:

            black_list.append(name)
    drop_features(dataset,black_list)
    print("|removed columns", black_list)

    # removes a row if any of the entry in the row is inf or nan
    masked = np.zeros(dataset.features_N_rows, dtype=np.bool)
    for ID in xrange(dataset.features.shape[0]):
        masked[ID] = np.any(np.isinf(dataset.features[ID])) or np.any(np.isnan(dataset.features[ID]))
    keep_rows(dataset,~masked)
    print("|removed rows", np.sum(masked))
    print("| features cleaned Rows,Cols=", dataset.features_N_rows, dataset.features_N_cols)
    print("")


