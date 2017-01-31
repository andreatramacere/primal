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
This module provides a factory for  the :class:`.table.Table` to build objects from
FITS or ascii filse, and to save the content of the :class:`.table.Table` to a fits file

Summary
---------
.. autosummary::
   build_table_from_fits_file

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
from ..io.fits import read_data

# Project
# relative import eg: from .mod import f
from .table import  Table


__author__ = "Andrea Tramacere"

# Constructors
def build_table_from_fits_file(input_file, black_listed_col_ids=None, black_listed_col_names=None, fits_ext=0):
    """
    Class factory using as input the table stored into the extension of a FITS file.

    Parameters
    ----------
    input_file : string
        input file path
    black_listed_col_ids : list of int
        list of column to skip
    black_listed_col_names : list of strings
        list of the names of the columns to skip
    fits_ext : int
        the extension of the fits file storing the table data

    Returns
    -------

    """
    data,h = read_data(input_file,fits_ext=fits_ext)
    return Table(data, black_listed_col_ids=black_listed_col_ids, black_listed_col_names=black_listed_col_names)


def from_ascii_file():
    pass