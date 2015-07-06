"""
Copyright 2015 by Kevin Kirchner, Luca Rupp, David Pauli

This file is part of CloudCrypt.

CloudCrypt is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CloudCrypt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

Diese Datei ist Teil von CloudCrypt.

CloudCrypt ist Freie Software: Sie können es unter den Bedingungen
der GNU Lesser General Public License, wie von der Free Software Foundation,
Version 3 der Lizenz oder (nach Ihrer Wahl) jeder späteren
veröffentlichten Version, weiterverbreiten und/oder modifizieren.

Fubar wird in der Hoffnung, dass es nützlich sein wird, aber
OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
Siehe die GNU Lesser General Public License für weitere Details.

Sie sollten eine Kopie der GNU Lesser General Public License zusammen mit diesem
Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.
"""

__author__ = 'Kevin'
"""
This module tests some functions of the module <cc_help>
"""

import unittest
from os.path import join

import cloudcrypt.cc_help as cc_help


class TestHelp(unittest.TestCase):
    """
    Tests must always derived from <unittest.TestCase>.
    """

    def testLanguage(self):
        """
        This test tests the behaviour of the class <cc_help.Help> when giving
        valid in invalid language codes.
        """
        helper = cc_help.Help("ger")
        self.assertEqual(helper._get_language_(), "ger")
        helper = cc_help.Help("eng")
        self.assertEqual(helper._get_language_(), "eng")
        helper = cc_help.Help("This is an invalid language code")
        self.assertEqual(helper._get_language_(), "eng")

    def testFileExist(self):
        """
        This method tests, if the check for file existence works correctly.
        """
        self.assertEqual(cc_help._does_file_exist_("help_test.py"), True)
        self.assertEqual(cc_help._does_file_exist_("BlaBlaBla.txt"), False)
        path = join("..", "help", "style.css")
        self.assertEqual(cc_help._does_file_exist_(path), True)
        path = join("..", "help", "ger", "error.html")
        self.assertEqual(cc_help._does_file_exist_(path), True)
        path = join("..", "help", "ger", "")
        self.assertEqual(cc_help._does_file_exist_(path), False)


if __name__ == "__main__":
    unittest.main()
