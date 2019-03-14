
.. _MLDataSet_user_guide:


Example of building a MLDataSet
===============================

We provide a simple workflow to build a fetures dataset using the class :class:`dataset.MLDataSet` (see for full API the module :mod:`~PrimalCore.homogeneous_table.dataset.MLDataSet`)

.. currentmodule:: PrimalCore.homogeneous_table.dataset

.. contents:: :local:

.. toctree::


Building a Features MLDataSet from a Table
------------------------------------------

we follow the approach in `Table_user_guide`_ to build a catalog using the :class:`PrimalCore.heterogeneous_table.table.Table`

.. code:: python

    from PrimalCore.heterogeneous_table.table import Table
    from ElementsKernel.Path import getPathFromEnvVariable

.. code:: python

    ph_catalog=getPathFromEnvVariable('PrimalCore/test_table.fits','ELEMENTS_AUX_PATH')

.. code:: python

    catalog=Table.from_fits_file(ph_catalog,fits_ext=0)


.. parsed-literal::

    | input data built
    | data Rows,Cols 1000 124


.. code:: python

    catalog.keep_columns(['FLUX*','reliable_S15','STAR','AGN','MASKED','FLAG_PHOT'],regex=True)

We  now build a Features dataset using the :class:`dataset.MLDataSet` class from the :mod:`PrimalCore.homogeneous_table.dataset` python module.

First we import the classes and the functions we need

.. code:: python

    from PrimalCore.homogeneous_table.dataset import MLDataSet

.. note::
   
   It is worth noting that  for the :class:`MLDataSet` class, most of the functions to modify the dataset 
   content have been implemented as functions in separate python modules. This is made on purpose, and shows a 
   different approach compared to that used for the :class:`PrimalCore.heterogeneous_table.table.Table` class, where 
   the functions are implemented as methods of the same class.

To build a MLDataSet directly from a Table  we can use the classmethod :func:`MLDataSet.new_from_table`

.. code:: python

    dataset=MLDataSet.new_from_table(catalog)


.. parsed-literal::

    | building features
    | features built
    | Rows,Cols 1000 50


.. code:: python

    print dataset.features_names


.. parsed-literal::

    ['FLUX_G_1', 'FLUX_G_2', 'FLUX_G_3', 'FLUX_R_1', 'FLUX_R_2', 'FLUX_R_3', 'FLUX_I_1', 'FLUX_I_2', 'FLUX_I_3', 'FLUX_VIS', 'FLUX_Z_1', 'FLUX_Z_2', 'FLUX_Z_3', 'FLUX_Y_1', 'FLUX_Y_2', 'FLUX_Y_3', 'FLUX_J_1', 'FLUX_J_2', 'FLUX_J_3', 'FLUX_H_1', 'FLUX_H_2', 'FLUX_H_3', 'FLUXERR_G_1', 'FLUXERR_G_2', 'FLUXERR_G_3', 'FLUXERR_R_1', 'FLUXERR_R_2', 'FLUXERR_R_3', 'FLUXERR_I_1', 'FLUXERR_I_2', 'FLUXERR_I_3', 'FLUXERR_VIS', 'FLUXERR_Z_1', 'FLUXERR_Z_2', 'FLUXERR_Z_3', 'FLUXERR_Y_1', 'FLUXERR_Y_2', 'FLUXERR_Y_3', 'FLUXERR_J_1', 'FLUXERR_J_2', 'FLUXERR_J_3', 'FLUXERR_H_1', 'FLUXERR_H_2', 'FLUXERR_H_3', 'FLAG_PHOT', 'FLUX_RADIUS_DETECT', 'MASKED', 'reliable_S15', 'STAR', 'AGN']


.. note::
    as you can see, the **__original_entry_ID__** is not present among the features, indeed it is used only to track 
    the original catalog IDs, but it is present as separate member of the dataset (we print onlty the 10 first
    elements)

.. code:: python

    print dataset.features_original_entry_ID[1:10]


.. parsed-literal::

    [1 2 3 4 5 6 7 8 9]


and in this way it **safely** can not be used as a feature.

Building a Features MLDataSet from a FITS file
----------------------------------------------

To build a MLDataSet directly from a FITS file we can use the classmethod :func:`MLDataSet.new_from_fits_file`

.. code:: python

    dataset_from_file=MLDataSet.new_from_fits_file(ph_catalog,fits_ext=0,\
                                                   use_col_names_list=['FLUX*','reliable_S15','STAR','AGN','MASKED','FLAG_PHOT'],\
                                                   regex=True)


.. parsed-literal::

    | input data built
    | data Rows,Cols 1000 124
    | building features
    | features built
    | Rows,Cols 1000 50


.. code:: python

    print dataset_from_file.features_names


.. parsed-literal::

    ['FLUX_G_1', 'FLUX_G_2', 'FLUX_G_3', 'FLUX_R_1', 'FLUX_R_2', 'FLUX_R_3', 'FLUX_I_1', 'FLUX_I_2', 'FLUX_I_3', 'FLUX_VIS', 'FLUX_Z_1', 'FLUX_Z_2', 'FLUX_Z_3', 'FLUX_Y_1', 'FLUX_Y_2', 'FLUX_Y_3', 'FLUX_J_1', 'FLUX_J_2', 'FLUX_J_3', 'FLUX_H_1', 'FLUX_H_2', 'FLUX_H_3', 'FLUXERR_G_1', 'FLUXERR_G_2', 'FLUXERR_G_3', 'FLUXERR_R_1', 'FLUXERR_R_2', 'FLUXERR_R_3', 'FLUXERR_I_1', 'FLUXERR_I_2', 'FLUXERR_I_3', 'FLUXERR_VIS', 'FLUXERR_Z_1', 'FLUXERR_Z_2', 'FLUXERR_Z_3', 'FLUXERR_Y_1', 'FLUXERR_Y_2', 'FLUXERR_Y_3', 'FLUXERR_J_1', 'FLUXERR_J_2', 'FLUXERR_J_3', 'FLUXERR_H_1', 'FLUXERR_H_2', 'FLUXERR_H_3', 'FLUX_RADIUS_DETECT', 'reliable_S15', 'STAR', 'AGN', 'MASKED', 'FLAG_PHOT']


Columns selection
-----------------

using ``use_col_names_list`` in the factories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Columns can be selected using the `use_col_names_list` parameter in the classmethod factories  :func:`MLDataSet.new_from_table` and :func:`MLDataSet.new_from_fits_file`

.. code:: python

    dataset=MLDataSet.new_from_table(catalog,use_col_names_list=['FLUX*','reliable_S15','STAR','AGN','MASKED','FLAG_PHOT'],\
                                    regex=True)


.. parsed-literal::

    | building features
    | features built
    | Rows,Cols 1000 50


.. code:: python

    print dataset.features_names


.. parsed-literal::

    ['FLUX_G_1', 'FLUX_G_2', 'FLUX_G_3', 'FLUX_R_1', 'FLUX_R_2', 'FLUX_R_3', 'FLUX_I_1', 'FLUX_I_2', 'FLUX_I_3', 'FLUX_VIS', 'FLUX_Z_1', 'FLUX_Z_2', 'FLUX_Z_3', 'FLUX_Y_1', 'FLUX_Y_2', 'FLUX_Y_3', 'FLUX_J_1', 'FLUX_J_2', 'FLUX_J_3', 'FLUX_H_1', 'FLUX_H_2', 'FLUX_H_3', 'FLUXERR_G_1', 'FLUXERR_G_2', 'FLUXERR_G_3', 'FLUXERR_R_1', 'FLUXERR_R_2', 'FLUXERR_R_3', 'FLUXERR_I_1', 'FLUXERR_I_2', 'FLUXERR_I_3', 'FLUXERR_VIS', 'FLUXERR_Z_1', 'FLUXERR_Z_2', 'FLUXERR_Z_3', 'FLUXERR_Y_1', 'FLUXERR_Y_2', 'FLUXERR_Y_3', 'FLUXERR_J_1', 'FLUXERR_J_2', 'FLUXERR_J_3', 'FLUXERR_H_1', 'FLUXERR_H_2', 'FLUXERR_H_3', 'FLUX_RADIUS_DETECT', 'reliable_S15', 'STAR', 'AGN', 'MASKED', 'FLAG_PHOT']


using dataset\_handler fucntions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Or, columns can be selected using specific selection functions, from the :mod:`~PrimalCore.homogeneous_table.dataset_handler` module

.. code:: python

    from PrimalCore.homogeneous_table.dataset_handler import drop_features
    from PrimalCore.homogeneous_table.dataset_handler import keep_features

for example we decide to drop columns with names matching expression  "FLUX\*1\*" by  using the :func:`~PrimalCore.homogeneous_table.dataset_handler.drop_features`

.. code:: python

    drop_features(dataset,['FLUX*1*'])
    dataset.features_names


.. parsed-literal::

    | features initial Rows,Cols= 1000 50
    | removing features ['FLUX_G_1', 'FLUX_R_1', 'FLUX_I_1', 'FLUX_Z_1', 'FLUX_Y_1', 'FLUX_J_1', 'FLUX_H_1', 'FLUXERR_G_1', 'FLUXERR_R_1', 'FLUXERR_I_1', 'FLUXERR_Z_1', 'FLUXERR_Y_1', 'FLUXERR_J_1', 'FLUXERR_H_1']
    | features final Rows,Cols= 1000 36
    




.. parsed-literal::

    ['FLUX_G_2',
     'FLUX_G_3',
     'FLUX_R_2',
     'FLUX_R_3',
     'FLUX_I_2',
     'FLUX_I_3',
     'FLUX_VIS',
     'FLUX_Z_2',
     'FLUX_Z_3',
     'FLUX_Y_2',
     'FLUX_Y_3',
     'FLUX_J_2',
     'FLUX_J_3',
     'FLUX_H_2',
     'FLUX_H_3',
     'FLUXERR_G_2',
     'FLUXERR_G_3',
     'FLUXERR_R_2',
     'FLUXERR_R_3',
     'FLUXERR_I_2',
     'FLUXERR_I_3',
     'FLUXERR_VIS',
     'FLUXERR_Z_2',
     'FLUXERR_Z_3',
     'FLUXERR_Y_2',
     'FLUXERR_Y_3',
     'FLUXERR_J_2',
     'FLUXERR_J_3',
     'FLUXERR_H_2',
     'FLUXERR_H_3',
     'FLUX_RADIUS_DETECT',
     'reliable_S15',
     'STAR',
     'AGN',
     'MASKED',
     'FLAG_PHOT']



Furtger we can decide to keep only columns with names matching the regular expression "FLUX\*2\*" by using the  :func:`~PrimalCore.homogeneous_table.dataset_handler.keep_features`  function from the :mod:`PrimalCore.homogeneous_table.dataset_handler` package

.. code:: python

    keep_features(dataset,['FLUX*2*'],regex=True)
    print dataset.features_names


.. parsed-literal::

    | features initial Rows,Cols= 1000 36
    | removing features ['FLUX_G_3', 'FLUX_R_3', 'FLUX_I_3', 'FLUX_VIS', 'FLUX_Z_3', 'FLUX_Y_3', 'FLUX_J_3', 'FLUX_H_3', 'FLUXERR_G_3', 'FLUXERR_R_3', 'FLUXERR_I_3', 'FLUXERR_VIS', 'FLUXERR_Z_3', 'FLUXERR_Y_3', 'FLUXERR_J_3', 'FLUXERR_H_3', 'FLUX_RADIUS_DETECT', 'reliable_S15', 'STAR', 'AGN', 'MASKED', 'FLAG_PHOT']
    | features final Rows,Cols= 1000 14
    
    ['FLUX_G_2', 'FLUX_R_2', 'FLUX_I_2', 'FLUX_Z_2', 'FLUX_Y_2', 'FLUX_J_2', 'FLUX_H_2', 'FLUXERR_G_2', 'FLUXERR_R_2', 'FLUXERR_I_2', 'FLUXERR_Z_2', 'FLUXERR_Y_2', 'FLUXERR_J_2', 'FLUXERR_H_2']


Adding features
---------------

And finally we can add a new feature with the :func:`~PrimalCore.homogeneous_table.dataset_handler.add_features` function
We can add a single feature:

.. code:: python

    from PrimalCore.homogeneous_table.dataset_handler import add_features
    
    test_feature=dataset.get_feature_by_name('FLUXERR_H_2')**2
    add_features(dataset,'test',test_feature)
    dataset.features_names




.. parsed-literal::

    ['FLUX_G_2',
     'FLUX_R_2',
     'FLUX_I_2',
     'FLUX_Z_2',
     'FLUX_Y_2',
     'FLUX_J_2',
     'FLUX_H_2',
     'FLUXERR_G_2',
     'FLUXERR_R_2',
     'FLUXERR_I_2',
     'FLUXERR_Z_2',
     'FLUXERR_Y_2',
     'FLUXERR_J_2',
     'FLUXERR_H_2',
     'test']



Or we can add a 2dim array of features

.. code:: python

    test_feature_2dim=np.zeros((dataset.features_N_rows,5))
    test_feature_2dim_names=['a','b','c','d','e']
    add_features(dataset,test_feature_2dim_names,test_feature_2dim)
    dataset.features_names




.. parsed-literal::

    ['FLUX_G_2',
     'FLUX_R_2',
     'FLUX_I_2',
     'FLUX_Z_2',
     'FLUX_Y_2',
     'FLUX_J_2',
     'FLUX_H_2',
     'FLUXERR_G_2',
     'FLUXERR_R_2',
     'FLUXERR_I_2',
     'FLUXERR_Z_2',
     'FLUXERR_Y_2',
     'FLUXERR_J_2',
     'FLUXERR_H_2',
     'test',
     'a',
     'b',
     'c',
     'd',
     'e']



We can think to a more meaningful example, i.e. we want to add flux
ratios. Lets start by defining the list of contigous bands, for the flux
evaluation

.. code:: python

    flux_bands_list_2=['FLUX_G_2','FLUX_R_2','FLUX_I_2','FLUX_Z_2','FLUX_Y_2','FLUX_J_2','FLUX_VIS','FLUX_VIS','FLUX_VIS']
    flux_bands_list_1=['FLUX_R_2','FLUX_I_2','FLUX_Z_2','FLUX_Y_2','FLUX_J_2','FLUX_H_2','FLUX_Y_2','FLUX_J_2','FLUX_H_2']

we import the module where we have defined the FluxRatio class (:mod:`PrimalCore.phz_tools.photometry`)

.. code:: python

    from PrimalCore.phz_tools.photometry import FluxRatio

.. code:: python

    for f1,f2 in zip(flux_bands_list_1,flux_bands_list_2):
        f1_name=f1.split('_')[1]
        f2_name=f2.split('_')[1]
        if f1 in dataset.features_names and f2 in dataset.features_names:
            f=FluxRatio('F_%s'%(f2_name+'-'+f1_name),f1,f2,features=dataset)
            add_features(dataset,f.name,f.values)


.. parsed-literal::

    /Users/orion/Work/Projects/Primal/PrimalCore/python/PrimalCore/phz_tools/photometry.py:110: RuntimeWarning: divide by zero encountered in true_divide
      return features.get_feature_by_name(band_2)/features.get_feature_by_name(band_1)
    /Users/orion/Work/Projects/Primal/PrimalCore/python/PrimalCore/phz_tools/photometry.py:110: RuntimeWarning: invalid value encountered in true_divide
      return features.get_feature_by_name(band_2)/features.get_feature_by_name(band_1)


.. note::
    Note that in this example we skipped the selection  CLEAN=" (FLAG_PHOT == 0) & (MASKED == 0) & (STAR == 0) & 
    (AGN == 0) & (reliable_S15==1)", so we have entries with flux values that are zero, and this results in the 
    corresponding warning messge due to zero division

.. code:: python

    dataset.features_names




.. parsed-literal::

    ['FLUX_G_2',
     'FLUX_R_2',
     'FLUX_I_2',
     'FLUX_Z_2',
     'FLUX_Y_2',
     'FLUX_J_2',
     'FLUX_H_2',
     'FLUXERR_G_2',
     'FLUXERR_R_2',
     'FLUXERR_I_2',
     'FLUXERR_Z_2',
     'FLUXERR_Y_2',
     'FLUXERR_J_2',
     'FLUXERR_H_2',
     'test',
     'a',
     'b',
     'c',
     'd',
     'e',
     'F_G-R',
     'F_R-I',
     'F_I-Z',
     'F_Z-Y',
     'F_Y-J',
     'F_J-H']



Operations on rows
------------------

filtering NaN/Inf with dataset\_preprocessing functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can get rid of the NAN/INF rows using  the :func:`~PrimalCore.preprocessing.dataset_preprocessing.drop_nan_inf` function

.. code:: python

    from PrimalCore.preprocessing.dataset_preprocessing import drop_nan_inf

.. code:: python

    drop_nan_inf(dataset)


.. parsed-literal::

    | features cleaning for nan/inf
    | features initial Rows,Cols= 1000 26
    | features initial Rows,Cols= 1000 26
    | removing features []
    | features final Rows,Cols= 1000 26
    
    |removed columns []
    |removed rows 468
    | features cleaned Rows,Cols= 532 26
    


