
from __future__ import division, absolute_import, print_function

__author__ = 'andrea tramacere'



#!/usr/bin/env python

from setuptools import setup, find_packages
import  glob



f = open("./requirements.txt",'r')
install_req=f.readlines()
f.close()


packs=find_packages(where='PrimalCore/python')
packs.extend(find_packages(where='PrimalInteractive/python'))

print ('packs',packs)


package_dir={"PrimalCore":'PrimalCore/python/PrimalCore'}
package_dir['PrimalInteractive']='PrimalInteractive/python/PrimalInteractive'

print ('package_dir',package_dir)



scripts_list=glob.glob('./PrimalInteractive/scripts/*')
setup(name='Primal',
      version=1.0,
      description='A Python Framework for Machine Learning (ML) applied to Photometric Redshift Estimation',
      author='Andrea Tramacere',
      author_email='andrea.tramacere@unige.ch',
      url='http://euclid-git.roe.ac.uk/SDC-CH/Primal_No_Elements',
      scripts=scripts_list,
      package_dir=package_dir,
      packages=packs,
      package_data={'../PrimalCore/auxdir':['PrimalCore/*']},
      install_requires=install_req,
)



