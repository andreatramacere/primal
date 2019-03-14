classification
==============
.. contents:: :local:



.. toctree::



API documentation
-------------------
.. currentmodule:: PrimalCore.models.classification
.. _sklearn: http://scikit-learn.org/stable/documentation.html



In this python module  the class :class:`Classifer` is implemented (see for full API the module :mod:`~PrimalCore.models.classification`).
This class implements :class:`~PrimalCore.models.base.BaseModel` derived class specialized for sklearn Regressors  :class:`sklearn.base.ClassifierMixin`
It also implements several class methods to build some predefined Classifiers

.. rubric:: Classifier Class

.. autosummary:: Classifier


.. autoclass:: Classifier



.. rubric:: Classifier classmethods


.. autosummary::
   ~Classifier.LDAClassifier
   ~Classifier.RFCClassifier
   ~Classifier.GBClassifier
   ~Classifier.SVLClassifier
   ~Classifier.SVKClassifier
