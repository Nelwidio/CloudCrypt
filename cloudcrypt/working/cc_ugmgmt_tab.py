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
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect


class UgMgmt(QWidget):
    
    def __init__(self, gui):
        super(UgMgmt, self).__init__()
        
        self.ui = gui
        self.tran = self.ui.tran
        self.parser = self.ui.configparser
        self.config = self.ui.config
        self.setObjectName("ugmtab")
        
        self.layout = QGridLayout(self)
        self.layout.setObjectName('ugmtab_layout')

        # new button
        self.button_new = QPushButton(self)
        self.button_new.setObjectName('ugmtab_button_new')
        self.button_new.setText(self.tran.get_text(self.button_new.objectName()))

        # delete button
        self.button_delete = QPushButton(self)
        self.button_delete.setObjectName('ugmtab_button_delete')
        self.button_delete.setText(self.tran.get_text(self.button_delete.objectName()))

        # edit button
        self.button_edit = QPushButton(self)
        self.button_edit.setObjectName('ugmtab_button_edit')
        self.button_edit.setText(self.tran.get_text(self.button_edit.objectName()))

        # arrow left to right
        self.button_ltrarrow = QPushButton(self)
        self.button_ltrarrow.setObjectName('ugmtab_button_arrow_ltr')
        self.button_ltrarrow.setIcon(QIcon('./resources/arrow_ltr.png'))

        # arrow right to left
        self.button_rtlarrow = QPushButton(self)
        self.button_rtlarrow.setObjectName('ugmtab_button_arrow_rtl')
        self.button_rtlarrow.setIcon(QIcon('./resources/arrow_rtl.png'))

        # setup the combo box
        self.combobox = QComboBox(self)
        self.combobox.setObjectName('ugmtab_combobox')

        # setup the left label
        self.label_left = QLabel(self)
        self.label_left.setObjectName('ugmtab_label_left')

        # setup the middle label
        self.label_middle = QLabel(self)
        self.label_middle.setObjectName('ugmtab_label_middle')

        # setup the right label
        self.label_right = QLabel(self)
        self.label_right.setObjectName('ugmtab_label_right')

        # setup the left scoll area
        self.scroll_left = QScrollArea(self)
        self.scroll_left.setWidgetResizable(True)
        self.scroll_left.setObjectName('ugmtab_scroll_left')

        # setup the widget that holds the contents of the left scroll area
        self.scroll_left_content = QWidget()
        self.scroll_left_content.setGeometry(QRect(0, 0, 150, 80))
        self.scroll_left_content.setObjectName('ugmtab_scroll_left_content')
        self.scroll_left.setWidget(self.scroll_left_content)

        # setup the middle scroll area
        self.scroll_middle = QScrollArea(self)
        self.scroll_middle.setWidgetResizable(True)
        self.scroll_middle.setObjectName('ugmtab_scroll_middle')

        # setup the widget that holds the contents of the middle scroll area
        self.scroll_middle_content = QWidget()
        self.scroll_middle_content.setGeometry(QRect(0, 0, 150, 80))
        self.scroll_middle_content.setObjectName('ugmtab_scroll_middle_content')
        self.scroll_middle.setWidget(self.scroll_middle_content)

        # setup the right scroll area
        self.scroll_right = QScrollArea(self)
        self.scroll_right.setWidgetResizable(True)
        self.scroll_right.setObjectName('ugmtab_scroll_right')

        # setup the widget that holds the contents of the middle scroll area
        self.scroll_right_content = QWidget()
        self.scroll_right_content.setGeometry(QRect(0, 0, 150, 80))
        self.scroll_right_content.setObjectName('ugmtab_scroll_right_content')
        self.scroll_right.setWidget(self.scroll_right_content)

        # add the components to the top level layout of the tab
        self.layout.addWidget(self.button_new, 0, 0, 1, 1)
        self.layout.addWidget(self.button_delete, 0, 1, 1, 1)
        self.layout.addWidget(self.button_edit, 0, 2, 1, 1)
        self.layout.addWidget(self.combobox, 0, 6, 1, 2)
        self.layout.addWidget(self.label_left, 1, 0, 1, 2)
        self.layout.addWidget(self.label_middle, 1, 3, 1, 2)
        self.layout.addWidget(self.label_right, 1, 5, 1, 2)
        self.layout.addWidget(self.scroll_left, 2, 0, 4, 2)
        self.layout.addWidget(self.scroll_middle, 2, 3, 4, 2)
        self.layout.addWidget(self.scroll_right, 2, 6, 4, 2)
        self.layout.addWidget(self.button_ltrarrow, 3, 5, 1, 1)
        self.layout.addWidget(self.button_rtlarrow, 4, 5, 1, 1)
