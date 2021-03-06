# adapted from https://github.com/neurodata/primitives-interfaces/blob/master/setup.py

import os
import sys
from setuptools import setup
from setuptools.command.install import install
from subprocess import check_output, call
from sys import platform

PACKAGE_NAME = 'graphstats'
MINIMUM_PYTHON_VERSION = 3, 6
VERSION = '0.0.1'

def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version_info < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {}.{}+ is required.".format(*MINIMUM_PYTHON_VERSION))


def read_package_variable(key):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join(PACKAGE_NAME, '__init__.py')
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(' ')
            if parts and parts[0] == key:
                return parts[-1].strip("'")
    assert False, "'{0}' not found in '{1}'".format(key, module_path)

check_python_version()
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description='Python interfaces for TA1 primitives',
    long_description='A library wrapping JHU\'s Python interfaces for the D3M program\'s TA1 primitives.',
    author='Disa Mhembere, Eric Bridgeford, Youngser Park, Heather G. Patsolic, Tyler M. Tomita, Jesse L. Patsolic',
    author_email="disa@jhu.edu",
    packages=[
              PACKAGE_NAME,
              #'ase',
              #'lcc',
              #'lse',
              #'dimselect',
              #'gclass',
              #'gclust',
              #'nonpar',
              #'numclust',
              #'ptr',
              #'omni',
              #'oocase',
              #'sgc',
              #'sgm',
              #'vnsgm'
    ],
    entry_points = {
        'd3m.primitives': [
            'AdjacencySpectralEmbedding=ase:AdjacencySpectralEmbedding',
            'LargestConnectedComponent=lcc:LargestConnectedComponent',
            'LaplacianSpectralEmbedding=lse:LaplacianSpectralEmbedding',
            'DimensionSelection=dimselect:DimensionSelection',
            'GaussianClassification=gclass:GaussianClassification',
            'GaussianClustering=gclust:GaussianClustering',
            'NonParametricClustering=nonpar:NonParametricClustering',
            'NumberOfClusters=numclust:NumberOfClusters',
            'OutOfCoreAdjacencySpectralEmbedding=oocase:OutOfCoreAdjacencySpectralEmbedding',
            'PassToRanks=ptr:PassToRanks',
            'SpectralGraphClustering=sgc:SpectralGraphClustering',
            'SeededGraphMatching=sgm:SeededGraphMatching',
            'VertexNominationSeededGraphMatching=vnsgm:VertexNominationSeededGraphMatching'
            ]
    },
    package_data = {'': ['*.r', '*.R']},
    include_package_data = True,
    install_requires=['typing', 'numpy', 'scipy','networkx',
        'python-igraph', 'rpy2', 'sklearn', 'jinja2', 'scipy', 'pandas'],
    url='https://github.com/hhelm10/grapstats',
)
