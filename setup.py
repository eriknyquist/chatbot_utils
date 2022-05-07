import unittest
import os
from setuptools import setup, find_packages
from distutils.core import Command

from chatbot_utils import __version__


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

class TestRunner(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        suite = unittest.TestLoader().discover("tests")
        t = unittest.TextTestRunner(verbosity = 2)
        t.run(suite)

setup(
    name='chatbot_utils',
    version=__version__,
    description=('Tools for creating chatbots'),
    long_description=long_description.strip(),
    url='http://github.com/eriknyquist/chatbot_utils',
    author='Erik Nyquist',
    author_email='eknyquist@gmail.com',
    license='Apache 2.0',
    install_requires=dependencies,
    packages=find_packages(),
    package_dir={'chatbot_utils':'chatbot_utils'},
    cmdclass={'test': TestRunner}
)
