# -*- coding: utf-8 -*-

###########################################################
# Gitcher 3.2
#
# The git profile switcher
#
# Copyright 2019-2020 Borja González Seoane
#
# Contact: garaje@glezseoane.es
###########################################################


"""Gitcher's model layer module

This module access and manipulate the 'CHERFILE', isolating this
operations to the rest of the program.
"""

import os
import subprocess
import operator
from os.path import expanduser
from shutil import which

from gitcher.prof import Prof
from gitcher.not_found_prof_error import NotFoundProfError

# Paths
HOME = expanduser('~')
CHERFILE = HOME + '/.cherfile'


# ===============================================
# =             CHERFILE model layer            =
# ===============================================

def check_cherfile() -> bool:
    """Function that checks if CHERFILE exists.

    :return: Confirmation about the existence of CHERFILE
    :rtype: bool
    """
    return os.path.exists(CHERFILE)


def create_cherfile() -> None:
    """Function that creates a CHERFILE.

    :return: None
    """
    open(CHERFILE, 'w')
    with open(CHERFILE, 'a') as f:
        print("####################\n"
              "# GITCHER CHERFILE #\n"
              "####################\n", file=f)


def recuperate_profs() -> [Prof]:
    """Function that access CHERFILE and extracts profiles to Prof objects
    list. If there are not gitcher profiles in CHERFILE, returns an empty list.
    This function sorts profiles on alphabetical order looking its profname
    value.

    :return: A sort list with all gitcher profiles saved
    :rtype: [Prof]
    """
    profs = list()
    f = open(CHERFILE, 'r')
    lines = filter(None, (line.rstrip() for line in f))  # Not empty lines
    lines = [line for line in lines if not line.startswith('#')]  # Not comment
    for line in lines:
        profname = line.split(",")[0]
        name = line.split(",")[1]
        email = line.split(",")[2]
        signkey = line.split(",")[3]
        signpref = line.split(",")[4].split("\n")[0]

        # Type conversions
        if signkey == "None":
            signkey = None
        signpref = (signpref == "True")

        prof = Prof(profname, name, email, signkey, signpref)
        profs.append(prof)

    return sorted(profs, key=operator.attrgetter('profname'))


def recuperate_prof(profname: str) -> Prof:
    """ Function that return the required gitcher profile. If it does not
    exist, raise a not found exception.

    :param profname: Name of the gitcher profile to operate with
    :type profname: str
    :return: The required profile
    :rtype: Prof
    :raise: NotFoundProfError
    """
    profs = recuperate_profs()
    for prof in profs:
        if prof.profname == profname:
            return prof

    raise NotFoundProfError  # If not founds profile and not returns before


def save_profile(prof: Prof) -> None:
    """ Function that saves a new gitcher profile to the CHERFILE.

    :param prof: Gitcher profile to save
    :type prof: str
    :return: None
    """
    prof = [prof.profname, prof.name, prof.email, str(prof.signkey),
            str(prof.signpref)]
    prof_string = ','.join(prof)
    with open(CHERFILE, 'a') as f:
        print(prof_string, file=f)


def delete_profile(profname: str) -> None:
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


# ===============================================
# =               Git model layer               =
# ===============================================

def check_git_installed() -> bool:
    """Function that checks if git command is installed and reachable.

    :return: Confirmation about the reachability of git command installation
    :rtype: bool
    """
    return which("git") is not None


def check_git_context() -> bool:
    """Function that checks if the current directory have a git repository.

    :return: Confirmation about the presence of a git repository in the
        current directory
    :rtype: bool    """
    cwd = os.getcwd()
    return os.path.exists(cwd + "/.git")


# noinspection PyShadowingNames
def switch_prof(profname: str, path: str = None, flag: str = '') -> None:
    """Function that plays the git profile switching.

    This function can receive a '--global' flag to switch profile globally.

    :param profname: Name of the gitcher profile to operate with
    :type profname: str
    :param path: The optional specified repository path
    :type path: str
    :param flag: With '--global' flag switch profile globally
    :type flag: str
    :return: None
    """
    if not path:
        path = os.getcwd()  #  Current working directory path
    prof = recuperate_prof(profname)

    go_to_cwd = "cd '{0}' && ".format(path)
    if flag == '--global':
        go_to_cwd = ""

    cmd = "{0}git config {1} user.name '{2}'".format(go_to_cwd, flag,
                                                     prof.name)
    os.system(cmd)

    cmd = "{0}git config {1} user.email {2}".format(go_to_cwd, flag,
                                                    prof.email)
    os.system(cmd)

    if prof.signkey is not None:
        cmd = "{0}git config {1} user.signingkey {2}". \
            format(go_to_cwd, flag, prof.signkey)
        os.system(cmd)
    else:
        cmd = "{0}git config {1} --unset user.signingkey". \
            format(go_to_cwd, flag)
        os.system(cmd)

    # Is necessary to run next command even preference is false because
    # 	it would be necessary overwrite git global criteria.
    cmd = "{0}git config {1} commit.gpgsign {2}". \
        format(go_to_cwd, flag, str(prof.signpref).lower())
    os.system(cmd)


def recuperate_git_current_prof(path: str = None) -> Prof:
    """Function that recuperates the applicable git configuration of the
    param passed path and builds with this data a gitcher Prof. If param
    passed is None, then use the current working directory to evaluate it.

    Warnings:
        - The path must be assert before or function raises an error.

    :param path: Path to recuperates git user configuration
    :type path: str
    :return: Rebuilt git profile as gitcher Prof object
    :rtype: Prof
    """
    if path is None:
        path = os.getcwd()
    go_to_path = "cd '{0}' && ".format(path)

    with subprocess.Popen(go_to_path + "git config user.name",
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          shell=True) as p:
        output, errors = p.communicate()
    name = output.decode('utf-8').split("\n")[0]

    with subprocess.Popen(go_to_path + "git config user.email",
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          shell=True) as p:
        output, errors = p.communicate()
    email = output.decode('utf-8').split("\n")[0]

    with subprocess.Popen(go_to_path + "git config user.signingKey",
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          shell=True) as p:
        output, errors = p.communicate()
    signkey = output.decode('utf-8').split("\n")[0]

    with subprocess.Popen(go_to_path + "git config commit.gpgsign",
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          shell=True) as p:
        output, errors = p.communicate()
    signpref = output.decode('utf-8').split("\n")[0]

    # Validations
    if signkey == "":
        signkey = None

    if signpref == "true":
        signpref = True
    elif signpref == "false":
        signpref = False

    return Prof('tmp', name, email, signkey, signpref)
