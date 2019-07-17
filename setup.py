# -*- coding: utf-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="ChangeCoordinate",
    version="1.1",
    author="GrayLea",
    author_email="graylea@163.com",
    description="百度/高德的坐标转换(仅适用于中国)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/GaryLea/ChangeCoordinate.git",
    packages=find_packages(),
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)

