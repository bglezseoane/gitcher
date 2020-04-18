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

"""Gitcher's dictionary class module.

This module contains the class that represents the gitcher dictionary
container class.
"""

from gitcher import model_layer


class Dictionary(object):
    """This class presents the gitcher dictionary container, with all the
    options keys and also with a collection of the user data obtained with
    the start of the program execution."""

    # noinspection PyShadowingNames
    def __init__(self):
        self.cmds_interactive_mode = ['s', 'g', 'a', 'd', 'u', 'm', 'q']
        self.cmds_fast_mode = ['l', 's', 'g', 'a', 'd', 'o']

        profs = model_layer.recuperate_profs()
        self.profs_profnames = [prof.profname for prof in profs]
        self.profs_names = [prof.name for prof in profs]
        self.profs_emails = [prof.email for prof in profs]
        # Next force string cast because signkey could be None
        self.profs_signkeys = [str(prof.signkey) for prof in profs]

    def get_union_all(self) -> [str]:
        """This function returns a list with the union of all the dictionary
        subsets."""
        return self.cmds_interactive_mode + self.cmds_fast_mode + \
            self.profs_profnames + self.profs_names + self.profs_signkeys

    def get_union_cmds_set(self) -> [str]:
        """This function returns a list with the union of all the dictionary
        subsets relatives to the gitcher operative context."""
        return self.cmds_interactive_mode + self.cmds_fast_mode

    def get_intersection_cmds_set(self) -> [str]:
        """This function returns a list with the intersection of the
        dictionary subsets relatives to the program fast mode and the
        program interactive mode."""
        return [set(self.cmds_interactive_mode) & set(self.cmds_fast_mode)]

    def get_union_git_set(self) -> [str]:
        """This function returns a list with the union of all the dictionary
        subsets relatives to the git context (i.e.: git profile names,
        user names, emails and signing keys)."""
        return self.profs_profnames + self.profs_names +\
            self.profs_emails + self.profs_signkeys
