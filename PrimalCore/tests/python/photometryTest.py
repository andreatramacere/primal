import unittest

from ElementsKernel.Path import getPathFromEnvVariable
from PrimalCore.heterogeneous_table.table import Table
from PrimalCore.homogeneous_table.dataset import MLDataSet
from PrimalCore.phz_tools.photometry import Mag,AsinhMag,Color,AsinhColor,FluxRatio
import  numpy as np

class PhotometryTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        ph_catalog = getPathFromEnvVariable('PrimalCore/test_table_photometry.fits', 'ELEMENTS_AUX_PATH')
        self.catalog=Table.from_fits_file(ph_catalog,fits_ext=1)
        self.dataset=MLDataSet.new_from_table(self.catalog,
                                     target_col_name='z_spec_S15',
                                     target_bins=20,
                                     target_binning='log',
                                     catalog_file='PrimalCore/test_table_photometry.fits')


    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_mag(self):
        computed = Mag('Mag_R','FLUX_R',zero_point=3.631E9,features=self.dataset)
        
        self.assertAlmostEqual(computed.values[0], 24.47800, places=3)   # for I 24.334143491104822
        self.assertAlmostEqual(computed.values[1], 25.12836, places=3)   # for I 23.792748661164076
        self.assertEqual(computed.name,'Mag_R')


    def test_asinhMag(self):
        computed = AsinhMag('AsinhMag_R','FLUX_R',b=1E-10, zero_point=3.631E9,features=self.dataset)
        
        self.assertAlmostEqual(computed.values[0], 24.197226574841781086134, places=10)   
        self.assertAlmostEqual(computed.values[1], 24.532293220408672901489, places=10)   
        self.assertEqual(computed.name,'AsinhMag_R')
        
        computed_i = AsinhMag('AsinhMag_I','FLUX_I',b=1E-10, zero_point=3.631E9,features=self.dataset)
        
        self.assertAlmostEqual(computed_i.values[0], 24.1031845539137647366657846119601, places=10)   
        self.assertAlmostEqual(computed_i.values[1], 23.6908109128280433547265431865470, places=10)   
        
    def test_color(self):
        computed = Color('COLOR_RI','MAG_I','MAG_R',features=self.dataset)
  
        self.assertAlmostEqual(computed.values[0], 0.143861, places=5)
        self.assertAlmostEqual(computed.values[1], 1.335613, places=5)        
        self.assertEqual(computed.name,'COLOR_RI')
    
    def test_asinhColor(self):
        computed = AsinhColor('ASINH_COLOR_RI','FLUX_I','FLUX_R',b=1E-10, zero_point=3.631E9,features=self.dataset)
  
        self.assertAlmostEqual(computed.values[0], 0.09404202093, places=5)
        self.assertAlmostEqual(computed.values[1], 0.84148230758, places=5)        
        self.assertEqual(computed.name,'ASINH_COLOR_RI')
        
    def test_fluxRatio(self):
        computed = FluxRatio('ratio_RI','FLUX_I','FLUX_R',features=self.dataset)
  
        self.assertAlmostEqual(computed.values[0], 0.87590216103, places=5)
        self.assertAlmostEqual(computed.values[1], 0.29225002376, places=5)        
        self.assertEqual(computed.name,'ratio_RI')
   

if __name__ == '__main__':
    unittest.main()
