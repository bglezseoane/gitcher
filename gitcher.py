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



# ===========================================
# =           Auxiliary functions           =
# ===========================================

def printProfError(profName):
	"""function that prints a nonexistent gitcher profile error."""
	print("[ERROR] Profile {0} not exists. Try again...".format(profName))


def printProfList():
	"""function that recuperates and prints the gitcher profile list."""
	f = open(CHERFILE, "r")
	for line in f:
		print(line.split(",")[0])


def checkProfile(profName):
	"""function that checks if a gitcher profile exists."""
	f = open(CHERFILE, "r")
	for line in f:
		if line.split(",")[0]==profName:
			return True
	return False # if not finds prof


def recoverProf(profName):
	"""function that recovers a gitcher profile.
	
	Warnings:
		- checkProfile must be asserted before.
		- CHERFILE can not content two profiles with the same name. The add
			function takes care of it.
	"""
	f = open(CHERFILE, "r")
	for line in f:
		words = line.split(",")
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


def checkOption(opt):
	"""function that checks the integrity of the input option."""
	return opt=="s" or opt=="g" or opt=="a" or opt=="d"


def yesOrNo(question):
	"""function that requires a yes or no answer"""
	reply = str(input(question + " (y|n): ")).lower().strip()
	if reply[0] == "y":
		return True
	if reply[0] == "n":
		return False
	else:
		print("[ERROR] Enter (y|n) answer...")
		yesOrNo(question)


def checkGitContext():
	"""function that checks if the current directory have a git repository."""
	cwd = os.getcwd()
	return os.path.exists(cwd + "/.git")


def switchProfile(profName, flag):
	"""function that plays the git profile switching."""
	if flag=="l":
		globSwitch=""
	elif flag=="g":
		globSwitch="--global"

	cwd = os.getcwd() # Current working directory path
	repo = Repo(cwd) # Repository per se instance
	prof = recoverProf(profName)

	repo.config_writer().set_value("user", "name", prof["name"]).release()
	repo.config_writer().set_value("user", "email", prof["email"]).release()
	if prof["signKey"] is not None:
		repo.config_writer().set_value("user", "signingKey", \
			prof["signKey"]).release()		
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
		switchProfile(profName, "l")
		print("[OK] Switched to {0} profile.".format(profName))
	else:
		print("[ERROR] Current working directory have not a git repository.")


def gSetProf(profName):
	"""function that sets the selected profile globally."""
	switchProfile(profName, "g")
	print("[OK] Set {0} as git default profile.".format(profName))


def addProf():
	"""function that adds a new profile."""
	print("\nLets go to add a new gitcher profile...")

	profName = input("Enter the profile name: ")
	while checkProfile(profName):
		print("[ERROR] {0} yet exists. Use another name...".format(profName))
		profName = input("Enter profile name: ")

	name = input("Enter the git user name: ")

	email = input("Enter the git user email: ")
	while not validate_email(email):
		print("[ERROR] Invalid email format. Try again...".format(email))
		email = input("Enter the git user email: ")

	if yesOrNo("Do you want to use a GPG sign key?"):
		signKey = input("Enter the git user signkey: ")
		signPref = str(yesOrNo("Do you want to autocheck every commit?"))
	else:
		signKey = None
		signPref = False

	prof = [profName, name, email, str(signKey), str(signPref)]
	profStr = ",".join(prof)
	# Save it...
	with open(CHERFILE,"a") as f:    
		print(profStr, file = f)


def delProf(profName):
	"""function that deletes the selected profile."""
	if yesOrNo("Are you sure to delete {0}?".format(profName)):
		f = open(CHERFILE, "r+") # Read and write mode
		lines = f.readlines()
		lines = [line.strip("\n") for line in lines]
		f.seek(0) # Return to the start of the file
		for line in lines:
			if line.split(",")[0]!=profName:
				print(line, file = f)
		f.truncate() # Delete possible dirty lines below
		f.close()



# ============================
# =           MAIN           =
# ============================

print("gitcher: a git profile switcher")

# First, check if CHERFILE exists and if not, propose to create it.
if not os.path.exists(CHERFILE):
	print("[ERROR] {0} not exists and it is necessary.".format(CHERFILE))
	if yesOrNo("Do you want to create {0}?".format(CHERFILE)):
		open(CHERFILE, "w")
		print("[OK] Gitcher config dotfile created. Go on...")
	else:
		print("[ERROR] Impossible to go on without gitcher config dotfile.")
		sys.exit(1)

printProfList()
print("\nOptions:")
print("s    set a profile to current directory repository.")
print("g    set a profile as global git profile.")
print("a    add a new profile.")
print("d    delete a profile.")
print("\nQuit with Ctrl.+C.")

opt = input("Option: ")
while not checkOption(opt):
	print("Invalid option! Use s|g|a|d. Quit with Ctrl.+C.")
	opt = input("Enter option: ")

if not opt=="a":
	profName = input("Select the desired profile entering its name: ")
	while not checkProfile(profName):
		printProfError(profName)
		profName = input("Enter profile name: ")

	if opt=="s":
		setProf(profName)
	elif opt=="g":
		gSetProf(profName)
	else:
		delProf(profName)
else:
	addProf()
