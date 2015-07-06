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

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

class OptionWizard(QDialog):

    def __init__(self, wizardtype, translator):
        super(OptionWizard, self).__init__()

        self.tran = translator

        self.layout = QGridLayout(self)
        self.title = self.tran.get_text(wizardtype)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('./resources/Logo_v2.png'))

        self.key_label = QLabel(self)
        self.key_label.setObjectName('wizard_key_label')
        self.key_label.setText(self.tran.get_text(self.key_label.objectName()))

        self.keyinput = QLineEdit(self)
        self.keyinput.setObjectName('wizard_key_input')
        self.keyinput.setText(self.tran.get_text(self.keyinput.objectName()))

        self.value_label = QLabel(self)
        self.value_label.setObjectName('wizard_value_label')
        self.value_label.setText(self.tran.get_text(self.value_label.objectName()))

        self.valueinput = QLineEdit(self)
        self.valueinput.setObjectName('wizard_value_input')
        self.valueinput.setText(self.tran.get_text(self.valueinput.objectName()))

        self.confirm = QPushButton(self)
        self.confirm.setObjectName('wizard_button_confirm')
        self.confirm.setText(self.tran.get_text(self.confirm.objectName()))
        self.confirm.clicked.connect(self.close)

        self.layout.addWidget(self.key_label, 0, 0, 1, 3)
        self.layout.addWidget(self.keyinput, 0, 3, 1, 7)
        self.layout.addWidget(self.value_label, 1, 0, 1, 3)
        self.layout.addWidget(self.valueinput, 1, 3, 1, 7)
        self.layout.addWidget(self.confirm, 2, 8, 2, 1)

        self.show()

    def setting_name(self):
        if self.keyinput:
            return self.keyinput.text()
        else:
            return None

    def setting_value(self):
        if self.valueinput:
            return self.valueinput.text()
        else:
            return ""
