#!/bin/bash

################################################################################
# Copyright 2015 by Kevin Kirchner, Luca Rupp, David Pauli
# 
# This file is part of CloudCrypt.
#
# CloudCrypt is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CloudCrypt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with CloudCrypt.  If not, see <http://www.gnu.org/licenses/>.
# 
# Diese Datei ist Teil von CloudCrypt.
#
# CloudCrypt ist Freie Software: Sie können es unter den Bedingungen
# der GNU Lesser General Public License, wie von der Free Software Foundation,
# Version 3 der Lizenz oder (nach Ihrer Wahl) jeder späteren
# veröffentlichten Version, weiterverbreiten und/oder modifizieren.
#
# CloudCrypt wird in der Hoffnung, dass es nützlich sein wird, aber
# OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
# Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
# Siehe die GNU Lesser General Public License für weitere Details.
#
# Sie sollten eine Kopie der GNU Lesser General Public License zusammen mit diesem
# Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.
################################################################################

if [[ "$UID" -eq 0 ]]
then
    echo "you really should not execute cloudcrypt as root user"
    exit 2
fi

version=`python3 cc_version.py || echo "wrong"`
imports=`python3 cc_check_imports.py`

if [[ "$version" -eq 0 ]] && [[ "$imports" -eq 0 ]]
then
    python3 './run.py'
    exit 0
else:
    exit 1
fi
