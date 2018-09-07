import time
import sys
import requests
import json
import argparse
import datetime
    
messages_json = []
messages_log = []


def getChat(cid,data,output_format):

    offset = data['vod']['offset']
    vodid = data['vod']['id']
    duration = float(data['duration'])

    endOfClipoffset = offset+duration
    endOfClipoffset = float(endOfClipoffset)

    CHUNK_ATTEMPTS = 6
    CHUNK_ATTEMPT_SLEEP = 10

    response = None
    vod_info = requests.get("https://api.twitch.tv/kraken/videos/v" + vodid, headers={"Client-ID": cid}).json()
    print("done")
    if "error" in vod_info:
        sys.exit("got an error in vod info response: " + str(vod_info))
    response = None
    # store the vod metadata in the first element of the message array
    print("downloading chat messages for the clip: ")
    while response == None or '_next' in response and float(response["comments"][0]["content_offset_seconds"])<endOfClipoffset+1:
        query = ('cursor=' + response['_next']) if response != None and '_next' in response else ('content_offset_seconds='+str(offset))
        for i in range(0, CHUNK_ATTEMPTS):
            error = None
            try:
                response = requests.get("https://api.twitch.tv/v5/videos/" + str(vodid) + "/comments?" + query, headers={"Client-ID": cid}).json()
            except requests.exceptions.ConnectionError as e:
                error = str(e)
            else:
                if "errors" in response or not "comments" in response:
                    error = "error received in chat message response: " + str(response)
            
            if error == None:
                total_comments = len(response["comments"])                
                msg_offset = response["comments"][total_comments-1]["content_offset_seconds"]
                progress_update = msg_offset - offset
                percent = int((progress_update*100/int(duration)))
                if percent > 100:
                    percent = 100
                sys.stdout.write('\r')
                sys.stdout.write("%%%d" % (percent))
                for comment in response["comments"]:
                    if comment['content_offset_seconds'] > offset and comment['content_offset_seconds'] < endOfClipoffset:
                        if output_format == "json":
                            messages_json.append(comment)
                        elif output_format == "log":
                            c_offset = int(comment['content_offset_seconds']) - int(offset)
                            c_time = "[" + str(datetime.timedelta(seconds=c_offset+1)) + "] "
                            c_name = "<" + comment["commenter"]["display_name"] + "> "
                            com = comment["message"]["body"]
                            messages_log.append(str(c_time)+c_name+com)
                        else:
                            messages_json.append(comment)
                            c_offset = int(comment['content_offset_seconds']) - int(offset)
                            c_time = "[" + str(datetime.timedelta(seconds=c_offset+1)) + "] "
                            c_name = "<" + comment["commenter"]["display_name"] + "> "
                            com = comment["message"]["body"]
                            messages_log.append(str(c_time)+c_name+com)
                break
            else:
                print("\nerror while downloading chunk: " + error)
                
                if i < CHUNK_ATTEMPTS - 1:
                        print("retrying in " + str(CHUNK_ATTEMPT_SLEEP) + " seconds ", end="")
                print("(attempt " + str(i + 1) + "/" + str(CHUNK_ATTEMPTS) + ")")
                
                if i < CHUNK_ATTEMPTS - 1:
                    time.sleep(CHUNK_ATTEMPT_SLEEP)
        
        if error != None:
            sys.exit("max retries exceeded.")
