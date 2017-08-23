import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('reversegear/reversegear.py').read(),
    re.M
    ).group(1)

with open('README.rst', 'rb') as f:
    long_descr = f.read().decode('utf-8')
    
setup(
    name = 'reversegear',
    entry_points = {
        'console_scripts': ['reversegear = reversegear.reversegear:main']
    },
    packages = ['reversegear'],
    py_modules = ['reversegear'],
    version = version,
    description = 'Offline reverse engineering tools for automotive networks.',
    long_description = long_descr,
    author = 'Eric Evenchick',
    author_email = 'eric@evenchick.com',
    install_requires = [
        'pyvit',
    ],
)
