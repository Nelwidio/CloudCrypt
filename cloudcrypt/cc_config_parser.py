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

import cloudcrypt.cc_con as cc_con
from xml.etree import ElementTree
from xml.parsers.expat import ExpatError
from xml.etree.ElementTree import ParseError
from xml.etree.ElementTree import Element, SubElement


class ConfigParser:
    """
    Provides methods for reading and writing xml based CloudCrypt config files
    """

    def __init__(self, path_to_config=cc_con.CC_DEFAULT_CONFIG_PATH):
        """
        Create a new CloudCrypt ConfigParser

        @param: path_to_config: The path to the config file the parser shall act upon.
        If this is left empty, a default value of a value specified in the methods is used
        @returns: A new CloudCrypt ConfigParse object
        """
        self.path_to_config = path_to_config
        try:
            open(self.path_to_config, 'a').close()
        except OSError:
            raise OSError('unable to create config file: ' + self.path_to_config)

    def read_config(self):
        """
        Read a CloudCrypt config file

        @param: path_to_config: The config file, that will be read. If it is empty, then the value from the
        constructor will be used and if that is also empty a default value is used
        @returns: A dictionary with the options names as keys and the option-values as values
        """
        options = {}
        # if a ParseError occurs, someone else has to handle it
        try:
            tree = ElementTree.parse(self.path_to_config)
        except:
            return {}
        root = tree.getroot()
        for child in root.findall('option'):
            try:
                # append all the found options to options
                options.update({str(child.find('key').text): str(child.find('value').text)})
            # if there is a option that can not be inserted into the dictionary, we just ignore it
            except TypeError:
                pass
        return options

    def write_config(self, options, path_to_config=None):
        """
        Write a CloudCrypt config file

        This Method takes a dictionary of options and writes it to a XML file.
        If the file does not already exist, it is created.
        If a options is already in the config file, the value is overwritten.
        This method does not check, if the options are valid CloudCrypt options
        @param: options: A dictionary of options that will be written to the config file
        @param: path_to_config: The path to the config file that will be written, if empty, the value from the
        constructor is used, if that is also empty, a default value is used
        @returns: None
        """
        if path_to_config is None:
            path_to_config = self.path_to_config

        # create a new file (it dosn't matter whether it is there already as we have to clear it
        # in any case to get rid of old options
        root = ElementTree.Element('cloudcrypt')
        tree = ElementTree.ElementTree(root)
        tree.write(self.path_to_config)

        root = tree.getroot()
        for k, v in options.items():
            if self._is_key_there_(str(k), root) is None:
                new = Element('option')
                key = SubElement(new, 'key')
                key.text = str(k)
                val = SubElement(new, 'value')
                val.text = str(v)
                root.append(new)
            else:
                for opt in root.findall('option'):
                    if str(opt.find('key').text) == str(k):
                        opt.find('value').text = str(v)
        try:
            self.indent(root)
            tree.write(path_to_config)
        except PermissionError:
            raise PermissionError('could not write config to' + path_to_config + "permission denied")
        except FileNotFoundError:
            raise FileNotFoundError('cloud not write config to' + path_to_config + "file not found")

    def _is_key_there_(self, key, root):
        for k in root.iter('key'):
            if str(k.text) == str(key):
                return k
        return None

    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

