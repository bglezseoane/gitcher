# -*- coding: utf-8 -*-


"""gitcher main

gitcher is a git switcher. It facilitates the switching
between git profiles, importing configuration settings such
as name, email and user signatures.
"""

import os
import sys

from validate_email import validate_email
from prettytable import PrettyTable

from gitcher import model_layer
from gitcher.prof import Prof
from gitcher.not_found_prof_error import NotFoundProfError

# Authorship
__author__ = 'Borja González Seoane'
__copyright__ = 'Copyright 2019, Borja González Seoane'
__credits__ = 'Borja González Seoane'
__license__ = 'LICENSE'
__version__ = '0.3b0'
__maintainer__ = 'Borja González Seoane'
__email__ = 'dev@glezseoane.com'
__status__ = 'Development'

# Prompt styles
COLOR_BLUE = '\033[94m'
COLOR_BRI_BLUE = '\033[94;1m'
COLOR_CYAN = '\033[96m'
COLOR_BRI_CYAN = '\033[96;1m'
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


def raise_order_format_error(arg: str = None) -> None:
    """Function that prints a command line format error advise and raises an
    exception. If arg is not specified, the function prints a complete order
    format error. If yes, raises an error advising the concrete argument
    implicated.

    :param arg: Implicated argument
    :type arg: str
    :return: None, print function
    :raise SyntaxErrorr: Raise error by a bad order compose.
    """
    if arg is not None:
        adv = "Check param {0} syntax!".format(arg)
        print(MSG_ERROR + " " + adv)
    else:
        adv = "Check order syntax composition!"
        print(MSG_ERROR + " " + adv)
    sys.exit(adv)


def print_prof_list() -> None:
    """Function that prints the gitcher profile list.

    :return: None, print function
    """
    cprof = model_layer.model_recuperate_git_current_prof()  # Current profile
    profs = model_layer.model_recuperate_profs()
    if profs:  # If profs is not empty
        profs_table = PrettyTable(['Prof', 'Name', 'Email',
                                   'GPG key', 'Autosign'])
        for prof in profs:
            row = prof.__tpl__()
            if prof.equivalent(cprof):
                row = [(COLOR_CYAN + profeat + COLOR_RST) for profeat in row]
                row[0] = row[0] + "*"
            profs_table.add_row(row)

        print(profs_table)
        print("*: current in use gitcher profile.")
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
        sys.exit(0)
    try:
        check_syntax(reply)
    except SyntaxError:
        listen(text)  # Recursive loop to have a valid value
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


def check_syntax(arg: str) -> None:
    """Check strings syntax. Gitcher does not avoid to use commas ','
    in string values.

    :param arg: Argument to check syntax
    :type arg: str
    :return: True or false
    :rtype: bool
    :raise SyntaxError: If arg is illegal
    """
    if ',' in arg:  # The comma (',') is an illegal char
        print(MSG_ERROR + " Do not use commas (','), is an illegal char here.")
        raise SyntaxError("Do not use commas (',')")


# noinspection PyShadowingNames
def check_opt(opt: str) -> bool:
    """Function that checks the integrity of the listen option.

    :param opt: User input option
    :type opt: str
    :return: Confirmation about the validation of the option
    :rtype: bool
    """
    return opt == 's' or opt == 'g' or opt == 'a' or opt == 'u' or opt == 'd'\
        or opt == 'q'


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
    repository. Profile name must be checked before.

    :param profname: Name of the gitcher profile to operate with
    :type profname: str
    :return: None
    """
    if model_layer.check_git_context():
        model_layer.model_switch_prof(profname)
        print(MSG_OK + " Switched to {0} profile.".format(profname))
    else:
        print(MSG_ERROR + " Current directory not contains a git repository.")


# noinspection PyShadowingNames
def set_prof_global(profname: str) -> None:
    """Function that sets the selected profile globally.

    It is not necessary to be called from a directory with a git repository.
    Profile name must be checked before.

    :param profname: Name of the gitcher profile to operate with
    :type profname: str
    :return: None
    """
    model_layer.model_switch_prof(profname, '--global')
    print(MSG_OK + " Set {0} as git default profile.".format(profname))


# noinspection PyShadowingNames
def add_prof() -> None:
    """Function that adds a new profile on interactive mode. Profile name
    have not to be checked before.

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
        signpref = yes_or_no("Do you want to autosign every commit?")
    else:
        signkey = None
        signpref = False

    # Save it...
    prof = model_layer.Prof(profname, name, email, signkey, signpref)
    model_layer.model_save_profile(prof)
    print(MSG_OK + " New profile {0} added.".format(profname))


# noinspection PyShadowingNames
def add_prof_fast(profname: str, name: str, email: str, signkey: str,
                  signpref: bool) -> None:
    """Function that adds a new profile on fast mode. Profile name have not
    to be checked before.

    :param profname:
    :type profname: str
    :param name:
    :type name: str
    :param email:
    :type email: str
    :param signkey:
    :type signkey: str
    :param signpref:
    :type signpref: bool
    :return: None
    """
    if not check_profile(profname):  # Profname have to be unique
        prof = model_layer.Prof(profname, name, email, signkey, signpref)
        model_layer.model_save_profile(prof)
        print(MSG_OK + " New profile {0} added.".format(profname))
    else:
        print(MSG_ERROR + " {0} yet exists!".format(profname))
        sys.exit("gitcher profile name already in use")


# noinspection PyShadowingNames
def delete_prof(profname: str) -> None:
    """Function that deletes the selected profile.

    Profile name must be checked before.

    :param profname: Name of the gitcher profile to operate with
    :type profname: [str]
    :return: None
    """
    model_layer.model_delete_profile(profname)
    print(MSG_OK + " Profile {0} deleted.".format(profname))


# noinspection PyShadowingNames
def update_prof() -> None:
    """Function that updates a profile on interactive mode. Profile name
    have not to be checked before.

    :return: None
    """
    print("\nLets go to update a gitcher profile...")

    old_profname = listen("Enter the profile name: ")
    while not check_profile(old_profname):
        print(MSG_ERROR + " {0} not exists. Change name...".format(
            old_profname))
        old_profname = listen("Enter profile name: ")

    prof = model_layer.model_recuperate_prof(old_profname)

    profname = old_profname
    if yes_or_no("Do you want to update the profile name?"):
        profname = listen("Enter the new profile name: ")
    name = prof.name
    if yes_or_no("Do you want to update the user name?"):
        name = listen("Enter the new name: ")
    email = prof.email
    if yes_or_no("Do you want to update the user email?"):
        email = listen("Enter the new email: ")
        while not validate_email(email):
            print(MSG_ERROR + " Invalid email format. Try again...".format(
                email))
            email = listen("Enter the new email: ")
    if yes_or_no("Do you want to update the GPG sign config?"):
        if yes_or_no("Do you want to use a GPG sign key?"):
            signkey = listen("Enter the git user signkey: ")
            signpref = yes_or_no("Do you want to autosign every commit?")
        else:
            signkey = None
            signpref = False
    else:
        signkey = prof.signkey
        signpref = prof.signpref

    # Remove the old profile
    model_layer.model_delete_profile(old_profname)
    # And save the new...
    prof = model_layer.Prof(profname, name, email, signkey, signpref)
    model_layer.model_save_profile(prof)
    print(MSG_OK + " Profile {0} updated.".format(profname))


# ===============================================
# =                     MAIN                    =
# ===============================================

def interactive_main() -> None:
    """Main launcher of gitcher program interactive mode. Dialogue with the
    user.

    :return: None
    """
    print(COLOR_BRI_BLUE + "**** gitcher: a git profile switcher ****" +
          COLOR_RST)

    print("gitcher profiles list:")
    print_prof_list()
    print("\nOptions:")
    print(COLOR_BRI_CYAN + "s" + COLOR_RST + "    set a profile to current "
                                             "directory repository.")
    print(COLOR_BRI_CYAN + "g" + COLOR_RST + "    set a profile as global "
                                             "git configuration.")
    print(COLOR_BRI_CYAN + "a" + COLOR_RST + "    add a new profile.")
    print(COLOR_BRI_CYAN + "u" + COLOR_RST + "    update a profile.")
    print(COLOR_BRI_CYAN + "d" + COLOR_RST + "    delete a profile.")
    print(
        "\nUse " + COLOR_BRI_CYAN + "q + ENTER" + COLOR_RST + " everywhere to "
                                                              "quit.\n")

    opt = listen("Option: ")
    while not check_opt(opt):
        print(MSG_ERROR + " Invalid opt! Use s|g|a|d. Type q to quit.")
        opt = listen("Enter option: ")

    if not opt == 'a' and not opt == 'u':
        profname = listen("Select the desired profile entering its name: ")
        while not check_profile(profname):
            print_prof_error(profname)
            profname = listen("Enter profile name: ")

        if opt == 's':
            set_prof(profname)
        elif opt == 'g':
            set_prof_global(profname)
        else:  # Option 'd'
            if yes_or_no("Are you sure to delete {0}?".format(profname)):
                delete_prof(profname)
    else:
        if opt == 'a':
            add_prof()
        else:  # Option 'u'
            update_prof()


def fast_main(cmd: [str]) -> None:
    """Runs fast passed options after to do necessary checks.

    :param cmd: Command line order by the user
    :type cmd: [str]
    :return: None
    """
    # First, check param syntax
    for param in cmd:
        try:
            check_syntax(param)
        except SyntaxError:
            sys.exit("Syntax error")

    # If syntax is okey, go on and check selected option
    opt = cmd[1].replace('-', '')
    if not check_opt(opt):
        print(MSG_ERROR + " Invalid option! Use -s|-g|-a|-d.")
        sys.exit("Invalid option")
    else:
        if len(cmd) < 3:  # cmd have to be 'gitcher <-opt> <profname> [
            # ...]'
            raise_order_format_error()
        # Catch profname, first parameter for all cases
        profname = cmd[2]

        if opt == 'a':
            if len(cmd) != 7:  # cmd have to be 'gitcher <-opt> <profname>
                # <name> <email> <signkey> <signpref>'
                raise_order_format_error()
            # Catch specific params
            name = cmd[3]
            email = cmd[4]
            if not validate_email(email):
                raise_order_format_error(email)
            signkey = cmd[5]
            if signkey == 'None':
                signkey = None
            signpref = cmd[6]
            if signpref == 'True':
                signpref = True
            elif signpref == 'False':
                signpref = False
            else:
                raise_order_format_error(cmd[5])

            add_prof_fast(profname, name, email, signkey, signpref)
        else:
            if not check_profile(profname):
                print_prof_error(profname)
                sys.exit("gitcher profile not exists")
            # Else, if the profile exists, continue...
            if opt == 's':
                set_prof(profname)
            elif opt == 'g':
                set_prof_global(profname)
            elif opt == 'd':
                delete_prof(profname)


if __name__ == "__main__":
    # First, check if git is installed
    if not model_layer.check_git_installed():
        print(
            MSG_ERROR + " git is not installed in this machine. Impossible to "
                        "continue.")
        sys.exit("git is not installed")

    # Next, check if CHERFILE exists. If not and gitcher is ran as
    # interactive mode, propose to create it
    cherfile = model_layer.CHERFILE
    if not os.path.exists(cherfile):
        print(MSG_ERROR + " {0} not exists and it is necessary.".format(
            cherfile))

        if (len(sys.argv)) > 1:
            if yes_or_no("Do you want to create {0}?".format(cherfile)):
                open(cherfile, 'w')
                print(MSG_OK + " Gitcher config dotfile created. Go on...")
            else:
                print(MSG_ERROR + "Impossible to go on without gitcher "
                                  "dotfile.")
                sys.exit("No gitcher file")
        else:
            sys.exit("No gitcher file")

    # After firsts checks, run gitcher
    if (len(sys.argv)) == 1:  # Interactive mode
        interactive_main()
    elif (len(sys.argv)) > 1:  # Fast mode
        fast_main(sys.argv)
