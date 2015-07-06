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

from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtCore import Qt
from cloudcrypt.cc_option_wizard import OptionWizard
from cloudcrypt import cc_con


class AdvSetTab(QWidget):

    def __init__(self, gui):
        super(AdvSetTab, self).__init__()

        self._ui = gui
        self._config = self._ui.config
        self._tran = self._ui.tran
        self._parser = self._ui.configparser
        self.setObjectName("advtab")

        # main layout of this tab
        self._layout = QGridLayout(self)
        self._layout.setObjectName('advtab_layout')

        # setup the new button
        self._button_new = QPushButton(self)
        self._button_new.setObjectName('advtab_button_new')
        self._button_new.setText(self._tran.get_text(self._button_new.objectName()))
        self._button_new.clicked.connect(self._new_setting)

        # setup the delete button
        self._button_del = QPushButton(self)
        self._button_del.setObjectName('advtab_button_delete')
        self._button_del.setText(self._tran.get_text(self._button_del.objectName()))
        self._button_del.clicked.connect(self._delete_setting)

        # setup the delete all
        self._button_del_all = QPushButton(self)
        self._button_del_all.setObjectName('advtab_button_delete_all')
        self._button_del_all.setText(self._tran.get_text(self._button_del_all.objectName()))
        self._button_del_all.clicked.connect(self._delete_config)

        # setup the reset all button
        self._button_res_all = QPushButton(self)
        self._button_res_all.setObjectName('advtab_button_reset_all')
        self._button_res_all.setText(self._tran.get_text(self._button_res_all.objectName()))
        self._button_res_all.clicked.connect(self._reset_config)

        # setup the option table
        self._table = QTableWidget(0, 2)
        self._table.setObjectName('advtab_table')
        self._table.setHorizontalHeaderLabels([self._tran.get_text('option'), self._tran.get_text('value')])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SingleSelection)
        self._table.setShowGrid(False)
        self._table.setGeometry(0, 0, 800, 400)
        self._table.itemChanged.connect(self._changed_setting)

        # add the elements to the top level layout of the tab
        self._layout.addWidget(self._button_new, 0, 0, 1, 1)
        self._layout.addWidget(self._button_del, 0, 1, 1, 1)
        self._layout.addWidget(self._button_del_all, 0, 2, 1, 1)
        self._layout.addWidget(self._button_res_all, 0, 3, 1, 1)
        self._layout.addWidget(self._table, 1, 0, 4, 4)

        # set the array with all elements that have tooltips
        self._tooltips = [
            self._button_new, self._button_del,
            self._button_del_all, self._button_res_all,
        ]

    def _changed_setting(self):
        """
        Update the config with the values from the ui

        :return:
        """
        # run through the table
        for a in range(self._table.rowCount()):
            # get key and value of the current row
            _key = self._table.item(a, 0).text() if self._table.item(a, 0) else ""
            _value = self._table.item(a, 1).text() if self._table.item(a, 1) else ""
            # update the config
            self._config[_key] = _value
        # make the default config visible in the ui, toggle tooltips, ...
        self.init()

    def _new_setting(self):
        """
        Add a new setting to the config

        :return: None
        """
        # get the number of rows in the table
        _rows = self._table.rowCount()
        # create a wizard to get the setting name and setting value from the user
        _wizard = OptionWizard(self._tran.get_text('option_wizard_title'), self._tran)
        # open the wizard
        _wizard.exec_()
        # only if the user has entered a setting name
        if _wizard.setting_name():
            # create a new item holding the entered data
            self._table.insertRow(_rows)
            _key = QTableWidgetItem(_wizard.setting_name())
            # make the new item editable and selectable
            _flags = _key.flags()
            _flags |= Qt.ItemIsSelectable
            _flags &= Qt.ItemIsEditable
            _key.setFlags(_flags)
            # add the new item to the table
            self._table.setItem(_rows, 0, _key)
            self._table.setItem(_rows, 1, QTableWidgetItem(_wizard.setting_value()))
            # add the new setting to the config
            self._config[_wizard.setting_name()] = _wizard.setting_value()
        # make the default config visible in the ui, toggle tooltips, ...
        self.init()

    def _delete_setting(self):
        """
        Remove the selected setting from config

        :return: None
        """
        # get the index of the selected row
        try:
            _row = self._table.selectedItems()[0].row()
        except KeyError:
            return
        # delete the options from config
        del self._config[self._table.selectedItems()[0].text()]
        # remove the row from the table
        self._table.removeRow(_row)
        # make the default config visible in the ui, toggle tooltips, ...
        self.init()

    def _delete_config(self):
        """
        Remove all setting from config

        :return: None
        """
        # clear the config
        self.config = {}
        # make the default config visible in the ui, toggle tooltips, ...
        self.init()

    def _reset_config(self):
        """
        Reset the config to default state

        :return: None
        """
        # reset config to default
        self._config = cc_con.DEFAULT_CONFIG
        # make the default config visible in the ui, toggle tooltips, ...
        self.init()

    def toggle_tooltips(self, onoff):
        """
        If "onoff" is either "True" or "true", then show tooltips for this tab, otherwise dont

        :param onoff: whether to show verbose tooltips
        :return: None
        """
        if onoff == "True" or onoff == "true":
            # run through the list with elements that have tooltips...
            for ele in self._tooltips:
                # and activate the tooltip for each element
                ele.setToolTip(self._tran.get_text(ele.objectName() + '_tooltip'))
        else:
            # run through the list with elements that have tooltips...
            for ele in self._tooltips:
                # and disable the tooltip for each element
                ele.setToolTip("")

    def lock(self):
        """
        Disable the ui components, so that the user cannot change settings while the program is running

        :return: None
        """
        self._toggle_ui_components(False)

    def unlock(self):
        """
        Enable the ui components, so that the user can change settings

        :return: None
        """
        self._toggle_ui_components(True)

    def _toggle_ui_components(self, onoff):
        """
        Enable/Disable ui components (DO NOT USE THIS DIRECTLY; use _lock()/_unlock())

        :param onoff: True to enable, False to disable
        :return: None
        """
        # enable/disable buttons
        self._button_del.setEnabled(onoff)
        self._button_del_all.setEnabled(onoff)
        self._button_new.setEnabled(onoff)
        self._button_res_all.setEnabled(onoff)
        # enable/disable editing of the items in the table
        for a in range(0, self._table.rowCount()):
            if onoff:
                self._table.setEnabled(True)
            else:
                self._table.setEnabled(False)

    def init(self):
        """
        What to do, when this tab is activated: fill the table with the contents of the config, ...

        :return: None
        """
        # prevent sending signals: otherwise this caused the itemChanged Signal of the table to fire which in turn
        # invokes this method, ... -> infinitely deep recursion
        self._table.blockSignals(True)
        # delete all rows from the table
        while self._table.rowCount() > 0:
            self._table.removeRow(0)
        # fill the table with the contents of the config
        _i = 0
        for key, value in self._config.items():
            self._table.insertRow(_i)
            self._table.setItem(_i, 0, QTableWidgetItem(key))
            self._table.setItem(_i, 1, QTableWidgetItem(value))
            _i += 1
        # toggle tooltips if necessary
        if cc_con.SHOW_VERB_TOOL in self._config:
            self.toggle_tooltips(self._config[cc_con.SHOW_VERB_TOOL])
        # if the options for showing tooltips has not been set they are shown per default
        else:
            self.toggle_tooltips("True")
        self._table.blockSignals(False)

    def config(self):
        """
        Return the internal configuration of this tab

        :return: A dictionary containing the configuration
        """
        return self._config
