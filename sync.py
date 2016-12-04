#!/usr/bin/python3

import sys

import os.path
import configparser
import argparse

from pathlib import Path

import requests

config = configparser.ConfigParser()
config.read(os.path.expanduser("~/.screeps_sync_config"))

login = config["credentials"]["login"]
password = config["credentials"]["password"]


parser = argparse.ArgumentParser(description="Synchronize a directory with a screeps account")

parser.add_argument("-b", "--branch", action="store", dest="branch", default="default", help="Screeps branch")

parser.add_argument("-d", "--download", action="store_true", dest="download", help="Fetch file/modules from Screeps server")

parser.add_argument("-k", "--keep", action="store_true", dest="keep", help="keep previous files in dir when downloading")


parser.add_argument("path", action="store", help="local path to fetch files/modules from (or store to in the download case")

args = parser.parse_args()

def upload(path):
    filelist = {f.name: f.open().read() for f in path.iterdir() if f.is_file()}

    document = {
        "branch": args.branch,
        "modules": filelist
    }

    r = requests.post(
        'https://screeps.com/api/user/code',
        auth=(login, password),
        json=document,
    )

    if r.status_code != 200:
        sys.exit("%s: HTTP error %s\n%s" % (sys.argv[0], r.status_code, r.json()))
    else:
        print(r.json(), file=sys.stderr)

def download(root):

    r = requests.get(
        'https://screeps.com/api/user/code',
        auth=(login, password),
        params={"branch": args.branch},
    )

    if r.status_code != 200:
        sys.exit("%s: HTTP error %s\n%s" % (sys.argv[0], r.status_code, r.json()))
    else:
        document = r.json()

        if "error" in document:
            sys.exit("%s: Server error: %s\nHint: check branch name" % (sys.argv[0], document["error"]))

        if document["branch"] != args.branch:
            sys.exit("%s: %s" % (sys.argv[0], "unknown branch %s (received branch: %s)" % (args.branch, document["branch"])))

        root.mkdir(parents=True, exist_ok=True)

        if not args.keep:
            for file in root.iterdir():
                file.unlink()

        for fn, content in document["modules"].items():
            path = root / fn
            print("Updating", path, file=sys.stderr)
            with path.open(mode="w") as f:
                f.write(content)


path = Path(args.path)

if args.download:
    download(path)
else:
    upload(path)

