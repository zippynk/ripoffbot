#!/usr/bin/env python

#  To run ripoffbot, type `python ripoffbot.py <host> <channel (no #)> [--ssl|--plain] <nick> [--classic] [--readconfig] [--nodb]` into a terminal, replacing the placeholders with your configuration.

# The `--classic` flag enables a mode intended to mirror the original mailbot as much as possible.
# The `--readconfig` flag reads all other data (with the exception of the `--classic` and `--nodb` flags) from the file titled `config.json` in the same directory as ripoffbot. This installation should contain an example configuration file, titled `config_example.json`.
# The `--password` flag prompts the user for a password when starting ripoffbot. Note that you may not be able to see the password as you type it, and that this can interfere with running ripoffbot in a location where you cannot actively input text. Does not run with `--readconfig`, as it does not apply there; the `config.json` file has an option for a password.
# The `--nodb` flag disables saving messages between sessions.

#  Based on Hardmath123's jokebot. https://github.com/hardmath123/jokebot
#  Modified to be a mailbot ripoff by Nathan Krantz-Fire (a.k.a zippynk). https://github.com/zippynk/ripoffbot
#  Ripped off from Aaron Weiss's mailbot (meaning that although no code was directly re-used, it behaves as similar to Aaron's mailbot as possible on the outside). https://github.com/aatxe/mailbot

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
import json
import getpass

if "/" in __file__:
    configLocation = os.path.dirname(__file__) +"/config.json"
else:
    configLocation = "config.json"
thisVersion = [0,3,1,"d"] # The version of ripoffbot, as a list of numbers (eg [0,1,0] means "v0.1.0"). A "d" at the end means that the current version is a development version and very well may break at some point.

if (len(sys.argv) < 5 or len(sys.argv) > 8) and not "--readconfig" in sys.argv:
    print """Usage: python ripoffbot.py <host> <channel (no #)> [--ssl|--plain] <nick> [--classic] [--readconfig] [--password] [--nodb]

The `--classic` flag enables a mode intended to mirror the original mailbot as much as possible.
The `--readconfig` flag reads all other data (with the exception of the `--classic` and `--nodb` flags) from the file titled `config.json` in the same directory as ripoffbot. This installation should contain an example configuration file, titled `config_example.json`.
The `--password` flag prompts the user for a password when starting ripoffbot. Note that you may not be able to see the password as you type it, and that this can interfere with running ripoffbot in a location where you cannot actively input text. Does not run with `--readconfig`, as it does not apply there; the `config.json` file has an option for a password.
The `--nodb` flag disables saving messages between sessions."""
    exit(0)

# Begin dev edition code.
if "d" in thisVersion:
    print "WARNING! This is a development version of ripoffbot. Proceeding may corrupt ripoffbot database files, crash, and/or have other consequences. Proceed at your own risk."
    if not raw_input("Are you sure you want to proceed? (y/n) ").lower() in ["yes","y","true","continue","yea","yeah","yup","sure"]:
        print "Aborting."
        exit(0)

# End Dev Edition Code.

if "--readconfig" in sys.argv:
    if os.path.isfile(configLocation):
        try:
            config = json.loads(open(configLocation,'r').read())
        except:
            print "Failed to decode configuration file."
            if "d" in thisVersion:
                print str(sys.exc_info()[0])
            exit(0)
        try:
            HOST = str(config["server"])
            if len(config["channels"]) > 1:
                print "Ripoffbot only supports joining one channel at a time. Exiting."
                exit(0)
            else:
                CHANNEL = str(config["channels"][0])
            SSL = config["use_ssl"]
            NICK = config["nickname"]
        except KeyError, e:
            print "Failed to decode configuration file."
            if "d" in thisVersion:
                print e
            exit(0)
        if "nick-password" in config.keys():
            PASSWORD = config["nick-password"]
        else:
            PASSWORD = False
        PORT = 6697 if SSL else 6667
    else:
        print "Failed to decode configuration file."
        if "d" in thisVersion:
            print "File " +configLocation +" does not exist."
        exit(0)

else:
    HOST = sys.argv[1]
    CHANNEL = "#"+sys.argv[2]
    SSL = sys.argv[3].lower() == '--ssl'
    PORT = 6697 if SSL else 6667

    NICK = sys.argv[4]
    
    if "--password" in sys.argv:
        PASSWORD = getpass.getpass("Password? ")
    else:
        PASSWORD = False

if "--classic" in sys.argv:
    CLASSICMODE = True
else:
    CLASSICMODE = False
    
if "--nodb" in sys.argv:
    USEDB = False
else:
    USEDB = True

if USEDB == True and os.path.isfile(os.path.expanduser("~") +'/.ripoffbot_database.p'):
    dbLoad = pickle.load(open(os.path.expanduser("~") +'/.ripoffbot_database.p','rb'))
    if dbLoad['version'] == [0,2,0]:
        messages = dbLoad['messages']
    if dbLoad['version'] == [0,3,0]:
        messages = dbLoad['messages']
    else:
        print "This database was created with an old or unknown version of ripoffbot. Please use the newest version (or correct fork) and try again. If this is not possible, move or delete the file '~/.ripoffbot_database.p' and re-run ripoffbot. A new database will be created automatically."
        exit(0)
else:
    messages = []
def saveDb():
    if USEDB == True:
        pickle.dump({'messages':messages,'version':thisVersion}, open(os.path.expanduser("~") +'/.ripoffbot_database.p','wb'))
    
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

s.sendall("NICK %s\r\n"%("tempnick" +str(random.randint(10000001,99999999))))
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
    else:
        name = False
    if words[1] == '001' and not connected:
        # As per section 5.1 of the RFC, 001 is the numeric response for
        # a successful connection/welcome message.
        connected = True
        if not PASSWORD == False:
            s.sendall("PRIVMSG NickServ :" +"ghost " +NICK +" " +PASSWORD +"\r\n")
            s.sendall("PRIVMSG NickServ :" +"identify " +NICK +" " +PASSWORD +"\r\n")
            print "Waiting for NickServ (this will take 10 seconds, and is necessary to make sure other instances are ghosted appropriately)..."
            time.sleep(10)
        s.sendall("NICK %s\r\n"%(NICK))
        s.sendall("JOIN %s\r\n"%(CHANNEL))
        print "Joining..."
    elif words[1] == 'PRIVMSG' and (words[2] == CHANNEL or words[2] == NICK) and ('@tell' in words[3] or ('@privtell' in words[3] and not CLASSICMODE)) and connected and len(words) >= 5 and not name == False:
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
    elif words[1] == 'PRIVMSG' and (words[2] == CHANNEL or words[2] == NICK) and '@help' in words[3] and connected and not CLASSICMODE and not name == False:
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"This mailbot uses the ripoffbot software, which is created by Nathan Krantz-Fire (a.k.a zippynk), based on Jokebot by Hardmath123, and loosely ripped off from Aaron Weiss's mailbot." +"\r\n")
        if "d" in thisVersion:
            s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"WARNING: THIS IS A DEVELOPMENT VERSION! USE AT YOUR OWN RISK!" +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +" " +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"Commands:" +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +" " +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"`@tell recipient message` delivers `message` to `recipient` when they are next \"seen\" saying something. If they are \"seen\" next in a private message to ripoffbot, `message` will be delivered in a reply to that message, and ripoffbot will send a notification message to the sender in the from that the sender sent the original `@tell` command (either in the public channel or via a private message)." +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"`@privtell recipient message` delivers `message` to `recipient` via a private message when they are next \"seen\" saying something. Wherever they are seen, `message` will still be sent to them privately. Upon delivery, ripoffbot will privately send a notification message to the sender." +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"`@help` displays a message similar to this guide, but tailored to IRC users." +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +" " +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"Ripoffbot source code: https://github.com/zippynk/ripoffbot (available under the Mozilla Public License 2.0)" +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"Jokebot source code: https://github.com/hardmath123/jokebot (available under the Unlicense)" +"\r\n")
        s.sendall("PRIVMSG %s :"%(CHANNEL if words[2] == CHANNEL else name) +"Original Mailbot source code: hhttps://github.com/aatxe/mailbot (not licensed at all, but that doesn't matter, since ripoffbot takes no direct code from this mailbot)" +"\r\n")
    if CLASSICMODE and not name == False:
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
    elif not name == False:
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
