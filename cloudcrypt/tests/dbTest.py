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

__author__ = 'david'

import os
import platform
import getpass
from os.path import normpath, realpath

# from cloudcrypt import cc_crypto
from .. import cc_usermgmt_2
from .. import cc_crypto

# set before test
if platform.system() is 'Linux':
    user = getpass.getuser()
    keyPathFolder = realpath(normpath("/home/" + user + "/keys/KeyFolderCloudCrypt"))
    path_to_db1 = realpath(normpath("/home/" + user + "/db/test.db"))
    path_to_db2 = realpath(normpath("/home/" + user + "/db/test2.db"))
elif platform.system() is 'Windows':
    keyPathFolder = realpath(normpath("C:/test/keys/KeyFolderCloudCrypt"))
    path_to_db1 = realpath(normpath("C:/test/db/test.db"))
    path_to_db2 = realpath(normpath("C:/test/db/test2.db"))
else:
    keyPathFolder = None
    path_to_db1 = None
    path_to_db2 = None

# test start

g = cc_usermgmt_2.Usermgmt(path_to_db=path_to_db1)

g.create_user(name="test1", fingerprint="print1")
g.create_user(name="test2", fingerprint="print2")
g.create_user(name="test3", fingerprint="print3")
g.create_user(name="test4", fingerprint="print4")

g.create_group(name="gruppe1")
g.create_group(name="gruppe2")
g.create_group(name="gruppe3")
g.create_group(name="gruppe4")

g.delete_user(fingerprint="print1")

print(g.get_user_names())
print(g.get_group_names())

g.add_user_to_groups("print2", ("gruppe3", "gruppe4"))
g.add_user_to_groups("print3", ("gruppe3", "gruppe4", "gruppe1"))
g.add_user_to_groups("print1", ("gruppe3", "gruppe4", "gruppe1"))

print(g.get_user_groups(fingerprint="print2"))

print(g.get_group_members(group="gruppe4"))

g.remove_user_from_group(user_fingerprint="print3",
                         group=("gruppe3", "gruppe4"))

g.edit_user(name="newName", fingerprint="print1")

print(g.get_group_ﬁngerprints(group="gruppe4"))

g.close_db()

# test default user add
secretPassphrase = "DUMMY PASSPHRASE YOU DONT NEED TO FILL ONE IN HERE FOR THE " \
                   "TEST"

g2 = cc_usermgmt_2.Usermgmt(path_to_db=path_to_db2)

crypto = cc_crypto.Crypto(keyPathFolder, secretPassphrase, g2)

g2.create_default_users(crypto.get_key_list_public())

print(g2.get_user_names())

g2.close_db()

# remove the 2 created db from the test
os.remove(path_to_db1)
os.remove(path_to_db2)
