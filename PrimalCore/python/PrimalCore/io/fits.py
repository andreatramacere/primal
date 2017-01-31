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
This module provides the implementation basic functions fo I/O with FITS files.





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
try:
    import  pyfits as pf
except:
    try:
        from astropy.io import fits as pf
    except ImportError:
        raise ImportError('')

import  numpy as np

# Project
# relative import eg: from .mod import f



def read_data(input_file,fits_ext=0,header=True):
    """
    reads the data and the header  from an extension of a fits file

    Parameters
    ----------
    input_file : file phat,file object, or file like object
    fits_ext : extension of the fits file storing the data

    Returns
    -------
    d : np structured array
    h : fits header, if `header` parameter is True
    """
    d,h=pf.getdata(input_file, ext=fits_ext,header=header)

    return np.array(d),h

def write_data(filename,data,extra_header_tuple_list=None,clobber=True):
    """
    write a :class:`numpy.ndarray` to a fits file


    Parameters
    ----------
    data : :class:`numpy.ndarray`
    filename : string
        filename

    Returns
    -------

    """
    if extra_header_tuple_list is None:
        pf.writeto(filename, data, clobber=clobber)
    else:
        hdu=pf.convenience._makehdu(data,None)
        hdu.header.extend(extra_header_tuple_list)
        hdu.writeto(filename,clobber=clobber)



