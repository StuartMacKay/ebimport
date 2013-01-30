import os

from setuptools import setup, find_packages


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as fp:
        return fp.read()


setup(
    name='ebimport',
    version='0.2.0',
    description='Tools for loading records into eBird',
    long_description=read("README.rst"),
    author='Stuart MacKay',
    author_email='smackay@flagstonesoftware.com',
    url='http://pypi.python.org/pypi/ebimport/',
    license='GPL',
    packages=find_packages(),
    package_data={'ebimport': [
        'data/portugalaves/species.csv',
        'data/portugalaves/locations.csv']
    },
    scripts=['ebimport/bin/ebconvert'],
    keywords='eBird import csv',
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Natural Language :: English",
        "Topic :: Text Processing :: Filters",
    ],
    install_requires=[
        'pycli',
    ],
)
