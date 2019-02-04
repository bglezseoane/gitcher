#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""gitcher main

gitcher is a git switcher. It facilitates the switching
between git profiles,importing configuration settings such
as name, email and user signatures.
"""


import sys, os, subprocess
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
COLOR_RST = '\033[0m' # Restore default prompt style

# Predefined messages
MSG_OK = "[" + COLOR_GREEN + "OK" + COLOR_RST + "]"
MSG_ERROR = "[" + COLOR_RED + "ERROR" + COLOR_RST + "]"



# ===========================================
# =           Auxiliary functions           =
# ===========================================

def printProfError(profName):
	"""function that prints a nonexistent gitcher profile error."""
	print(MSG_ERROR + " Profile {0} not exists. Try again...".format(profName))


def printProfList():
	"""function that recuperates and prints the gitcher profile list."""
	f = open(CHERFILE, 'r')
	for line in f:
		print("-    " + COLOR_CYAN + line.split(",")[0] + COLOR_RST)


def listen(text):
	"""function that listen a user input, checks if it not a
		'q' (i.e.: quit escape command) and then canalize
		message to caller function."""
	reply = input(text)
	if reply=='q':
		raise SystemExit
	else:
		return reply


def yesOrNo(question):
	"""function that requires a yes or no answer"""
	reply = str(listen(question + " (y|n): ")).lower().strip()
	if reply[0] == 'y':
		return True
	if reply[0] == 'n':
		return False
	else:
		print(MSG_ERROR + " Enter (y|n) answer...")
		yesOrNo(question)


def checkOption(opt):
	"""function that checks the integrity of the listen option."""
	return opt=='s' or opt=='g' or opt=='a' or opt=='d' or opt=='q'


def checkProfile(profName):
	"""function that checks if a gitcher profile exists."""
	f = open(CHERFILE, 'r')
	for line in f:
		if line.split(',')[0]==profName:
			return True
	return False # if not finds prof


def checkGitContext():
	"""function that checks if the current directory have a git repository."""
	cwd = os.getcwd()
	return os.path.exists(cwd + "/.git")


def recoverProf(profName):
	"""function that recovers a gitcher profile.
	
	Warnings:
		- checkProfile must be asserted before.
		- CHERFILE can not content two profiles with the same name. The add
			function takes care of it.
	"""
	f = open(CHERFILE, 'r')
	for line in f:
		words = line.split(',')
		if words[0]==profName:
			# Return as dictionary
			prof = {
				"profName": profName,
				"name": words[1],
				"email": words[2],
				"signKey": words[3],
				"signPref": words[4]
			}
			return prof


def switchProfile(profName, flag):
	"""function that plays the git profile switching."""
	if flag=='l':
		switchGlob="repository"
	elif flag=='g':
		switchGlob="global"

	cwd = os.getcwd() # Current working directory path
	repo = Repo(cwd) # Repository per se instance
	prof = recoverProf(profName)

	repo.config_writer(config_level = switchGlob).set_value("user", "name", \
		prof["name"]).release()

	repo.config_writer(config_level = switchGlob).set_value("user", "email", \
		prof["email"]).release()

	if prof["signKey"] is not None:
		repo.config_writer(config_level = switchGlob).set_value("user", \
			"signingkey", prof["signKey"]).release()		

		cmd = "cd {0} && git config commit.gpgsign {1}".format(cwd, \
			prof["signPref"].lower())
			# It is neccesary to run even preference is false because
			# 	it would be neccesary overwrite git global criteria.
		os.system(cmd) 
		


# ======================================
# =           Main launchers           =
# ======================================

def setProf(profName):
	"""function that sets the selected profile locally."""
	if checkGitContext():
		switchProfile(profName, 'l')
		print(MSG_OK + " Switched to {0} profile.".format(profName))
	else:
		print(MSG_ERROR + " Current directory not contains a git repository.")


def gSetProf(profName):
	"""function that sets the selected profile globally."""
	switchProfile(profName, 'g')
	print(MSG_OK + " Set {0} as git default profile.".format(profName))


def addProf():
	"""function that adds a new profile."""
	print("\nLets go to add a new gitcher profile...")

	profName = listen("Enter the profile name: ")
	while checkProfile(profName):
		print(MSG_ERROR + " {0} yet exists. Change name...".format(profName))
		profName = listen("Enter profile name: ")

	name = listen("Enter the git user name: ")

	email = listen("Enter the git user email: ")
	while not validate_email(email):
		print(MSG_ERROR + " Invalid email format. Try again...".format(email))
		email = listen("Enter the git user email: ")

	if yesOrNo("Do you want to use a GPG sign key?"):
		signKey = listen("Enter the git user signkey: ")
		signPref = str(yesOrNo("Do you want to autocheck every commit?"))
	else:
		signKey = None
		signPref = False

	prof = [profName, name, email, str(signKey), str(signPref)]
	profStr ='",'.join(prof)
	# Save it...
	with open(CHERFILE,'a') as f:    
		print(profStr, file = f)


def delProf(profName):
	"""function that deletes the selected profile."""
	if yesOrNo("Are you sure to delete {0}?".format(profName)):
		f = open(CHERFILE, '+') # Read and write mode
		lines = f.readlines()
		lines = [line.strip('n') for line in lines]
		f.seek(0) # Return to the start of the file
		for line in lines:
			if line.split(',')[0]!=profName:
				print(line, file = f)
		f.truncate() # Delete possible dirty lines below
		f.close()



# ============================
# =           MAIN           =
# ============================

print(COLOR_BRI_BLUE + "**** gitcher: a git profile switcher ****" + COLOR_RST)

# First, check if CHERFILE exists and if not, propose to create it.
if not os.path.exists(CHERFILE):
	print(MSG_ERROR + " {0} not exists and it is necessary.".format(CHERFILE))
	if yesOrNo("Do you want to create {0}?".format(CHERFILE)):
		open(CHERFILE, 'w')
		print(MSG_OK + " Gitcher config dotfile created. Go on...")
	else:
		print(MSG_ERROR + " Impossible to go on without gitcher dotfile.")
		sys.exit(1)

print("gitcher profiles list:")
printProfList()
print("\nOptions:")
print(COLOR_CYAN + 's' + COLOR_RST + "    set a profile to current "\
	"directory repository.")
print(COLOR_CYAN + 'g' + COLOR_RST + "    set a profile as global "\
	"git configuration.")
print(COLOR_CYAN + 'a' + COLOR_RST + "    add a new profile.")
print(COLOR_CYAN + 'd' + COLOR_RST + "    delete a profile.")
print(COLOR_CYAN + 'q' + COLOR_RST + "    quit (escape available all time).")

opt = listen("Option: ")
while not checkOption(opt):
	print("Invalid option! Use s|g|a|d. Type q to quit.")
	opt = listen("Enter option: ")

if not opt=='a':
	profName = listen("Select the desired profile entering its name: ")
	while not checkProfile(profName):
		printProfError(profName)
		profName = listen("Enter profile name: ")

	if opt=='s':
		setProf(profName)
	elif opt=='g':
		gSetProf(profName)
	else:
		delProf(profName)
else:
	addProf()

