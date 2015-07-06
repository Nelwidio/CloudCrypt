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

import cc_core

# to configure
f1 = os.path.normpath("C:/test/data1")
f2 = os.path.normpath("C:/test/data2")
keyPathFolder = os.path.normpath("C:/test/keys/KeyFoulderCloudCrypt")
secretPassphrase = "pass"

path_to_db1 = "C:/test/db/test.db"

core = cc_core.Core(f1=f1, f2=f2, db_path=path_to_db1)

core.start_crypto(key_path_folder=keyPathFolder, pass_phrase=secretPassphrase, own_keyring=True)

core.start_sync()
