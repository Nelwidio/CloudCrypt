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
This is a module of the project <CloudCrypt>. Its main feature
is to display help pages in html-format in the system's default
webbrowser.
"""

from os.path import exists, isfile, join, realpath, dirname
from urllib.parse import urlunparse
from webbrowser import open, get, Error

# here we store the preferred webbrowsers; if none of them is installed,
# we cannot use anchors
PREFERRED_BROWSERS = ['firefox', 'chrome', 'safari', 'chromium', 'konqueror',
                      'opera', 'lynx', 'windows-default']


def _does_file_exist_(file_name):
    """
    This function checks if a file exists. If it does exist and it is a file,
    it will return <True>. Otherwise it will return <False>.

    :param file_name: name of the file to check for
    :return: <True> if file exists and is a file, <False> otherwise
    """
    if exists(str(file_name)):
        if isfile(str(file_name)):
            return True
        else:
            return False
    else:
        return False


def _set_language_(language):
    """
    Takes the language as a string and returns the appropriate language code.
    If <language> is 'ger' the function returns 'ger'. In all other cases it
    returns 'eng'.

    :param language: the language to choose
    :return: 'ger' if <language> is 'ger', 'eng' otherwise
    """
    if str(language) == "de":
        return "ger"
    else:
        return "eng"


class Help(object):
    """
    This class provides a function to open up html help pages in the system's
    default web browser.
    """

    def __init__(self, language="eng"):
        """
        Constructor of <Help>. Takes <language> as parameter (its default value
        is 'eng'). After creating the object, the language of the object will be
        set and a uninitialized object for the web browser is defined.

        :param language: Parameter for the language
        :return: None
        """
        self.lang = _set_language_(str(language))
        self.folder = join(dirname(__file__), "help", self.lang)
        self.web = None

    def _get_language_(self):
        """
        Returns the value of the classe's member variable <lang>.

        :return: Value of <self.lang>. Will either be 'ger' or 'eng'.
        """
        return str(self.lang)

    def open_help(self, page, anchor):
        """
        Opens the specified help page. If <page> cannot be found, an error
        page will be opened. <anchor> will be attached to the url to enable
        the user to navigate inside a single html-page. The anchor will only
        be added, if one of the preferred browser is installed on the system
        (in order to prevent errors or strange behaviour).

        :param page: The page to open. The page is a html-file inside the
        folder 'help/<lang-code>/'.
        :param anchor: The anchor to attach to the url. Will be ignored if
        none of the prefered browsers is installed
        :return: The opened url as string
        """

        # First we create the path to the requested file. The file always is in
        # 'help/<lang>/'. If the file does exist, we append its name to the
        # path, if it does not exist, we append 'error.html', so the error-page
        # in the requested language will be displayed.
        requested = realpath(join(self.folder, str(page)))
        if not _does_file_exist_(requested):
            file_name = join(self.folder, "error.html")
            anchor = ''  # the error page does not need anchors
        else:
            file_name = requested

        # Here we try to get a handle for one of the prefered web browsers.
        # If we can get one, we take the handle and stop searching for another
        # handle. If we cannot get a handle (which means the browser is not
        # installed, we print an error message and take the next browser.
        web = None
        for browser in PREFERRED_BROWSERS:
            try:
                web = get(browser)
                break
            except Error:
                print("Was not able to open browser <" + str(browser) +
                      ">. Trying another...")

        # Here we open the url. The variable <web> will be <None> if we did not
        # find a handle for a prefered browser. So we open the url without
        # attaching the anchor (by requesting an automatic handle). Otherwise we
        # can append the url, because we can use one of the prefered browsers.
        if web:
            url = urlunparse(['file', '', realpath(file_name), '', '',
                              str(anchor)])
            web.open(url)
            return str(url)
        else:
            url = urlunparse(['file', '', realpath(file_name), '', '', ''])
            open(url)
            return str(url)


if __name__ == "__main__":
    pass
