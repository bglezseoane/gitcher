# -*- coding: utf-8 -*-


"""gitcher setup module"""

from setuptools import setup

# Authorship
__author__ = 'Borja González Seoane'
__copyright__ = 'Copyright 2019, Borja González Seoane'
__credits__ = 'Borja González Seoane'
__license__ = 'LICENSE'
__version__ = '3.0'
__maintainer__ = 'Borja González Seoane'
__email__ = 'garaje@glezseoane.es'
__status__ = 'Production'


setup(
    name='gitcher',
    version='3.0',
    packages=['gitcher'],
    entry_points={
        'console_scripts': [
            'gitcher=gitcher.__main__:main',
        ],
    },
    python_requires='>=3.6',
    install_requires=['validate_email==1.3', 'prettytable==0.7.2'],
    data_files=[('share/man/man1', ['manpages/gitcher.1']),
                ("", ["LICENSE"])],
    url='https://github.com/glezseoane/gitcher',
    download_url='https://github.com/GlezSeoane/gitcher/archive/v3.0.tar.gz',
    license='LICENSE',
    author='Borja González Seoane',
    author_email='garaje@glezseoane.es',
    description='The git profile switcher.',
    long_description='The git profile switcher. It facilitates the switching '
                     'between git profiles, importing configuration settings '
                     'such as name, email and user signatures.',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Topic :: Software Development :: Version Control',
        'Topic :: Software Development :: Version Control :: Git'
    ],
)
