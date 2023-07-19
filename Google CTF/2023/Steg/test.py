from setuptools import Extension
from setuptools import setup

encoder_module = Extension('encoder', sources=['encoder.c'])

setup(name = 'encoder',
      version = '1.0',
      description = 'An encoder module',
      ext_modules = [encoder_module]
)
