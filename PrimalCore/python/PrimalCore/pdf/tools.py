"""
Overview
--------
   
general info about this module


Module API
----------
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
try:
    import  pyfits as pf
except:
    try:
        from astropy.io import fits as pf
    except ImportError:
        raise ImportError('')

import  numpy as np

# Project
# relative import eg: from .mod import f

from .stats import eval_pdf_gmm
from ..io.fits import write_data


def extract_pdf(model,ml_dataset,z_phot=None,pdf_grid_size=100,gmm_components=2,out_file_name=None):

    """

    Parameters
    ----------
    model : a :class:`PrimalCore.models.base.BaseModel` based model
    ml_dataset : :class:`PrimalCore.homogeneous_table.dataset.MLDataSet` dataset
    z_phot : 1dim array
        predicted z_phot, if None is evalauted from model and ml_dataset
    pdf_grid_size : int (Optional)
        the size of the grid to evaluate the pdf
    gmm_components : int (Optional) default=5
        the number of components in teh GMM model to test
    out_file_name : basestring
        output file name

    Returns
    -------
    pdf :

    """

    if  hasattr(model.clf,'estimators_')==False:
        return None


    trials=len(model.clf.estimators_)

    if z_phot is None:
        z_phot=model.clf.predict(ml_dataset.features)

    c1 = pf.Column(name='original_row_ID', format='J', array=ml_dataset.features_original_entry_ID)
    c2 = pf.Column(name='z_spec', format='D', array=ml_dataset.target_array)
    c3 = pf.Column(name='z_phot', format='D', array=z_phot)
    c4 = pf.Column(name='z_phot_values', format='%dD'%(trials), )
    c5 = pf.Column(name='z_phot_pdf_grid', format='%dD' % (pdf_grid_size), )
    c6 = pf.Column(name='z_phot_pdf', format='%dD' % (pdf_grid_size), )
    coldefs = pf.ColDefs([c1,c2,c3,c4,c5,c6])
    tbhdu = pf.BinTableHDU.from_columns(coldefs)

    pred_z_phot = model.eval_estimators_predictions(ml_dataset.features)

    for trial in xrange(trials):


        tbhdu.data['z_phot_values'][:,trial]=pred_z_phot[:,trial]

    for entry in xrange(pred_z_phot.shape[0]):
        z_grid, gmm_pdf = eval_pdf_gmm(z_values=pred_z_phot[entry],grid_size=pdf_grid_size,n_components=gmm_components)
        tbhdu.data['z_phot_pdf_grid'][entry] = z_grid
        tbhdu.data['z_phot_pdf'][entry] = gmm_pdf

    if out_file_name is not None:
        header_tuple_list = [('cat_file', ml_dataset.catalog_file, 'catalog file')]

        write_data(out_file_name,tbhdu.data,extra_header_tuple_list=header_tuple_list)


    return np.array(tbhdu.data)
