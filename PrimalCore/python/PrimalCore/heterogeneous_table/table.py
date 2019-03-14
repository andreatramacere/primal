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
This module provides the implementation of the :class:`Table` class, a class designed to handle heterogeneous tables.


Classes and Inheritance Structure
----------------------------------------------
.. inheritance-diagram::
    Table



Summary
---------
.. autosummary::
    Table



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
from collections import Iterable

# Dependencies
# eg numpy 
# absolute import eg: import numpy as np
import numpy as np
from numpy.lib import recfunctions

# Project
# relative import eg: from .mod import f
from .tools import check_array_type,build_names_list
from ..io.fits import   read_data






class Table(object):



    """
    This class implements an heterogeneous table

    for useful examples see the :ref:`table_user_guide` section



    Parameters
    ----------
    data : 2-dim  numpy ndarrary, numpy struct array, numpy record array
        the array with the input data
    black_listed_col_ids: list of int
        the list of columns to skip from the input data
    black_listed_col_names: list of strings
        the list of column names to skip from the input data
    regex : bool
        if True, regex is applied to black_listed_col_names
    store_entry_ID : bool
        bool value, if True, then a column named original_entry_ID is storing the ordinal ID
        of the input data

    """

    def __init__(self,data, \
                 black_listed_col_ids=None, \
                 black_listed_col_names=None, \
                 regex=True, \
                 store_entry_ID=True):

        self._data_original_entry_ID_name='__original_entry_ID__'
        self._set(data, \
                  black_listed_col_ids=black_listed_col_ids, \
                  black_listed_col_names=black_listed_col_names,\
                  store_entry_ID=store_entry_ID,\
                  regex=regex)



    @property
    def dtype(self):
        """
        Returns the np.dtype of `data`
        """
        return  self._data.dtype

    @property
    def column_names(self):
        """
        Returns the list of names of the fields of `data`
        """
        return list(self.dtype.names)

    @property
    def N_rows(self):
        """
        Returns the number of rows in `data`
        """
        if self._data is not None:
            return  self._data.shape[0]
        else:
            return None

    @property
    def N_cols(self):
        """
        Returns the number of cols in `data`
        """
        if self._data is not None:
            return len(self._data.dtype.names)
        else:
            return None

    @property
    def original_entry_ID(self):
        """
        Returns the original_entry_ID of the rows in the input table
        """
        if self._data is not None:
            return self._data[self._data_original_entry_ID_name]
        else:
            return None

    @property
    def data(self):
        """
        Returns the np.recarray storing the table data
        """
        return self._data

    def _set(self,data,black_listed_col_ids=None,black_listed_col_names=None, regex=True,store_entry_ID=True):
        """
        Method to set the `_data` attribute

        Parameters
        ----------
        data :  2-dim  numpy ndarrary, numpy struct array, numpy record array
            the ndarray array storing the data of the table
        black_listed_col_ids: list of int
            the list of columns to skip from the input data
        black_listed_col_names: list of strings
            the list of column names to skip from the input data
        regex : bool
            if True, regex is applied to black_listed_col_names
        store_entry_ID : bool
            bool value, if True, then a column named original_entry_ID is storing the ordinal ID
            of the input data



        """

        is_2dimarray, is_struct_array, is_record_array = check_array_type(data)
        if is_2dimarray==False and is_struct_array ==False and is_record_array==False:
            try:
                debug_mess='data type %s  with shape=%s'%(type(data),np.shape(data))
            except:
                debug_mess=''

            raise RuntimeError("data has to be a 2dim numpy array, or a numpy record array, or a numpy structured array, found",debug_mess)


        if black_listed_col_ids is not None:
            if type(black_listed_col_ids)==list:
                black_listed_col_ids = list([black_listed_col_ids])

        if black_listed_col_names is not None:
            if type(black_listed_col_names)==list:
                black_listed_col_names = list([black_listed_col_names])

        if is_2dimarray == True:
            if black_listed_col_ids is not None:
                data = np.delete(data, black_listed_col_ids, 1)
            elif black_listed_col_names is not None:
                raise RuntimeError("input data has no column names, please provide black_listed_col_ids ")

            selected_cols = np.arange(data.shape[1])
            _data_dtype = [('col_%d' % ID, data.dtype) for ID, foo in enumerate(selected_cols)]
            self._data_names = list(self._data_dtype)
            self._data_array = np.zeros(data.shape[0], dtype=_data_dtype)

            for ID, col_name in enumerate(self._data_names):
                self._data[col_name] = data[:, ID]

        else:


            if black_listed_col_names is not None:
                names_list = build_names_list(black_listed_col_names,list(data.dtype.names), regex=regex, skip=True)
                self._data = recfunctions.drop_fields(data, names_list)
            elif black_listed_col_ids is not None:
                self._data = recfunctions.drop_fields(data, [data.dtype.names[black_listed_col_ids]])
            else:
                self._data = np.copy(data)


        if store_entry_ID==True:
            self._data = recfunctions.append_fields(self._data,  self._data_original_entry_ID_name,
                                                      np.arange(self._data.size), usemask=False)


        #self._data_N_rows = self._data_array.size
        #self._data_N_cols = len(self._data_names)

        print("| input data built")
        print("| data Rows,Cols", self.N_rows, self.N_cols)

    def print_entry(self,ID):
        for name in self.column_names:
            print (name,' =',self.data[ID][name])

    def add_columns(self, column_names, values_array, usemask=False, dtypes=None):
        """
        Add new fields to an existing array.

        The names of the fields are given with the `column_names` arguments,
        the corresponding values with the `values_array` arguments.

        Parameters
        ----------

        column_names : string, sequence
            String or sequence of strings corresponding to the names
            of the new fields.
        values_array : array or sequence of arrays
            Array or sequence of arrays storing the fields to add to the base.
        dtypes : sequence of datatypes
            Datatype or sequence of datatypes.
            If None, the datatypes are estimated from the `values_array`.

        Returns
        -------

        """
        self._data =recfunctions.append_fields(self._data, column_names, values_array, usemask=usemask,
                                          dtypes=dtypes)

    def drop_columns(self, drop_names_list,regex=True):
        """
        Drops the columns whose name match names in  drop_names_list, or regex in drop_names_list
        if regex==True

        Parameters
        ----------
        drop_names_list : string, sequence
            String or sequence of strings corresponding to the names
            of the fields to drop.
        regex : bool
            if True, regex is applied to black_listed_col_names
        Returns
        -------

        """
        drop_names_list = build_names_list(drop_names_list, self.column_names, regex=regex, matching=True)

        self._data= recfunctions.drop_fields(self._data, drop_names_list, usemask=False, asrecarray=False)

    def keep_columns(self, keep_names_list,regex=True):
        """
        Keeps only the columns whose name match names in  keep_names_list, or regex in keep_names_list
        if regex==True

        Parameters
        ----------
        column_names : string, sequence
            String or sequence of strings corresponding to the names
            of the fields to drop.
        regex : bool
            if True, regex is applied to black_listed_col_names
        Returns
        -------

        """
        drop_names_list = build_names_list(keep_names_list, self.column_names, regex=regex, matching=False)
        if self._data_original_entry_ID_name in drop_names_list:
            drop_names_list.remove(self._data_original_entry_ID_name)
        self._data= recfunctions.drop_fields(self._data, drop_names_list, usemask=False, asrecarray=False)


    def add_rows(self,values_array):
        """
        Add rows to the table

        .. WARNING::
            adding rows might impact the original_entry_ID

        Parameters
        ----------
        values_array : 2-dim  numpy ndarrary, numpy struct array, numpy record array
            the ndarray array storing the data to add to the table

        Returns
        -------

        """
        is_2dimarray, is_struct_array, is_record_array = check_array_type(values_array)
        if is_2dimarray==True:
            extra_rows=values_array.shape[0]
        elif is_struct_array == True:
            extra_rows=values_array.size
        elif is_record_array==True:
            extra_rows = values_array.size
        else:
            raise RuntimeError(
                "values_array has to be a 2dim numpy array, or a numpy record array, or a numpy structured array")

        self._data.resize(self.N_rows+extra_rows)
        for ID,d in enumerate(values_array):
            self._data[self.N_rows-extra_rows+ID]=tuple(d)




    #def drop_rows_by_indices(self,indices):
    #    """
    #    NOT IMPLEMENTED YET
    #    Returns
    #    -------
    #
    #    """
    #    #implement by using drop_rows
    #    pass

    def drop_rows(self, rows):
        """
        This method allows to drop rows passing a boolean 1d-array, a list, or an int 1dim np.array
        The entries with rows==True, or corresponding to the indices in rows, will be dropped

        Parameters
        ----------
        rows : boolean 1dim array, list, int 1dim np.array


        """
        print("| filtering data rows")
        print("| data initial Rows =", self.N_rows)
        self._data = self._data[~rows]
        print("| data filtered initial Rows =", self.N_rows)
        print("")

    def keep_rows(self, rows):
        """
        This method allows to keep rows passing a boolean 1d-array, a list, or an int 1dim np.array
        The entries with rows==True, or corresponding to the indices in rows, will be kept, the
        remaining will be dropped

        Parameters
        ----------
        rows : boolean 1dim array, list, int 1dim np.array

        """
        print("| filtering data rows")
        print("| data initial Rows,Cols=", self._data.shape)
        self._data = self._data[rows]
        print("| data filtered Rows,Cols=", self._data.shape)
        print("")

    # Constructors
    @classmethod
    def from_fits_file(cls, input_file, black_listed_col_ids=None, black_listed_col_names=None, fits_ext=0):
        """
        This function provides a method to read a data table from a FITS file, and reaturns a :class:`.Table` object

        Parameters
        ----------
        cls
        input_file : file path
            the input fits file
        id_column_name :
        id_column_num
        fits_ext

        Returns
        -------

        """
        data, h = read_data(input_file, fits_ext=fits_ext)
        return cls(data, black_listed_col_ids=black_listed_col_ids, black_listed_col_names=black_listed_col_names)

    @classmethod
    def from_ascii_file(cls):
        pass

    @staticmethod
    def _check_is_Table(test):
        return isinstance(test, Table)