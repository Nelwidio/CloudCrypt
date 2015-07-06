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

__author__ = 'Kevin'

"""
This module provides functionality to synchronize from source-folder to the
cloud-folder and vice versa.
"""

import os
import cloudcrypt.cc_crypto as cc_crypto


class Sync(object):

    def __init__(self):
        self.crypt = cc_crypto.Crypto()

    def sync_source_cloud(self, src, dest, passphrase, ignore=None):
        """
        Synchronizes from the source to the cloud folder. It only copies
        files, if they are newer (according to the MAC-timestamps).
        Must be invoked as follows:
        sync_cloud_source(<sourceFolder>, <cloudFolder>, <passphrase>, <None>)

        :param src: the source folder
        :param dest: the cloud folder
        :param passphrase: the passphrase for encryption
        :param ignore: files to ignore (should usually be None)
        :return: None
        """
        if os.path.isdir(src):
            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(src)
            if ignore is not None:
                ignored = ignore(src, files)
            else:
                ignored = set()
            for f in files:
                if f not in ignored:
                    self.sync_source_cloud(os.path.join(src, f),
                                           os.path.join(dest, f),
                                           str(passphrase), ignore)
        else:
            if os.path.exists(dest):
                mod_time_src = os.path.getmtime(src)
                mod_time_dest = os.path.getmtime(dest)
                if mod_time_src > mod_time_dest:
                    self.crypt.encrypt_file_symmetric(src, dest,
                                                      str(passphrase))
            else:
                self.crypt.encrypt_file_symmetric(src, dest, str(passphrase))

    def sync_cloud_source(self, src, dest, passphrase, ignore=None):
        """
        Synchronizes from the cloud to the source folder. It only copies
        files, if they are newer (according to the MAC-timestamps).
        Must be invoked as follows:
        sync_cloud_source(<cloudFolder>, <sourceFolder>, <passphrase>, <None>)

        :param src: the cloud folder
        :param dest: the source folder
        :param passphrase: the passphrase for decryption
        :param ignore: files to ignore (should usually be None)
        :return: None
        """
        if os.path.isdir(src):
            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(src)
            if ignore is not None:
                ignored = ignore(src, files)
            else:
                ignored = set()
            for f in files:
                if f not in ignored:
                    self.sync_cloud_source(os.path.join(src, f),
                                           os.path.join(dest, f),
                                           str(passphrase), ignore)
        else:
            if os.path.exists(dest):
                mod_time_src = os.path.getmtime(src)
                mod_time_dest = os.path.getmtime(dest)
                if mod_time_src > mod_time_dest:
                    self.crypt.decrypt_file_symmetric(src, dest,
                                                      str(passphrase))
            else:
                self.crypt.decrypt_file_symmetric(src, dest, str(passphrase))
