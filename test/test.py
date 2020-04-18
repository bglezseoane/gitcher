# -*- coding: utf-8 -*-

###########################################################
# Gitcher 3.2 (Test suite)
#
# The git profile switcher
#
# Copyright 2019-2020 Borja González Seoane
#
# Contact: garaje@glezseoane.es
###########################################################

"""Gitcher's test suite."""

import os
import shutil
import tempfile
import unittest
import warnings
from unittest import TestCase, mock

import git

import gitcher.__main__ as gitcher
import gitcher.model_layer as model_layer
import gitcher.prof as prof


# noinspection DuplicatedCode
class UnitTestSuite(TestCase):
    """Unit test suite.

    Checks the model operative from the most superficial layer available.
    """

    def test_set_prof(self):
        """Simulates the set order to check the correct operative effect."""
        warnings.simplefilter("ignore",
                              ResourceWarning)  # Working with tmp files

        # Uses a mock tmp cherfile
        tmp_dir = tempfile.mkdtemp()
        cherfile_path = tempfile.mkstemp(dir=tmp_dir, prefix='tmp_cherfile')
        mock.patch('model_layer.CHERFILE', cherfile_path)
        model_layer.create_cherfile()

        # Commiter data to create the mock repo
        commiter1_name = 'jane'
        commiter1_mail = 'janedoe@home'
        commiter1_sign = "1234567A"
        commiter1_sign_pref = True

        # Create a mock repo
        commiter = commiter1_name + ' <' + commiter1_mail + '>'
        repo_path = create_tmp_dir_with_repo(commiter)

        # Really commiter profile
        prof1_name = "sample1"
        prof1 = prof.Prof(profname=prof1_name,
                          name=commiter1_name,
                          email=commiter1_mail,
                          signkey=commiter1_sign,
                          signpref=commiter1_sign_pref)

        # Another sample profile
        prof2_name = "sample2"
        commiter2_name = 'Pepe García'
        commiter2_mail = 'pepe@none.aq'
        commiter2_sign = 'None'
        commiter2_sign_pref = False
        prof2 = prof.Prof(profname=prof2_name,
                          name=commiter2_name,
                          email=commiter2_mail,
                          signkey=commiter2_sign,
                          signpref=commiter2_sign_pref)

        gitcher.add_prof_fast(prof1_name, commiter1_name, commiter1_mail,
                              commiter1_sign, commiter1_sign_pref)
        gitcher.add_prof_fast(prof2_name, commiter2_name,
                              commiter2_mail, commiter2_sign,
                              commiter2_sign_pref)

        model_layer.switch_prof(prof1.profname, path=str(repo_path))
        current_prof = model_layer.recuperate_git_current_prof(str(repo_path))

        self.assertEqual(prof1, current_prof)

        # Clean environment
        os.remove(cherfile_path[1])
        remove_tmp_dir(repo_path)

    def test_add_prof(self):
        """Simulates the add order to check the correct operative effect."""

        warnings.simplefilter("ignore",
                              ResourceWarning)  # Working with tmp files

        # Uses a mock tmp cherfile
        tmp_dir = tempfile.mkdtemp()
        cherfile_path = tempfile.mkstemp(dir=tmp_dir, prefix='tmp_cherfile')
        mock.patch('model_layer.CHERFILE', cherfile_path)
        model_layer.create_cherfile()

        # Commiter data to create the mock repo
        commiter1_name = 'jane'
        commiter1_mail = 'janedoe@home'
        commiter1_sign = "1234567A"
        commiter1_sign_pref = True

        # Create a mock repo
        commiter = commiter1_name + ' <' + commiter1_mail + '>'
        repo_path = create_tmp_dir_with_repo(commiter)

        # Really commiter profile
        prof1_name = "sample1"
        prof1 = prof.Prof(profname=prof1_name,
                          name=commiter1_name,
                          email=commiter1_mail,
                          signkey=commiter1_sign,
                          signpref=commiter1_sign_pref)

        # Another sample profile
        prof2_name = "sample2"
        commiter2_name = 'Pepe García'
        commiter2_mail = 'pepe@none.aq'
        commiter2_sign = 'None'
        commiter2_sign_pref = False
        prof2 = prof.Prof(profname=prof2_name,
                          name=commiter2_name,
                          email=commiter2_mail,
                          signkey=commiter2_sign,
                          signpref=commiter2_sign_pref)

        gitcher.add_prof_fast(prof1_name, commiter1_name, commiter1_mail,
                              commiter1_sign, commiter1_sign_pref)
        gitcher.add_prof_fast(prof2_name, commiter2_name,
                              commiter2_mail, commiter2_sign,
                              commiter2_sign_pref)

        profs = model_layer.recuperate_profs()
        for x in [prof1, prof2]:
            self.assertTrue(x in profs)

        # Clean environment
        os.remove(cherfile_path[1])
        remove_tmp_dir(repo_path)

    def test_delete_prof(self):
        """Simulates the delete order to check the correct operative effect."""

        warnings.simplefilter("ignore",
                              ResourceWarning)  # Working with tmp files

        # Uses a mock tmp cherfile
        tmp_dir = tempfile.mkdtemp()
        cherfile_path = tempfile.mkstemp(dir=tmp_dir, prefix='tmp_cherfile')
        mock.patch('model_layer.CHERFILE', cherfile_path)
        model_layer.create_cherfile()

        # Commiter data to create the mock repo
        commiter1_name = 'jane'
        commiter1_mail = 'janedoe@home'
        commiter1_sign = "1234567A"
        commiter1_sign_pref = True

        # Create a mock repo
        commiter = commiter1_name + ' <' + commiter1_mail + '>'
        repo_path = create_tmp_dir_with_repo(commiter)

        # Really commiter profile
        prof1_name = "sample1"
        prof1 = prof.Prof(profname=prof1_name,
                          name=commiter1_name,
                          email=commiter1_mail,
                          signkey=commiter1_sign,
                          signpref=commiter1_sign_pref)

        # Another sample profile
        prof2_name = "sample2"
        commiter2_name = 'Pepe García'
        commiter2_mail = 'pepe@none.aq'
        commiter2_sign = 'None'
        commiter2_sign_pref = False
        prof2 = prof.Prof(profname=prof2_name,
                          name=commiter2_name,
                          email=commiter2_mail,
                          signkey=commiter2_sign,
                          signpref=commiter2_sign_pref)

        gitcher.add_prof_fast(prof1_name, commiter1_name, commiter1_mail,
                              commiter1_sign, commiter1_sign_pref)
        gitcher.add_prof_fast(prof2_name, commiter2_name,
                              commiter2_mail, commiter2_sign,
                              commiter2_sign_pref)

        # Now, deletes prof2
        gitcher.delete_prof(prof2.profname)

        profs = model_layer.recuperate_profs()
        self.assertTrue(prof1 in profs)
        self.assertFalse(prof2 in profs)

        # Clean environment
        os.remove(cherfile_path[1])
        remove_tmp_dir(repo_path)


if __name__ == '__main__':
    unittest.main()


# ===============================================
# =         Test general util functions         =
# ===============================================
def create_tmp_dir_with_repo(commiter: str) -> tempfile.TemporaryDirectory:
    """Creates a secure tmp directory with an init repository."""
    tmp_dir = tempfile.mkdtemp()

    # Now inits a sample repo
    repo = git.Repo.init(tmp_dir)

    # Create sample data
    for i in range(1, 5):
        tempfile.mkstemp(suffix='.py', dir=tmp_dir)

    repo.git.add('--all')
    repo.git.commit('-m', 'Commit test effects #1', author=commiter)

    return tmp_dir


def remove_tmp_dir(tmp_dir: tempfile.TemporaryDirectory) -> None:
    shutil.rmtree(str(tmp_dir))
