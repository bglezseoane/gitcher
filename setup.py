# -*- coding: utf-8 -*-

###########################################################
# Gitcher 3.2 (Setup file)
#
# The git profile switcher
#
# Copyright 2019-2020 Borja González Seoane
#
# Contact: garaje@glezseoane.es
###########################################################

from setuptools import setup


setup(
    name='gitcher',
    version='3.2',
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
    url='https://github.com/bglezseoane/gitcher',
    download_url='https://github.com/bglezseoane/gitcher/archive/v3.2.tar.gz',
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
