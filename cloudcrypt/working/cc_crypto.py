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
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

Diese Datei ist Teil von CloudCrypt.

CloudCrypt ist Freie Software: Sie können es unter den Bedingungen
der GNU Lesser General Public License, wie von der Free Software Foundation,
Version 3 der Lizenz oder (nach Ihrer Wahl) jeder späteren
veröffentlichten Version, weiterverbreiten und/oder modifizieren.

Fubar wird in der Hoffnung, dass es nützlich sein wird, aber
OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
Siehe die GNU Lesser General Public License für weitere Details.

Sie sollten eine Kopie der GNU Lesser General Public License zusammen mit diesem
Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.
"""

__author__ = ''

import os
import gnupg


class Crypto:
    def __init__(self, key_path_folder, pass_phrase, user_db, own_keyring=True):
        """
        Create a new Crypto object

        :param key_path_folder: path the folder holding the gpg keyring
        :param pass_phrase: secret pgp passphrase for the gpg keyring
        :param own_keyring: True to use an existing gpg keyring from the user;
                False to create a new GPG keyring
        :return: a new Crypto object
        """

        # TODO für die Zukunft bevor du überall einen Kommentar hinschreibst bei Methoden/Variablen die du
        # nicht verstehst
        # lies dir zuerst die !!gesammte!! Datei durch. es ist sinnlos dir newPrivatKey zu erklären wenn du nicht
        # mal weißt wo ich sie einsetze was die Mehtode macht usw.

        # init variables
        self.newPrivateKey = False  # TODO was ist das? -> code lesen -> gibt es einen neuen Private Key
        self.privateKey = None  # TODO was ist das? -> code gesmmt lesen -> fingerprint prv key
        self.passPhrase = pass_phrase
        self.newShare = False  # TODO was ist das warum new share und old share? -> gibt es einen neuen Share
        self.oldShare = {}  # TODO was ist das? -> die alte share liste
        self.share = {}  # TODO was ist das? -> die aktuelle share liste
        self.user_db = user_db

        # init of keyring
        # TODO was ist das? willst du die keyring datei erzeugen
        # evtl ist eine Variable die mir den Pfad zum Folder speichert nützlich, ob unbedingt self
        # haette nicht sein muessen.
        self.key_path_folder = os.path.normpath(str(key_path_folder))

        if own_keyring:
            self.gpg = gnupg.GPG(gnupghome=self.key_path_folder)
        else:
            # TODO: was ist das? warum ist das keine instanzvariable?
            # das ist meiner Ordner für den Keyring, warum weil nicht nötig
            name_folder = os.path.join(self.key_path_folder, "KeyFolderCloudCrypt")
            self.gpg = gnupg.GPG(gnupghome=name_folder)
            # TODO: warum zählst du die keys?
            # wie viele es sind interresiert micht nicht, ich brauch was eindeutiges zum identifizieren der
            # einzelnen dic einteräge
            key_count = 0
            # TODO: warum verwendest du ein directory hierfür? was sind die schlüssel (des directories)
            #  und was sind die werte
            # das bezieht sich auf meinen Kommentar weiter oben
            keys = {}

            # counts keys and saves them in dictionary to import them later into the keyring
            for dirName, dirNames, fileNames in os.walk(self.key_path_folder):
                for filename in fileNames:
                    print(os.path.join(dirName, filename))
                    keys[key_count] = os.path.join(dirName, filename)
                    key_count += 1
            # TODO: warum printest du? soll da eine message in die UI?
            # yeph denn das sind die Keys die ich importiert habe.
            print(keys)

            run = 0

            # imports keys
            # TODO: ich nehme an, du willst die schlüssel aus einem bereis existierenden schlüsselbund
            # einlesen? ist das richtig?
            # nein, ich mag die schlüssel wie der Kommentar sagt importieren, ich habe bis jetzt nur den keyring
            #  ganz oben
            # erstellt und muss jetzt die Keys reinbekommen
            while run != key_count:
                key_data = open(keys[run]).read()
                self.gpg.import_keys(key_data)
                run += 1
        # TODO: wofür brauchst du die variable? willst du die fingerprints fürs verschlüsseln? Warum sind die variablen
        # keine instanzvariablen
        # ich muss wissen welche priv keys es gibt
        private_key = self.gpg.list_keys(secret=True)
        # TODO: wofür brauchst du die variable
        # wenn es keinen private key gibt
        no_private_key = False
        # TODO: ist das die behandlung ob du einen privaten schlüssel zum entschlüsseln hast? Und warum ist das
        # True, wenn du keinen privaten schlüssel hast?
        # ja das ist sie da es noch keine exception gibt bzw auch sinnlos wäre nur weil es keinen priv key gibt
        # das programm abstürzen zu lassen.
        # warum Ture, naja wenn man den Variablen namen übersetzt dann bedeutete das so viel wie "kein privater
        # Schlüssel" und wenn das zutrifft dann ist das True = wahr
        if len(private_key) > 0:
            self.privateKey = private_key[0]
        else:
            no_private_key = True
        # TODO: was soll passieren: programm ende oder message in der UI?
        # message an die UI wenn ich irgendwas habe mit der ich messagen kann.
        # ergaenzend noch was das hier macht man legt all die keys die man hat in einen ordner es liest alle keys
        # aus und erstellt einen neuen keyring in einem subfolder
        if no_private_key:
            pass  # throw Exception

    def get_key_list_private(self):
        """
        :return: private Key list of keyring
        """
        return self.gpg.list_keys(secret=True)

    def get_key_list_public(self):
        """

        :return: public key list of keyring
        """
        return self.gpg.list_keys()

    def set_private_key(self, finger_print):
        # TODO: wie mehr als ein private key??? ein gpg schlüsselbund enthält ein bis n schlüssel;
        # jeder dieser schlüssel
        # TODO: besteht aus 1 bis n subschlüsseln; jeder dieser subschlüssel besteht aus einem privaten und einem
        # TODO: öffentlichem anteil. -> was ist hier gemeint?
        # haben wir heute im meeting besprochen, sollte also klar sein.
        """
        set a private key if more then one exist

        :param finger_print: fingerprint of the private key to use
        :return:
        """
        if self.privateKey != finger_print:
            self.newPrivateKey = True
            self.privateKey = finger_print

    def get_private_key(self):
        # TODO: siehe set_private_key
        # siehe set private key :)
        """
        :return:get the private key that is used
        """
        return self.privateKey

    def set_pass_phrase(self, pass_phrase):
        """

        :param pass_phrase: secret pass phrase
        :return: --
        """
        self.passPhrase = pass_phrase

    # not tested yet
    def delete_keys(self, fingerprint, secret=False):
        """
        delete key from keyring

        :param fingerprint: fingerprint to delete
        :param secret: true if also delete private key
        :return:
        """
        self.gpg.delete_keys(fingerprints=fingerprint, secret=secret)

    # not tested yet
    def generate_gnupg_key(self, name, email, expire_date, key_type, key_length, passphrase, keyserver_uri):
        """
        generate a new private key if none exists

        :param name: Name
        :param email: Mail
        :param expire_date: expire Date
        :param key_type: key Type (eg RSA)
        :param key_length: length of key (eg 4096)
        :param passphrase: secret passphrase
        :param keyserver_uri: keyserver to upload to
        :return:
        """
        inp = self.gpg.gen_key_input(name_real=name,
                                     name_email=email,
                                     expire_date=expire_date,
                                     key_type=key_type,
                                     key_length=key_length,
                                     subkey_usage='encrypt,sign,auth',
                                     passphrase=passphrase,
                                     keyserver=keyserver_uri)
        key = self.gpg.gen_key(inp)
        self.set_pass_phrase(passphrase)

    # speicherort? -> not tested yet
    def export_key(self, fingerprint, secret=False):
        # TODO: meinst du export zum schlüsselaustausch?
        # ja
        """
        export a key from a Keyring
        :param fingerprint: fingerprint to export
        :param secret: if also the private key should be exported default False
        :return:
        """
        if secret:
            self.gpg.export_keys(fingerprint, secret=secret)
            self.gpg.export_keys(fingerprint)
        else:
            self.gpg.export_keys(fingerprint)
            # testen

    def import_online_keys(self, server, keyids):
        # TODO: wie läuft den eingentlich die überprüfung der fingerprints?
        # ob es die Fingerprints gibt oder ob ich dem key vertraue?
        """
        import a key from a key server

        :param server: keyserver
        :param keyids: keyid
        :return:
        """
        key = self.gpg.recv_keys(server, keyids)
        self.gpg.import_keys(key)

        # TODO: sorry, hab grad keine zeit das noch weiter anzusehen

    def copy_file_encrypt(self, f1, f2, time_sync=True):
        """
        Copies files from the local folder to the cloud folder and encrypts it.

        :param f1: file to be copied
        :param f2: new encrypted copied file
        :return:
        """

        # create share list
        encrypt_list = [self.privateKey['fingerprint']]

        if os.path.isfile(f1):
            if f1 in self.share:
                # get the share fingerprints
                listing = self.user_db.get_group_fingerprints(self.share[f1])
                encrypt_list.append(listing)
            with open(f1, 'rb') as f:
                self.gpg.encrypt_file(
                    f, recipients=encrypt_list,
                    output=f2,
                    always_trust=True
                )
        if time_sync:
            self._time_sync(f1, f2)

    def copy_file_decrypt(self, f1, f2, time_sync=True):
        """
        Copies the file from the cloud folder to the local folder.

        :param f1: file to be decrypted
        :param f2: new decrypted file
        :return:
        """
        # check if file is a pgp file
        # sehr rudimentär aber funktionstüchtig wieso nicht eleganter, weil ich keine eigenen dateiendungen vergebe
        read = open(f1, 'r')
        check = read.read(6)
        if check != "-----B":
            return

        if os.path.isfile(f1):
            with open(f1, 'rb') as f:
                self.gpg.decrypt_file(f, passphrase=self.passPhrase, output=f2, always_trust=True)

        if time_sync:
            self._time_sync(f1, f2)

    def _time_sync(self, f1, f2):
        """
        Time Sync for less sync afford at start up.

        :param f1: the file with the right time
        :param f2: the new created time with incorrect time
        :return:
        """

        # get stats
        stat = os.stat(f1)
        f1_a_time = stat.st_atime
        f1_m_time = stat.st_mtime
        # set tuple
        time = (f1_a_time, f1_m_time)
        # change time
        os.utime(path=f2, times=time)

    def set_share_list(self, share):
        """
        Set the share dictionary.

        The dictionary have to look like this:
        all shared folders on one side
        and the public key fingerprints list on the other side

        Attention you have to use new_sync afterwards.

        :param share: the new share list
        :return:
        """
        if self.share != share:
            self.newShare = True
            self.oldShare = self.share
            self.share = share

    def get_share_list(self):
        """
        :return: the at the moment used shared list
        """
        return self.share

    def get_sync_required(self):
        """
        if we need a new sync

        :return: --
        """
        if self.newShare or self.newPrivateKey:
            return True
        else:
            return False

    def set_share_ﬂag(self, change=False):
        """
        set newShare flag to false if you ran new sync

        :param change: True if change back
        :return: --
        """
        if change:
            self.newShare = False

    def get_share_flag(self):
        """
        :return: the share flag (True/False)
        """
        return self.newShare

    def get_new_private_key_flag(self):
        """

        :return:the private Key flag (True/False)
        """
        return self.newPrivateKey

    def set_new_private_key_ﬂag(self, change=False):
        """
        set newPrivateKeyFlag

        :param change: True if change back
        :return: --
        """
        if change:
            self.newPrivateKey = False

    def get_old_share_list(self):
        """
        not important for the user but vor the new sync
        :return: returns the previous share list
        """
        return self.oldShare
