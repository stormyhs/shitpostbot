# Shitpost Selfbot


A discord self-bot to automate shitposting for your everyday needs. Caution: May be a little racist.

I have no clue where we are taking this thing. It's just there for the sake of being there.

# Usage
!!! READ THE CODE FOR YOURSELF !!!

The obvious out of the way, you will have to `python -m pip install [library name]` for any libraries you may be missing.

Afterwards, open the `config.py` file, and enter your token.

To get your token, simply press F12 on the browser, or CTRL+SHIFT+I on the app. Tab over to networking, and keep clicking packets until you find one with the `Authorization` key.

## Commands
`(prefix)command (required) [optional]`
### Text fun
- `slowprint (content)` loops through the content, editing the message as it goes.
- `ascii (content)` uses `artii.herokuapp.com` to edit the message into ascii art.
- `binary (content)` text to binary.
- `tochar (content)` binary to text.
### Reactions
- `addreactspam (mention) (emoji)` reacts with the specified emoji every time the mentioned user sends a message.
- `rmreactspam (mention)` stops reacting to that user.
- `addkeyspam (keyword) (emoji)` adds reaction to messages that include the keyword
- `rmkeyspam (keyword)` stops reactong to that keyword
- `clearreactspam` clears the reacts list entirely.
### Gif spam
- `spam (key)` spams key in the `giflist.json` file.
- `addspam (key) (link)` adds new entry for you to spam all day
- `rmspam` removes the entry from `giflist.json`

# Changelog

### v0.10
- Added giflist editing commands.

### v0.9
- Added reactspam for keywords.
- Slightly bettter readme

### v0.8
- Improved json loading for getreactions
- Increased the delay between actions 
- `author` is now a subclass of ctx

### v0.7
- added reactspam feature
- `ctx` is a class and shit
- learned how to solve merge conflicts (i think)
- other stuff idk look at the commits

### v0.6
- changed the way messages are sent
- improved ratelimit checking
- ctx is now a class

### v0.5
- added nefarious logger :troll:
- added binary to text command

### v0.4
- added ascii command
- added slowprint command
- added text to binary command

### v0.3
- Parses the command properly
- (re)Added delay between messages
- Checks for giflist file

### v0.2
- very basic prototype

### v0.1
- initial