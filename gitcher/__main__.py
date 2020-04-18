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

"""Gitcher's main."""

import os
import readline
import signal
import sys

from validate_email import validate_email
from prettytable import PrettyTable

from gitcher import model_layer, dictionary
from gitcher.completer import TabCompleter
from gitcher.prof import Prof
from gitcher.not_found_prof_error import NotFoundProfError

# Prompt styles
COLOR_BLUE = '\033[94m'
COLOR_BRI_BLUE = '\033[94;1m'
COLOR_CYAN = '\033[96m'
COLOR_BRI_CYAN = '\033[96;1m'
COLOR_GREEN = '\033[92m'
COLOR_RED = '\033[91m'
COLOR_YELLOW = '\033[93m'
COLOR_BOLD = '\033[1m'
COLOR_RST = '\033[0m'  # Restore default prompt style

# Predefined messages
MSG_OK = "[" + COLOR_GREEN + "OK" + COLOR_RST + "]"
MSG_ERROR = "[" + COLOR_RED + "ERROR" + COLOR_RST + "]"
MSG_WARNING = "[" + COLOR_YELLOW + "WARNING" + COLOR_RST + "]"


# ===============================================
# =             Initial validations             =
# ===============================================
# First, check if git is installed
if not model_layer.check_git_installed():
    print(
        MSG_ERROR + " git is not installed in this machine. Impossible to "
                    "continue.")
    sys.exit(1)

# Next, check if CHERFILE exists. If not, create it
if not model_layer.check_cherfile():
    model_layer.create_cherfile()
    print(MSG_OK + " Gitcher config dotfile created. Go on...")


# Unique global instance for the execution gitcher dictionary
dictionary = dictionary.Dictionary()


# ===============================================
# =             Auxiliary functions             =
# ===============================================
def quit_gracefully(signum, frame) -> None:
    """Function that prints a bye message. It is used to attach to escape
    signal (i.e.: Ctrl.+C) during the performance of the program. So, it
    is the exit function.

    :return: None, print function
    """
    print(COLOR_BLUE + "Bye!" + COLOR_RST)
    sys.exit(0)


# Register previous function, linking it with Ctrl.+C
signal.signal(signal.SIGINT, quit_gracefully)


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
    :raise SyntaxError: Raise error by a bad order compose.
    """
    if arg is not None:
        adv = "Check param {0} syntax!".format(arg)
        print(MSG_ERROR + " " + adv)
    else:
        adv = "Check order syntax composition!"
        print(MSG_ERROR + " " + adv)
    sys.exit(1)


def print_prof_list() -> None:
    """Function that prints the gitcher profile list.

    :return: None, print function
    """
    cprof = model_layer.recuperate_git_current_prof()  # Current profile
    profs = model_layer.recuperate_profs()
    if profs:  # If profs is not empty
        _, terminal_width = os.popen('stty size', 'r').read().split()
        terminal_width = int(terminal_width)

        """Catches the length of the largest compose profile to represent, 
        taking the length of the largest attribute of each column."""
        big_atts = ['', '', '', '', '']
        for prof in profs:
            if len(prof.profname) > len(big_atts[0]):
                big_atts[0] = prof.profname
            if len(prof.name) > len(big_atts[1]):
                big_atts[1] = prof.name
            if len(prof.email) > len(big_atts[2]):
                big_atts[2] = prof.email
            if len(str(prof.signkey)) > len(big_atts[3]):
                big_atts[3] = str(prof.signkey)
            if len(str(prof.signpref)) > len(big_atts[4]):
                big_atts[4] = str(prof.signpref)
        big_prof_len = len(''.join(big_atts))
        big_prof_len += 16  # Spaces and bars to separate attributes

        if terminal_width >= big_prof_len:  # Viable table representation
            """Switchs between table and list representations to avoid graphic 
            crashes. Compares the terminal width with the length of the biggest 
            profs list element."""
            profs_table = PrettyTable(['Prof', 'Name', 'Email',
                                       'PGP key', 'Autosign'])
            for prof in profs:
                row = prof.tpl()
                if prof == cprof:
                    row = [(COLOR_CYAN + profatt + COLOR_RST) for profatt in
                           row]
                    row[0] += "*"
                profs_table.add_row(row)
            print(profs_table)
            print("*: current in use gitcher profile.")
        else:  # Not viable table representation
            for prof in profs:
                if prof == cprof:
                    print("- " + COLOR_CYAN + prof.profname + ": " +
                          prof.simple_str() + COLOR_RST + " [CURRENT]")
                else:
                    print("- " + prof.profname + ": " + prof.simple_str())
    else:
        print("No gitcher profiles saved yet. Use 'a' option to add one.")


def listen(question: str = None, autocompletion_context: [str] = None) -> str:
    """Function that listen an user input, validates it and then canalize 
    message to caller function. This function also provides the support for 
    autocompletion. To use it, its neccesary to pass as second param the 
    context list of keys against match.

    :param question: Text of the question to the user
    :type question: str
    :param autocompletion_context: List of keys against match text to
        autocompletion. None to do not use this service
    :type autocompletion_context: [str]
    :return: User reply after canalize question via 'input()' function
    :rtype: str
    """
    if autocompletion_context:  # Set autocompletion set
        # Init autocompletion support
        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")
        completer = TabCompleter(autocompletion_context)
        readline.set_completer(completer.service)

    if question:
        reply = input(question).strip()
    else:
        reply = input().strip()

    if autocompletion_context:  # Clean autocompletion set
        # noinspection PyUnboundLocalVariable
        completer = TabCompleter([])
        readline.set_completer(completer.service)

    try:
        check_syntax(reply)
    except SyntaxError:
        listen(question)  # Recursive loop to have a valid value

    return reply


def yes_or_no(question: str) -> bool:
    """Function that requires a yes or no answer

    :param question: Yes or no question to the user
    :type question: str
    :return: User reply
    :rtype: bool
    """
    reply = str(listen(question + " (y|n): ",
                       autocompletion_context=['y', 'n'])).lower().strip()
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
def check_opt(opt_input: str,
              interactive_mode: bool = False,
              fast_mode: bool = False,
              whole: bool = False) -> bool:
    """Function that checks the integrity of the listen option. Options codes
    of the interactive and the fast mode can be passed.

    interactive_mode flag is to indicate that the check provides to an
    interactive_mode call.

    fast_mode flag is to indicate that the check provides to an fast_mode call.

    This flags act as switches to their respective modes. It is possible to
    combine various or even all modes simply by setting to True their
    respective flags. It is like the algebraic union operation.

    The whole flag traces the subscribed union of sets directly.

    Note that the default sets every flags to False, so the reply will be
    always False.

    :param opt_input: User input option
    :type opt_input: str
    :param fast_mode: Flag to indicate that the check is to validate from a
        fast mode call
    :type fast_mode: bool
    :param interactive_mode: Flag to indicate that the check is to validate
        from a interactive mode call
    :type interactive_mode: bool
    :param whole: Flag to check if the passed opt its valid for at least
        one of the modes
    :type whole: bool
    :return: Confirmation about the validation of the passed option
    :rtype: bool
    """
    opts_stock = []  # Initial empty

    # Expansions attending to config
    if whole:
        opts_stock.extend(dictionary.get_union_all())
    else:
        if interactive_mode:
            opts_stock.extend(dictionary.cmds_interactive_mode)
        if fast_mode:
            opts_stock.extend(dictionary.cmds_fast_mode)

    # Try to match
    if any(opt_input == opt_pattern for opt_pattern in opts_stock):
        return True
    else:
        return False


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
        return model_layer.recuperate_prof(profname)
    except NotFoundProfError:
        raise NotFoundProfError


# ===============================================
# =                Main launchers               =
# ===============================================

def list_profs() -> None:
    """Function that prints a list with saved profiles.

    :return: None, print function
    """
    profs = model_layer.recuperate_profs()
    if profs:  # If profs is not empty
        for prof in profs:
            print("Profile " + prof.profname + ": " + prof.simple_str())
    else:
        print("No gitcher profiles saved yet. Use 'a' option to add one.")


def show_current_on_prof() -> None:
    """Function that shows the current in use ON profile information.

    :return: None, print function
    """
    cprof = model_layer.recuperate_git_current_prof()  # Current profile

    # Now, cprof is compared against saved profiles list. cprof is an
    # extract of the git user configuration, that is independent of the
    # gitcher data and scope. So, with next operations it is checked if
    # current config is saved on gitcher, and it is created a mixed dataset to
    # print the information
    profs = model_layer.recuperate_profs()
    for prof in profs:
        if cprof == prof:
            print("Profile " + prof.profname + ": " + cprof.simple_str())
            return
    # If not found in list...
    print(MSG_OK + " Unsaved profile: " + cprof.simple_str())


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
        model_layer.switch_prof(profname)
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
    model_layer.switch_prof(profname, flag='--global')
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

    if yes_or_no("Do you want to use a PGP sign key?"):
        signkey = listen("Enter the git user signkey: ")
        signpref = yes_or_no("Do you want to autosign every commit?")
    else:
        signkey = None
        signpref = False

    # Save it...
    prof = model_layer.Prof(profname, name, email, signkey, signpref)
    model_layer.save_profile(prof)
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
        model_layer.save_profile(prof)
        print(MSG_OK + " New profile {0} added.".format(profname))
    else:
        print(MSG_ERROR + " {0} yet exists!".format(profname))
        sys.exit(1)


# noinspection PyShadowingNames
def update_prof() -> None:
    """Function that updates a profile on interactive mode. Profile name
    have not to be checked before.

    :return: None
    """
    print("\nLets go to update a gitcher profile...")

    old_profname = listen("Enter the profile name: ",
                          dictionary.profs_profnames)
    while not check_profile(old_profname):
        print(MSG_ERROR + " {0} not exists. Change name...".format(
            old_profname))
        old_profname = listen("Enter profile name: ",
                              dictionary.profs_profnames)

    prof = model_layer.recuperate_prof(old_profname)

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
    if yes_or_no("Do you want to update the PGP sign config?"):
        if yes_or_no("Do you want to use a PGP sign key?"):
            signkey = listen("Enter the git user signkey: ")
            signpref = yes_or_no("Do you want to autosign every commit?")
        else:
            signkey = None
            signpref = False
    else:
        signkey = prof.signkey
        signpref = prof.signpref

    # Remove the old profile
    model_layer.delete_profile(old_profname)
    # And save the new...
    prof = model_layer.Prof(profname, name, email, signkey, signpref)
    model_layer.save_profile(prof)
    print(MSG_OK + " Profile {0} updated.".format(profname))


# noinspection PyShadowingNames
def mirror_prof(origin_profname: str) -> None:
    """Function that mirrors a profile to create a duplicate of it.

    Profile name must be checked before.

    :param origin_profname: Name of the gitcher profile to operate with
    :type origin_profname: [str]
    :return: None
    """
    new_profname = listen("Enter the new profile name (can not be the same "
                          "that the origin profile): ")
    while check_profile(new_profname):
        print(MSG_ERROR + " {0} yet exists. Change name...".format(
            new_profname))
        new_profname = listen("Enter profile name: ")

    prof = model_layer.recuperate_prof(origin_profname)

    profname = new_profname
    name = prof.name
    email = prof.email
    signkey = prof.signkey
    signpref = prof.signpref

    # Save the new profile...
    prof = model_layer.Prof(profname, name, email, signkey, signpref)
    model_layer.save_profile(prof)
    print(MSG_OK + " Profile {0} created.".format(profname))


# noinspection PyShadowingNames
def delete_prof(profname: str) -> None:
    """Function that deletes the selected profile.

    Profile name must be checked before.

    :param profname: Name of the gitcher profile to operate with
    :type profname: [str]
    :return: None
    """
    model_layer.delete_profile(profname)
    print(MSG_OK + " Profile {0} deleted.".format(profname))


# ===============================================
# =                     MAIN                    =
# ===============================================

def interactive_main() -> None:
    """Main launcher of gitcher program interactive mode. Dialogue with the
    user.

    :return: None
    """
    print(COLOR_BRI_BLUE + "**** gitcher: the git profile switcher ****" +
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
    print(COLOR_BRI_CYAN + "m" + COLOR_RST + "    mirror a profile to create a"
                                             " duplicate.")
    print(COLOR_BRI_CYAN + "d" + COLOR_RST + "    delete a profile.")
    print(COLOR_BRI_CYAN + "q" + COLOR_RST + "    quit. Also can use " +
          COLOR_BRI_CYAN + "Ctrl.+C" + COLOR_RST + " everywhere.\n")

    opt = listen("Option: ", dictionary.get_union_cmds_set())
    while not check_opt(opt, interactive_mode=True):
        print(MSG_ERROR + " Invalid opt! Use " +
              '|'.join(dictionary.cmds_interactive_mode) +
              ". Type exit to quit.")
        opt = listen("Enter option: ", dictionary.get_union_cmds_set())

    if opt == 'q':  # Always quite
        print(COLOR_BLUE + "Bye!" + COLOR_RST)
        sys.exit(0)
    if not opt == 'a' and not opt == 'u':
        profname = listen("Select the desired profile entering its name: ",
                          dictionary.profs_profnames)
        while not check_profile(profname):
            print_prof_error(profname)
            profname = listen("Enter profile name: ",
                              dictionary.profs_profnames)

        if opt == 's':
            set_prof(profname)
        elif opt == 'g':
            set_prof_global(profname)
        elif opt == 'm':
            mirror_prof(profname)
        else:  # Option 'd'
            if yes_or_no(MSG_WARNING + " Are you sure to delete {0}?".format(
                    profname)):
                delete_prof(profname)
    else:
        if opt == 'a':
            add_prof()
        else:  # Option 'u'
            update_prof()

    print("\n")  # Graphical interaction separator in loop context


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

    # If syntax is ok, go on and check selected option
    opt = cmd[1].replace('-', '')
    if not check_opt(opt, fast_mode=True):
        print(MSG_ERROR + " Invalid option! Use -[" +
              '|'.join(dictionary.cmds_fast_mode) + "]")
        sys.exit(1)
    else:
        if opt == 'o':
            if len(cmd) == 2:  # cmd have to be only 'gitcher <-o>'
                show_current_on_prof()
            else:
                raise_order_format_error()
        elif opt == 'l':
            if len(cmd) == 2:  # cmd have to be only 'gitcher <-l>'
                list_profs()
            else:
                raise_order_format_error()
        elif len(cmd) >= 3:  # cmd have to be 'gitcher <-opt> <profname> [...]'
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
            else:  # Else it is always necessary to check the profile
                if len(cmd) == 3:  # Security check
                    if not check_profile(profname):
                        print_prof_error(profname)
                        sys.exit(1)
                    # Else, if the profile exists, continue...
                    if opt == 's':
                        set_prof(profname)
                    elif opt == 'g':
                        set_prof_global(profname)
                    elif opt == 'd':
                        delete_prof(profname)
                else:
                    raise_order_format_error()
        else:
            raise_order_format_error()


def main():
    if (len(sys.argv)) == 1:  # Interactive mode, closure execution in a loop
        while True:  # The user inputs the exit order during the session
            interactive_main()
    elif (len(sys.argv)) > 1:  # Fast mode
        fast_main(sys.argv)


if __name__ == "__main__":
    main()
