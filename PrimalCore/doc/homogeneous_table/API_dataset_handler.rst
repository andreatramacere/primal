dataset handler
===================
.. contents:: :local:



.. toctree::



.. currentmodule:: PrimalCore.homogeneous_table.dataset_handler

In this python module are implemented functions to handle :class:`PrimalCore.homogeneous_table.dataset.MLDataSet`,
in such a way that all the operations (row-wise) will be properly applied to members:
- :py:attr:`PrimalCore.homogeneous_table.dataset.MLDataSet.features`
- :py:attr:`PrimalCore.homogeneous_table.dataset.MLDataSet.target_array`
- :py:attr:`PrimalCore.homogeneous_table.dataset.MLDataSet.weight_array`
- :py:attr:`PrimalCore.homogeneous_table.dataset.MLDataSet.columns_mask`

API documentation
-------------------

.. rubric:: features handling functions


.. autosummary::
    ~PrimalCore.homogeneous_table.dataset_handler.add_features
    ~PrimalCore.homogeneous_table.dataset_handler.dataset_append
    ~PrimalCore.homogeneous_table.dataset_handler.drop_features
    ~PrimalCore.homogeneous_table.dataset_handler.keep_features
    ~PrimalCore.homogeneous_table.dataset_handler.keep_rows
    ~PrimalCore.homogeneous_table.dataset_handler.new_from_rows
    ~PrimalCore.homogeneous_table.dataset_handler.sort_feature_columns_position

User guide
-----------
