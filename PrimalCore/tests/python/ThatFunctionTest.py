import unittest

from ElementsKernel.Path import getPathFromEnvVariable
from PrimalCore.heterogeneous_table.table import Table
import  numpy as np
class TableTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        ph_catalog = getPathFromEnvVariable('PrimalCore/euclid_cosmos_DC2_S2_v2.1_valid.fits', 'ELEMENTS_AUX_PATH')
        self.catalog=Table.from_fits_file(ph_catalog,fits_ext=1)


    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_keep_columns(self):
        self.catalog .keep_columns(['FLUX_G*', 'MAG_G_*', 'MAGERR_G*'], regex=True)
        self.assertEqual(self.catalog.column_names,['FLUX_G_1','FLUX_G_2','FLUX_G_3',
                                                     'MAG_G_1',
                                                     'MAG_G_2',
                                                     'MAG_G_3',
                                                     'MAGERR_G_1',
                                                     'MAGERR_G_2',
                                                     'MAGERR_G_3',
                                                     '__original_entry_ID__'])


    def test_drop_columns(self):
        self.catalog.drop_columns(['MAGERR*'],regex=True)
        self.assertNotIn(['MAGERR_G_1'],self.catalog.column_names)

    def test_add_columns(self):
        x = np.arange(self.catalog.N_rows)

        self.catalog.add_columns(['x', 'y'], [x, x])
        names=['x','y']
        for name in names:
            self.assertIn(name ,self.catalog.column_names)

if __name__ == '__main__':
    unittest.main()