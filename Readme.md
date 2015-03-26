# Ripoffbot

Ripoffbot is an IRC mailbot. It is based off and is of jokebot by Hardmath123, and was modified into  a ripoff of Aaron Weiss's mailbot by Nathan Krantz-Fire (a.k.a zippynk). However, since then, it has gained several new features that said mailbot does not include.

WARNING: THIS IS A DEVELOPMENT VERSION OF RIPOFFBOT! USE AT YOUR OWN RISK!

To run ripoffbot, type `python ripoffbot.py <host> <channel (no #)> [--ssl|--plain] <nick> [--classic]` into a terminal, replacing the placeholders with your configuration.

The `--classic` flag enables a mode intended to mirror the original mailbot as much as possible.
The `--readconfig` flag reads all other data (with the exception of the `--classic` flag from the file titled `config.json` in the same directory as ripoffbot. This installation should contain an example `config.json` file.

# Commands (run from IRC):

`@tell recipient message` delivers `message` to `recipient` when they are next "seen" saying something. If they are "seen" next in a private message to ripoffbot, `message` will be delivered in a reply to that message, and ripoffbot will send a notification message to the sender in the from that the sender sent the original `@tell` command (either in the public channel or via a private message).

`@privtell recipient message` delivers `message` to `recipient` via a private message when they are next "seen" saying something. Wherever they are seen, `message` will still be sent to them privately. Upon delivery, ripoffbot will privately send a notification message to the sender. Not available in classic mode.

`@help` displays a message similar to this guide, but tailored to IRC users. Not available in classic mode.

# Database

Ripoffbot stores messages in a file titled `.ripoffbot_database.p` in the home directory of the account that runs it.

# License

This Source Code Form is subject to the terms of the Mozilla Public

License, v. 2.0. If a copy of the MPL was not distributed with this

file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Source/Attribution

Ripoffbot source code: https://github.com/zippynk/ripoffbot

Jokebot source code: https://github.com/hardmath123/jokebot

Original Mailbot source code: https://github.com/aatxe/mailbot