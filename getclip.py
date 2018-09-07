from app import grabber
from app import clip
from app import output
import argparse
import json
import requests
import sys

#Generate parser arguments
parser = argparse.ArgumentParser(description="twitch Clip chat data grabber")
parser.add_argument("-s","--slug", metavar="", required=True, help="Twitch clib slug i.e. HungryOnerousCoffeeFrankerZ", type=str)
parser.add_argument("-i","--clientid", metavar="", required=True, help="your client id", type=str)
parser.add_argument("-f","--format", metavar="", help="json or console", type=str)
args = parser.parse_args()

#api id
cid = args.clientid
slug = args.slug
o_format = args.format

#get clip metadata
data = clip.getClipData(args.clientid, args.slug)
if data == None:
    sys.exit("your client id is broken\ncheck your client id")
elif data == "wrongslug":
    sys.exit("slug is broken\ncheck clip slug (link)")

print()

streamer_name = data["broadcaster"]["name"]
grabber.getChat(cid,data,args.format)

output.writetofile(o_format,slug,streamer_name)
print("\nsaving "+slug)

print("DONE!")
