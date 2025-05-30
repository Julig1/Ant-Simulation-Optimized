from setuptools import setup
from Cython.Build import cythonize
import numpy as np

setup(
    ext_modules=cythonize("ant_simulation.pyx"),
    include_dirs=[np.get_include()]  # Add NumPy include path here
)
