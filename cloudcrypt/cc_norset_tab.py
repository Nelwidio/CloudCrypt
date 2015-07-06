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
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
from cloudcrypt.cc_sync_thread import SyncThread
from cloudcrypt import cc_con
import base64
import os


class NorSetTab(QWidget):

    def __init__(self, gui):
        super(NorSetTab, self).__init__()

        self._ui = gui
        self._tran = self._ui.tran
        self._config = self._ui.config
        self._parser = self._ui.configparser
        self._thread = None
        self._running = False
        self.setObjectName("settab")

        self._layout = QGridLayout(self)
        self._layout.setObjectName('settab_layout')

        # label for the plaintext directory
        self._label_clear = QLabel(self)
        self._label_clear.setObjectName('settab_label_clear')
        self._label_clear.setText(self._tran.get_text(self._label_clear.objectName()))

        # plaintext input
        self._input_clear = QLineEdit(self)
        self._input_clear.setObjectName('settab_input_clear')
        self._input_clear.setText('')
        self._input_clear.setReadOnly(True)
        self._input_clear.textChanged.connect(lambda: self._config.update({cc_con.SCR_DIR: self._input_clear.text()}))

        # plaintext button
        self._button_clear = QPushButton(self)
        self._button_clear.setObjectName('settab_button_clear')
        self._button_clear.setText(self._tran.get_text(self._button_clear.objectName()))
        self._button_clear.clicked.connect(self._browse_clear_dir)

        # label for the enc directory
        self._label_enc = QLabel(self)
        self._label_enc.setObjectName('settab_label_enc')
        self._label_enc.setText(self._tran.get_text(self._label_enc.objectName()))

        # enc input
        self._input_enc = QLineEdit(self)
        self._input_enc.setObjectName('settab_input_enc')
        self._input_enc.setReadOnly(True)
        self._input_enc.textChanged.connect(lambda: self._config.update({cc_con.DST_DIR: self._input_enc.text()}))

        # enc button
        self._button_enc = QPushButton(self)
        self._button_enc.setObjectName('settab_button_enc')
        self._button_enc.setText(self._tran.get_text(self._button_enc.objectName()))
        self._button_enc.clicked.connect(self._browse_enc_dir)

        # label for the key
        self._label_key1 = QLabel(self)
        self._label_key1.setObjectName("settab_label_key1")
        self._label_key1.setText(self._tran.get_text(self._label_key1.objectName()))

        # set up the input field for the password
        self._input_key1 = QLineEdit(self)
        self._input_key1.setObjectName("settab_tab_input_key1")
        self._input_key1.setEchoMode(QLineEdit.Password)
        self._input_key1.textChanged.connect(self._verify_passwords)

        # set up the show password button for key1
        self._button_key1 = QPushButton(self)
        self._button_key1.setObjectName('settab_button_key1')
        self._button_key1.setText(self._tran.get_text(self._button_key1.objectName()))
        self._button_key1.pressed.connect(lambda: self._toggle_password(self._input_key1))
        self._button_key1.released.connect(lambda: self._toggle_password(self._input_key1))

        # set up the label for the key confirmation field
        self._label_key2 = QLabel(self)
        self._label_key2.setObjectName("settab_label_key2")
        self._label_key2.setText(self._tran.get_text(self._label_key2.objectName()))

        # set up the input field for the password confirmation
        self._input_key2 = QLineEdit(self)
        self._input_key2.setObjectName("settab_tab_input_key2")
        self._input_key2.setEchoMode(QLineEdit.Password)
        self._input_key2.textChanged.connect(self._verify_passwords)

        # setup the show password button for the password comfirmation
        self._button_key2 = QPushButton(self)
        self._button_key2.setObjectName('settab_button_key2')
        self._button_key2.setText(self._tran.get_text(self._button_key2.objectName()))
        self._button_key2.pressed.connect(lambda: self._toggle_password(self._input_key2))
        self._button_key2.released.connect(lambda: self._toggle_password(self._input_key2))

        # widget that is holding the slider
        self._widget_slider = QWidget(self)
        self._widget_slider.setObjectName('settab_widget_slider')

        # layout of the widget that is holding the slider
        self._widget_slider_layout = QGridLayout(self._widget_slider)
        self._widget_slider_layout.setObjectName('settab_widget_slider_layout')
        self._widget_slider.setLayout(self._widget_slider_layout)

        # left label of the slider
        self._label_left_slider = QLabel(self._widget_slider)
        self._label_left_slider.setObjectName('settab_label_left_slider')
        self._label_left_slider.setText(self._tran.get_text(self._label_left_slider.objectName()))
        self._label_left_slider.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # right label of the slider
        self._label_right_slider = QLabel(self._widget_slider)
        self._label_right_slider.setObjectName('settab_label_right_slider')
        self._label_right_slider.setText(self._tran.get_text(self._label_right_slider.objectName()))

        # setup the slider itself
        self._slider = QSlider(self._widget_slider)
        self._slider.setObjectName('settab_slider_slider')
        self._slider.setOrientation(Qt.Horizontal)
        self._slider.setMaximumWidth(50)
        self._slider.setMinimum(0)
        self._slider.setMaximum(1)
        self._slider.valueChanged.connect(self.slider_moved)

        # add widgets to the slider sub layout
        self._widget_slider_layout.addWidget(self._label_left_slider, 0, 0, 1, 1)
        self._widget_slider_layout.addWidget(self._label_right_slider, 0, 2, 1, 1)
        self._widget_slider_layout.addWidget(self._slider, 0, 1, 1, 1)

        # button to write the config button
        self._button_write_config = QPushButton(self)
        self._button_write_config.setObjectName('settab_button_write_config')
        self._button_write_config.setText(self._tran.get_text(self._button_write_config.objectName()))
        self._button_write_config.clicked.connect(self._ui.write_config)

        # the horizontal line in the settings tab
        self._hline = QFrame(self)
        self._hline.setFrameShape(QFrame.HLine)
        self._hline.setFrameShadow(QFrame.Sunken)
        self._hline.setObjectName('settab_hline')

        # the show advanced settings tab checkbox
        self._checkbox_advset = QCheckBox(self)
        self._checkbox_advset.setObjectName('settab_checkbox_advanced_settings')
        self._checkbox_advset.setText(self._tran.get_text(self._checkbox_advset.objectName()))
        self._checkbox_advset.stateChanged.connect(self._toggle_advset_tab)

        # the display verbose tooltips checkbox
        self._checkbox_vertoo = QCheckBox(self)
        self._checkbox_vertoo.setObjectName('settab_checkbox_verbose_tooltips')
        self._checkbox_vertoo.setText(self._tran.get_text(self._checkbox_vertoo.objectName()))
        self._checkbox_vertoo.stateChanged.connect(lambda: self.toggle_tooltips(None))

        # add the elements to the main layout
        self._layout.addWidget(self._label_clear, 0, 0, 1, 1)
        self._layout.addWidget(self._input_clear, 0, 1, 1, 1)
        self._layout.addWidget(self._button_clear, 0, 2, 1, 1)
        self._layout.addWidget(self._label_enc, 1, 0, 1, 1)
        self._layout.addWidget(self._input_enc, 1, 1, 1, 1)
        self._layout.addWidget(self._button_enc, 1, 2, 1, 1)
        self._layout.addWidget(self._label_key1, 2, 0, 1, 1)
        self._layout.addWidget(self._input_key1, 2, 1, 1, 1)
        self._layout.addWidget(self._button_key1, 2, 2, 1, 1)
        self._layout.addWidget(self._label_key2, 3, 0, 1, 1)
        self._layout.addWidget(self._input_key2, 3, 1, 1, 1)
        self._layout.addWidget(self._button_key2, 3, 2, 1, 1)
        self._layout.addWidget(self._hline, 4, 0, 1, 3)
        self._layout.addWidget(self._checkbox_advset, 5, 0, 1, 1)
        self._layout.addWidget(self._checkbox_vertoo, 5, 2, 1, 1)
        self._layout.addWidget(self._widget_slider, 6, 2, 1, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        self._layout.addWidget(self._button_write_config, 6, 0, 1, 1)

        self._tooltips = [
            self._label_clear, self._input_clear, self._button_clear,
            self._label_enc, self._input_enc, self._button_enc,
            self._label_key1,
            self._input_key1, self._button_key1,
            self._label_key2, self._input_key2, self._button_key2,
            self._checkbox_advset, self._checkbox_vertoo
        ]

    def _browse_clear_dir(self):
        """
        Open a directory browser to select the directory for the plaintexts and
        set the text of the corresponding QLineEdit

        :return: None
        """
        # the file browser will only allow choosing directories
        _opt = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        # open the file browser
        _dir = QFileDialog.getExistingDirectory(None, self._tran.get_text('settab_button_clear_desc'), self._input_clear.text(), _opt)
        if _dir:
            self._input_clear.setText(str(_dir))

    def _browse_enc_dir(self):
        """
        Open a directory browser to select the directory for the ciphertexts
        and set the text of the corresponding QLineEdit

        :return: None
        """
        # the file browser will only allow choosing directories
        _opt = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        # open the file browser
        _dir = QFileDialog.getExistingDirectory(None, self._tran.get_text('settab_button_enc_desc'), self._input_enc.text(), _opt)
        if _dir:
            self._input_enc.setText(str(_dir))

    def _verify_passwords(self):
        """
        Check if the passwords the user entered are equal and satisfy the security requirements for passwords.

        :return: True if the passwords are valid; False if they are not
        """
        if self._check_password_equality() and self._check_security_policy():
            # the passwords are valid, so we can insert it into the config
            self._config[cc_con.USER_PW] = self._input_key1.text()
            return True
        else:
            return False

    def _check_security_policy(self):
        """
        Check if the passwords the user entered meet the CloudCrypt security requirements for passwords

        :return: True if the password is sufficient and False if it isn't
        """
        _length1 = len(str(self._input_key1.text()))
        _length2 = len(str(self._input_key2.text()))
        _ret = True
        # check if the first password is long enough
        if not (cc_con.PASSWORD_MIN_LEN <= _length1 <= cc_con.PASSWORD_MAX_LEN):
            # password is not long enough, so mark it as invalid
            self._mark_invalid(self._input_key1)
            self._mark_invalid(self._input_key2)
            # output error message
            self._ui.add_message(self._tran.get_text('password_1_policy_violation'))
            _ret = False
        else:
            # password is long enough, so remove messages claiming otherwise
            self._ui.del_message(self._tran.get_text('password_1_policy_violation'))
        # check if the second passsword is long enough
        if not (cc_con.PASSWORD_MIN_LEN <= _length2 <= cc_con.PASSWORD_MAX_LEN):
            # password not long enough, so mark it as invalid
            self._mark_invalid(self._input_key1)
            self._mark_invalid(self._input_key2)
            # output error message
            self._ui.add_message(self._tran.get_text('password_2_policy_violation'))
            _ret = False
        else:
            # password is long enough, so remove messages claiming otherwise
            self._ui.del_message(self._tran.get_text('password_2_policy_violation'))
        # both passwords are sufficient
        return _ret

    def _check_password_equality(self):
        """
        Check if the two passwords the user provided are equal and mark the input fields accordingly


        :return: True if the passwords are equal and False if they are not
        """
        _ret = True
        # check if they are equal
        if self._input_key1.text() != self._input_key2.text():
            # passwords not equal -> mark input fields and output message
            self._mark_invalid(self._input_key1)
            self._mark_invalid(self._input_key2)
            # output error message
            self._ui.add_message(self._tran.get_text('passwords_not_equal'))
            _ret = False
        else:
            # passwords equal -> mark input fields and remove passwords not equal message
            self._mark_valid(self._input_key1)
            self._mark_valid(self._input_key2)
            # output error message
            self._ui.del_message(self._tran.get_text('passwords_not_equal'))
            _ret = True
        if _ret and self._input_key1.text() == base64.b64decode(b'Sm9zaHVh').decode('utf-8'):
            self._ui.helper.open_help('test.html', '')
        # passwords are equal
        return _ret

    @staticmethod
    def _mark_invalid(field):
        """
        Mark a invalid input field

        :param field: the field that shall be marked as invalid
        :return: None
        """
        try:
            field.setStyleSheet("QLineEdit{background: red;}")
        except AttributeError:
            pass  # TODO error handling

    @staticmethod
    def _mark_valid(field):
        """
        Mark a valid input field

        :param field: the field that shall be marked as valid
        :return: None
        """
        try:
            field.setStyleSheet("QLineEdit{background: green;}")
        except AttributeError:
            pass  # TODO error handling

    def _toggle_advset_tab(self):
        """
        Show or hide the advanced settings tab

        :return: None
        """
        if not self._checkbox_advset.isChecked():
            self._ui.show_adv_tab(False)
            self._config[cc_con.SHOW_ADV_SET] = "False"
        else:
            self._ui.show_adv_tab(True)
            self._config[cc_con.SHOW_ADV_SET] = "True"

    def is_running(self):
        """
        Whether the synchronisation between the two directories is currently running

        :return: True, if the synchronisation is running and False if it is not
        """
        return self._running

    def tooltip_state(self):
        """
        Whether the tooltips are turned on or off; True indicates on and False indicates off

        :return: True if the tooltips are on and False if they are off
        """
        if cc_con.SHOW_VERB_TOOL in self._config:
            return self._str_to_bool(self._config[cc_con.SHOW_VERB_TOOL])
        else:
            return True

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
        self._button_clear.setEnabled(onoff)
        self._button_enc.setEnabled(onoff)
        self._button_key1.setEnabled(onoff)
        self._button_key2.setEnabled(onoff)
        self._checkbox_advset.setEnabled(onoff)
        self._checkbox_vertoo.setEnabled(onoff)
        self._button_write_config.setEnabled(onoff)

    def slider_moved(self, val=None):
        """
        What to do, when the slider has been moved: check input fields and if the input is valid start the synchronisation
        between the two directories

        :param val:
        :return:
        """
        # user specified an new value for the slider
        if val and val == "off" or val == "Off":
            _value = 0
        elif val and val == "On" or val == "on":
            _value = 1
        # user did not specify a new value for the slider
        else:
            _value = self._slider.value()
        # stop synchronisation between the two directories
        if _value == 0:
            self._ui.core_ref.stop_sync()
            # unset the flag indicating that the synchronisation is running
            self._running = False
            # allow the user to modify settings again, now that the synchronisation has stopped
            self.unlock()
        # check if all the input needed to start the synchronisation is valid
        elif _value == 1:
            if self._input_clear is None or self._input_enc is None:
                self.ui.add_message("Geben sie für beide Ordner eine Pfad an")
                self._slider.setValue("Off")
                return
            if not self._verify_passwords():
                self._slider.setValue("Off")
                return
            # check if the passwords satisfy the security policy for passwords
            if not self._check_security_policy():
                self._settab_slider_slider.setValue("Off")
                return
            # check if the password is correct
            _user_pass = str(self._input_key1.text())
            if not self._ui.core_ref.is_password_correct(_user_pass):
                # password wrong
                self._ui.add_message(self._tran.get_text('password_not_correct'))
                self._slider.setValue("Off")
                return
            # password correct -> delete messages claiming otherwise from the message area
            elif self._tran.get_text('password_not_correct') in self._ui.messages:
                self._ui.del_messages(self._tran.get_text('password_not_correct'))
            # check if the directory paths are good
            _source = str(self._input_clear.text())
            _cloud = str(self._input_enc.text())
            if not os.path.exists(_source):
                # source directory path not good -> add message to message area
                self._ui.add_message(self._tran.get_text('source_folder_not_exist'))
                self._slider.setValue("Off")
                return
            # source path correct -> delete message claiming otherwise from the message area
            elif self._tran.get_text('source_folder_not_exist') in self._ui.messages:
                    self._ui.del_messages(self._tran.get_text('source_folder_not_exist'))
            if not os.path.exists(_cloud):
                # cloud directory path not good -> add message to message area
                self._ui.add_message(self._tran.get_text('cloud_folder_not_exist'))
                self._ui.slider.setValue("Off")
                return
            # cloud path correct -> delete message claiming otherwise from the message area
            elif self._tran.get_text('cloud_folder_not_exist') in self._ui.messages:
                    self._ui.del_messages(self._tran.get_text('cloud_folder_not_exist'))

            # all checks where successful -> start synchronisation
            self._thread = SyncThread(self._ui.core_ref, _source, _cloud, _user_pass)
            self._thread.start()
            # lock the ui, so that the user cannot change settings while the synchronisation is running
            self.lock()
            # set the flag indicating that the synchronisation is running
            self._running = True

    @staticmethod
    def _toggle_password(field):
        """
        Display passwords in a QLineEdit in clear text and display clear text in a QLineEdit as password

        :param field: The field for which the echo mode shall be switched
        :return: None
        """
        try:
            if field.echoMode() == QLineEdit.Password:
                field.setEchoMode(QLineEdit.Normal)
            else:
                field.setEchoMode(QLineEdit.Password)
        except AttributeError:  # TODO error handling
            pass

    @staticmethod
    def _str_to_bool(string):
        """
        Convert a string to boolean: "True" and "true" become True, everything else becomes False

        :param string: The string that shall be converted
        :return: True if the string was "True" or "true" and False if the string is something else
        """
        if string == "True" or string == "true":
            return True
        else:
            return False

    def toggle_tooltips(self, onoff=""):
        """
        Turn tool tips for this tab on or off

        :param onoff: "True" or "true" to turn tooltips on, False (actually everything but "True" and "true") to turn tooltips off
            if onoff is not set, then this method just toggles the tooltips
        :return: None
        """
        # update config
        self._config[cc_con.SHOW_VERB_TOOL] = str(self._checkbox_vertoo.isChecked())
        if onoff:
            # user specified whether he wants to turn tooltips on or off
            if onoff == "True" or onoff == "true":
                # turn on
                for ele in self._tooltips:
                    ele.setToolTip(self._tran.get_text(ele.objectName() + cc_con.TOOLTIP_POSTFIX))
            else:
                # turn off
                for ele in self._tooltips:
                    ele.setToolTip("")
        else:
            # user did not specify whether he wants to turn tooltips on or off
            if cc_con.SHOW_VERB_TOOL in self._config and self._config[cc_con.SHOW_VERB_TOOL] == "True":
                self.toggle_tooltips("True")
            elif cc_con.SHOW_VERB_TOOL in self._config:
                self.toggle_tooltips("False")

    def init(self):
        """
        What to do, when this tab is activated: fill the table with the contents of the config, ...

        :return: None
        """
        # plaintext directory input field
        if cc_con.SCR_DIR in self._config:
            self._input_clear.setText(self._config[cc_con.SCR_DIR])
        else:
            self._input_clear.setText(cc_con.SCR_DIR_DEFAULT)

        # encrypted directory input field
        if cc_con.DST_DIR in self._config:
            self._input_enc.setText(self._config[cc_con.DST_DIR])
        else:
            self._input_enc.setText(cc_con.DST_DIR_DEFAULT)

        # the two password input fields
        if cc_con.USER_PW in self._config:
            self._input_key1.setText(self._config[cc_con.USER_PW])
            self._input_key2.setText(self._config[cc_con.USER_PW])
        else:
            self._input_key1.setText(cc_con.USER_PW_DEFAULT)
            self._input_key2.setText(cc_con.USER_PW_DEFAULT)

        # show advanced tab checkbox
        if cc_con.SHOW_ADV_SET in self._config:
            self._checkbox_advset.setChecked(self._str_to_bool(self._config[cc_con.SHOW_ADV_SET]))
        else:
            self._checkbox_advset.setChecked(self._str_to_bool(cc_con.SHOW_ADV_SET_DEFAULT))

        # show verbose tooltips checkbox
        if cc_con.SHOW_VERB_TOOL in self._config:
            self._checkbox_vertoo.setChecked(self._str_to_bool(self._config[cc_con.SHOW_VERB_TOOL]))
        else:
            self._checkbox_vertoo.setChecked(self._str_to_bool(cc_con.SHOW_VERB_TOOL_DEFAULT))

    def config(self):
        """
        Return the internal configuration of this tab

        :return: A dictionary containing the configuration
        """
        return self._config


