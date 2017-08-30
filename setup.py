import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*\'(.*)\'',
    open('reversegear/reversegear.py').read(),
    re.M
    ).group(1)

setup(
    name='reversegear',
    entry_points={
        'console_scripts': ['reversegear = reversegear.reversegear:main']
    },
    packages=['reversegear'],
    py_modules=['reversegear'],
    version=version,
    description='Offline reverse engineering tools for automotive networks.',
    long_description='See: https://github.com/linklayer/reversegear/blob/master/README.rst',
    author='Eric Evenchick',
    author_email='eric@evenchick.com',
    install_requires=[
        'pyvit',
    ],
    keywords=['networks', 'automotive', 'reverse engineering'],
    download_url=('https://github.com/linklayer/reversegear/archive/%s.tar.gz'
                  % version)
)
