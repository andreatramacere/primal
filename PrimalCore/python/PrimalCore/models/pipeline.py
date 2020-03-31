"""
Overview
--------
   
general info about this module


Classes and Inheritance Structure
----------------------------------------------
.. inheritance-diagram:: BasePipeline

Summary
---------
.. autosummary::
    BasePipeline
    pipeline_stratified_kfold_cv
    
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
import types

# Dependencies
# eg numpy 
# absolute import eg: import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE,RFECV
from sklearn.preprocessing import StandardScaler




class BasePipeline(Pipeline):
    """
    Base class to wrap :class:`sklearn.pipeline.Pipeline`

    Parameters
    ----------
    transformers_dic : dictionary
        a dictionary of sklearn transformers
    final_estimator : :class:`PrimalCore.models.base.BaseModel` derived object

    scorer : function(x,y,weights=None)
        overrides the model.clf.score method


    """
    def __init__(self,transformers_dic,final_estimator,scorer=None):

        self.transformers_dic=transformers_dic
        self.model=final_estimator

        _stages_list=[]

        for k in self.transformers_dic:
            _stages_list.append((k,transformers_dic[k]))


        _stages_list.append(('clf',final_estimator.clf))

        self.sk_pipeline=Pipeline(_stages_list)


        if scorer is not None:
            self.sk_pipeline.named_steps['clf'].score = types.MethodType(scorer, self.sk_pipeline.named_steps['clf'])

        _methods_names_list=['fit','predict']

        for meth_name in _methods_names_list:
            if hasattr(self.sk_pipeline,meth_name):
                setattr(self,meth_name,getattr(self.sk_pipeline,meth_name))



    @property
    def step_names(self):
        """
        Returns the names of each step of the pipeline, these are keys of the dictionary `named_steps` that is
         a member of the :class:`sklearn.pipeline.Pipeline` class.

        Returns
        -------
        step names : dictionary keys
            the names of each step of the skelearn pipeline
        """
        return self.sk_pipeline.named_steps.keys()


def pipeline_stratified_kfold_cv(model,scorer=None,cv=5):
    """
    Factory for  :class:`BasePipeline` based on
        - StandardScaler
        - Recursive Feature Elimination based on CV
        - a user provided model
        - a user provided scorer

    Parameters
    ----------
    model : :class:`PrimalCore.models.base.BaseModel` derived object
    scorer : function(x,y,weights=None)
        overrides the model.score method

    Returns
    -------
    BasePipeline :   :class:`BasePipeline`
        the kfold cv pipeline

    """
    transformers_dic={}
    transformers_dic['scl']=StandardScaler()
    transformers_dic['rfecv']=RFECV(estimator=model.clf,cv=cv,scoring=scorer)


    return BasePipeline(transformers_dic,model,scorer=scorer)

