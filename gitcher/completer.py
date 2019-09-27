# -*- coding: utf-8 -*-


"""gitcher completer class module

This module presents the class that represents a gitcher completer for user
inputs.
"""

import readline

# Authorship
__author__ = 'Borja González Seoane'
__copyright__ = 'Copyright 2019, Borja González Seoane'
__credits__ = 'Borja González Seoane'
__license__ = 'LICENSE'
__version__ = '3.0'
__maintainer__ = 'Borja González Seoane'
__email__ = 'garaje@glezseoane.es'
__status__ = 'Production'


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
