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

from os.path import dirname, join
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from cloudcrypt import cc_con
import cloudcrypt.cc_texts as cc_texts
import cloudcrypt.cc_help as cc_help
from cloudcrypt.cc_advset_tab import AdvSetTab
from cloudcrypt.cc_norset_tab import NorSetTab


class Gui(QWidget):

    def __init__(self, config, core, language='de'):
        super(Gui, self).__init__()

        # setup the translation object
        self.language = language
        self.tran = cc_texts.Texts(self.language)
        self.helper = cc_help.Help(self.language)
        self.configparser = config
        self.config = config.read_config()
        self.core_ref = core
        self.messages = set()
        self.thread = None
        self.mainLayout = None
        self.mainsplitter = None
        self.maintabwidget = None
        self.status_line = None
        self.settab = None
        self.advtab = None
        self.keytab = None
        self.ugtab = None
        self_selected_tab = None

        # set the main window name and icon
        self.setWindowTitle(self.tran.get_text("title"))
        self.setWindowIcon(QIcon(join(dirname(__file__), "resources/Logo_v2.png")))

        # configure the main window
        self.setObjectName('main_window')
        self.resize(800, 700)
        self.center()

        self.status_line = QTextBrowser(self.mainsplitter)
        self.status_line.setObjectName('status_line')

        # setup the main layout
        self.mainLayout = QGridLayout(self)
        self.mainLayout.setObjectName('main_layout')

        # setup the main splitter
        self.mainsplitter = QSplitter(self)
        self.mainsplitter.setOrientation(Qt.Vertical)
        self.mainsplitter.setObjectName('main_splitter')

        # setup the tab widget
        self.maintabwidget = QTabWidget(self.mainsplitter)
        self.maintabwidget.setObjectName('main_tab_widget')

        # make sure, the tab are is bigger than the message area
        self.maintabwidget_sizepolicy = QSizePolicy()
        self.maintabwidget_sizepolicy.setVerticalStretch(2)
        self.maintabwidget.setSizePolicy(self.maintabwidget_sizepolicy)
        self.maintabwidget.currentChanged.connect(self._sync)

        # setup the settings tab
        self.settab = NorSetTab(self)
        self._selected_tab = self.settab
        self.advtab = AdvSetTab(self)
        self.maintabwidget.addTab(self.settab, self.tran.get_text('settings_title'))
        self.settab.init()

        # setup the status line
        self.status_line = QTextBrowser(self.mainsplitter)
        self.status_line.setObjectName('status_line')

        # add the elements to the main layout
        self.mainLayout.addWidget(self.mainsplitter, 0, 0, 1, 1)
        self.menubar = QMenuBar()
        self.help_menu = QMenu(self.tran.get_text('help_menu_title'), self)
        self.help_action = self.help_menu.addAction(self.tran.get_text('help_menu_action'))
        self.help_action.triggered.connect(self.open_help_page)
        self.menubar.addMenu(self.help_menu)
        self.mainLayout.setMenuBar(self.menubar)

        self.set_style_sheet()

    def set_style_sheet(self):
        if cc_con.THEME in self.config:
            try:
                with open(cc_con.THEME_PREFIX + self.config[cc_con.THEME] + cc_con.THEME_POSTFIX, "r") as theme:
                    self.setStyleSheet(theme.read())
            except EnvironmentError:
                print("ERROR: Theme not found, using default theme")
                with open(cc_con.THEME_PREFIX + self.config[cc_con.THEME_DEFAULT] + cc_con.THEME_POSTFIX, "r") as theme:
                    self.setStyleSheet(theme.read())

    def show_adv_tab(self, onoff):
        """
        Show or hide the advanced settings tab

        :param onoff: True to show the advanced settings tab and false to hide it
        :return: None
        """
        # check if the advanced tab is already in the tablist
        tab_in_tablist = True if self.maintabwidget.indexOf(self.advtab) != -1 else False
        if onoff and not tab_in_tablist:
            self.maintabwidget.addTab(self.advtab, self.tran.get_text('advanced_title'))
        elif tab_in_tablist:
            self.maintabwidget.removeTab(self.maintabwidget.indexOf(self.advtab))

    def browse_config(self):
        """
        Opens a file browser to select the config file and
        sets the QEditLine according to the selection.

        :return: None
        """
        filename, _ = QFileDialog.getOpenFileName(self, self.tran.get_text('adv_tab_button_config_desc'),
                self.advtab_input_config.text(), "XML (*.xml)")
        if filename:
            self.advtab_input_config.setText(str(filename))

    def get_config_path(self):
        if self.advtab_input_config == "":
            return None
        else:
            return self.advtab_input_config.text()

    def get_plain_path(self):
        if self.settab_input_clear == "":
            return None
        else:
            return self.settab_input_clear.text()

    def get_cipher_path(self):
        if self.settab_input_enc == "":
            return None
        else:
            return self.settab_input_enc.text()

    def open_help_page(self):
        self.helper.open_help("index.html", "")

    def write_config(self):
        self.messages.add(str(self.config))
        self.messages.add(self.tran.get_text('writing_config'))
        self._renew_message_area()
        self.configparser.write_config(self.config)

    def _renew_message_area(self):
        self.status_line.setText("")
        for message in self.messages:
            self.status_line.append(message)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def add_message(self, message):
        self.messages.add(message)
        self._renew_message_area()

    def del_message(self, message):
        """
        Remove a message from the message area

        :param message: the message to remove
        :return: True if the message was removed sucessfully and False if the message was not there to begin with
        """
        try:
            self.messages.remove(message)
            self._renew_message_area()
            return True
        except KeyError:
            return False

    def str_to_bool(self, text):
        if text in 'True':
            return True
        else:
            return False

    def _sync(self):
        self.config = self._selected_tab.config()
        self.configparser.write_config(self._selected_tab.config())
        if self.maintabwidget.count() > 0:
            self.maintabwidget.currentWidget().init()
            if self.settab.is_running():
                self.maintabwidget.currentWidget().lock()
            else:
                self.maintabwidget.currentWidget().unlock()
            if self.settab.tooltip_state():
                self.maintabwidget.currentWidget().toggle_tooltips("True")
            else:
                self.maintabwidget.currentWidget().toggle_tooltips("False")
            self._selected_tab = self.maintabwidget.currentWidget()

    def closeEvent(self, event):
        reply = QMessageBox.question(None, '', self.tran.get_text('exit_cloudcrypt'), QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        self.write_config()
        if reply == QMessageBox.Yes:
            self.settab.slider_moved("off")
            event.accept()
        else:
            event.ignore()
