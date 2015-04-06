#!/usr/bin/env python

#  This script can be used to recover databases that have a developer version encoded in them and are therefore inaccessible. It only works for version 0.3.1(d) and up.

#  By Nathan Krantz-Fire (a.k.a zippynk). Distributed with ripoffbot. https://github.com/zippynk/ripoffbot

#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import os
import pickle
from datetime import datetime

thisVersion = [0,3,1] # The version of ripoffbot, as a list of numbers (eg [0,1,0] means "v0.1.0"). A "d" at the end means that the current version is a development version and very well may break at some point.

# Begin dev edition code.
if "d" in thisVersion:
    print "WARNING! This is a development version of ripoffbot. Proceeding may corrupt ripoffbot database files, crash, and/or have other consequences. Proceed at your own risk."
    if not raw_input("Are you sure you want to proceed? (y/n) ").lower() in ["yes","y","true","continue","yea","yeah","yup","sure"]:
        print "Aborting."
        exit(0)

# End Dev Edition Code.

print "WARNING! You are trying to do the impossible - convert a developer database to a regular one. This may result in errors."
if not raw_input("Are you sure you want to proceed? (y/n) ").lower() in ["yes","y","true","continue","yea","yeah","yup","sure"]:
    print "Aborting."
    exit(0)


dbLoad = pickle.load(open(os.path.expanduser("~") +'/.ripoffbot_database.p','rb'))
if dbLoad['version'] == [0,2,0]:
    messages = dbLoad['messages']
if dbLoad['version'] == [0,3,0]:
    messages = dbLoad['messages']
else:
    print "This database was created with an old or unknown version of ripoffbot, and the developer recovery script could not recover it. Please use the newest version (or correct fork) and try again. If this is not possible or does not work, move or delete the file '~/.ripoffbot_database.p' and re-run ripoffbot. A new database will be created automatically."
    exit(0)

pickle.dump({'messages':messages,'version':thisVersion}, open(os.path.expanduser("~") +'/.ripoffbot_database.p','wb'))