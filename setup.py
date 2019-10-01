#!/usr/bin/env python
# coding=utf-8

from setuptools import find_packages, setup
from SecretChat import VERSION

setup(
        name='SecretChat',
        version=VERSION,
        url='git@github.com:Ro0tk1t/SecretChat.git',
        author='ro0tk1t',
        packages=find_packages(),
        python_requires='>=3.6',
        include_package_data=True,

        install_requires=[
            'flask>=1.1.0',
            'flask-login',
            'flask-mongoengine',
            'flask-sqlalchemy',
            'flask-bootstrap',
            'flask-principal',
            'flask-bcrypt',
            ],

        extras_require={
            'build': [
                'nosetest',
                ]
            }
        )
