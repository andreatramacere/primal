preprocessing
==================
.. contents:: :local:



.. toctree::


.. currentmodule:: PrimalCore.preprocessing

Introduction
------------
.. _sklearn: http://scikit-learn.org/stable/documentation.html


The :mod:`PrimalCore.preprocessing` implements dataset preprocessing functions for Machine Learning based on `sklearn`_
These functions are designed to work with  the :class:`PrimalCore.homogeneous_table.dataset.MLDataSet` classes

   * The :mod:`PrimalCore.preprocessing.dataset_preprocessing` implements  preprocessing functionalities based on the
      * :mod:`sklearn.model_selection` for training/test stratified/shuffled splitting
      * :mod:`sklearn.preprocessing` for scaling/replacing/standardization of the features entries

   * The :mod:`PrimalCore.preprocessing.features_selection` implements  functionalities for dimensionality reduction
   based on feature elimiantion (recursive/cv)  based on :mod:`sklearn.feature_selection`



Modules relationship and UML diagrams
-------------------------------------






Coding documentation
--------------------
.. toctree::
   :maxdepth: 0

   dataset preprocessing <API_dataset_preprocessing.rst>
   features selection <features_selection.rst

User guides
-----------


Full API
--------
:mod:`PrimalCore.preprocessing`