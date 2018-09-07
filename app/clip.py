import requests
import json

def getClipData (cid, slug):
    #get clips' metadata
    prefix = 'https://api.twitch.tv/kraken/clips/'
    print("requesting metadata")
    url = prefix+slug
    r = requests.get(url, headers={"client-id":cid, "Accept":"application/vnd.twitchtv.v5+json"})
    r_code = r.status_code
    
    if r_code == 400:
        return None
    elif r_code == 404:
        return "wrongslug"
    else:
        data = json.loads(r.text)
        return data