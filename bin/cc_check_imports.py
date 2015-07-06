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

__author__ = 'Luca'

if __name__ == '__main__':

    import sys

    # list of missing modules
    missing = []

    try:
        import PyQt5.QtWidgets
    except ImportError:
        missing.append("PyQt5.QtWidgets")

    try:
        import PyQt5.QtCore
    except ImportError:
        missing.append("PyQt5.QtCore")

    try:
        import PyQt5.QtGui
    except ImportError:
        missing.append(("PyQt5.QtGui"))

    try:
        import cloudcrypt.cc_advset_tab
    except ImportError:
        missing.append("cloudcrypt.cc_advset_tab")

    try:
        import cloudcrypt.cc_con
    except ImportError:
        missing.append("cloudcrypt.cc_con")

    try:
        import cloudcrypt.cc_config_parser
    except ImportError:
        missing.append("cloudcrypt.cc_config_parser")

    try:
        import cloudcrypt.cc_core
    except ImportError:
        missing.append("cloudcrypt.cc_core")

    try:
        import cloudcrypt.cc_crypto
    except ImportError:
        missing.append("cloudcrypt.cc_crypto")

    try:
        import cloudcrypt.cc_gui
    except ImportError:
        missing.append("cloudcrypt.cc_gui")

    try:
        import cloudcrypt.cc_help
    except ImportError:
        missing.append("cloudcrypt.cc_help")

    try:
        import cloudcrypt.cc_norset_tab
    except ImportError:
        missing.append("cloudcrypt.cc_norset_tab")

    try:
        import cloudcrypt.cc_option_wizard
    except ImportError:
        missing.append("cloudcrypt.cc_option_wizard")

    try:
        import cloudcrypt.cc_sync
    except ImportError:
        missing.append("cloudcrypt.cc_sync")

    try:
        import cloudcrypt.cc_sync_thread
    except ImportError:
        missing.append("cloudcrypt.cc_sync_thread")

    try:
        import cloudcrypt.cc_texts
    except ImportError:
        missing.append("cloudcrypt.cc_texts")

    try:
        import xml.etree
    except ImportError:
        missing.append("xml.etree")

    try:
        import xml.parsers
    except ImportError:
        missing.append("xml.parsers")

    try:
        import gnupg
    except ImportError:
        missing.append("gnupg")

    try:
        import urllib.parse
    except ImportError:
        missing.append("urllib.parse")

    try:
        import webbrowser
    except ImportError:
        missing.append("webbrowser")

    try:
        import base64
    except ImportError:
        missing.append("base64")

    try:
        import threading
    except ImportError:
        missing.append("threading")

    try:
        import sqlite3
    except ImportError:
        missing.append("sqlite3")

    if not missing:
        # all modules available
        sys.exit(0)
    else:
        # modules are missing
        sys.exit(1)
