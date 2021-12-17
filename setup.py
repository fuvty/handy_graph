#!/usr/bin/env python

# from distutils.core import setup
from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='handy_graph',
    version='0.1',
    description='Commonly used python graph processing tool by Tianyu Fu',
    author='Tianyu Fu',
    author_email='fuvty@outlook.com',
    url='https://github.com/fuvty/handy_graph.git',
    packages=setuptools.find_packages(),
    license='Apache-2.0',
    long_description=long_description,
    install_requires=['networkx'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)