#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""gitcher main

gitcher is a git switcher. It facilitates the switching
between git profiles,importing configuration settings such
as name, email and user signatures.
"""

import sys
import os
from os.path import expanduser
from validate_email import validate_email
from git import Repo

# Authorship
__author__ = "Borja González Seoane"
__copyright__ = "Copyright 2019, Borja González Seoane"
__credits__ = "Borja González Seoane"
__license__ = "GPL-3.0"
__version__ = "0.1"
__maintainer__ = "Borja González Seoane"
__email__ = "dev@glezseoane.com"
__status__ = "Development"

# Paths
HOME = expanduser("~")
CHERFILE = HOME + "/.cherfile"

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


# ===========================================
# =           Auxiliary functions           =
# ===========================================

def print_prof_error(profname):
    """function that prints a nonexistent gitcher profile error."""
    print(MSG_ERROR + " Profile {0} not exists. Try again...".format(profname))


def print_prof_list():
    """function that recuperates and prints the gitcher profile list."""
    f = open(CHERFILE, 'r')
    for line in f:
        print("-    " + COLOR_CYAN + line.split(",")[0] + COLOR_RST)


def listen(text):
    """function that listen a user input, checks if it not a 'q' (i.e.: quit
	escape command) and then canalize message to caller function."""
    reply = input(text)

    if reply == 'q':
        raise SystemExit
    else:
        return reply


def yes_or_no(question):
    """function that requires a yes or no answer"""
    reply = str(listen(question + " (y|n): ")).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        print(MSG_ERROR + " Enter (y|n) answer...")
        yes_or_no(question)


def check_opt(opt):
    """function that checks the integrity of the listen option."""
    return opt == 's' or opt == 'g' or opt == 'a' or opt == 'd' or opt == 'q'


def check_profile(profname):
    """function that checks if a gitcher profile exists."""
    f = open(CHERFILE, 'r')
    for line in f:
        if line.split(',')[0] == profname:
            return True
    return False  # if not finds prof


def check_git_context():
    """function that checks if the current directory have a git repository."""
    cwd = os.getcwd()
    return os.path.exists(cwd + "/.git")


def recover_prof(profname):
    """function that recovers a gitcher profile.
	
	Warnings:
		- check_profile must be asserted before.
		- CHERFILE can not content two profiles with the same name. The add
			function takes care of it.
	"""
    f = open(CHERFILE, 'r')
    for line in f:
        words = line.split(',')
        if words[0] == profname:
            # Return as dictionary
            prof = {
                "profname": profname,
                "name": words[1],
                "email": words[2],
                "signkey": words[3],
                "signpref": words[4]
            }
            return prof


def switch_prof(profname, flag):
    """function that plays the git profile switching."""
    switch_global = "repository"
    if flag == 'g':
        switch_global = "global"

    cwd = os.getcwd()  #  Current working directory path
    repo = Repo(cwd)  # Repository per se instance
    prof = recover_prof(profname)

    repo.config_writer(config_level=switch_global). \
        set_value("user", "name", prof["name"]).release()

    repo.config_writer(config_level=switch_global). \
        set_value("user", "email", prof["email"]).release()

    if prof["signkey"] is not None:
        repo.config_writer(config_level=switch_global). \
            set_value("user", "signingkey", prof["signkey"]).release()

        # Is neccesary to run next command even preference is false because
        # 	it would be neccesary overwrite git global criteria.
        cmd = "cd {0} && git config commit.gpgsign {1}".\
            format(cwd, prof['signpref'].lower())
        os.system(cmd)


# ======================================
# =           Main launchers           =
# ======================================

def set_prof(profname):
    """function that sets the selected profile locally."""
    if check_git_context():
        switch_prof(profname, 'l')
        print(MSG_OK + " Switched to {0} profile.".format(profname))
    else:
        print(MSG_ERROR + " Current directory not contains a git repository.")


def set_prof_global(profname):
    """function that sets the selected profile globally."""
    switch_prof(profname, 'g')
    print(MSG_OK + " Set {0} as git default profile.".format(profname))


def add_prof():
    """function that adds a new profile."""
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

    prof = [profname, name, email, str(signkey), str(signpref)]
    profStr = '",'.join(prof)
    # Save it...
    with open(CHERFILE, 'a') as f:
        print(profStr, file=f)


def delete_prof(profname):
    """function that deletes the selected profile."""
    if yes_or_no("Are you sure to delete {0}?".format(profname)):
        f = open(CHERFILE, '+')  # Read and write mode
        lines = f.readlines()
        lines = [line.strip('n') for line in lines]
        f.seek(0)  # Return to the start of the file
        for line in lines:
            if line.split(',')[0] != profname:
                print(line, file=f)
        f.truncate()  # Delete possible dirty lines below
        f.close()


# ============================
# =           MAIN           =
# ============================

print(COLOR_BRI_BLUE + "**** gitcher: a git profile switcher ****" + COLOR_RST)

# First, check if CHERFILE exists and if not, propose to create it.
if not os.path.exists(CHERFILE):
    print(MSG_ERROR + " {0} not exists and it is necessary.".format(CHERFILE))
    if yes_or_no("Do you want to create {0}?".format(CHERFILE)):
        open(CHERFILE, 'w')
        print(MSG_OK + " Gitcher config dotfile created. Go on...")
    else:
        print(MSG_ERROR + " Impossible to go on without gitcher dotfile.")
        sys.exit(1)

print("gitcher profiles list:")
print_prof_list()
print("\nopts:")
print(COLOR_CYAN + 's' + COLOR_RST + "    set a profile to current " \
                                     "directory repository.")
print(COLOR_CYAN + 'g' + COLOR_RST + "    set a profile as global " \
                                     "git configuration.")
print(COLOR_CYAN + 'a' + COLOR_RST + "    add a new profile.")
print(COLOR_CYAN + 'd' + COLOR_RST + "    delete a profile.")
print(COLOR_CYAN + 'q' + COLOR_RST + "    quit (escape available all time).\n")

opt = listen("opt: ")
while not check_opt(opt):
    print(MSG_ERROR + " Invalid opt! Use s|g|a|d. Type q to quit.")
    opt = listen("Enter opt: ")

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
