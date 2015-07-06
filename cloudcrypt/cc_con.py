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

import os

# width of the main window
MAIN_WIDTH = 900

# height of the main window
MAIN_HEIGHT = 500

# the title of the main window
MAIN_TITLE = 'CloudCrypt'

# the default path to the config file
CC_DEFAULT_CONFIG_PATH = os.path.join('..', 'config', 'config.conf')

CC_DEFAULT_PASSWORD_PATH = os.path.join('..', 'config', 'PASSWORD_FILE')

LANGFILE_PREFIX = os.path.join('..', 'texts', 'cc_texts_')

LANGFILE_ENDING = '.txt'

CONFIG_FILE_COMMENTARY = "#"

TOOLTIP_POSTFIX = '_tooltip'

PASSWORD_MIN_LEN = 8

PASSWORD_MAX_LEN = 63

########################################################################################################################
#                                               Begin Config Options                                                   #
########################################################################################################################

# the name of the password config option
USER_PW = "user_password"
USER_PW_DEFAULT = ""

# the path to the directory containing the plain text files
SCR_DIR = "path_to_plaintext_dir"
SCR_DIR_DEFAULT = ""

# the path to the directory where CloudCrypt will put the encrypted files
DST_DIR = "path_to_encrypted_dir"
DST_DIR_DEFAULT = ""

# whether CloudCrypt will show the advanced settings tab
SHOW_ADV_SET = "show_advanced_settings"
SHOW_ADV_SET_DEFAULT = ""

# whether CloudCrypt will show verbose tooltips
SHOW_VERB_TOOL = "show_verbose_tooltips"
SHOW_VERB_TOOL_DEFAULT = ""

# path to a qss file that will be used for the ui
THEME = "theme"
THEME_DEFAULT = "default"
THEME_PREFIX = os.path.join('..', 'themes', '')
THEME_POSTFIX = ".qss"

# whether the message area is shown
SHOW_MSG_AREA = "show_message_area"
SHOW_MSG_AREA_DEFAULT = ""

# whether CloudCrypt asks before it closes
QUIT_WITHOUT_CONFIRM = "quit_without_asking"
QUIT_WITHOUT_CONFIRM_DEFAULT = ""

# whether to start CloudCrypt minimized
START_MINIMIZED = "start_minimized"
START_MINIMIZED_DEFAULT = ""

# whether the program is run for the first time; used to generate the actual encryption key
FIRST_RUN_FLAG = "is_softwares_first_run"

DEFAULT_CONFIG = {}

########################################################################################################################
#                                               End Config Options                                                     #
########################################################################################################################



