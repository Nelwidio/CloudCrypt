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

import sqlite3
import os

import cc_con


class Usermgmt():
    """
    Class to manage users groups.

    This Class uses a SQLite database to manage users and groups.
    """

    def __init__(self,
                 path_to_database=cc_con.CC_DEFAULT_USERMGMT_PATH,
                 path_to_gpg_keyring=cc_con.CC_DEFAULT_GPG_KEY_PATH):
        """
        Create a new Usermgmt object and initialize the database

        :crypto: A instance of cc_crypto, this is needed to check, if a users key is in the key database
        :param path_to_db: The path to the user and group database
        :return: A new Usermgmt object
        """
        self.crypto = crypto
        self.path_to_database = path_to_database
        self.path_to_gpg_key = path_to_gpg_keyring
        if os.path.exists(self.path_to_database):
            self.conn = sqlite3.connect(self.path)
        else:
            self.conn = sqlite3.connect(self.path)
            # to make sure the database is properly closed
            with self.conn:
                cur = self.conn.cursor()
                # Create tables for the new database
                cur.execute(cc_con.CC_USERMGMT_CREATE_TABLE_USER)
                cur.execute(cc_con.CC_USERMGMT_CREATE_TABLE_GROUP_NAME)
                cur.execute(cc_con.CC_USERMGMT_CREATE_TABLE_GROUPS)
            # Save the changes to the database
            self.conn.commit()

    def create_user(self, name, fingerprint, path_to_gpg_key=self.path_to_gpg_key, groups=None):
        """
        Create a new user.

        This Method creates a new user and inserts it into the user and group management database.
        It searches a gpg keyring for the users key and assigns it to the entry in the database.
        :param name: The name of the new user.
        :param fingerprint: The fingerprint of the key that will be assigned to the user. The Method searches a gpg
        key database for this fingerprint
        :param path_to_gpg_key: The path to the gpg keyring that will be searched for the users key
        :param groups: Groups is a tuple of strings that specify the names of groups the new user will be added to
        :return: None
        """

        # check, if the user name fulfills the requirements for a username
        if not self._is_valid_name(name):
            raise ValueError(name + 'is not a valid name for a user')
        # check, if the group names fulfill the requirements for group names
        if groups:
            for name in groups:
                # if a group name is not valid, then remove it from the groups tuple
                if not self._is_valid_name(name):
                    lis = list(groups)
                    del (lis[name])
                    groups = tuple(lis)
        # check, if the key database exists
        if not os.path.exists(path_to_gpg_key):
            raise FileNotFoundError('file' + path_to_gpg_key + "not found")
        # check, if the fingerprint is contained in the key database
        if not self.crypto.is_key(fingerprint):
            raise ValueError('key with fingerprint' + fingerprint + 'was not found in the database')

        # add the new user to the database
        # to make sure, the database is properly closed
        with self.conn:
            cur = self.conn.cursor()
            # check, if the user is already in the database
            cur.execute("Select * from 'user' where name = ?", name)
            # the user was not already in the database
            if not cur.fetchone():
                cur.execute("INSERT INTO 'user'('name','fingerprint') VALUES (?,?);", (name, fingerprint))
            else:
                raise ValueError('the user' + name + 'was already in the database')
                # TODO: add the user to the groups
        self.conn.commit()

    @staticmethod
    def _is_valid_name(name):
        """
        Check, if a name fulfills the requirements for a CloudCrypt user or group name

        :param: name: The string that will be checked
        :returns: True if the name is valid and False if the name is not valid
        """
        if not name or len(name) > 64:
            return False
        # efficient way to determine, if the name is ascii
        try:
            name.decode('ascii')
        except UnicodeDecodeError:
            return False
        return True

    def create_group(self, name, usernames=None):
        """
        Create a new group.

        This Method creates a new group and adds it to the user and group database.
        Optionally the Method can take a tuple of user names which will be added to the group
        :param name: The name of the new group; if the group name already exists in the database a exception is raised
        :param usernames: A tuple of strings which contain names of users that will be added to the new group.
        If a name is not found in the database it is just ignored
        :return: None
        """
        # check, if the group name is a valid name
        if not self._is_valid_name(name):
            raise ValueError(name + 'is not a valid group name')
        # check, if the group names are valid; if one is not, it is just ignored and removed from the tuple
        if usernames:
            for name in usernames:
                if not self._is_valid_name(name):
                    lis = list(usernames)
                    del (lis[name])
                    usernames = tuple(lis)
        # assure, that the resource is closed properly after usage
        with self.conn:
            cur = self.conn.cursor()
            # check, if the group name is already used
            cur.execute("Select * from 'group_name' where name = ?", name)
            # if it is not already used, than add the new group to the database
            if not cur.fetchone():
                cur.execute("INSERT INTO 'group_name'('name') VALUES (?);", name)
            else:
                raise ValueError(name + 'is already used as a group name in the database')
                # TODO add the user names to the group
        self.conn.commit()

    def delete_user(self, name, path_to_database=self.path_to_database):
        """
        Delete a user from the user and group database

        This Method deletes a user from the user and group database.
        The user is deleted from all tables in the database.

        :param name: The name of the user that will be deleted. As it is a requirement for names to be unique we can
        use it here to identify the user
        :param path_to_database: The path to the database from which the user is about to be delted
        :return: None
        """
        # check if the specified user name is valid
        if not self._is_valid_name(name):
            raise ValueError(name + 'is not a valid name for a user')
        # check, if the specified database file exists
        if not os.path.exists(path_to_database):
            raise ValueError(path_to_database + 'not found')
        # make sure that the resource is properly freed after usage
        with self.conn:
            cur = self.conn.cursor()
            # check, if there is a user with the specified name in the database
            cur.execute("Select * from 'user' where name = ?", name)
            if cur.fetchone():
                cur.execute("DELETE FROM 'user' WHERE name = ?;", name)
                # TODO delete the user from the other tables
            else:
                raise ValueError('user' + name + 'cannot be deleted from the database, there is no such user.')
        self.conn.commit()

    def get_user_names(self, path_to_database=self.path_to_database):
        """
        Return a tuple containing the names of all users in the database.

        :param: path_to_database: The path to the database that contains the users who's names you want
        :return: A tuple containing the names of all users in the database
        """
        return cur.execute("Select name from 'user'", path_to_database)

    def get_group_names(self, path_to_database=self.path_to_database):
        """
        Return a tuple containing the names of all groups in the database

        :param: path_to_database: The path to the database that contains the groups who's names you want
        :return: A tuple containing the names of all groups in the database
        """
        return self._get_names("Select name from 'group_name'", path_to_database)

    def _get_names(self, query, path_to_database=self.path_to_database):
        """
        Query the user and group database and pack the result into a tuple

        :param: query: The query that is passed to the database
        :param: path_to_database: The path to the database the query will act upon
        :return: A tuple containing the result of the query
        """
        # check, if the specified database file exists
        if not os.path.exists(path_to_database):
            raise ValueError(path_to_database + 'not found')
        # make sure, that the resource is freed after use
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(query)
        # make a tuple out of the query result and return it
        return tuple(cur.fetchall())

    # TODO those two methods are not ready yet; Job for tomorrow
    # Anmerkung: wofür brauchen wir die Mehtode ich kann mir kein sinvolles Szenarion vorstellen.
    def get_user_groups(self, name, path_to_database=self.path_to_database):
        """
        get all groups a user is in, to authenticate the user we take the fingerprint because its unique
        the name isn't

        :param fingerprint: fingerprint of the user to search
        :return: all groups the user is in
        """
        return self._get_members(name, "Select id from 'user' where fingerprint = ?",
                                 "Select name from groups INNER JOIN 'group_name' ON group_name.id"
                                 " == groups.group_id where user_id = ?",
                                 path_to_database)

    def get_group_members(self, name, path_to_database=self.path_to_database):
        """
        get all members of a group a user is in

        :param group: the name of the group
        :return: --
        """
        return self._get_members(name, "Select id from 'group_name' where name = ?",
                                 "Select name from groups INNER JOIN 'user' ON user.id == "
                                 "groups.user_id where groups.group_id =?",
                                 path_to_database)

    def _get_members(self, name, object_exist_query, info_query, path_to_database=self.path_to_database):
        """
        """
        # check, if name fulfills the requirements for a name
        if not self._is_valid_name(name):
            raise ValueError(name + 'is not a valid name')
        # check, if the database file exists
        if not os.path.exists(path_to_database):
            raise ValueError(path_to_database + 'not found')
        # make sure the resource is properly freed after use
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(object_exist_query, name)
            if cur.fetchone():
                cur.execute(info_query, name)
                return tuple(cur.fetchall)

                ########################################

    def create_default_users(self, public_key_list):
        """
        takes the public_key_list of the crypto class and creats a user list of all People in the keyring

        :param public_key_list: public_key_list
        :return: --
        """
        # if public key list is empty return
        if not public_key_list:
            return

        for user in public_key_list:
            # extract fingerprint out of list
            fingerprint = user['fingerprint']
            # extract the name out of list and dictionary
            user_name = user['uids']
            user_name = user_name[0]
            user_name = str(user_name)
            user_name = user_name.split(' <')
            # create the user
            self.create_user(name=user_name[0], fingerprint=fingerprint)

    def add_user_to_groups(self, fingerprint, groups):
        """
        add a user (authenticated through fingerprint) to a group

        :param fingerprint: fingerprint of user
        :param groups: groups to add to (list) eg ("group1", "group2)
        :return: --
        """
        # check if name exists
        c = self.conn.cursor()
        t = (fingerprint,)
        c.execute("Select * from 'user' where fingerprint = ?", t)
        user_ret = c.fetchone()

        # check if the group id exists
        t = (groups[0],)
        c.execute("Select id from 'group_name' where name = ?", t)
        group_name_ret = c.fetchone()

        # add user to group if both group and user exist
        if user_ret is not None and group_name_ret is not None:
            # iterate through groups
            for single_group in groups:
                # get the id from group
                t = (single_group,)
                c.execute("Select id from 'group_name' where name = ?", t)
                id_group = c.fetchone()
                # check if user is already in group if not
                question = (user_ret[0], id_group[0])
                c.execute("Select * from 'groups' where  user_id = ? and group_id = ?", question)
                # fill him in here
                if c.fetchone() is None:
                    t = (user_ret[0], id_group[0])
                    c.execute("INSERT INTO 'groups'('user_id','group_id') VALUES (?,?);", t)
                    self.conn.commit()

    def remove_user_from_group(self, user_fingerprint, group):
        """
        remove a user from a group

        :param user_fingerprint: fingerprint of the user
        :param group: the group name you want to remove him from
        :return: --
        """
        # check if user is valid
        c = self.conn.cursor()
        t = (user_fingerprint,)
        c.execute("Select id from 'user' where fingerprint = ?", t)
        user_ret = c.fetchone()

        # if user exists
        if user_ret is not None:
            # go through all the groups which got handled over to this method
            for single_group in group:
                # get the id of the groupe
                t = (single_group,)
                c.execute("Select id from 'group_name' where name = ? ", t)
                ident = c.fetchone()
                # remove user here
                t = (user_ret[0], ident[0])
                c.execute("DELETE FROM 'groups' where groups.user_id = ? AND groups.group_id = ?", t)
                self.conn.commit()

    def edit_user(self, name, fingerprint):
        """
        edit a users name

        :param name: new name
        :param fingerprint: fingerprint of the user
        :return: --
        """
        # find out if user is valid
        c = self.conn.cursor()
        t = (fingerprint,)
        c.execute("Select id from 'user' where fingerprint = ?", t)
        user_ret = c.fetchone()

        # if he is update him
        if user_ret is not None:
            t = (name, user_ret[0])
            c.execute("UPDATE 'user' SET 'name'=? WHERE id = ?", t)
            self.conn.commit()

    def get_group_ﬁngerprints(self, group):
        """
        get all fingerprints of a group

        needed for the crypto class to encrypt

        :param group: name of group
        :return: list of fingerprints
        """
        # get the group id
        c = self.conn.cursor()
        t = (group,)
        c.execute("Select id from 'group_name' where name = ?", t)
        group_id = c.fetchone()

        # get all the fingerprints of the people who are in that group
        if group_id is not None:
            t = (group_id[0],)
            c.execute(
                "Select fingerprint from 'user' INNER JOIN 'groups' ON groups.user_id "
                "== user.id where groups.group_id = ?", t)
            return c.fetchall()

    def close_db(self):
        """
        close db connection

        :return: --
        """
        self.conn.close()
