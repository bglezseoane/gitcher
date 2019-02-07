# -*- coding: utf-8 -*-


"""gitcher setup module"""

from distutils.core import setup

# Authorship
__author__ = 'Borja González Seoane'
__copyright__ = 'Copyright 2019, Borja González Seoane'
__credits__ = 'Borja González Seoane'
__license__ = 'LICENSE'
__version__ = '0.1a1'
__maintainer__ = 'Borja González Seoane'
__email__ = 'dev@glezseoane.com'
__status__ = 'Development'


setup(
    name='gitcher',
    version='0.1a1',
    packages=['gitcher'],
    url='https://gitlab.com/GlezSeoane/gitcher',
    license='LICENSE',
    author='Borja González Seoane',
    author_email='dev@glezseoane.com',
    description='A git switcher.',
    long_description='A git switcher. It facilitates the switching between '
                     'git profiles,importing configuration settings such as '
                     'name email and user signatures.',
    install_requires=['validate_email']
)
