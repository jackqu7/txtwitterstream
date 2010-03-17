#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name="txTwitterStream",
    version="0.0.2",
    description="A fork of Alexandre Fiori's TwistedTwitterStream Twitter client library for the Twitter Streaming API",
    author="Wade Simmons",
    url="http://github.com/wadey/txtwitterstream",
    py_modules=["txtwitterstream"],
    install_requires=["twisted >= 9.0.0"],
)
