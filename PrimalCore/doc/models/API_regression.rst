regression
==========
.. contents:: :local:



.. toctree::



API documentation
-------------------
.. currentmodule:: PrimalCore.models.regression
.. _sklearn: http://scikit-learn.org/stable/documentation.html



In this python module  the class :class:`Regressor` is implemented (see for full API the module :mod:`~PrimalCore.models.regression`).
This class implements :class:`~PrimalCore.models.base.BaseModel` derived class specialized for sklearn Regressors  :class:`sklearn.base.RegressorMixin`
It also implements several class methods to build some predefined Regressor

.. rubric:: Regressor Class

.. autosummary:: Regressor


.. autoclass:: Regressor



.. rubric:: Regressor classmethods


.. autosummary::
   ~Regressor.RFRegressor
   ~Regressor.GBRegressor
   ~Regressor.ABRegressor
   ~Regressor.KNRegressor
   ~Regressor.SVRRegressor


