# -*- coding: utf-8 -*-


"""gitcher prof class module

This module constains the class that represents a gitcher profile instance.
"""

# Authorship
__author__ = 'Borja González Seoane'
__copyright__ = 'Copyright 2019, Borja González Seoane'
__credits__ = 'Borja González Seoane'
__license__ = 'LICENSE'
__version__ = '0.4b0'
__maintainer__ = 'Borja González Seoane'
__email__ = 'dev@glezseoane.com'
__status__ = 'Development'


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
            signkey_str = "Disabled"
            signpref_str = ""

        return self.profname + ": " + self.name + ", " + self.email + ", " +\
            signkey_str + ", " + signpref_str

    def __simple_str__(self):
        """This function return a minimalistic representation of the profile,
        without its name. It is util to some high level functions.
        """
        if self.signkey is not None:
            signkey_str = self.signkey
            if self.signpref:
                signpref_str = "Enabled"
            else:
                signpref_str = "Disabled"
        else:
            signkey_str = "Disabled"
            signpref_str = ""

        return self.name + ", " + self.email + ", " + signkey_str\
            + ", " + signpref_str

    def __tpl__(self):
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

    def equivalent(self, other) -> bool:
        """This function checks if self profile is equivalent to another
        (i.e.: all params equal except the profname).
        """
        if self.name == other.name:
            if self.email == other.email:
                if self.signkey == other.signkey:
                    if self.signpref == other.signpref:
                        return True
        # Else...
        return False
