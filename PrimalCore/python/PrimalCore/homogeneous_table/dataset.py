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
This module provides the implementation of the :class:`MLDataSet` class, a class designed to handle heterogeneous tables.


Classes and Inheritance Structure
----------------------------------------------
.. inheritance-diagram:: MLDataSet



Summary
---------
.. autosummary:: MLDataSet



Module API
----------
"""


from __future__ import absolute_import, division, print_function

from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object, map, zip)


# Standard library
# eg copy
# absolute import rg:from copy import deepcopy
import  copy

# Dependencies
# eg numpy 
# absolute import eg: import numpy as np
import  numpy as np

# Project
# relative import eg: from .mod import f
from ..heterogeneous_table.tools import build_names_list
from ..heterogeneous_table.table import Table
from .tools import  *
__author__ = "Andrea Tramacere"


class MLDataSet(object):
    """
    This class contains the features 2-dim array together with
    the target array, and the weight array



    Parameters
    ----------
    features : 2dim array
        each column represents a feature, each row represents an entry

    features_names : list of strings, optional
        a list of string with the name of each features

    target_array : 1dim array, optional
        the target used for training/classification, size= number of rows in features

    target_bins : int, optional
        if the target is not a label, or it is a continuous variable, the stratified sampling
        might fail. Setting target_bins, a binning is performed with bins equal to target_bins.
        Each entry will have label given by the bin ID

    target_binning : str, optional, default='linear'
        The binning strategy: 'linear' or 'log'

    weight_array : 1dim array, optional
        the weight array, used for the training,  size= number of rows in features

    features_original_entry_ID  : 1dim array of int, optional
        the original entry ID of the entries



    """
    def __init__(self,features,\
                 features_names=None,\
                 target_array=None, \
                 target_bins=None, \
                 target_binning='linear',\
                 weight_array=None, \
                 columns_mask=None,
                 rows_mask=None,
                 features_original_entry_ID=None,
                 catalog_file=None):
        """


        """
        self._features=features

        if features_names is not None:
            self._features_names=features_names
        else:
            self._features_names=['F_%d'%ID for ID in range(features.shape[1])]


        if target_array is not None:
            self._target_array=np.copy(target_array)
        else:
            self._target_array=None

        self.target_bins=target_bins

        if target_binning is not None:
            if target_binning not in ['linear','log']:
                raise RuntimeError('target_binning possible choices linear or log, found' % target_binning)

        self.target_binning=target_binning

        if weight_array is not None:
            self._weight_array=np.copy(weight_array)
        else:
            self._weight_array=None

        self._features_original_entry_ID=features_original_entry_ID
        self._stratifying_array=None

        self.catalog_file=catalog_file

        self.columns_mask=columns_mask
        self.rows_mask=rows_mask

        print("| features built")
        print("| Rows,Cols",self.features_N_rows,self.features_N_cols)


    #------------------------------------
    # Properties
    #------------------------------------
    @property
    def features(self):
        """
        getter

        Returns
        -------
        `_features`: list
            the features `numpy.darray`, read-only.

        """
        return self._features[self.rows_mask][:,self.columns_mask]

    @property
    def columns_mask(self):
        """
        getter/setter

        Returns
        -------
        `_columns_mask` : 1dim bool array
            the column mask


        setter

        Parameters
        ----------
        mask :  1dim bool array
            sets the column mask
        """
        return self._columns_mask

    @columns_mask.setter
    def columns_mask(self, mask):
        if mask is not None:
            check_array_is_1dim(mask)
            check_same_size(mask,self.features_N_cols)
        else:
            mask = np.ones(self.features_N_cols,dtype=np.bool)
        self._columns_mask=mask

    @property
    def rows_mask(self):
        """
        getter/setter

        Returns
        -------
        `_rows_mask` : 1dim bool array
            the rows mask


        setter

        Parameters
        ----------
        mask :  1dim bool array
            sets the row mask
        """
        return self._rows_mask

    @rows_mask.setter
    def rows_mask(self, mask):
        if  mask is not None:
            check_array_is_1dim(mask)
            check_same_size(mask, self.features_N_rows)
        else:
            mask=np.ones(self.features_N_rows,dtype=np.bool)
        self._rows_mask= mask


    @property
    def features_names(self):
        """
        getter/setter

        Returns
        -------
        `_features_names` : list,  the features names list


        setter

        Parameters
        ----------
        names : list
            sets the  features names list
        """
        if np.issubdtype(self.columns_mask.dtype,np.bool):
            ids=np.where(self.columns_mask==True)[0]
        else:
            ids=self.columns_mask
        return [self._features_names[i] for i in ids]

    @features_names.setter
    def features_names(self,names):
        check_same_size(len(names),self.features_N_cols)
        self._features_names=names



    @property
    def target_array(self):
        """
        getter/setter

        Returns
        -------
        _target_array : `numpy.ndarray`
            the target array


        setter

        Parameters
        ----------
        array : `numpy.ndarray`
           the new target array

        """
        return self._target_array[self.rows_mask]

    @target_array.setter
    def target_array(self,array):
        check_array_is_1dim(array)
        check_same_size(array.size,self.features_N_rows)
        self._target_array=np.copy(array)



    @property
    def stratifying_array(self):
        """
        getter

        Returns
        -------
         _stratifying_array : `numpy.ndarray`
             the stratifying array, obtained by binning the target_array
        """
        if self.target_bins is None:
            return self.target_array[self.rows_mask]

        if self._stratifying_array is not None:
            return self._stratifying_array[self.rows_mask]
        else:
            self._update_stratifying_array(binning=self.target_binning)
            return self._stratifying_array[self.rows_mask]

    def _update_stratifying_array(self,binning=None):
        """
        Updates the value of :member:`PrimalCore.homogeneous_table.dataset._stratifying_array`

        Parameters
        ----------
        binning

        Returns
        -------

        """
        if binning is None:
            binning=self.target_binning

        if self.target_bins is None:
            self._stratifying_array= self._target_array

        else:
            if binning == 'linear':
                x1 = self._target_array.min()
                x2 = self._target_array.max()
                bins = np.linspace(x1, x2, self.target_bins)
            elif binning == 'log':
                x1 = np.log10(self._target_array.min())
                x2 = np.log10(self._target_array.max())
                bins = np.logspace(x1, x2, self.target_bins)

            self._stratifying_array= np.digitize(self._target_array, bins, right=True)


    @property
    def weight_array(self):
        """
        getter/setter

        Returns
        -------
        _weight_array : `numpy.ndarray`
            the weight array


        setter

        Parameters
        ----------
        array : `numpy.ndarray`
            the weight array
        """
        return self._weight_array[self.rows_mask]

    @weight_array.setter
    def weight_array(self,array):
        if array is not None:
            check_array_is_1dim(array)
            check_same_size(array.size,self.features_N_rows)
            self._weight_array=np.copy(array)
        else:
            self._weight_array=None

    @property
    def features_original_entry_ID(self):
        """
        getter/setter

        Returns
        -------
        _features_original_entry_ID : `numpy.ndarray`
            the original entry ID


        setter

        Parameters
        ----------
        array : `numpy.ndarray`
            the original entry ID
        """
        return self._features_original_entry_ID[self.rows_mask]

    @features_original_entry_ID.setter
    def features_original_entry_ID(self,array):
        check_array_is_1dim(array)
        check_same_size(array.size,self.features_N_rows)
        self._features_original_entry_ID=np.copy(array)


    @property
    def features_N_rows(self):
        """
        getter

        Returns
        -------
        ._features.shape[0]: int
            the number or rows of `_features`
        """
        return  self._features.shape[0]


    @property
    def features_N_cols(self):
        """
        getter

        Returns
        -------
        ._features.shape[1]: int
            the number or columns of `_features`
        """
        return  self._features.shape[1]

    def set_feature(self,feature_name,values):
        """
        Change the name of a feature

        Parameters
        ----------
        feature_name : string

        values
        """
        check_array_is_1dim(values)
        check_same_size(values.size, self.features_N_rows)
        if feature_name not in self._features_names:
            raise RuntimeError('feature name  %s not existing',feature_name)

        for ID,name in enumerate(self._features_names):
                if name==feature_name:
                    self._features[:,ID]=values


    def rename_feature(self,old_name,new_name):
        """
        Change the name of a feature

        Parameters
        ----------
        old_name : string

        new_name : string
        """
        if old_name not in self.features_names:
            raise  RuntimeError('name %s not present in _features_names')
        else:
            self._features_names=[new_name if x==old_name else x for x in self._features_names]
    #------------------------------------
    # factories
    #------------------------------------
    @classmethod
    def new_from_fits_file(cls,
                           file,
                           fits_ext=0,
                           **argw):
        """
        Class method to build a MLDataSet from a fitsfile object

        Parameters
        ----------
        file : basestring
         the fits file

        fits_ext : int (default=0)
            the fits extension corresponding to the table

        argw :
            the same argw in :func:`~MLDataSet.new_from_table`

        Returns
        -------

        """
        table=Table.from_fits_file(file,fits_ext=fits_ext)
        return MLDataSet.new_from_table(table,**argw)

    @classmethod
    def new_from_table(cls,table,\
                       target_array=None,\
                       weight_array=None,\
                       target_col_name=None,\
                       target_col_num=None,\
                       target_bins=None, \
                       target_binning='linear',\
                       original_entry_ID_col_name='__original_entry_ID__',\
                       use_col_names_list=[],\
                       skip_col_names_list=[],\
                       use_col_num_list=[],\
                       skip_col_num_list=[],\
                       regex=True,\
                       rows_IDs_use_list=[],\
                       rows_IDs_skip_list=[],
                       catalog_file=None):

        """
        Class method to build a MLDataSet from :class:`PrimalCore.heterogeneous_table.table.Table` object

        Parameters
        ----------
        table :  :class:`PrimalCore.heterogeneous_table.table.Table` object

        target_array : 1dim array, optional
            the target used for training/classification, size= number of rows in features

        weight_array : 1dim array, optional
            the weight array, used for the training,  size= number of rows in features

        target_bins : int, optional
            if the target is not a label, or it is a contineous variable, the stratified sampling m
            might fail. Setting target_bins, a binning is performed with bins equal to target_bins.
            Each entry will have label given by the bin ID

        target_binning : str, optional, default='linear'
            The binning strategy: 'linear' or 'log'

        target_col_num : int, optional
            the ID of the column in the Table, tu be used as target

        original_entry_ID_col_name : string, optional
            as default the '__original_entry_ID__' will be used

        use_col_names_list : list of strings, optional
            the list fo column names to select. If regex==True, all the columns names matching any
            of the regular expression will be used

        skip_col_names_list :list of strings, optional
            the list fo column names to discard. If regex==True, all the columns names matching any
            of the regular expression will be discarded

        use_col_num_list : list of int
         the list on columns IDs to use

        skip_col_num_list : list of int
         the list on columns IDs to discard

        regex : boolean, default=True
            if True, regular expression are used for `use_col_names_list` and `skip_col_names_list`

        rows_IDs_use_list : list of int, or 1dim array of int
            the rows IDs to use

        rows_IDs_skip_list  : list of int, or 1dim array of int
            the rows IDs to discard


        catalog_file : string

        Returns
        -------

        """

        print("| building features")
        cols_ID_use_list=range(table.N_cols)
        names_list=table.column_names

        if target_col_num is not None:
            cols_ID_use_list.remove(target_col_num)

        if target_col_name is not None:
            names_list.remove(target_col_name)

        #column filtering
        if skip_col_num_list!=[] and skip_col_num_list is not None:
            cols_ID_use_list=[ID for ID in range(table.N_cols) if ID not in skip_col_num_list]
            names_list=names_list[cols_ID_use_list]

        if use_col_num_list!=[] and use_col_num_list is not None:
            cols_ID_use_list=use_col_num_list
            names_list=names_list[cols_ID_use_list]




        if use_col_names_list!=[] and use_col_names_list is not None:
            names_list=build_names_list(use_col_names_list,names_list,regex=regex,matching=True)

        skip_col_names_list.append(original_entry_ID_col_name)
        if skip_col_names_list!=[] and skip_col_names_list is not None:
            names_list=build_names_list(skip_col_names_list,names_list,regex=regex,matching=False)

        features_names=names_list
        features=np.vstack([table.data[item] for item in names_list]).T
        features_original_entry_ID=table.data[original_entry_ID_col_name]




        if target_col_name is not None:
            if target_col_name in features_names:
                raise RuntimeError("features  can not be used as target")
            else:
                target_array=table.data[target_col_name]

        if target_col_num is not None:
            if target_col_num in cols_ID_use_list:
                raise RuntimeError("features  can not be used as target")
            else:
                target_array=table.data[:,target_col_num]


        #row filtering
        if rows_IDs_use_list!=[] and    rows_IDs_use_list!=None:
            features=features[rows_IDs_use_list]
            features_original_entry_ID=features_original_entry_ID[rows_IDs_use_list]
            if target_array is not None:
                target_array=target_array[rows_IDs_use_list]
            if weight_array is not None:
                weight_array=weight_array[rows_IDs_use_list]

        if rows_IDs_skip_list!=[] and    rows_IDs_skip_list!=None:
            use_list=[ID for ID in range(table.N_rows) if ID not in rows_IDs_skip_list]
            features=features[use_list]
            features_original_entry_ID=features_original_entry_ID[use_list]
            if target_array is not None:
                target_array=target_array[use_list]
            if weight_array is not None:
                weight_array=weight_array[use_list]





        return MLDataSet(features,\
                         features_names=features_names, \
                         target_bins=target_bins, \
                         target_binning=target_binning, \
                         target_array=target_array,\
                         weight_array=weight_array,\
                         features_original_entry_ID=features_original_entry_ID,
                         catalog_file=catalog_file)







    #------------------------------------
    # getters
    #------------------------------------
    def get_feature_by_name(self,feature_name):
        """
        Returns the values of the features corresponding to the name

        Parameters
        ----------
        feature_name : string
            the name of the feature

        Returns
        -------
        features values : `numpy.ndarray` 1dim
            the feature values
        """
        if feature_name not in self.features_names:
            raise RuntimeError('feature name  %s not existing',feature_name)
        for ID,name in enumerate(self.features_names):
                if name==feature_name:
                    return self.features[:,ID]



    #------------------------------------
    # checkers
    #------------------------------------
    def _check_shapes(self):

        if self._features.ndim!=2:
            raise RuntimeError("features array has to be a 2dim array")

        if self._features_names is not None:
            if self._features.shape[0]!=len(self._features_names):
                raise RuntimeError("features and features names have different size")

        if self._target_array is not None:
            if self._target_array.ndim!=1:
                raise RuntimeError("target array has to 1dim array")
            if self._features.shape[0]!=self._target_array.size:
                raise RuntimeError("features and target names have different size")

        if self._weight_array is not None:
            if self._target_array.ndim!=1:
                raise RuntimeError("weight array has to 1dim array")
            if self._features.shape[0]!=self._weight_array.size:
                raise RuntimeError("features and weight names have different size")

        if self._features_original_entry_ID is not None:
            if self._features.shape[0]!=len(self._features_original_entry_ID):
                raise RuntimeError("features and features_original_entry_ID  have different size")


    @staticmethod
    def _check_is_MLDataSett(test,raise_execption=False):
        if raise_execption==False:
            return isinstance(test,MLDataSet)

        else:
            if isinstance(test,MLDataSet):
                return True
            else:
                raise RuntimeError('dataset is not a MLDataSet object')