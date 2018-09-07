# Twitch Clip Chat!

Fetch the chat log of the given clip!

This is a python script which lets you download a given Twitch Clip's chat data as json, log or both. It takes the "slug" (postfix of the clip link) of the clip and your client id. You can learn commands with the -h argument.

You can get your client id from Twitch: https://dev.twitch.tv/dashboard/apps

## Installation
```
git clone https://github.com/OgulcanCelik/twitch-clip-chat.git
pip install requests

```

## Usage

```bash
python getclip.py -s SparklyGrotesqueStingrayPMSTwin -i 0123456789abcdefghijABCDEFGHIJ 
```

```bash
python getclip.py -s SparklyGrotesqueStingrayPMSTwin -i 0123456789abcdefghijABCDEFGHIJ -f json
```

```bash
python getclip.py -s SparklyGrotesqueStingrayPMSTwin -i 0123456789abcdefghijABCDEFGHIJ -f log
```

## Output

You will get a folder named as the given clip's broadcaster and separate folders named json and log depending on the format argument given. 
