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

__author__ = ''

import sqlite3
import os


class Usermgmt:
    """
    Class to create users groups and read there finger prints with the help of
    a sqlite database.

    Es fehlen noch die Exceptions was aber leicht eingefügt ist nur hinter allen
    if abfragen dann die Exception.
    Wir müssen noch klären wie wir das machen. (eigene Exceptionklase,....)
    """

    def __init__(self, path_to_db):
        """
        initializes a new db or uses a already existing one

        :param path_to_db: path to db
        :return: --
        """
        self.path = os.path.realpath(str(path_to_db))
        if os.path.exists(self.path):
            self.conn = sqlite3.connect(self.path)
        else:
            self.conn = sqlite3.connect(self.path)
            c = self.conn.cursor()

            # Create table
            c.execute(
                "CREATE TABLE 'user' ('id' INTEGER NOT NULL PRIMARY KEY "
                "AUTOINCREMENT, 'name' TEXT NOT NULL, "
                "'fingerprint' TEXT NOT NULL);")

            c.execute("CREATE TABLE 'group_name' ( 'id' INTEGER PRIMARY KEY "
                      "AUTOINCREMENT, 'name' TEST UNIQUE);")

            c.execute("CREATE TABLE 'groups' ('user_id' INTEGER,"
                      "'group_id' INTEGER);")

            # Save (commit) the changes
            self.conn.commit()

    def create_user(self, name, fingerprint):
        """
        creates a user with name and fingerprint

        :param name: name
        :param fingerprint: fingerprint
        :return: --
        """
        c = self.conn.cursor()
        t = (fingerprint,)
        c.execute("Select * from 'user' where fingerprint = ?", t)
        t = (name, fingerprint)
        if c.fetchone() is None:
            c.execute("INSERT INTO 'user'('name','fingerprint') "
                      "VALUES (?,?);", t)
            self.conn.commit()

    def create_default_users(self, public_key_list):
        """
        takes the public_key_list of the crypto class and creats a user list of
        all People in the keyring

        :param public_key_list: public_key_list
        :return: --
        """
        if not public_key_list:
            return

        for user in public_key_list:
            fingerprint = user['fingerprint']
            user_name = user['uids']
            user_name = user_name[0]
            user_name = str(user_name)
            user_name = user_name.split(' <')
            self.create_user(name=user_name[0], fingerprint=fingerprint)

    def create_group(self, name):
        """
        creates a new group

        :param name: name of the group
        :return: --
        """
        c = self.conn.cursor()
        t = (name,)
        c.execute("Select * from 'group_name' where name = ?", t)
        if c.fetchone() is None:
            c.execute("INSERT INTO 'group_name'('name') VALUES (?);", t)
            self.conn.commit()

    def delete_user(self, fingerprint):
        """
        fingerprint brauchen wir weil das unique ist

        :param fingerprint: fingerprint of user
        :return: --
        """
        c = self.conn.cursor()
        t = (fingerprint,)
        c.execute("Select * from 'user' where fingerprint = ?", t)
        if c.fetchone() is not None:
            c.execute("DELETE FROM 'user' WHERE name = ?;", t)
            self.conn.commit()

    def get_user_names(self):
        """
        get all names from the users
        :return: list of all users in db
        """
        c = self.conn.cursor()
        c.execute("Select name from 'user'")
        return c.fetchall()

    def get_group_names(self):
        """
        get a list of all groups in db
        :return: list of all groups in db
        """
        c = self.conn.cursor()
        c.execute("Select name from 'group_name'")
        return c.fetchall()

    def get_user_groups(self, fingerprint):
        """
        get all groups a user is in, to authenticate the user we take the
        fingerprint because its unique the name isn't

        :param fingerprint: fingerprint of the user to search
        :return: all groups the user is in
        """
        c = self.conn.cursor()
        t = (fingerprint,)
        c.execute("Select id from 'user' where fingerprint = ?", t)
        t = c.fetchone()
        if t is not None:
            c.execute("Select name from groups INNER JOIN 'group_name' "
                      "ON group_name.id == groups.group_id where user_id = ? ",
                      t)
            return c.fetchall()

    def get_group_members(self, group):
        """
        get all members of a group a user is in

        :param group: the name of the group
        :return: --
        """
        c = self.conn.cursor()
        t = (group,)
        c.execute("Select id from 'group_name' where name = ?", t)
        t = c.fetchone()
        if t is not None:
            c.execute("Select name from groups INNER JOIN 'user' ON user.id == groups.user_id where groups.group_id =?",
                      t)
            return c.fetchall()

    def add_user_to_groups(self, fingerprint, groups):
        """
        add a user (authenticated through fingerprint) to a group

        :param fingerprint: fingerprint of user
        :param groups: groups to add to (list) eg ("group1", "group2)
        :return: --
        """
        c = self.conn.cursor()
        t = (fingerprint,)
        c.execute("Select * from 'user' where fingerprint = ?", t)
        user_ret = c.fetchone()

        t = (groups[0],)
        c.execute("Select id from 'group_name' where name = ?", t)
        group_name_ret = c.fetchone()

        if user_ret is not None and group_name_ret is not None:
            for single_group in groups:
                t = (single_group,)
                c.execute("Select id from 'group_name' where name = ?", t)
                id_group = c.fetchone()
                question = (user_ret[0], id_group[0])
                c.execute("Select * from 'groups' where  user_id = ? and group_id = ?", question)
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
        c = self.conn.cursor()
        t = (user_fingerprint,)
        c.execute("Select id from 'user' where fingerprint = ?", t)
        user_ret = c.fetchone()

        if user_ret is not None:
            for single_group in group:
                t = (single_group,)
                c.execute("Select id from 'group_name' where name = ? ", t)
                identification = c.fetchone()
                t = (user_ret[0], identification[0])
                c.execute("DELETE FROM 'groups' where groups.user_id = ? AND groups.group_id = ?", t)
                self.conn.commit()

    def edit_user(self, name, fingerprint):
        """
        edit a users name

        :param name: new name
        :param fingerprint: fingerprint of the user
        :return: --
        """
        c = self.conn.cursor()
        t = (fingerprint,)
        c.execute("Select id from 'user' where fingerprint = ?", t)
        user_ret = c.fetchone()

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
        c = self.conn.cursor()
        t = (group,)
        c.execute("Select id from 'group_name' where name = ?", t)
        group_id = c.fetchone()

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
