import os
from setuptools import setup, find_packages

import sqlize_pg as pkg


def read(fname):
    """ Return content of specified file """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='sqlize-pg',
    version=pkg.__version__,
    author='Outernet Inc',
    author_email='apps@outernet.is',
    description='Lightweight SQL query builder',
    license='GPLv3',
    keywords='sql query builder',
    url='https://github.com/Outernet-project/sqlize-pg',
    packages=find_packages(),
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)
