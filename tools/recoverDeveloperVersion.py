#!/usr/bin/env python

#  This script can be used to recover databases that have a developer version encoded in them and are therefore inaccessible. It only works for databases from version 0.3.0 and up.

#  By Nathan Krantz-Fire (a.k.a zippynk). Distributed with ripoffbot. https://github.com/zippynk/ripoffbot

#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import os
import pickle
from datetime import datetime

thisVersion = [0,3,2,"d"] # The version of ripoffbot, as a list of numbers (eg [0,1,0] means "v0.1.0"). A "d" at the end means that the current version is a development version and very well may break at some point.

# Begin dev edition code.
if "d" in thisVersion:
    print "WARNING! This is a development version of ripoffbot. Proceeding may corrupt ripoffbot database files, crash, and/or have other consequences. Proceed at your own risk. (Also, converting a developer database version to another developer database version will work in the short run, but you'll have to do it again soon.)"
    if not raw_input("Are you sure you want to proceed? (y/n) ").lower() in ["yes","y","true","continue","yea","yeah","yup","sure"]:
        print "Aborting."
        exit(0)

# End Dev Edition Code.

print "WARNING! You are trying to do the impossible - convert a developer database to a regular one. This may result in errors."
if not raw_input("Are you sure you want to proceed? (y/n) ").lower() in ["yes","y","true","continue","yea","yeah","yup","sure"]:
    print "Aborting."
    exit(0)


dbLoad = pickle.load(open(os.path.expanduser("~") +'/.ripoffbot_database.p','rb'))

if dbLoad['version'] == [0,3,0,"d"]:
    messages = dbLoad['messages']
elif dbLoad['version'] == [0,3,1,"d"]:
    messages = dbLoad['messages']
elif dbLoad['version'] == [0,3,2,"d"]:
    messages = dbLoad['messages']
elif not "d" in dbLoad['version']:
    print "This database is not a developer version."
    exit(0)
else:
    print "This database was created with an old or unknown version of ripoffbot, and the developer recovery script could not recover it. Please use the newest version (or correct fork) and try again. If this is not possible or does not work, move or delete the file '~/.ripoffbot_database.p' and re-run ripoffbot. A new database will be created automatically."
    exit(0)

pickle.dump({'messages':messages,'version':thisVersion}, open(os.path.expanduser("~") +'/.ripoffbot_database.p','wb'))
