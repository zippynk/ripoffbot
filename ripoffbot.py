#!/usr/bin/env python

#  To run ripoffbot, type `python ripoffbot.py <host> <channel (no #)> [--ssl|--plain] <nick> [--classic]` into a terminal, replacing the placeholders with your configuration.

#  The `--classic` flag makes ripoffbot run in a simpler mode, more like the mailbot that inspired it.

#  Based on jokebot by Hardmath123. https://github.com/hardmath123/jokebot
#  Modified to be a mailbot ripoff by Nathan Krantz-Fire (a.k.a zippynk). https://github.com/zippynk/ripoffbot

#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.


import socket
import select
import random
import ssl
import sys
import time
import os
import pickle
from datetime import datetime
import timestampcompare


thisVersion = [0,2,0] # The version of ripoffbot, as a list of numbers (eg [0,1,0] means "v0.1.0")

if len(sys.argv) != 5 and len(sys.argv) != 6:
    print "Usage: python ripoffbot.py <host> <channel (no #)> [--ssl|--plain] <nick> [--classic]"
    exit(0)

# Begin dev edition code. Comment this stuff out in release versions.

print "WARNING! This is a development version of ripoffbot. Proceeding may corrupt ripoffbot database files, crash, and/or have other consequences. Proceed at your own risk."
if not raw_input("Are you sure you want to proceed? (y/n) ").lower() in ["yes","y","true","continue","yea","yeah","yup","sure"]:
    print "Aborting."
    exit(0)

# End Dev Edition Code.

if os.path.isfile(os.path.expanduser("~") +'/.ripoffbot_database.p'):
    dbLoad = pickle.load(open(os.path.expanduser("~") +'/.ripoffbot_database.p','rb'))
    if dbLoad['version'] == [0,2,0]:
        messages = dbLoad['messages']
    else:
        print "This database was created with an old or unknown version of ripoffbot. Please use the newest version (or correct fork) and try again. If this is not possible, move or delete the file '~/.ripoffbot_database.p' and re-run ripoffbot. A new database will be created automatically."
        exit(0)
else:
    messages = []
def saveDb():
    pickle.dump({'messages':messages,'version':[0,1,1]}, open(os.path.expanduser("~") +'/.ripoffbot_database.p','wb'))

HOST = sys.argv[1]
CHANNEL = "#"+sys.argv[2]
SSL = sys.argv[3].lower() == '--ssl'
PORT = 6697 if SSL else 6667

NICK = sys.argv[4]

if len(sys.argv) >= 6:
    if sys.argv[5].lower() == '--classic':
        CLASSICMODE = True
    else:
        CLASSICMODE = False
else:
    CLASSICMODE = False
    
print CLASSICMODE

plain = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = ssl.wrap_socket(plain) if SSL else plain

print "Connecting..."

s.connect((HOST, PORT))
def read_loop(callback):
    data = ""
    CRLF = '\r\n'
    while True:
        time.sleep(0.2)
        try:
            readables, writables, exceptionals = select.select([s], [s], [s]) 
            if len(readables) == 1:
                data += s.recv(512);
                while CRLF in data:
                    message = data[:data.index(CRLF)]
                    data = data[data.index(CRLF)+2:]
                    callback(message)
        except KeyboardInterrupt:
            print "Leaving..."
            s.sendall("PART %s :Bye\r\n"%(CHANNEL))
            s.close()
            exit(0)

print "Registering..."

s.sendall("NICK %s\r\n"%(NICK))
s.sendall("USER %s * * :A mail bot\r\n"%(NICK))


connected = False
def got_message(message):
    print message
    global connected # yes, bad Python style. but it works to explain the concept, right?
    words = message.split(' ')
    if 'PING' in message:
        s.sendall('PONG\r\n') # it never hurts to do this :)
    if words[0][0] == ":":
        writing = True
        name = ''
        for i in words[0][1:len(words[0])-1]:
            if i == ' ' or i == '!':
                writing = False
            else:
                if writing == True:
                    name = name +i
    if words[1] == '001' and not connected:
        # As per section 5.1 of the RFC, 001 is the numeric response for
        # a successful connection/welcome message.
        connected = True
        s.sendall("JOIN %s\r\n"%(CHANNEL))
        print "Joining..."
    elif words[1] == 'PRIVMSG' and (words[2] == CHANNEL or words[2] == NICK) and ('@tell' in words[3] or ('@privtell' in words[3] and not CLASSICMODE)) and connected and len(words) >= 5:
        # Someone probably said `@tell`.
        if words[4] == NICK:
            s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +name +": I'm right here!" + "\r\n")
        else:
            if '@privtell' in words[3] and words[2] == CHANNEL:
                s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +name +": You can't use @privtell in a public channel - only in private messages. Please use @tell or resend using @privtell in a private message to me. Type @help for more information." + "\r\n")
            else:
                messages.append([name,words[4],' '.join(words[5:len(words)]),'@privtell' in words[3],words[2] == CHANNEL,datetime.now()])
                saveDb()
                s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +name +": I'll let them know!" + "\r\n")
    elif words[1] == 'PRIVMSG' and (words[2] == CHANNEL or words[2] == NICK) and '@help' in words[3] and connected and not CLASSICMODE:
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"This mailbot uses the ripoffbot software, which is created by Nathan Krantz-Fire (a.k.a zippynk), and based on Jokebot by Hardmath123." +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +" " +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"WARNING: THIS IS A DEVELOPMENT VERSION! USE AT YOUR OWN RISK!" +"\r\n") # Comment this out for release versions.
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +" " +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"Commands:" +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +" " +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"`@tell recipient message` delivers `message` to `recipient` when they are next \"seen\" saying something. If they are \"seen\" next in a private message to ripoffbot, `message` will be delivered in a reply to that message, and ripoffbot will send a notification message to the sender in the from that the sender sent the original `@tell` command (either in the public channel or via a private message)." +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"`@privtell recipient message` delivers `message` to `recipient` via a private message when they are next \"seen\" saying something. Wherever they are seen, `message` will still be sent to them privately. Upon delivery, ripoffbot will privately send a notification message to the sender." +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"`@help` displays a message similar to this guide, but tailored to IRC users." +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +" " +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"Ripoffbot source code: https://github.com/zippynk/ripoffbot (available under the Mozilla Public License)" +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +" " +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"Jokebot source code: https://github.com/hardmath123/jokebot (available under the Unlicense)" +"\r\n")
    if CLASSICMODE:
        messagesToPop = []
        for i in range(len(messages)):
            if messages[i][1] == name:
                deltastring = timestampcompare.usefulComparison(datetime.now(),messages[i][5])
                if messages[i][3] == False:
                    s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +name +": " +deltastring +', ' +messages[i][0] +' said ' +messages[i][2] + "\r\n")
                else:
                    s.sendall("PRIVMSG %s :"%(name) +name +": " +deltastring +', ' +messages[i][0] +' said ' +messages[i][2] + "\r\n")
                    s.sendall("PRIVMSG %s :"%(messages[i][0]) +messages[i][0] +": Notified " +name +".\r\n")
                messagesToPop.append(i)
        if len(messagesToPop) > 0:
            for i in sorted(messagesToPop, reverse=True):
                messages.pop(i)
            saveDb()
    else:
        messagesToPop = []
        for i in range(len(messages)):
            if messages[i][1] == name:
                deltastring = timestampcompare.usefulComparison(datetime.now(),messages[i][5])
                if messages[i][3] == False:
                    s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +name +": " +deltastring +', ' +messages[i][0] +' said ' +messages[i][2] + "\r\n")
                    if words[2] == NICK:
                        if messages[i][4] == True: # If the message was sent via a public channel.
                            s.sendall("PRIVMSG %s :"%(CHANNEL) +messages[i][0] +": Notified " +name +".\r\n")
                        else: # If the message was not sent via a public channel, meaning it was sent via a private message.
                            s.sendall("PRIVMSG %s :"%(messages[i][0]) +messages[i][0] +": Notified " +name +".\r\n")
                else:
                    s.sendall("PRIVMSG %s :"%(name) +name +": " +deltastring +', ' +messages[i][0] +' said ' +messages[i][2] + "\r\n")
                    s.sendall("PRIVMSG %s :"%(messages[i][0]) +messages[i][0] +": Notified " +name +".\r\n")
                messagesToPop.append(i)
        if len(messagesToPop) > 0:
            for i in sorted(messagesToPop, reverse=True):
                messages.pop(i)
            saveDb()
    
read_loop(got_message)