#!/usr/bin/python
# coding: utf-8

from setuptools import setup
__author__ = "Chirag Vashist"
setup(
    name='huffman-zip',
    version='0.0.1',
    description='File Compressor based on Huffman Algorithm.',
    author='Chirag Vashist',
    author_email='chiragvashist007@gmail.com',
    license='GNU',
    url='https://github.com/SerChirag/huffman-zip',
    packages=['hzip'],
    entry_points={
        'console_scripts' : ['hzip=hzip:main',]
    },
)