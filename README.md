# ads-tgbot
Telegram bot for advertising (forwarding/sending) messages to all joined groups automatically by interval

### Config

Configure in `accounts.json`, supported multiple accounts in json structure

*Note*
* For forwarding message `"promo_message"` will be ignored, when is `"forward_message"` filled.
* "time_interval" is in minutes.
* `"reply_message"` is feature if someone write to user-bot

### Run
```
py promov2.py
```
