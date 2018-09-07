import json
import os, os.path
import errno
from app import grabber

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass

def safe_open_w(path):
    mkdir_p(os.path.dirname(path))
    return open(path, 'w', encoding='utf-8')

def writetofile(output_format, slug,name):
    if output_format == "json":
        with safe_open_w(name+"'s clips/json/"+slug+".json") as the_file:
            json.dump(grabber.messages_json,the_file,indent=2, sort_keys=True)
    elif output_format == "log":
        with safe_open_w(name+"'s clips/log/"+slug+".log") as the_file:
            for item in grabber.messages_log:
                the_file.write("%s\n" % item)
    else:
        with safe_open_w(name+"'s clips/json/"+slug+".json") as the_file:
            json.dump(grabber.messages_json,the_file,indent=2, sort_keys=True)
        with safe_open_w(name+"'s clips/log/"+slug+".log") as the_file:
            for item in grabber.messages_log:
                the_file.write("%s\n" % item)