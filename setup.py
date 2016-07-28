from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='pyshadowcopy',
    version='0.0.1',
    description='Python class to work with Shadow Copy on Windows',
    long_description=long_description,
    url='https://github.com/sblosser/pyshadowcopy',
    author='sblosser',
    license='MIT',
    keywords=['Windows', 'VSS', 'win32'],
    py_modules=['vss'],
    install_requires=['pypiwin32'],
)
