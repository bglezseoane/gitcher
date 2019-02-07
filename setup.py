# -*- coding: utf-8 -*-


"""gitcher setup module"""

from setuptools import setup

# Authorshipen
__author__ = "Borja González Seoane"
__copyright__ = "Copyright 2019, Borja González Seoane"
__credits__ = "Borja González Seoane"
__license__ = "GPL-3.0"
__version__ = "0.1a0"
__maintainer__ = "Borja González Seoane"
__email__ = "dev@glezseoane.com"
__status__ = "Development"


setup(
    name='gitcher',
    version='0.1a0',
    packages=[''],
    url='https://gitlab.com/GlezSeoane/gitcher',
    license='GPL-3.0',
    author='Borja González Seoane',
    author_email='dev@glezseoane.com',
    description='A git switcher.',
    long_description=['A git switcher. It facilitates the switching between '
                      'git profiles,importing configuration settings such as'
                      'name, email and user signatures.'],
    scripts=['gitcher.py'],
    install_requires=['validate_email']
)
