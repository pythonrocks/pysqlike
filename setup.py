"""A setuptools based setup module for pysqlike.
"""


from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pysqlike',
    version='0.1.4',
    description='Native python sqlite-like db implementation for learning purposes.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pythonrocks/pysqlike',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6, <4',
    project_urls={
        'Source': 'https://github.com/pythonrocks/pysqlike',
    },
)
