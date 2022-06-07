# Shitpost Selfbot
A discord self-bot to automate shitposting.

# Usage
!!! READ THE CODE FOR YOURSELF !!!

!!! SELF-BOTS ARE AGAINST TOS  !!!

The obvious out of the way, you will have to `python -m pip install [library name]` for any libraries you may be missing. I'll make a requirements file when I care.

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
#### React on user
- `adduserreact (mention) (emoji)` reacts with the specified emoji every time the mentioned user sends a message.
- `rmuserreact (mention)` stops reacting to that user.
- `clearuserreact` clears the reacts list entirely.
#### React on keyword
- `addkeyspam (keyword) (emoji)` adds reaction to messages that include the keyword
- `rmkeyspam (keyword)` stops reactong to that keyword
#### Other
- `randreact (message id)` adds 10 fully random reactions to the message.

### Gif spam
- `spam (key)` spams key in the `giflist.json` file.
- `addspam (key) (link)` adds new entry for you to spam all day
- `rmspam` removes the entry from `giflist.json`

### Status Cycling
#### The default loop timer is 5 minutes. Feel free to change it in `configs.py`.
- `statuscyclelist` shows a list of your statuses.
- `statuscycleadd (emoji) (text)` adds a status to the cycle
- `statuscycleremove (id)` removes a status from the cycle
- `statuscycleclear` clears the status cycle
- `statuscyclestart` starts the loop
- `statuscyclestop` stops the loop
