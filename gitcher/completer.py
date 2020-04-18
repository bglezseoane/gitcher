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

"""Gitcher's completer class module.

This module presents the class that represents a gitcher completer for user
inputs.
"""

import readline


class TabCompleter(object):
    """Class that represents a gitcher tab user input completer."""

    def __completer(self, input: str, state: int) -> str:
        """This function provides an autocompletion service for the user
        inputs.

        :param input: User input try
        :type input: str
        :param state: User input prediction selector
        :type state: int
        :return: User reply after canalize question via 'input()' function.
        :rtype: str
        """
        line = readline.get_line_buffer()

        if not line:
            return [pat + " " for pat in self.pattern_list][state]

        else:
            return [pat + " " for pat in self.pattern_list
                    if pat.startswith(line)][state]

    def __init__(self, pattern_list: [str]):
        self.pattern_list = pattern_list
        self.service = self.__completer
