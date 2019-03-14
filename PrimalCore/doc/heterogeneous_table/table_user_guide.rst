
.. _Table_user_guide:

Table user guide
================

.. currentmodule:: PrimalCore.heterogeneous_table.table

We provide a simple workflow to build a catalog using the class :class:`Table` (see for full API the module :mod:`PrimalCore.heterogeneous_table.table`)

.. contents:: :local:

.. toctree::


Building a catalog, from a FITS file, using the Table class
-----------------------------------------------------------

Aux files setup
~~~~~~~~~~~~~~~

We use the Elements ``getPathFromEnvVariable`` function, that is in
charge to determine the proper file path.

.. code:: python

    from ElementsKernel.Path import getPathFromEnvVariable

and we set the path to catalog file path

.. code:: python

    ph_catalog=getPathFromEnvVariable('PrimalCore/test_table.fits','ELEMENTS_AUX_PATH')
    print ph_catalog


.. parsed-literal::

    /Users/orion/Work/Projects/Primal/PrimalCore/auxdir/PrimalCore/test_table.fits


As yuo can see, the file path has been safely and correctly determined by ``getPathFromEnvVariable``.

We  import  the :class:`Table` class, that we will use for the catalog construction. This class is able to handle heterogeneous data, by using numpy recarray and implements also method to handle the data row-wise and column wise (see :class:`PrimalCore.heterogeneous_table.table.Table` and :mod:`PrimalCore.heterogeneous_table.table` for more details) 

.. code:: python

    from PrimalCore.heterogeneous_table.table import Table

Table construcion using the from\_fits\_file class method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, we can  build our catalog usinfg the  :class:`Table` class and the classmetod :func:`Table.from_fits_file`

.. code:: python

    catalog=Table.from_fits_file(ph_catalog,fits_ext=0)


.. parsed-literal::

    | input data built
    | data Rows,Cols 1000 124


.. code:: python

    print catalog.N_rows


.. parsed-literal::

    1000


Table construcion sing the io.build\_table\_from\_fits\_file factory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

as alternative we can use the :func:`PrimalCore.heterogeneous_table.io.build_table_from_fits_file` factory

.. code:: python

    from PrimalCore.heterogeneous_table.io import build_table_from_fits_file
    catalog=build_table_from_fits_file(ph_catalog,fits_ext=1)


.. parsed-literal::

    | input data built
    | data Rows,Cols 1000 124


Modifying the Table catalog
---------------------------

colums operations
~~~~~~~~~~~~~~~~~

We select only some columns with the :func:`Table.keep_columns`, and regualar expression syntax


keep\_columns
^^^^^^^^^^^^^

.. code:: python

    catalog.keep_columns(['FLUX_G*','MAG_G_*','MAGERR_G*','reliable_S15','STAR','AGN','MASKED','FLAG_PHOT'],regex=True)
    catalog.column_names




.. parsed-literal::

    ['FLUX_G_1',
     'FLUX_G_2',
     'FLUX_G_3',
     'FLAG_PHOT',
     'MAG_G_1',
     'MAG_G_2',
     'MAG_G_3',
     'MAGERR_G_1',
     'MAGERR_G_2',
     'MAGERR_G_3',
     'MASKED',
     'reliable_S15',
     'STAR',
     'AGN',
     '__original_entry_ID__']



drop\_columns
^^^^^^^^^^^^^

We remove only some columns with the  method :func:`Table.drop_columns`, and regualar expression syntax


.. code:: python

    catalog.drop_columns(['MAGERR*'],regex=True)
    catalog.column_names




.. parsed-literal::

    ['FLUX_G_1',
     'FLUX_G_2',
     'FLUX_G_3',
     'FLAG_PHOT',
     'MAG_G_1',
     'MAG_G_2',
     'MAG_G_3',
     'MASKED',
     'reliable_S15',
     'STAR',
     'AGN',
     '__original_entry_ID__']



add\_columns
^^^^^^^^^^^^

we add a new column using the  :func:`Table.add_columns` method

.. code:: python

    x=np.arange(catalog.N_rows)
    
    catalog.add_columns(['x','y'],[x,x])
    catalog.column_names




.. parsed-literal::

    ['FLUX_G_1',
     'FLUX_G_2',
     'FLUX_G_3',
     'FLAG_PHOT',
     'MAG_G_1',
     'MAG_G_2',
     'MAG_G_3',
     'MASKED',
     'reliable_S15',
     'STAR',
     'AGN',
     '__original_entry_ID__',
     'x',
     'y']



rows operations
~~~~~~~~~~~~~~~

We show how to perform operation on the rows.

drop\_rows
^^^^^^^^^^

we drop some rows using a boolean mask with the :func:`Table.drop_rows` method

.. code:: python

    msk=np.zeros(catalog.N_rows,dtype=np.bool)
    msk[0:100]=True
    
    catalog.drop_rows(msk)


.. parsed-literal::

    | filtering data rows
    | data initial Rows = 1000
    | data filtered initial Rows = 900
    


.. code:: python

    print catalog.N_rows


.. parsed-literal::

    900


.. code:: python

    print catalog.original_entry_ID.min()


.. parsed-literal::

    100


.. code:: python

    catalog.original_entry_ID.max()




.. parsed-literal::

    999



.. note::
    as you see the original_entry_ID is correctly starting from 100 because we dropped elements from ID=0 to ID=99

keep\_row
^^^^^^^^^

We can select rows using a boolean mask with the :func:`Table.keep_rows` method. This method will keep only the rows corresponind to mask==True.
For example imagine that you want  to filter the catalog keeping only the rows respecting  the condition for a clean cut: ``CLEAN=" (FLAG_PHOT == 0) & (MASKED == 0) & (STAR == 0) & (AGN == 0) & (reliable_S15==1)"
this can be obtained by:``

.. code:: python

    CLEAN= (catalog.data['FLAG_PHOT']==0)*(catalog.data['MASKED']==0)*(catalog.data['STAR']==0)*(catalog.data['AGN']==0)
    CLEAN*= catalog.data['reliable_S15']==1
    catalog.keep_rows(CLEAN)


.. parsed-literal::

    | filtering data rows
    | data initial Rows,Cols= (900,)
    | data filtered Rows,Cols= (3,)
    


add\_rows
^^^^^^^^^

we add rows to a table, using the :func:`Table.add_rows` method

we have to provide a values\_array that as to be 2dim numpy array, or a
rec\_array, or structured array

.. code:: python

    new_row=np.arange(catalog.N_cols).reshape(1,catalog.N_cols)
    catalog.add_rows(new_row)

.. code:: python

    print catalog.N_rows


.. parsed-literal::

    4


.. code:: python

    print catalog.original_entry_ID[-5:]


.. parsed-literal::

    [288 515 711  11]


.. warning::

    **adding rows migth impact the original_entry_ID**, indeed we  note that the last original_entry_ID is equal to 6,     i.e. the last element of the row that we added

merging catalogs
----------------

In the following we show how merge two catalogs

using the :func:`PrimalCore.heterogeneous_table.table_handler.tables_merge_rows`

.. code:: python

    from PrimalCore.heterogeneous_table.table_handler import tables_merge_rows

.. code:: python

    new_cat=tables_merge_rows(catalog,catalog)


.. parsed-literal::

    | input data built
    | data Rows,Cols 8 14


.. code:: python

    print new_cat.original_entry_ID


.. parsed-literal::

    [288 515 711  11 288 515 711  11]


.. code:: python

    print new_cat.N_rows


.. parsed-literal::

    8


.. warning::

    As in the case of **adding rows**, this operation  impact the original_entry_ID.
