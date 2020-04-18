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

"""Gitcher's profile class module

This module constains the class that represents a gitcher profile instance.
"""


class Prof(object):
    """Class that represents a gitcher profile."""

    def __init__(self, profname: str, name: str, email: str,
                 signkey: str = None, signpref: bool = False):
        self.profname = profname
        self.name = name
        self.email = email
        self.signkey = signkey
        self.signpref = signpref

    def __str__(self):
        if self.signkey is not None:
            signkey_str = self.signkey
            if self.signpref:
                signpref_str = "Enabled"
            else:
                signpref_str = "Disabled"
        else:
            signkey_str = "Sign disabled"
            signpref_str = "Autosign disabled"

        return self.profname + ": " + ", ".join([self.name, self.email,
                                                 signkey_str, signpref_str])

    def simple_str(self):
        """This function return a minimalistic representation of the profile,
        without its name. It is util to some high level functions.
        """
        if self.signkey is not None:
            signkey_str = self.signkey
            if self.signpref:
                signpref_str = "autosign enabled"
            else:
                signpref_str = "autosign disabled"
        else:
            signkey_str = "sign disabled"
            signpref_str = "autosign disabled"

        return ", ".join([self.name, self.email, signkey_str, signpref_str])

    def tpl(self):
        """This function return a tuple representation of the object."""
        if self.signkey is not None:
            signkey_str = self.signkey
            if self.signpref:
                signpref_str = "Enabled"
            else:
                signpref_str = "Disabled"
        else:
            signkey_str = "Disabled"
            signpref_str = ""

        return self.profname, self.name, self.email, signkey_str, signpref_str

    def __hash__(self):
        return hash((self.name + self.email + str(self.signkey) +
                     str(self.signpref)))

    def __eq__(self, other):
        return hash(self) == hash(other)
