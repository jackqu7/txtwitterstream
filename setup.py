#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

trove_classifiers=[
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: BSD License",
    "License :: DFSG approved",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Topic :: Utilities",
    "Topic :: Software Development :: Libraries",
    ]

setup(
    name="txTwitterStream",
    version="0.0.2",
    description="A fork of Alexandre Fiori's TwistedTwitterStream Twitter client library for the Twitter Streaming API",
    author="Wade Simmons",
    author_email="wade@wades.im",
    url="http://github.com/wadey/txtwitterstream",
    py_modules=["txtwitterstream"],
    install_requires=["Twisted >= 9.0.0"],
    license = "BSD",
    classifiers=trove_classifiers,
    zip_safe = False, # We prefer unzipped for easier access.
)
