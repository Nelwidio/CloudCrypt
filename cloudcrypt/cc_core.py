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

__author__ = 'Kevin, Luca'

import time
import os
import sys
from PyQt5 import QtWidgets
import cloudcrypt.cc_sync as cc_sync
import cloudcrypt.cc_gui as cc_gui
import cloudcrypt.cc_con as cc_con
import cloudcrypt.cc_config_parser as cc_config
import cloudcrypt.cc_crypto as cc_crypto


class Core(object):

    def __init__(self):
        self.source = ""
        self.cloud = ""
        self.password_file = cc_con.CC_DEFAULT_PASSWORD_PATH
        self.user_passphrase = "ABCDEF"
        self.passphrase = ""
        self.options = None
        self.crypto = cc_crypto.Crypto()
        self.sync = cc_sync.Sync()
        self.stop = True

        # create the config parser object
        self.config = cc_config.ConfigParser(os.path.join(os.path.dirname(__file__), cc_con.CC_DEFAULT_CONFIG_PATH))
        self.options = self.config.read_config()

        # create the gui
        self.app = QtWidgets.QApplication(sys.argv)
        if "language" in self.options:
            self.mainwin = cc_gui.Gui(config=self.config, core=self,
                                      language=self.options["language"])
        else:
            self.mainwin = cc_gui.Gui(config=self.config, core=self,
                                      language="de")
        self.mainwin.show()
        sys.exit(self.app.exec_())

    def start_sync(self, source_folder, cloud_folder, user_passwd):
        """
        This function starts synchronizing between <source_folder> and
        <cloud_folder>. If it is the first time to start sync, the function
        generates a new password file and encrypts it. Otherwise it will use
        the password file to read the password and start sync. The sync
        runs until <stop_sync> is called.

        :param source_folder: source folder
        :param cloud_folder: cloud folder
        :param user_passwd: the user's password (used to encrypt and decrypt
            password file)
        :return: None
        """
        self.user_passphrase = str(user_passwd)
        self.source = str(source_folder)
        self.cloud = str(cloud_folder)
        if cc_con.FIRST_RUN_FLAG in self.options:
            if self.options[cc_con.FIRST_RUN_FLAG] == "True":
                self.crypto.generate_new_password(64, self.password_file, self.user_passphrase)
                self.options[cc_con.FIRST_RUN_FLAG] = "False"
        else:
            self.crypto.generate_new_password(64, self.password_file,
                                              self.user_passphrase)
            self.options.update({cc_con.FIRST_RUN_FLAG: "False"})

        self.config.write_config(self.options)
        self.passphrase = self.crypto.get_passwd(self.password_file,
                                                 self.user_passphrase)
        if not os.path.exists(str(self.source)):
            raise RuntimeError("Source folder does not exist")
        if not os.path.exists(str(self.cloud)):
            raise RuntimeError("Cloud folder does not exist")
        self.stop = False
        while not self.stop:
            # print("Running from " + str(self.source) + " to " + str(self.cloud) + " with " + str(self.passphrase))

            self.sync.sync_source_cloud(str(self.source), str(self.cloud),
                                        str(self.passphrase), None)
            self.sync.sync_cloud_source(str(self.cloud), str(self.source),
                                        str(self.passphrase), None)

            time.sleep(30)
        return

    def is_password_correct(self, pwd):
        if os.path.exists(self.password_file):
            output = self.crypto.get_passwd(self.password_file, str(pwd))
            if not output:
                return False
            else:
                return True
        else:
            return True

    def stop_sync(self):
        """
        Stops the sync.

        :return:
        """
        self.stop = True

if __name__ == '__main__':
    app = Core()
