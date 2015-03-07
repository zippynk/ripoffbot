#!/usr/bin/env python

#  To run ripoffbot, type "python ripoffbot.py <host> <channel (no #)> [--ssl|--plain] <nick>"

#  A fork of jokebot, by Hardmath123. https://github.com/hardmath123/jokebot
#  Modified to be a mailbot ripoff by Nathan Krantz-Fire (a.k.a zippynk). https://github.com/zippynk/ripoffbot

#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

#  Things that still need to be implemented:
#  'some time' needs to be replaced with Time since the message that it's currently dealing with was sent

import socket
import select
import random
import ssl
import sys
import time
import os
import pickle

# Begin dev edition code. Comment this stuff out in release versions.

print "WARNING! This is a development version of ripoffbot. Proceeding may corrupt ripoffbot database files, crash, and/or have other consequences. Proceed at your own risk."
if not raw_input("Are you sure you want to proceed? (y/n) ").lower() in ["yes","y","true","continue","yea","yeah","yup","sure"]:
    print "Aborting."
    exit(0)

# End Dev Edition Code.

thisVersion = [0,1,1] # The version of ripoffbot, as a list of numbers (eg [0,1,0] means "v0.1.0")

if os.path.isfile(os.path.expanduser("~") +'/.ripoffbot_database.p'):
    dbLoad = pickle.load(open(os.path.expanduser("~") +'/.ripoffbot_database.p','rb'))
    if dbLoad['version'] == [0,1,1]:
        messages = dbLoad['messages']
    else:
        print "This database was created with an old or unknown version of ripoffbot. Please use the newest version (or correct fork) and try again. If this is not possible, move or delete the file '~/.ripoffbot_database.p and re-run ripoffbot. A new database will be created automatically."
        exit(0)
else:
    messages = []
def saveDb():
    pickle.dump({'messages':messages,'version':[0,1,1]}, open(os.path.expanduser("~") +'/.ripoffbot_database.p','wb'))

if len(sys.argv) != 5:
    print "Usage: python ripoffbot.py <host> <channel (no #)> [--ssl|--plain] <nick>"
    exit(0)

HOST = sys.argv[1]
CHANNEL = "#"+sys.argv[2]
SSL = sys.argv[3].lower() == '--ssl'
PORT = 6697 if SSL else 6667

NICK = sys.argv[4]

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
        messagesToPop = []
        for i in range(len(messages)):
            if messages[i][1] == name:
                s.sendall("PRIVMSG %s :"%(CHANNEL) +name +": " +'some time' +' ago, ' +messages[i][0] +' said ' +messages[i][2] + "\r\n")
                messagesToPop.append(i)
        if len(messagesToPop) > 0:
            for i in sorted(messagesToPop, reverse=True):
                messages.pop(i)
            saveDb()
    if words[1] == '001' and not connected:
        # As per section 5.1 of the RFC, 001 is the numeric response for
        # a successful connection/welcome message.
        connected = True
        s.sendall("JOIN %s\r\n"%(CHANNEL))
        print "Joining..."
    elif words[1] == 'PRIVMSG' and words[2] == CHANNEL and '@tell' in words[3] and connected:
        # Someone probably said `@tell`.
        if words[4] == NICK:
            s.sendall("PRIVMSG %s :"%(CHANNEL) +name +": I'm right here!" + "\r\n")
        else:
            messages.append([name,words[4],' '.join(words[5:len(words)])])
            saveDb()
            s.sendall("PRIVMSG %s :"%(CHANNEL) +name +": I'll let them know!" + "\r\n")
    
read_loop(got_message)
