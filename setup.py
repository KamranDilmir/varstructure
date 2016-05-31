# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='varstructure',
    version='0.0.1',
    description='varstructure package',
    long_description=readme,
    author='Kamran Dilmir',
    author_email='m.dilmir@unimelb.edu.au',
    url='https://github.com/KamranDilmir/varstructure',
    license=license,
    entry_points={
        'console_scripts': ['varstructure = varstructure.core:main']
    },
    packages=find_packages(exclude=('tests', 'docs'))
)
