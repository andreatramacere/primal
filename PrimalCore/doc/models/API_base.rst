base
======
.. contents:: :local:



.. toctree::



API documentation
-------------------
.. currentmodule:: PrimalCore.models.base
.. _sklearn: http://scikit-learn.org/stable/documentation.html



In this python module  the class :class:`BaseModel` is implemented (see for full API the module :mod:`~PrimalCore.models.base`).
This class implements a base model to wrap  `sklearn`_ models. The class offers:
    * full access to the  `sklearn`_ model  through the memeber :attr:`~BaseModel.clf`
    * possibility to define a dicitionary of the model paramters (useful for the model regularization)
    * a method :meth:`~BaseModel.feature_importances` to handle the features importances
    * a method :meth:`~BaseModel.save_mldataset_predictions` to save predictions using the expected data structure of a data
    set implemented  by the class :class:`~PrimalCore.homogeneous_table.dataset.MLDataSet`.
    * a method :meth:`~BaseModel.save_predictions`  to save predictions for a  generic dataset

.. rubric:: BaseModel Class

.. autosummary:: BaseModel


.. rubric:: BaseModel methods


.. autosummary::
   ~BaseModel.feature_importances
   ~BaseModel.eval_estimators_predictions
   ~BaseModel.save_mldataset_predictions
   ~BaseModel.save_predictions



