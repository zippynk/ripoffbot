#!/usr/bin/env python

# A python library for comparing timestamps, distributed as part of ripoffbot.

# Written by Nathan Krantz-Fire (a.k.a zippynk).
# Source available at https://github.com/zippynk/ripoffbot as part of the Ripoffbot source code.

#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime
def usefulComparison(a,b):
    delta = a-b
    if delta.days > 365:
        if int(round(float(delta.days)/365.0)) == 1:
            deltastring = "A year ago"
        else:
            deltastring = str(int(round(float(delta.days)/365.0))) +" years ago"
    elif delta.days >= 30:
        if int(round(float(delta.days)/30.0)) == 1:
            deltastring = "A month ago"
        elif int(round(float(delta.days)/30.0)) == 12:
            deltastring = "A year ago"
        else:
            deltastring = str(int(round(float(delta.days)/30.0))) +" months ago"
    elif delta.days >= 7:
        if int(round(float(delta.days)/7.0)) == 1:
            deltastring = "A week ago"
        elif int(round(float(delta.days)/7.0)) == 30:
            deltastring = "A month ago"
        else:
            deltastring = str(int(round(float(delta.days)/7.0))) +" weeks ago"
    elif delta.days > 0:
        if delta.seconds >= 43200:
            if delta.days+1 == 1:
                deltastring = "A day ago"
            # No "== 7" here, since the definition already ruled it out.
            else:
                deltastring = str(delta.days+1) +" days ago"
        else:
            if delta.days == 1:
                deltastring = "A day ago"
            # No "== 7" here, since the definition already ruled it out.
            else:
                deltastring = str(delta.days) +" days ago"
    elif delta.seconds >= 3600:
        if int(round(float(delta.seconds)/3600.0)) == 1:
            deltastring = "An hour ago"
        elif int(round(float(delta.seconds)/3600.0)) == 24:
            deltastring = "A day ago"
        else:
            deltastring = str(int(round(float(delta.seconds)/3600.0))) +" hours ago"
    elif delta.seconds >= 60:
        if int(round(float(delta.seconds)/60.0)) == 1:
            deltastring = "A minute ago"
        elif int(round(float(delta.seconds)/60.0)) == 60:
            deltastring = "An hour ago"
        else:
            deltastring = str(int(round(float(delta.seconds)/60.0))) +" minutes ago"
    elif delta.seconds > 30: # no "a second ago", since it has to be at least 30 seconds ago, and no "a minute ago", since this doesn't round and therefore can't round up to 60
        deltastring = str(delta.seconds) +" seconds ago"
    elif delta.days < 0 or delta.seconds < 0:
        deltastring = "The timing of this is a little unclear, but at some point or another"
    else:
        deltastring = "Moments ago"
    return deltastring
# The rest of this is useful for testing, but should be commented out when actually using the library.
#a = input("Year: ")
#b = input("Month: ")
#c = input("Day: ")
#d = input("Hour: ")
#e = input("Minute: ")
#f = input("Second: ")
#print str(datetime(a,b,c,d,e,f))
#now = (datetime.now())
#print str(now)
#print usefulComparison(now,datetime(a,b,c,d,e,f))