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
__version__ = '0.4b0'
__maintainer__ = 'Borja González Seoane'
__email__ = 'dev@glezseoane.com'
__status__ = 'Development'


class TabCompleter(object):
    """Class that represents a gitcher tab user input completer."""

    # noinspection PyShadowingNames
    def create_list_completer(self, pattern_list: [str]) -> None:
        """This is a closure that creates a method that autocompletes from
        the given list.

        :param pattern_list: List of patterns to match
        :type pattern_list: [str]
        """

        def completer(input: str, state: int) -> str:
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
                return [pat + " " for pat in pattern_list][state]

            else:
                return [pat + " " for pat in pattern_list
                        if pat.startswith(line)][state]

        self.completer = completer
