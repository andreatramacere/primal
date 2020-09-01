"""
Overview
--------
   
general info about this module


Classes and Inheritance Structure
----------------------------------------------
.. inheritance-diagram:: 
    BaseModel

Summary
---------
.. autosummary::
   BaseModel
    
Module API
----------

.. _sklearn: http://scikit-learn.org/stable/documentation.html
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
import  numpy as np
from sklearn.ensemble import GradientBoostingRegressor
# Project
# relative import eg: from .mod import f
from ..homogeneous_table.dataset_handler import check_dataset_decorate
from ..io.fits import write_data
import joblib
import pickle
class WrappedModel(object):

    def __init__(self,name):
        self.name=name



def check_wrapping_dictionary(wrapping_dictionary):
    pass



class BaseModel(object):
    """

     This class implements a base model to wrap  `sklearn`_ models. Or to wrap non-sklearn models
     making them compatible with the `sklearn`_  framework

     Parameters
     ----------
     clf : :class:`sklearn.base.RegressorMixin` or :class:`sklearn.base.ClassifierMixin` derived object
        the skelarn model wrapped in the class

     par_grid_dict : dictionary
        the dictionary of `clf` that we want to use for regularziation

     add_scorer : function  with a signature f(object, features, targe)
        a function to evaluate a specific score, that can be used as alternative
        to the `clf` one, having the same signature.
        It is useful to use in the case of :mod:`PrimalCore.models.pipeline`

     name : basestring
        model name
     """
    def __init__(self, clf, par_grid_dict=None,add_scorer=None,name=None):

        self.clf = clf
        self.par_grid_dict = par_grid_dict
        self.score=add_scorer
        self.name=name


    def save(self,file_name=None):
        _t=None
        if file_name is None:
            file_name=self.name+'.plk'

        joblib.dump(self, file_name)

    @staticmethod
    def load(file_name):
        return joblib.load(file_name)



    @classmethod
    def from_non_sklearn(cls,model_to_wrap,model_bridge_dictionary, par_grid_dict=None,name=None):
        """
        Class method to wrap non-sklearn models
        Parameters
        ----------
        model_to_wrap
        model_bridge_dictionary
        par_grid_dict
        name

        Returns
        -------

        """
        check_wrapping_dictionary(model_bridge_dictionary)
        clf=WrappedModel(name)

        for k in model_bridge_dictionary.keys:
            setattr(clf,k,model_bridge_dictionary[k])


        return cls(clf,par_grid_dict=par_grid_dict,name=name)

    def feature_importances(self,feature_names):
        """
        This method gets features importances from  `sklearn`_ models
        having the `feature_importances_` or the `coef_` attribute

        Parameters
        ----------
        feature_names : iterable string
            the list of fetures names

        Returns
        -------
        imp_arr : a structured  :class:`numpy.ndarray`
            an ndarray storing the feature names (field=`name`) and scores (field=`score`)

        """
        if hasattr(self.clf,'feature_importances_'):
            imp=self.clf.feature_importances_

        elif hasattr(self.clf,'coef_'):
            imp=self.clf.coef_
        else:
            imp=None

        if imp is not None:
            dt = [('name', '|S128'), ('score', np.float32)]
            imp_arr = np.zeros(len(feature_names), dtype=dt)

            for ID, name in enumerate(feature_names):
                imp_arr['name'][ID] = name
                imp_arr['score'][ID] = self.clf.feature_importances_[ID]

            imp_arr=imp_arr[np.argsort(imp_arr, order=('score', 'name'))]
        else:
            imp_arr=None

        return imp_arr




    def eval_estimators_predictions(self,features):
        """
        Returns a matrix with the prediction of each single estimator for an ensamble estimator

        Parameters
        ----------
        features

        Returns
        -------

        """
        if hasattr(self.clf, 'estimators_'):
            _preds = np.zeros((features.shape[0],len(self.clf.estimators_)))

        if isinstance(self.clf,GradientBoostingRegressor):
            for i in range(len(self.clf.estimators_.reshape(-1))):
              _preds[:,i]=self.clf.estimators_.reshape(-1)[i].predict(features)
        else:
            for i in range(len(self.clf.estimators_)):
              _preds[:,i]=self.clf.estimators_[i].predict(features)

        return _preds




    @check_dataset_decorate
    def save_mldataset_predictions(self,filename,dataset,pred=None,clobber=True):
        """
        Saves the models predictions for a dataset. Actual values are taken
        from :attr:`~PrimalCore.homogeneous_table.dataset.MLDataSet.target_array`
        The catalog file attribute from :class:`~PrimalCore.homogeneous_table.dataset.MLDataSet`
        is saved  as a fits header keyword `cat_file`

        Parameters
        ----------
        filename : basestring
            file name

        dataset : `~PrimalCore.homogeneous_table.dataset.MLDataSet` object

        pred : 1dim array (default is None), Optional
            predicted values, if `None`, the model will predict with :attr:`~PrimalCore.homogeneous_table.dataset.MLDataSet.features`

        clobber : bool (default is True), Optional
            flag to activate pyfits `clobber`

        Returns
        -------

        """
        if pred is None:
            pred = self.clf.predict(dataset.features)
        actual=dataset.target_array

        id=dataset.features_original_entry_ID

        self.save_predictions(filename,pred,actual=actual,id=id,clobber=clobber,catalog_file=dataset.catalog_file)



    def save_predictions(self,filename,pred,actual=None,id=None,clobber=True,catalog_file=None):
        """
        save the models predictions for a  generic dataset

        Parameters
        ----------
        filename : basestring
            file name
        pred : 1dim array
            the predicted values
        actual : 1dim array (default is None), Optional
            the actual values
        id : the original entry id

        clobber : bool (default is True), Optional
            flag to activate pyfits `clobber`

        catalog_file : a catalog file, with entries matching `id`
           this value is  saved as a fits header keyword `cat_file`

        Returns
        -------

        """

        header_tuple_list = [('cat_file', catalog_file, 'catalog file')]

        dt = [('pred', pred.dtype.str)]

        if actual is not None:
            dt.append(('actual', actual.dtype.str))

        if id is not None:
            dt.append(('original_entry_ID', id.dtype.str))

        data = np.zeros(pred.size, dtype=dt)
        data['pred'] = pred

        if actual is not None:
            data['actual'] = actual
        if id is not None:
            data['original_entry_ID'] = id
        #print(data,dt)
        #   return data
        write_data(filename, data, extra_header_tuple_list=header_tuple_list,clobber=clobber)
