# -*- coding: utf-8 -*-

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
along with CloudCrypt.  If not, see <http://www.gnu.org/licenses/>.

Diese Datei ist Teil von CloudCrypt.

CloudCrypt ist Freie Software: Sie können es unter den Bedingungen
der GNU Lesser General Public License, wie von der Free Software Foundation,
Version 3 der Lizenz oder (nach Ihrer Wahl) jeder späteren
veröffentlichten Version, weiterverbreiten und/oder modifizieren.

CloudCrypt wird in der Hoffnung, dass es nützlich sein wird, aber
OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
Siehe die GNU Lesser General Public License für weitere Details.

Sie sollten eine Kopie der GNU Lesser General Public License zusammen mit diesem
Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.
"""

__author__ = 'Luca, Kevin'

"""
This module provides a class for parsing a language file in order to implement
some kind of localization mechanism. The object takes a language code and
reads the corresponding language file (which is a simple txt-file with key-value
pairs separated by '=') and builds a list out of the keys and values. Through
a function one can access the values of specified keys.
"""

from os.path import exists, dirname, join

import cloudcrypt.cc_con as cc_con


class Texts(object):
    """
    Class for parsing a language file of a specified language.
    """

    def __init__(self, language,
                 prefix=cc_con.LANGFILE_PREFIX,
                 ending=cc_con.LANGFILE_ENDING):
        """
        Constructor of the object. Takes a language code, a prefix for the
        filename and the ending of the filename. From this parameters the path
        to the language file is being built. If the file does not exist, an
        appropriate error message will be printed and the program exits. If the
        file exists, it will be parsed.

        :param language: language code
        :param prefix: prefix for the file (default is a value in cc_con)
        :param ending: ending for the file (default is a value in cc_con)
        :return: None
        """
        self.language = language
        # the datastructure that holds all the texts for cloudcrypt
        self.texts = {}
        # path to the file. Consists of the path of this script file and
        # the prefix + language code + ending
        self.filename = join(dirname(__file__), prefix + self.language + ending)

        # if the file does not exist print a message
        if not exists(str(self.filename)):
            print("ERROR! Was not able to open language file '" +
                  self.filename + "'")
        else:
            # open the file in read mode and read it line by line
            with open(self.filename, 'r') as f:
                for line in f:
                    # remove the newline
                    line = line[:-1]
                    # strip leading and trailing whitespace
                    line = line.strip()
                    # commentaries
                    if cc_con.CONFIG_FILE_COMMENTARY in line:
                        line = line.split(cc_con.CONFIG_FILE_COMMENTARY, 1)[0]
                    # only proceed, if the format of the line is valid
                    if "=" in line:
                        temp = line.split('=', 1)
                        # ignore whitespace around the "="
                        temp[0] = temp[0].strip()
                        temp[1] = temp[1].strip()
                    else:
                        continue
                    # if an text is not aleady in the datastructure insert it
                    if temp[0] and temp[0] not in self.texts:
                        self.texts[temp[0]] = []
                    # add the translation to the list and ignore empty lines
                    try:
                        self.texts[temp[0]].append(temp[1][:])
                    except IndexError:
                        self.texts[temp[0]].append("")

    def get_text(self, name):
        """
        This function returns the value of a given key as string. If the key
        does not exist, the function will return <None>.

        :param name: the key of which you want to get the value
        :return: the value as string if the <name> exists, <None> otherwise
        """
        if name in self.texts:
            return self.texts[name][0]
        else:
            return None
