#!/usr/bin/env python3
'''
curve_fit_gui setup config
'''
import os
from setuptools import setup

here = os.path.dirname(__file__)

about = {}
with open(os.path.join(here, 'python_package_template', '__about__.py')) as fobj:
    exec(fobj.read(), about)

setup(
    name='curve_fit_gui',
    version='0.1.0',
    packages=[
        'curve_fit_gui',
    ],
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib'
    ],
    include_package_data=True,
    author='Maxime Bouton',
    author_email='maxim.bouton@gmail.com',
    maintainer='Maxime Bouton',
    maintainer_email='maxim.bouton@gmail.com',
    description="GUI to select points for curve fitting",
    url='https://github.com/MaximeBouton/curve_fit_gui'
)
