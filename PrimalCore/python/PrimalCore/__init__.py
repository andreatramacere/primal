'''
Definition of a python package using extend_path
to create a namespace

Created on Apr 29, 2016

author: hubert
'''

# copyright: 2012-2020 Euclid Science Ground Segment
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3.0 of the License, or (at your option)
# any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA


from __future__ import absolute_import, division, print_function


from os import path


import pkgutil
__path__ = pkgutil.extend_path(__path__, __name__)  # @ReservedAssignment

__all__=[]

pkg_dir = path.abspath(path.dirname(__file__))
pkg_name = path.basename(pkg_dir)

for importer, modname, ispkg in pkgutil.walk_packages(path=[pkg_dir],
                                                      prefix=pkg_name+'.' ,
                                                      onerror=lambda x: None):
    if ispkg == True:
        __all__.append(modname)
    else:
        pass

print(__all__)