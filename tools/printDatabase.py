#!/usr/bin/env python

#  Tool for viewing ripoffbot databases.
#  Created by Nathan Krantz-Fire (a.k.a zippynk).
#  Ships with ripoffbot - http://github.com/zippynk/ripoffbot

#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import pickle
from datetime import datetime

thisVersion = [0,4,0,"d"] # The version of ripoffbot, as a list of numbers (eg [0,1,0] means "v0.1.0"). A "d" at the end means that the current version is a development version and very well may break at some point.

# Begin dev edition code.
if "d" in thisVersion:
    print "WARNING! This is a development version of ripoffbot. Proceeding may corrupt ripoffbot database files, crash, and/or have other consequences. Proceed at your own risk."
    if not raw_input("Are you sure you want to proceed? (y/n) ").lower() in ["yes","y","true","continue","yea","yeah","yup","sure"]:
        print "Aborting."
        exit(0)

# End Dev Edition Code.

if os.path.isfile(os.path.expanduser("~") +'/.ripoffbot_database.p'):
    dbLoad = pickle.load(open(os.path.expanduser("~") +'/.ripoffbot_database.p','rb'))
    if dbLoad['version'] == [0,2,0]:
        messages = dbLoad['messages']
    elif dbLoad['version'] == [0,3,0]:
        messages = dbLoad['messages']
    elif dbLoad['version'] == [0,3,1]:
        messages = dbLoad['messages']
    elif dbLoad['version'] == [0,3,2,"d"]:
        messages = dbLoad['messages']
    else:
        print "This database was created with an old or unknown version of ripoffbot. Please use the newest version (or correct fork) and try again. If this is not possible or does not work, move or delete the file '~/.ripoffbot_database.p' and re-run ripoffbot. A new database will be created automatically. You may also want to try running recoverDeveloperVersion.py to recover a script marked with a developer version tag."
        exit(0)
else:
    messages = []
def saveDb(): # not needed for current functionality, but keeping just in case
    if USEDB == True:
        pickle.dump({'messages':messages,'version':thisVersion}, open(os.path.expanduser("~") +'/.ripoffbot_database.p','wb'))

for i in messages:
    print "Created with ripoffbot version: " +str(dbLoad['version'])
    print "{0} -> {1} - {2} ({3}, {4}): {5}".format(i[0],i[1],str(i[5]),"Sent publically" if i[4] else "Sent privately","To be delivered publically" if i[3] else "To be delivered privately",i[2])
