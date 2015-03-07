#!/usr/bin/env python

# A small piece of ripoffbot, for testing time differences, since those are hard to test in the real implementation.

# Written by Nathan Krantz-Fire (a.k.a zippynk).

#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime
a = input("Year? ")
b = input("Month? ")
c = input("Day? ")
d = input("Hour? ")
e = input("Minute? ")
f = input("Second? ")
delta = datetime.now()-datetime(a,b,c,d,e,f)
if delta.days > 365:
    if int(round(float(delta.days)/365.0)) == 1:
        deltastring = "A year ago"
    else:
        deltastring = str(int(round(float(delta.days)/365.0))) +" years ago"
elif delta.days >= 30:
    if int(round(float(delta.days)/30.0)) == 1:
        deltastring = "A month ago"
    else:
        deltastring = str(int(round(float(delta.days)/30.0))) +" months ago"
elif delta.days >= 7:
    deltastring = str(int(round(float(delta.days)/7.0))) +" weeks ago"
elif delta.days > 0:
    if delta.seconds >= 43200:
        if delta.days+1 == 1:
            deltastring = "A day ago"
        else:
            deltastring = str(delta.days+1) +" days ago"
    else:
        if delta.days == 1:
            deltastring = "A day ago"
        else:
            deltastring = str(delta.days) +" days ago"
elif delta.seconds >= 3600:
    if int(round(float(delta.seconds)/3600.0)) == 1:
        deltastring = "An hour ago"
    else:
        deltastring = str(int(round(float(delta.seconds)/3600.0))) +" hours ago"
elif delta.seconds >= 60:
    if int(round(float(delta.seconds)/60.0)) == 1:
        deltastring = "A minute ago"
    else:
        deltastring = str(int(round(float(delta.seconds)/60.0))) +" minutes ago"
elif delta.seconds > 30: # no "a second ago", since it has to be at least 30 seconds ago
    deltastring = str(delta.seconds) +" seconds ago"
elif delta.days < 0 or delta.seconds < 0:
    deltastring = "The timing of this is a little unclear, but at some point or another"
else:
    deltastring = "Moments ago"
print deltastring