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

__author__ = 'David'

import os
import hashlib
import shutil
from threading import BoundedSemaphore

from watchdog.events import FileSystemEventHandler


class CoreSync(FileSystemEventHandler):
    """
    pre_sync does the initial sync the other methodes are used from watchdog.
    """

    def __init__(self, f1, f2, crypto):
        self.sourceFolder = f1
        self.cloudFolder = f2
        self.gpg = crypto
        self.Lock = BoundedSemaphore()
        self.hash = hashlib.md5()

    def pre_sync(self):
        """
        This Method pre synchronises the two folders. It only copy files to the other folder if it doesn't exist.
        It won't delete any data!

        :return: nothing
        """

        # the two directories to sync
        # changed the name to dir1 and dir2 for easier programming for me
        str_dir1 = self.sourceFolder
        str_dir2 = self.cloudFolder

        # time sync difference
        # if a file exists in both folders and the time is not the same we can define a "buffer" in which the programm
        # still sees the as same
        sync_difference = 0

        # list files and make sure there are no hidden ones (Linux and Mac).
        list_items_path1 = []  # only path
        list_items_name1 = []  # the name of the file you can join both for full name
        list_items_path2 = []
        list_items_name2 = []

        # scan source Folder for all files
        for path, subDirs, files in os.walk(str_dir1):
            list_items_path1.append(os.path.normpath(path))
            for name in files:
                list_items_name1.append(os.path.normpath(os.path.join(path, name)))

        # scan cloud Folder for all files
        for path, subDirs, files in os.walk(str_dir2):
            list_items_path2.append(os.path.normpath(path))
            for name in files:
                list_items_name2.append(os.path.normpath(os.path.join(path, name)))

        # delete source Folder and cloud Folder path
        # in the two list returned from the two for loops there will be the self.sourceFolder and the self.cloudFolder
        # i dont need them and so i delete them out of the list
        if list_items_path1:
            if os.path.normpath(str_dir1) in list_items_path1:
                list_items_path1.remove(os.path.normpath(str_dir1))
        if list_items_path2:
            if os.path.normpath(str_dir2) in list_items_path2:
                list_items_path2.remove(os.path.normpath(str_dir2))

        # sync folders from source Folder
        # first we need all the folders otherwise we cant store the files
        for folder in list_items_path1:
            if folder.replace(os.path.normpath(str_dir1), os.path.normpath(str_dir2)) not in list_items_path2:
                t = str(folder)
                t = t.replace(os.path.normpath(str_dir1), os.path.normpath(str_dir2))
                if not os.path.exists(t):
                    os.mkdir(t)

        # sync folders from cloud Folder
        # first we need all the folders otherwise we cant store the files
        for folder in list_items_path2:
            if folder.replace(os.path.normpath(str_dir2), os.path.normpath(str_dir1)) not in list_items_path1:
                t = str(folder)
                t = t.replace(os.path.normpath(str_dir2), os.path.normpath(str_dir1))
                if not os.path.exists(t):
                    os.mkdir(t)

        # sync files from source Folder
        for file in list_items_name1:
            if file.replace(os.path.normpath(str_dir1), os.path.normpath(str_dir2)) not in list_items_name2:
                # if file only exists in one folder
                t = str(file)
                t = t.replace(os.path.normpath(str_dir1), os.path.normpath(str_dir2))
                self.gpg.copy_file_encrypt(file, t)
            else:
                # if file exists in two folders
                t = str(file)
                t = t.replace(os.path.normpath(str_dir1), os.path.normpath(str_dir2))
                dict_mod = {file: os.stat(file).st_mtime,
                            t: os.stat(t).st_mtime}

                # if time doesnt match
                if dict_mod[file] != dict_mod[t]:
                    if dict_mod[file] > dict_mod[t] + sync_difference:
                        self.gpg.copy_file_encrypt(t, file)
                    elif dict_mod[t] > dict_mod[file] + sync_difference:
                        self.gpg.copy_file_decrypt(t, file)

        # sync files from cloud Folder
        for file in list_items_name2:
            if file.replace(os.path.normpath(str_dir2), os.path.normpath(str_dir1)) not in list_items_name1:
                # if file only exists in one folder
                t = str(file)
                t = t.replace(os.path.normpath(str_dir2), os.path.normpath(str_dir1))
                self.gpg.copy_file_decrypt(file, t)
            else:
                # if file exists in two folders
                t = str(file)
                t = t.replace(os.path.normpath(str_dir2), os.path.normpath(str_dir1))
                dict_mod = {file: os.stat(file).st_mtime,
                            t: os.stat(t).st_mtime}

                # if the times don't match (time is in seconds)
                if dict_mod[file] != dict_mod[t]:
                    if dict_mod[file] > dict_mod[t] + sync_difference:
                        self.gpg.copy_file_decrypt(t, file)
                    elif dict_mod[t] > dict_mod[file] + sync_difference:
                        self.gpg.copy_file_decrypt(t, file)
        # waere cool wenn das auf der Console stehen koennte ;)
        print("init done")

    def on_created(self, event):
        """
        Event action.
        Called when a file or directory is created.

        :param event: the triggered event
        :return: only syc operations
        """
        with self.Lock:

            print("create")
            # kann man auch auf der console ausgeben dann sieht man das mitrptokolieren der syncrhonisierten daten
            # werde da auch das created (naechste Variable) dazugeben damit man den namen sieht

            created = os.path.normpath(event.src_path)

            # if directory
            if os.path.isdir(created):
                created = os.path.normpath(event.src_path)
                # if source Folder
                if self.sourceFolder in created:
                    created = created.replace(self.sourceFolder, self.cloudFolder)
                    if not os.path.exists(created):
                        os.mkdir(created)
                else:
                    # if cloud folder
                    created = created.replace(self.cloudFolder, self.sourceFolder)
                    if not os.path.exists(created):
                        os.mkdir(created)

            # if file
            if os.path.isfile(created):
                if self.sourceFolder in created:
                    # if source Folder
                    new_created = created.replace(self.sourceFolder, self.cloudFolder)
                    if not os.path.exists(new_created):
                        self.gpg.copy_file_encrypt(f1=created, f2=new_created)
                else:
                    # if cloud folder
                    new_created = created.replace(self.cloudFolder, self.sourceFolder)
                    if not os.path.exists(new_created):
                        self.gpg.copy_file_decrypt(f1=created, f2=new_created)

    def on_deleted(self, event):
        """
        Event action
        Called when a file or directory is deleted.

        :param event: the triggered event
        :return: only syc operations
        """

        with self.Lock:
            print("del")

            deleted = os.path.normpath(event.src_path)

            if self.sourceFolder in deleted:
                # if source Folder
                deleted = deleted.replace(self.sourceFolder, self.cloudFolder)
                if os.path.isdir(deleted):
                    if os.path.exists(deleted):
                        shutil.rmtree(deleted, True)
                else:
                    if os.path.exists(deleted):
                        os.remove(deleted)
            else:
                # if cloud Folder
                deleted = deleted.replace(self.cloudFolder, self.sourceFolder)
                if os.path.isdir(deleted):
                    if os.path.exists(deleted):
                        shutil.rmtree(deleted, True)
                else:
                    if os.path.exists(deleted):
                        os.remove(deleted)

    def on_modified(self, event):
        """
        Event action.
        Called when a file or directory is modified.

        Why do we need a temp file?
        The time modification of a file is registerd with this event so if we wouldn't
        compare the two temp files with hashes and then stop a new encryption/decryption
        we would have an endless loop.

        :param event: the triggered event
        :return: only syc operations
        """

        with self.Lock:

            print("mod")

            mod = os.path.normpath(event.src_path)

            if os.path.isdir(mod):
                pass
            else:
                # get other path
                if self.sourceFolder in mod:
                    new_mod = mod.replace(self.sourceFolder, self.cloudFolder)
                else:
                    new_mod = mod.replace(self.cloudFolder, self.sourceFolder)

                h1 = None
                h2 = None

                if os.path.exists(mod) and os.path.exists(new_mod):
                    # create a temp file for comparing the two files
                    # why cant compare a encrypted and decrypted file need to temporarily decrypt the file and
                    # calc hash
                    path_to_this_folder = os.path.realpath("cc_core_sync.py")
                    base_name = os.path.basename(path_to_this_folder)
                    temp = path_to_this_folder.replace(base_name, "")
                    temp = os.path.join(temp, os.path.basename(mod))

                    if self.sourceFolder in mod:
                        self.gpg.copy_file_decrypt(f1=new_mod, f2=temp, time_sync=False)
                    else:
                        self.gpg.copy_file_decrypt(f1=mod, f2=temp, time_sync=False)
                    # calc hashes
                    h1 = self._calc_md5_hash(mod)
                    h2 = self._calc_md5_hash(temp)
                    # del temp file
                    os.remove(temp)

                if os.path.isfile(mod):
                    if (h1 is not None and h2 is not None) and h1 == h2:
                        pass
                    elif self.sourceFolder in mod:
                        self.gpg.copy_file_encrypt(f1=mod, f2=new_mod)
                    else:
                        self.gpg.copy_file_decrypt(f1=mod, f2=new_mod)

    def on_moved(self, event):
        """
        Event action.
        Called when a file or a directory is moved or renamed.

        :param event: the triggered event
        :return: only syc operations
        """

        with self.Lock:

            print("mov")

            renamed = os.path.normpath(event.src_path)
            renamed2 = os.path.normpath(event.dest_path)

            if self.sourceFolder in renamed:
                # if the event trigers in the source Folder
                renamed = renamed.replace(self.sourceFolder, self.cloudFolder)
                renamed2 = renamed2.replace(self.sourceFolder, self.cloudFolder)
                if os.path.exists(renamed):
                    os.rename(renamed, renamed2)
            else:
                # if the event triggers in the cloud Folder
                renamed = renamed.replace(self.cloudFolder, self.sourceFolder)
                renamed2 = renamed2.replace(self.cloudFolder, self.sourceFolder)
                if os.path.exists(renamed):
                    os.rename(renamed, renamed2)

    def _calc_md5_hash(self, file):
        """
        calculates an md5 hash of a file

        :param file: given file
        :return: md5 hash
        """
        self.hash = hashlib.md5()
        with open(file, 'rb') as file:
            buf = file.read()
            self.hash.update(buf)

        return self.hash.hexdigest()
