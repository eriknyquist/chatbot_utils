import unittest
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
README = os.path.join(HERE, "README.rst")
REQFILE = 'requirements.txt'

classifiers = [
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
]

long_description = ""
if os.path.isfile(README):
    with open(README, 'r') as f:
        long_description = f.read()

dependencies = []
if os.path.exists(REQFILE):
    with open(REQFILE, 'r') as fh:
        dependencies = fh.readlines()

setup(
    name='chatbot_utils',
    version='0.1',
    description=('Tools for creating chatbots'),
    long_description=long_description,
    url='http://github.com/eriknyquist/chatbot_utils',
    author='Erik Nyquist',
    author_email='eknyquist@gmail.com',
    license='Apache 2.0',
    install_requires=dependencies,
    packages=find_packages(),
    package_dir={'chatbot_utils':'chatbot_utils'},
)
