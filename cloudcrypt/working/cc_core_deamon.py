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

from watchdog.observers import Observer


class CoreSyncDaemon():
    """Manages the watchdog Plugin"""

    def __init__(self, gpg, directory):
        self.directory_observer = directory
        self.gpg = gpg
        self.observer = Observer()
        print("test")

    def starter(self):
        """
        starts watchdog
        :return: noting
        """
        print("running")
        print(self.directory_observer)
        self.observer.schedule(self.gpg, self.directory_observer, recursive=True)
        self.observer.start()
        self.observer.join()

    def stop(self):
        """
        stops the deamon
        need to test it when cc_usermgmt is finished
        :return:
        """
        print("stop")
        self.observer.stop()

    def start(self):
        """
        starts deamon again
        need to test it when cc_usermgmt is finished
        :return:
        """
        print("start")
        self.observer.start()
