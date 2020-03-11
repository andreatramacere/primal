"""
Overview
--------
   
general info about this module


Summary
---------
.. autosummary::
   Mag
   AsinhMag
   Color
   AsinhColor
   FluxRatio

Module API
----------
"""


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
                      
from numpy import log10, log, arcsinh

__author__ = "Andrea Tramacere"

# Standard library
# eg copy
# absolute import rg:from copy import deepcopy

# Dependencies
# eg numpy 
# absolute import eg: import numpy as np

# Project
# relative import eg: from .mod import f

      
class Mag(object):
    """
    Class to build a feature array of magnitude from a flux feature array

    Parameters
    ----------
    name : string
        name of the new feature
    band_1 : sting
        name of the input feature
    zero_point: float
        flux zero-point, by default 3.631E9 : AB mag for flux in mJy
    features : optional, :class:`PrimalCore.python.PrimalCore.homogeneous_table.dataset.MLDataSet` object

    """
    def __init__(self,name,band_1,zero_point=3.631E9,features=None):

        self.name=name
        self.band_1=band_1
        self.zero_point=zero_point

        if features is not None:
            self.values=self.build(features,self.band_1,self.zero_point)


    def build(self,features,band_1,zero_point):
        return -2.5*log10(features.get_feature_by_name(band_1)/zero_point) 


class AsinhMag(object):
    """
    Class to build a feature array of asinh modified magnitude from a flux feature array
    See Lupton 99 (https://arxiv.org/pdf/astro-ph/9903081.pdf)

    Parameters
    ----------
    name : string
        name of the new feature
    band_1 : sting
        name of the input feature
    b:float
        softening parameter
    zero_point: float
        flux zero-point, by default 3.631E9 : AB mag for flux in mJy

    features : optional, :class:`PrimalCore.python.PrimalCore.homogeneous_table.dataset.MLDataSet` object

    """
    def __init__(self,name,band_1,b,zero_point=3.631E9,features=None):

        self.name=name
        self.band_1=band_1
        self.b=b
        self.zero_point=zero_point

        if features is not None:
            self.values=self.build(features,self.band_1,self.b,self.zero_point)


    def build(self,features,band_1,b,zero_point):
        a = 1.0857362 # Pogson ratio = 2.5*log10(e)
        return -a*(arcsinh(features.get_feature_by_name(band_1)/(zero_point*2.0*b))+log(b)) 

class Color(object):
    """
    Class to build a feature array of  colors from two magnitudes features arrays

    Parameters
    ----------
    name : string
        name of the new feature
    band_1 : sting
        name of the input feature
    band_2 :
        name of the input feature
    features : optional, :class:`PrimalCore.python.PrimalCore.homogeneous_table.dataset.MLDataSet` object

    """
    def __init__(self,name,band_1,band_2,features=None):

        self.name=name
        self.band_1=band_1
        self.band_2=band_2

        if features is not None:
            self.values=self.build(features,self.band_1,self.band_2)


    def build(self,features,band_1,band_2):
        return features.get_feature_by_name(band_2)-features.get_feature_by_name(band_1)
        
class AsinhColor(object):
    """
    Class to build a feature array of Asinh colors from two flux features arrays
    See Lupton 99 (https://arxiv.org/pdf/astro-ph/9903081.pdf)

    Parameters
    ----------
    name : string
        name of the new feature
    band_1 : sting
        name of the input feature
    band_2 :
        name of the input feature
    b:float
        softening parameter
    zero_point: float
        flux zero-point, by default 3.631E9, : AB mag for flux in mJy
    features : optional, :class:`PrimalCore.python.PrimalCore.homogeneous_table.dataset.MLDataSet` object

    """
    def __init__(self,name,band_1,band_2,b,zero_point=3.631E9,features=None):

        self.name=name
        self.band_1=band_1
        self.band_2=band_2
        self.b=b
        self.zero_point=zero_point

        if features is not None:
            self.values=self.build(features,self.band_1,self.band_2,self.b,self.zero_point)


    def build(self,features,band_1,band_2,b,zero_point):
        a = 1.0857362 # Pogson ratio = 2.5*log10(e)
        return -a*(arcsinh(features.get_feature_by_name(band_2)/(zero_point*2.0*b)) - arcsinh(features.get_feature_by_name(band_1)/(zero_point*2.0*b))) 
        
        

class FluxRatio(object):
    """
    Class to build a flux feature array from  two fluxes features arrays

    Parameters
    ----------
    name : string
        name of the new feature
    band_1 : sting
        name of the input feature
    band_2 :
        name of the input feature
    features : optional, :class:`PrimalCore.python.PrimalCore.homogeneous_table.dataset.MLDataSet` object

    """
    def __init__(self,name,band_1,band_2,features=None):

        self.name=name
        self.band_1=band_1
        self.band_2=band_2

        if features is not None:
            self.values=self.build(features,self.band_1,self.band_2)


    def build(self,features,band_1,band_2):
        return features.get_feature_by_name(band_2)/features.get_feature_by_name(band_1)
