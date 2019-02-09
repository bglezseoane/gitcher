# -*- coding: utf-8 -*-


"""gitcher model layer module

This module access and manipulate the CHERFILE, isolating this operations to
the rest of the program. """

from os.path import expanduser

from gitcher.prof import Prof
from gitcher.not_found_prof_error import NotFoundProfError

# Authorship
__author__ = 'Borja González Seoane'
__copyright__ = 'Copyright 2019, Borja González Seoane'
__credits__ = 'Borja González Seoane'
__license__ = 'LICENSE'
__version__ = '0.2a1'
__maintainer__ = 'Borja González Seoane'
__email__ = 'dev@glezseoane.com'
__status__ = 'Development'

# Paths
HOME = expanduser('~')
CHERFILE = HOME + '/.cherfile'


def model_recuperate_profs() -> [Prof]:
    """Function that access CHERFILE and extracts profiles to Prof objects
    list. If there are not gitcher profiles in CHERFILE, returns an empty list.

    :return: A list with all gitcher profiles saved.
    :rtype: [Prof]
    """
    profs = list()
    f = open(CHERFILE, 'r')
    for line in f:
        if not line.startswith('#'):  # Comment line
            profname = line.split(",")[0]
            name = line.split(",")[1]
            email = line.split(",")[2]
            signkey = line.split(",")[3]
            signpref = line.split(",")[4]

            # Type conversions
            if signkey == "None":
                signkey = None
            signpref = bool(signpref)

            prof = Prof(profname, name, email, signkey, signpref)
            profs.append(prof)

    return profs


def model_recuperate_prof(profname: str) -> Prof:
    """ Function that return the required gitcher profile. If it does not
    exist, raise a not found exception.

    :param profname: Name of the gitcher profile to operate with
    :type profname: str
    :return: The required profile
    :rtype: Prof
    :raise: NotFoundProfError
    """
    profs = model_recuperate_profs()
    for prof in profs:
        if prof.profname == profname:
            return prof

    raise NotFoundProfError  # If not founds profile and not returns before


def model_save_profile(prof: Prof) -> None:
    """ Function that saves a new gitcher profile to the CHERFILE.

    :param prof: Gitcher profile to save
    :type prof: str
    :return: None
    """
    prof = [prof.profname, prof.name, prof.email, prof.signkey, prof.signpref]
    prof_string = ','.join(prof)
    with open(CHERFILE, 'a') as f:
        print(prof_string, file=f)


def model_delete_profile(profname: str) -> None:
    """ Function that deletes a gitcher profile from the CHERFILE.

    :param profname: Name of the gitcher profile to operate with
    :type profname: str
    :return: None
    """
    f = open(CHERFILE, 'r+')  # Read and write mode
    lines = f.readlines()
    lines = [line.strip('\n') for line in lines]
    f.seek(0)  # Return to the start of the file
    for line in lines:
        if line.split(',')[0] != profname:
            print(line, file=f)
    f.truncate()  # Delete possible dirty lines below
    f.close()
