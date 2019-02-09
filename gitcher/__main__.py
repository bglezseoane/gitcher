# -*- coding: utf-8 -*-


"""gitcher main

gitcher is a git switcher. It facilitates the switching
between git profiles, importing configuration settings such
as name, email and user signatures.
"""

import os

from validate_email import validate_email
from shutil import which
from prettytable import PrettyTable

from gitcher import model_layer
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

# Prompt styles
COLOR_BLUE = '\033[94m'
COLOR_BRI_BLUE = '\033[94;1m'
COLOR_CYAN = '\033[96;1m'
COLOR_GREEN = '\033[92m'
COLOR_RED = '\033[91m'
COLOR_BOLD = '\033[1m'
COLOR_RST = '\033[0m'  # Restore default prompt style

# Predefined messages
MSG_OK = "[" + COLOR_GREEN + "OK" + COLOR_RST + "]"
MSG_ERROR = "[" + COLOR_RED + "ERROR" + COLOR_RST + "]"


# ===============================================
# =             Auxiliary functions             =
# ===============================================

# noinspection PyShadowingNames
def print_prof_error(profname: str) -> None:
    """Function that prints a nonexistent gitcher profile error.

    :param profname: Name of the gitcher profile to operate with
    :type profname: str
    :return: None, print function
    """
    print(MSG_ERROR + " Profile {0} not exists. Try again...".format(profname))


def print_prof_list() -> None:
    """Function that prints the gitcher profile list.

    :return: None, print function
    """
    profs = model_layer.model_recuperate_profs()
    if profs:  # If profs is not empty
        profs_table = PrettyTable(['Prof', 'Name', 'Email',
                                   'GPG key', 'Autosign'])
        for prof in profs:
            profs_table.add_row(prof.__str__())

        print(profs_table)
    else:
        print("No gitcher profiles saved yet. Use 'a' option to add one.")


def listen(text: str) -> str:
    """Function that listen an user input, validates it, checks if it not a
    'q' (i.e.: quit escape command) and then canalize message to caller
    function.

    :param text: Name of the gitcher profile to operate with
    :type text: str
    :return: User reply after canalize question via 'input()' function.
    :rtype: str
    """
    reply = input(text)
    if reply == 'q':
        raise SystemExit
    elif ',' in reply:  # The comma (',') is an illegal char
        print(MSG_ERROR + " Do not use commas (','), is an illegal char here.")
        raise ValueError
    else:
        return reply


def yes_or_no(question: str) -> bool:
    """Function that requires a yes or no answer

    :param question: Yes or no question to the user
    :type question: str
    :return: User reply
    :rtype: bool
    """
    reply = str(listen(question + " (y|n): ")).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        print(MSG_ERROR + " Enter (y|n) answer...")
        yes_or_no(question)


# noinspection PyShadowingNames
def check_opt(opt: str) -> bool:
    """Function that checks the integrity of the listen option.

    :param opt: User input option
    :type opt: str
    :return: Confirmation about the validation of the option
    :rtype: bool
    """
    return opt == 's' or opt == 'g' or opt == 'a' or opt == 'd' or opt == 'q'


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
def check_profile(profname: str) -> bool:
    """Function that checks if a gitcher profile exists.

    :param profname: Name of the gitcher profile to operate with
    :type profname: str
    :return: Confirmation about the existence of gitcher profile required
    :rtype: bool
    """
    try:
        recover_prof(profname)
        return True
    except NotFoundProfError:
        return False  # If not finds prof


# noinspection PyShadowingNames
def recover_prof(profname: str) -> Prof:
    """Function that recovers a gitcher profile through a model query.

    Warnings:
        - CHERFILE can not content two profiles with the same name. The add
            function takes care of it.

    :param profname: Name of the gitcher profile to operate with
    :type profname: str
    :return: gitcher profile required
    :rtype: Prof
    :raise: NotFoundProfError
    """
    try:
        return model_layer.model_recuperate_prof(profname)
    except NotFoundProfError:
        raise NotFoundProfError


# ===============================================
# =                Main launchers               =
# ===============================================

# noinspection PyShadowingNames
def set_prof(profname: str) -> None:
    """Function that sets the selected profile locally.

    It is imperative that it be called from a directory with a git
    repository.

    :param profname: Name of the gitcher profile to operate with
    :type profname: str
    :return: None
    """
    if check_git_context():
        model_layer.model_switch_prof(profname)
        print(MSG_OK + " Switched to {0} profile.".format(profname))
    else:
        print(MSG_ERROR + " Current directory not contains a git repository.")


# noinspection PyShadowingNames
def set_prof_global(profname: str) -> None:
    """Function that sets the selected profile globally.

    It is not necessary to be called from a directory with a git repository.

    :param profname: Name of the gitcher profile to operate with
    :type profname: str
    :return: None
    """
    model_layer.model_switch_prof(profname, '--global')
    print(MSG_OK + " Set {0} as git default profile.".format(profname))


# noinspection PyShadowingNames
def add_prof() -> None:
    """Function that adds a new profile.

    :return: None
    """
    print("\nLets go to add a new gitcher profile...")

    profname = listen("Enter the profile name: ")
    while check_profile(profname):
        print(MSG_ERROR + " {0} yet exists. Change name...".format(profname))
        profname = listen("Enter profile name: ")

    name = listen("Enter the git user name: ")

    email = listen("Enter the git user email: ")
    while not validate_email(email):
        print(MSG_ERROR + " Invalid email format. Try again...".format(email))
        email = listen("Enter the git user email: ")

    if yes_or_no("Do you want to use a GPG sign key?"):
        signkey = listen("Enter the git user signkey: ")
        signpref = str(yes_or_no("Do you want to autocheck every commit?"))
    else:
        signkey = None
        signpref = False

    # Save it...
    prof = model_layer.Prof(profname, name, email, signkey, signpref)
    model_layer.model_save_profile(prof)


# noinspection PyShadowingNames
def delete_prof(profname: str) -> None:
    """Function that deletes the selected profile.

    :param profname: Name of the gitcher profile to operate with
    :type profname: str
    :return: None
    """
    if yes_or_no("Are you sure to delete {0}?".format(profname)):
        model_layer.model_delete_profile(profname)


# ===============================================
# =                     MAIN                    =
# ===============================================

def main() -> None:
    """Main launcher of gitcher program package.

    :return: None
    """
    print(COLOR_BRI_BLUE + "**** gitcher: a git profile switcher ****" +
          COLOR_RST)

    # First, check if CHERFILE exists and if not, propose to create it.
    cherfile = model_layer.CHERFILE
    if not os.path.exists(cherfile):
        print(MSG_ERROR + " {0} not exists and it is necessary.".format(
            cherfile))
        if yes_or_no("Do you want to create {0}?".format(cherfile)):
            open(cherfile, 'w')
            print(MSG_OK + " Gitcher config dotfile created. Go on...")
        else:
            print(MSG_ERROR + " Impossible to go on without gitcher dotfile.")
            exit(1)

    # Next, check if git is installed
    if not check_git_installed():
        print(
            MSG_ERROR + " git is not installed in this machine. Impossible to "
                        "continue.")
        exit(1)

    print("gitcher profiles list:")
    print_prof_list()
    print("\nOptions:")
    print(COLOR_CYAN + 's' + COLOR_RST + "    set a profile to current "
                                         "directory repository.")
    print(COLOR_CYAN + 'g' + COLOR_RST + "    set a profile as global "
                                         "git configuration.")
    print(COLOR_CYAN + 'a' + COLOR_RST + "    add a new profile.")
    print(COLOR_CYAN + 'd' + COLOR_RST + "    delete a profile.")
    print("\nUse " + COLOR_CYAN + 'q + ENTER' + COLOR_RST + " everywhere to "
                                                            "quit.\n")

    opt = listen("Option: ")
    while not check_opt(opt):
        print(MSG_ERROR + " Invalid opt! Use s|g|a|d. Type q to quit.")
        opt = listen("Enter option: ")

    if not opt == 'a':
        profname = listen("Select the desired profile entering its name: ")
        while not check_profile(profname):
            print_prof_error(profname)
            profname = listen("Enter profile name: ")

        if opt == 's':
            set_prof(profname)
        elif opt == 'g':
            set_prof_global(profname)
        else:
            delete_prof(profname)
    else:
        add_prof()


if __name__ == "__main__":
    main()
