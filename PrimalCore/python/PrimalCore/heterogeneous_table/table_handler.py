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
This module provides the implementation of handling functions for the  :class:`~Table` class.



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
from numpy.lib import recfunctions
import  numpy as np

# Project
# relative import eg: from .mod import f
from .table import Table




def tables_merge_rows(tab1,tab2,update_original_entry_ID=False):
    """
    merges to Tables, rows wise

    .. WARNING::
        merging Tables might impact the original_entry_ID

    Parameters
    ----------
    tab1 :  :class:`Table` object
    tab2 :  :class:`Table` object
    update_original_entry_ID

    Returns
    -------
    table :class:`Table` object
    """
    for tab in [tab1,tab1]:
        if Table._check_is_Table(tab):
            pass
        else:
            raise RuntimeError('tab1 or tab2 are not both DataSetBase objects')
    return Table(data=np.concatenate((tab1.data,tab2.data)),store_entry_ID=update_original_entry_ID)


def tables_merge_columns(tab1,tab2):
    """
    merges to Tables, columns wise

    Parameters
    ----------
    tab1 : :class:`Table` object
    tab2 : :class:`Table` object

    Returns
    -------
    table :class:`Table` object
    """
    for tab in [tab1,tab1]:
        if Table._check_is_Table(tab):
            pass
        else:
            raise RuntimeError('tab1 or tab2 are not both DataSetBase objects')

    return Table(data=recfunctions.merge_arrays((tab1.data,tab2.data),usemask=False))


