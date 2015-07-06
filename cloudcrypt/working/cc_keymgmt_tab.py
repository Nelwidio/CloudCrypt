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

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtCore import QRect


class KeyMgmt(QWidget):

    def __init__(self, gui):
        super(KeyMgmt, self).__init__()

        self.ui = gui
        self.tran = self.ui.tran
        self.parser = self.ui.configparser
        self.config = self.ui.config
        self.setObjectName("keytab")

        self.layout = QGridLayout(self)
        self.layout.setObjectName('keytab_layout')

        # the new button
        self.button_new = QPushButton(self)
        self.button_new.setObjectName('key_tab_button_new')
        self.button_new.setText(self.tran.get_text(self.button_new.objectName()))

        # edit button
        self.button_edit = QPushButton(self)
        self.button_edit.setObjectName('key_tab_button_edit')
        self.button_edit.setText(self.tran.get_text(self.button_edit.objectName()))

        # setup the delete button
        self.button_delete = QPushButton(self)
        self.button_delete.setObjectName('key_tab_button_delete')
        self.button_delete.setText(self.tran.get_text(self.button_delete.objectName()))

        # import button
        self.button_import = QPushButton(self)
        self.button_import.setObjectName('key_tab_button_import')
        self.button_import.setText(self.tran.get_text(self.button_import.objectName()))

        # export button
        self.button_export = QPushButton(self)
        self.button_export.setObjectName('key_tab_button_export')
        self.button_export.setText(self.tran.get_text(self.button_export.objectName()))

        # drop down menu
        self.combobox = QComboBox(self)
        self.combobox.setObjectName('key_tab_combobox')

        # scroll area
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName('key_tab_scroll')

        # widget that holds the scroll area contents
        self.scroll_content = QWidget()
        self.scroll_content.setGeometry(QRect(0, 0, 800, 400))
        self.scroll_content.setObjectName('key_tab_scroll_content')

        # layout for the scroll area main widget
        self.scroll_content_layout = QGridLayout(self.scroll_content)
        self.scroll_content_layout.setObjectName('key_tab_scroll_content_layout')

        # setup the tree widget
        self.tree = QTreeWidget(self.scroll_content)
        self.tree.setObjectName('key_tab_tree')

        # add the tree widget to the layout of the scroll area
        self.scroll_content_layout.addWidget(self.tree)     # TODO change to grid layout

        # add the contents of the scroll area to the scroll area
        self.scroll.setWidget(self.scroll_content)

        # add the components to the main layout
        self.layout.addWidget(self.button_new, 0, 0, 1, 1)
        self.layout.addWidget(self.button_edit, 0, 1, 1, 1)
        self.layout.addWidget(self.button_delete, 0, 2, 1, 1)
        self.layout.addWidget(self.button_import, 0, 3, 1, 1)
        self.layout.addWidget(self.button_export, 0, 4, 1, 1)
        self.layout.addWidget(self.combobox, 0, 5, 1, 1)
        self.layout.addWidget(self.scroll, 1, 0, 1, 6)

        # add relevant widgets to tooltip list
        self.tooltips = [
            self.button_delete, self.button_edit, self.button_import,
            self.button_new, self.button_export, self.combobox
            ]
