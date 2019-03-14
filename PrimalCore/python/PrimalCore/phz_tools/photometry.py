"""
Overview
--------
   
general info about this module


Summary
---------
.. autosummary::
   Color
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

__author__ = "Andrea Tramacere"

# Standard library
# eg copy
# absolute import rg:from copy import deepcopy

# Dependencies
# eg numpy 
# absolute import eg: import numpy as np

# Project
# relative import eg: from .mod import f



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
