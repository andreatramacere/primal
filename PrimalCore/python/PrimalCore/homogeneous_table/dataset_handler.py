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
This module provides the implementation of handling functions for  the :class:`MLDataSet` class`



Module API
----------
"""


from __future__ import absolute_import, division, print_function

from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object, map, zip)


# Standard library
# eg copy
# absolute import rg:from copy import deepcopy

# Dependencies
# eg numpy 
# absolute import eg: import numpy as np
import numpy as np
import decorator
import copy

# Project
# relative import eg: from .mod import f
from .dataset import MLDataSet
from .tools import *
from ..heterogeneous_table.tools import build_names_list

try:
    basestring
    str=basestring

except NameError:
    pass

__author__ = "Andrea Tramacere"


@decorator.decorator
def check_dataset_decorate(func,dataset,*args, **kwargs):
    MLDataSet._check_is_MLDataSett(dataset)
    return func(dataset,*args, **kwargs)


@decorator.decorator
def check_names_list_decorate(func,dataset,names,*args, **kwargs):
    if isinstance(names,str):
        feature_names_list=[names]

    elif type(names)==list:
        feature_names_list=names

    elif check_array_is_1dim(names):
        #this works both for array of boolan or
        #arrays of integerz
        IDs=np.arange(len(dataset._features_names))
        #IDs=IDs[names]

        feature_names_list=[dataset._features_names[ID] for ID in IDs]

    else:
        raise RuntimeError('features names is not compatible with str, list, or array')

    for name in feature_names_list:
        if isinstance(name, str):
            pass
        else:
            raise RuntimeError('features names is not compatible with str, list of strings, array of strings')

    return func(dataset,feature_names_list,*args, **kwargs)


#------------------------------------
# Factories
#------------------------------------
@check_dataset_decorate
def new_from_rows(dataset, selected):
    """
    Creates a new :class:`MLDataSet` from an existing one, by row selection

    Parameters
    ----------
    selected

    Returns
    -------

    """
    new = copy.deepcopy(dataset)
    keep_rows(new, selected)
    return new


#------------------------------------
# add/remove features columns-wise
#------------------------------------
@check_dataset_decorate
@check_names_list_decorate
def add_features(dataset,feature_names_list,features):
    """
    add features to an existing DataSet

     .. WARNING::
        adding features  will append True values to :attr:`.dataset.MLDataSet.columns_mask`

    Parameters
    ----------
    dataset : instance of :class:`.dataset.MLDataSet`
    feature_names_list : list of strings or string
    features : list of np.arrays or np.array

    Returns
    -------

    """

    if type(feature_names_list)!=list:
        feature_names_list=[feature_names_list]

    if check_array_is_1dim(features):
        features = np.reshape(features,(features.size, 1))
        if check_same_size(features.size, dataset.features_N_rows):
            pass
        else:
           raise RuntimeError('number of rows in features not equal to number of rows in data.features')

    if check_array_is_2dim(features):
        if check_same_size(features.shape[0], dataset.features_N_rows):
            pass
        else:
           raise RuntimeError('number of rows in features not equal to number of rows in data.features')

    if check_same_size(features.shape[1], len(feature_names_list)):
        pass
    else:
        raise RuntimeError('number of columns in features  not equal to number of items in feature_names_list')

    dataset._features = np.column_stack((dataset._features, features))
    dataset._features_names.extend  (feature_names_list)
    if dataset.columns_mask is not None:
        extra_size=len(dataset._features_names)-dataset.columns_mask.size
        dataset.columns_mask=np.append(dataset.columns_mask,np.ones(extra_size,dtype=np.bool))


@check_dataset_decorate
@check_names_list_decorate
def drop_features(dataset,removing_feature_names_list,regex=True):
    """
    drops all the features whose names match any element in the  removing_feature_names_list. If regex == True, the list of columns to remove
    is built by finding any column name in the cloumns_names of dataset that matches  the regex of any elements of
    removing_feature_names_list

    Parameters
    ----------
    dataset : instance of :class:`.dataset.MLDataSet`
    removing_feature_names_list : list of strings or string, or array of int or array of bools
    regex : bool
        flag to use regular expression

    Returns
    -------

    """
    _select_features(dataset, removing_feature_names_list, regex=True, remove=True)



@check_dataset_decorate
@check_names_list_decorate
def keep_features(dataset,keeping_feature_names_list,regex=True):
    """
    keeps all the features whose names match any element in keeping_feature_names_list. If regex == True, the list of columns to keep
    is built by finding any column name in the cloumns_names of dataset that matches  the regex of any elements of
    keeping_feature_names_list

    Parameters
    ----------
    dataset : instance of :class:`.dataset.MLDataSet`
    keeping_feature_names_list :  list of strings or string, or array of int or array of bools
    regex : bool
        flag to use regular expression

    Returns
    -------

    """

    _select_features(dataset, keeping_feature_names_list, regex=True, remove=False)



def _select_features(dataset,names_list,regex=True,remove=False):
    """

    Parameters
    ----------
    dataset : instance of :class:`.dataset.MLDataSet`
    names_list: list of strings or string, or array of int or array of bools
    regex : bool
        flag to use regular expression

    remove :bool
        if `True`, matching columns names removed, if `False`  matching columns names are kept

    Returns
    -------

    """
    if regex is True:
        removing_names_list=build_names_list(names_list,dataset._features_names,regex=regex,matching=remove)
    else :
        removing_names_list=[name for name in dataset._features_names if name not in names_list]

    for feature_name in removing_names_list:
        if feature_name not in dataset._features_names:
            raise RuntimeError('feature name not existing ')

    remove_ID_list = []

    print("| features initial Rows,Cols=", dataset.features_N_rows, dataset.features_N_cols)
    print("| removing features", removing_names_list)

    for ID, name in enumerate(dataset._features_names[:]):
        if name in removing_names_list:
            remove_ID_list.append(ID)
            dataset._features_names.remove(name)


    if remove_ID_list != []:
        dataset._features = np.delete(dataset._features, remove_ID_list, 1)

    if dataset.columns_mask is not None:
        dataset.columns_mask=np.delete(dataset.columns_mask, remove_ID_list,)
    print("| features final Rows,Cols=", dataset.features_N_rows, dataset.features_N_cols)
    print("")




#------------------------------------
# sorting columns
#------------------------------------
@check_dataset_decorate
def sort_feature_columns_position(dataset, id_array):
    """
    Sorts the columns position according to  id_array

    Parameters
    ----------
    dataset  :  :class:`.dataset.MLDataSet` object
    id_array : array of int

    Returns
    -------

    """
    if dataset._check_is_dataset(dataset):
        pass
    else:
        raise RuntimeError('dataset is not a MLDataSet object')

    dataset._features = dataset._features[:, id_array]
    if dataset._columns_mask is not None:
        dataset._columns_mask= dataset._columns_mask[id_array]

    dataset._set_features_names([dataset._features_names[id] for id in id_array])


#------------------------------------
# row-wise operations
#------------------------------------

@check_dataset_decorate
def keep_rows(dataset, selected):
    """
    keeps only the rows corresponding to the boolean array selected==True

    Parameters
    ----------
    dataset : instance of :class:`.dataset.MLDataSet`
    selected : 1d boolean array,or list, or 1d int array. same size of  :class:`.dataset.MLDataSet.features_N_rows`

    Returns
    -------

    """


    dataset._features = dataset._features[selected]

    if dataset._features_original_entry_ID is not None:
        dataset._features_original_entry_ID = dataset._features_original_entry_ID[selected]

    if dataset._target_array is not None:
        dataset.target_array = dataset._target_array[selected]

    if dataset._weight_array is not None:
        dataset.weight_array = dataset._weight_array[selected]

    if dataset._rows_mask is not None:
        dataset._rows_mask = dataset._rows_mask[selected]








#------------------------------------
# merging dataets
#------------------------------------
@check_dataset_decorate
def dataset_append(dataset1, dataset2):
    """
    Row-wise appending of dataset2 to dataset1
    Parameters
    ----------
    dataset1 : :class:`.dataset.MLDataSet` object
    dataset2 : :class:`.dataset.MLDataSet` object

    Returns
    -------

    """
    for dataset in [dataset1,dataset2]:
        if MLDataSet._check_is_DataSet(dataset):
            pass
        else:
            raise RuntimeError('dataset1 or dataset2 are not both DataSetBase objects')

    dataset1._features_array = np.row_stack((dataset1._features_array, dataset2._features_array))

    dataset1._target_array=_append_if_both_exist(dataset1.target_array, dataset2.target_array)
    dataset1._features_original_entry_ID = _append_if_both_exist(dataset1._features_original_entry_ID, dataset2._features_original_entry_ID)
    dataset1._weight_array = _append_if_both_exist(dataset1._weight_array, dataset2._weight_array)
    dataset1._columns_mask = _append_if_both_exist(dataset1._columns_mask, dataset2._columns_mask)
    dataset1._rows_mask = _append_if_both_exist(dataset1._rows_mask, dataset2._rows_mask)


def _append_if_both_exist(a,b):
    if a is not None and b is not None:
        return  np.append(a,b)
    else:
        return None

