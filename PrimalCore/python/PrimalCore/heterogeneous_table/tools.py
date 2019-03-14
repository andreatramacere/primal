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
This module provides the implementation of tools functions for the  :class:`~Table` class.


Summary
---------
.. autosummary::
   :toctree:


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
import fnmatch
import re
# Dependencies
# eg numpy 
# absolute import eg: import numpy as np
import  numpy as np

# Project
# relative import eg: from .mod import f





def check_array_type( data):
    """

    Parameters
    ----------
    data : array


    Returns
    -------
    is_2dimarray : bool
    is_struct_array : bool
    is_record_array : bool
    """

    is_2dimarray = False
    is_struct_array = False
    is_record_array = False

    if data.dtype.type == np.void and data.ndim == 1 and  data.dtype.names is not None:
        is_struct_array = True

    if data.dtype.type == np.record and data.ndim == 1:
        is_record_array = True

    if data.ndim == 2 and is_record_array == False and is_struct_array == False:
        is_2dimarray = True


    return is_2dimarray, is_struct_array,is_record_array


def build_names_list(names_list,column_names_list,regex=True,matching=True):
    """
    Returns a list of names among those provided in `names_list` matching the names in `column_names_list`
        * If `matching` is True, then all the names in `column_names_list`  that matches at least one  name names_list are returned in the output list
        * If `matching` is False, then all the names in `column_names_list`  that do not match any name in names_list are returned in the output list
        * If `regex` is True, then the matching is done according tu usual regular expression syntax



    Parameters
    ----------
    names_list : list of strings
        the list of names/regexp to match against the `column_names_list`
    column_names_list : list of strings
        the list of column names
    regex : bool
    skip  : bool

    Returns
    -------
    selected_names_list : list of strings
        the list of selected column names

    """

    if type(names_list) != list:
        names_list = list([names_list])

    if matching==True:
        selected_names_list=[]
    else:
        selected_names_list=column_names_list[:]

    if regex==True:
        for use_name in names_list:
            regex = fnmatch.translate(use_name)
            matches = [name for name in column_names_list if re.match(regex, name)]
            #print ('matches',regex,matches)
            for match in matches:
                if matching==True:
                    if match not in selected_names_list:
                        selected_names_list.append(match)
                else:
                    if match  in selected_names_list:
                        #print ("removing",match)
                        selected_names_list.remove(match)
    else:
        for ID,name in enumerate(column_names_list):
            if name  in names_list:
                if matching==True:
                    selected_names_list.append(name)
                else :
                    selected_names_list.remove(name)

    return selected_names_list


