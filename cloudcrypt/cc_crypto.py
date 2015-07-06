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
This module provides functions to symmetrically encrypt and decrypt files
with a user's passphrase
"""

import gnupg
import os
import random
import string

def touch(file_name):
    """
    creates a file if it does not exist

    :param file_name: the file to create
    :return:
    """
    if not os.path.exists(str(file_name)):
        with open(str(file_name), 'a'):
            os.utime(str(file_name), None)

def is_pgp_file(file_name):
    """
    checks if a file is a ascii armored pgp file according to the header

    :param file_name: the file to check
    :return:
    """
    if not os.path.exists(str(file_name)):
        return False
    else:
        expected = "-----BEGIN PGP MESSAGE-----"
        with open(str(file_name), "r") as fh:
            content = fh.read(27)
            if content == expected:
                return True
            else:
                return False

class Crypto(object):

    def __init__(self):
        """
        Initialize GnuPG. Encoding is 'latin-1' (leaves bytes as-is and should
        not result in exceptions, which may happen with utf-8).

        :return: None
        """
        self.gpg = gnupg.GPG()
        self.gpg.encoding = 'utf-8'

    def encrypt_file_symmetric(self, input_file, output_file, passp):
        """
        This function encrypts a file symmetrically with AES256-algorithm.
        It takes an input file, encrypts it and writes it to an output file.
        If the input file does not exist, this functions raises a
        FileExistsError. If the input is not readable or the output is not
        writable, it will raise a PermissionError. If the encryption fails
        because of other (unknown) reasons, it will raise a RuntimeError.

        :param input_file: the file to encrypt
        :param output_file: the file to write the encrypted output to
        :param passhrase: the passphrase to encrypt the file with
        :return:
        """
        if os.path.isfile(str(input_file)):
            if os.access(str(input_file), os.R_OK):
                touch(str(output_file))
                with open(str(input_file), "rb") as fh:
                    data = fh.read()
                encrypted = self.gpg.encrypt(data=data, recipients=None,
                                             symmetric='AES256',
                                             passphrase=passp)
                with open(str(output_file), 'w') as fh:
                    fh.write(str(encrypted))
            else:
                raise PermissionError("File to encrypt is not readable")
        else:
            raise FileExistsError("File for encryption does not exist")

    def decrypt_file_symmetric(self, input_file, output_file, passp):
        """
        This function decrypts a file symmetrically. It will automatically use
        the appropriate algorithm. The function reads the contents of
        <input_file>, decrypts it and writes the decrypted content to the output
        file.
        If the input file does not exist, the function raises an
        FileExistsError. If the input is not readable or the output is not
        writable, it will raise a PermissionError. If an error occurs during
        the decryption (most probably a false passphrase) it will raise a
        RuntimeError.

        :param input_file: the file to decrypt
        :param output_file: the file to write the decrypted data to
        :param passphrase: the passphrase for decryption
        :return:
        """
        if not is_pgp_file((str(input_file))):
            return
        if os.path.isfile(str(input_file)):
            if os.access(str(input_file), os.R_OK):
                touch(str(output_file))
                with open(str(input_file), "rb") as fh:
                    content = fh.read()
                decrypted = self.gpg.decrypt(content, passphrase=passp)
                with open(str(output_file), "w") as fh:
                    fh.write(str(decrypted))
            else:
                raise PermissionError("File to decrypt is not readable")
        else:
            raise FileExistsError("File for decryption does not exist")

    def generate_new_password(self, length, filename, user_passp):
        """
        Generates a new pseudo random password (with lowercase and uppercase
        letters, digits and punctuation symbols) with a length of <length>.
        The result will be encrypted with <user_passp> and stored in <filename>.
        If the file does already exist, the function returns. Otherwise it will
        create the file and write the content.

        :param length: length of the password to generate
        :param filename: the filename to store the encrypted password in
        :param user_passp: the user's password to encrypt the random password
            with
        :return: None
        """
        if os.path.exists(str(filename)):
            return
        passwd = ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                                                      string.ascii_lowercase +
                                                      string.digits +
                                                      string.punctuation)
                         for _ in range(length))
        touch(str(filename))
        encrypt = self.gpg.encrypt(data=passwd, recipients=None,
                                   symmetric='AES256',
                                   passphrase=str(user_passp))
        with open(str(filename), 'w') as fp:
            fp.write(str(encrypt))

    def get_passwd(self, filename, user_passp):
        """
        Reads the random password from <filename>. If the file does not exist,
        the function returns None. If the file exists, the function reads its
        content, checks if it is a gpg file, decrypt it with <user_passp> and
        return it. If anything fails (not a gpg file or wrong user password)
        the function returns None.

        :param filename: name of the file to read
        :param user_passp: passphrase to decrypt the file with
        :return: None it something fails, the random password out of the file
        as a string if successfull.
        """
        if not is_pgp_file(str(filename)):
            return None
        if os.path.isfile(str(filename)):
            with open(str(filename), "r") as fp:
                content = fp.read()
            decrypted = self.gpg.decrypt(content, passphrase=str(user_passp))
            if str(decrypted) != str(""):
                return str(decrypted)
            else:
                return None
