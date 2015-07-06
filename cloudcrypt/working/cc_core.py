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

__author__ = ''

from threading import Thread
import os
import shutil

import cc_core_deamon
import cc_crypto
import cc_core_sync
import cc_usermgmt


class Core():
    def __init__(self, f1, f2, db_path):
        """

        :param f1: folder with data
        :param f2: folder with encrypted Data
        :param db_path: path to db
        :return: --
        """
        self.sourceFolder = f1
        self.cloudFolder = f2
        self.dp_path = db_path
        self.db = cc_usermgmt.Usermgmt(self.dp_path)
        self.t1 = None
        self.t2 = None
        self.run = None
        self.run2 = None
        self.crypto = None
        self.core_sync = None

    def start_crypto(self, key_path_folder, pass_phrase, own_keyring):
        """
        init crypto class
        :param key_path_folder:
        :param pass_phrase:
        :param own_keyring:
        :return:
        """
        self.crypto = cc_crypto.Crypto(key_path_folder, pass_phrase, self.db, own_keyring=own_keyring)

    def start_sync(self):
        """
        start pre sync and start the deamon
        :return:
        """
        self.core_sync = cc_core_sync.CoreSync(self.sourceFolder, self.cloudFolder, self.crypto)
        self.core_sync.pre_sync()
        self.runner()

    def do_sync_if_needed(self):
        """
        here we sync new if key or share changed.
        need to test it when cc_usermgmt is finished
        :return:
        """
        if not self.crypto.get_sync_required():
            self.run.stop()
            self.run2.stop()
            if not (self.t1.is_alive() and self.t2.is_alive()):
                self.new_sync()
                self.runner()

    def get_key_list_private(self):
        """
        see explanation in cc_crypto.py
        :return:
        """
        return self.crypto.get_key_list_private()

    def get_key_list_public(self):
        """
        see explanation in cc_crypto.py
        :return:
        """
        return self.crypto.get_key_list_public()

    def set_private_key(self, fingerprint):
        """
        see explanation in cc_crypto.py
        :return:
        """
        self.crypto.set_private_key(fingerprint)

    def get_private_key(self):
        """
        see explanation in cc_crypto.py
        :return:
        """
        return self.crypto.get_private_key()

    def set_pass_phrase(self, pass_phrase):
        """
        see explanation in cc_crypto.py
        :return:
        """
        self.crypto.set_pass_phrase(pass_phrase)

    def delete_keys(self, fingerprint):
        """
        see explanation in cc_crypto.py
        :return:
        """
        self.delete_keys(fingerprint)

    def generate_gnupg_key(self, name, email, expire_date, key_type, key_length, pass_phrase, key_server_uri):
        """
        see explanation in cc_crypto.py
        :return:
        """
        self.crypto.generate_gnupg_key(name, email, expire_date, key_type, key_length, pass_phrase, key_server_uri)

    def export_key(self, fingerprint):
        """
        see explanation in cc_crypto.py
        :return:
        """
        self.export_key(fingerprint)

    def import_online_keys(self, server, fingerprint):
        """
        see explanation in cc_crypto.py
        :return:
        """
        self.crypto.import_online_keys(server=server, keyids=fingerprint)

    def set_share_list(self, share):
        """
        see explanation in cc_crypto.py
        :return:
        """
        self.crypto.set_share_list(share=share)

    def get_share_list(self):
        """
        see explanation in cc_crypto.py
        :return:
        """
        return self.crypto.get_share_list()

    def create_user(self, name, fingerprint):
        """
        see explanation in cc_cc_usermgmt.py
        :return:
        """
        self.db.create_user(name, fingerprint)

    def create_default_users(self, public_key_list):
        """
        see explanation in cc_cc_usermgmt.py
        :return:
        """
        self.db.create_default_users(public_key_list)

    def create_group(self, name):
        """
        see explanation in cc_cc_usermgmt.py
        :return:
        """
        self.db.create_group(name)

    def delete_user(self, fingerprint):
        """
        see explanation in cc_cc_usermgmt.py
        :return:
        """
        self.db.delete_user(fingerprint)

    def get_user_names(self):
        """
        see explanation in cc_cc_usermgmt.py
        :return:
        """
        return self.db.get_user_names()

    def get_group_names(self):
        """
        see explanation in cc_cc_usermgmt.py
        :return:
        """
        return self.db.get_group_names()

    def get_user_groups(self, fingerprint):
        """
        see explanation in cc_cc_usermgmt.py
        :return:
        """
        return self.db.get_user_groups(fingerprint)

    def get_group_members(self, group):
        """
        see explanation in cc_cc_usermgmt.py
        :return:
        """
        return self.db.get_group_members(group)

    def add_user_to_groups(self, fingerprint, groups):
        """
        see explanation in cc_cc_usermgmt.py
        :return:
        """
        self.db.add_user_to_groups(fingerprint, groups)

    def remove_user_from_group(self, user_fingerprint, group):
        """
        see explanation in cc_cc_usermgmt.py
        :return:
        """
        self.db.remove_user_from_group(user_fingerprint, group)

    def edit_user(self, name, fingerprint):
        """
        see explanation in cc_cc_usermgmt.py
        :return:
        """
        self.db.edit_user(name, fingerprint)

    def get_group_ﬁngerprints(self, group):
        """
        see explanation in cc_cc_usermgmt.py
        :return:
        """
        return self.db.get_group_ﬁngerprints(group)

    def close_db(self):
        """
        see explanation in cc_cc_usermgmt.py
        :return:
        """
        self.db.close_db()

    # -----------------------------------------------------------------------
    def runner(self):
        """
        creates threads
        :return: --
        """
        self.t1 = Thread(target=self.run1, args=(self.sourceFolder,))
        self.t1.start()

        self.t1 = Thread(target=self.run1, args=(self.cloudFolder,))
        self.t1.start()

    def run1(self, foulder):
        """
        starts thread 1
        :return: --
        """
        self.run = cc_core_deamon.CoreSyncDaemon(gpg=self.core_sync, directory=foulder)
        self.run.starter()

    def new_sync(self):
        """
        Resynchronises the source Folder to the cloud folder if the Private Key changes or the share changes.

        Attention: if the private Key changes the cloud folder gets deleted and completely rebuilt.

        :return: nothing
        """
        new_private_key = self.crypto.get_new_private_key_flag()
        new_share = self.crypto.get_share_flag()

        share = self.crypto.get_share_list()
        old_share = self.crypto.get_old_share_list()

        if new_private_key is False:
            return

        if new_share is False:
            return

        if new_private_key is True and new_share is True:
            self.crypto.set_share_flag(True)
            new_share = self.crypto.get_share_flag()

        # the two directories to sync
        str_dir1 = self.sourceFolder
        str_dir2 = self.cloudFolder

        # list files and make sure there are no hidden ones (Linux and Mac).
        list_items_path1 = []
        list_items_name1 = []
        list_items_path2 = []
        list_items_name2 = []

        # scan cloud Folder
        for path, subDirs, files in os.walk(str_dir2):
            list_items_path2.append(os.path.normpath(path))
            for name in files:
                list_items_name2.append(os.path.normpath(os.path.join(path, name)))

        # delete source Folder and cloud Folder path
        if list_items_path1:
            if os.path.normpath(str_dir1) in list_items_path1:
                list_items_path1.remove(os.path.normpath(str_dir1))
        if list_items_path2:
            if os.path.normpath(str_dir2) in list_items_path2:
                list_items_path2.remove(os.path.normpath(str_dir2))

        if new_private_key is True:
            # delete the whole cloud folder
            cloud_content = os.listdir(self.cloudFolder)
            for item in cloud_content:
                if os.path.isdir(item):
                    shutil.rmtree(os.path.normpath(os.path.join(self.cloudFolder, item)), True)
                else:
                    os.remove(os.path.normpath(os.path.join(self.cloudFolder, item)))

        # sync folders from source Folder
        for folder in list_items_path1:
            if folder.replace(os.path.normpath(str_dir1), os.path.normpath(str_dir2)) not in list_items_path2:
                t = str(folder)
                t = t.replace(os.path.normpath(str_dir1), os.path.normpath(str_dir2))
                if not os.path.exists(t):
                    os.mkdir(t)

        if new_private_key is True:
            for file in list_items_name1:
                t = str(file)
                t = t.replace(os.path.normpath(str_dir1), os.path.normpath(str_dir2))
                self.crypto.copy_file_encrypt(file, t)

        if new_share is True:
            # get the difference between old share and new one
            remove_share = set(old_share).difference(share)

            # remove the old not anymore existing shares
            for file in remove_share:
                t = str(file)
                t = t.replace(os.path.normpath(str_dir1), os.path.normpath(str_dir2))
                if os.path.exists(t):
                    os.remove(t)
                self.crypto.copy_file_encrypt(f1=file, f2=t)

            to_share = []
            # creates list for all the new shares and the changed shares
            for entry in share:
                if entry in share and old_share[str(entry)] != share[str(entry)]:
                    to_share.append(entry)
                if entry not in share:
                    to_share.append(entry)

            # sync files from source Folder which share changed
            for file in to_share:
                t = str(file)
                t = t.replace(os.path.normpath(str_dir1), os.path.normpath(str_dir2))
                if os.path.exists(t):
                    os.remove(t)
                self.crypto.copy_file_encrypt(f1=file, f2=t)
