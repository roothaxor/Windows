#!/usr/bin/env python
# coding: utf-8
# transfer.sh cleartext client
# Version: 20161214.1
# Author: Darren Martyn, Harry Roberts
from __future__ import print_function
import sys
import os
import base64
import logging
import argparse
import tempfile
import subprocess
import requests
import progressbar
import clipboard


LOG = logging.getLogger(__name__)


def rand_password():
    return base64.b32encode(os.urandom(15))


# http://stackoverflow.com/questions/11367140/python-popen-gpg-supply-passphrase-and-encryption-text-both-through-stdin-or-fi
def _gpg_pipe(args, data, passphrase):
    keypipe = os.pipe()
    os.write(keypipe[1], passphrase + '\n')
    os.close(keypipe[1])

    argv = ['gpg', '--passphrase-fd', str(keypipe[0]), '-q', '--batch'] + args
    p = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate(data)
    os.close(keypipe[0])

    if p.returncode: # pragma: no cover
        raise RuntimeError("Failed to run, returncode: " + str(p.returncode))
    return out


def make_progress_bar():
    return progressbar.ProgressBar(
        redirect_stdout=True,
        redirect_stderr=True,
        widgets=[
            progressbar.Percentage(),
            progressbar.Bar(),
            ' (',
            progressbar.AdaptiveTransferSpeed(),
            ' ',
            progressbar.ETA(),
            ') ',
        ])


class upload_in_chunks(object):
    def __init__(self, filename, chunksize=1 << 13):
        self.filename = filename
        self.chunksize = chunksize
        self.totalsize = os.path.getsize(filename)
        self.readsofar = 0
        self.bar = make_progress_bar()

    def __iter__(self):
        with open(self.filename, 'rb') as file:
            self.bar.start(self.totalsize)
            while True:
                data = file.read(self.chunksize)
                if not data:
                    break
                self.readsofar += len(data)
                self.bar.update(self.readsofar)
                yield data
            self.bar.finish()

    def __len__(self):
        return self.totalsize


class IterableToFileAdapter(object):
    def __init__(self, iterable):
        self.iterator = iter(iterable)
        self.length = len(iterable)

    def read(self, size=-1): # TBD: add buffer for `len(data) > size` case
        return next(self.iterator, b'')

    def __len__(self):
        return self.length


def encrypt(file_path):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    os.unlink(tmp.name)
    password = rand_password()
    _gpg_pipe(['-c', '-o', tmp.name, file_path], '', password)
    return password, tmp.name


def decrypt(file_path, password):
    output_file = file_path[:-4]
    _gpg_pipe(['-d', '-o', output_file, file_path], '', password)
    os.unlink(file_path)


def upload(args, file_path):
    _, filename = os.path.split(file_path)
    remove_file = False
    password = None
    if args.encrypt:
        remove_file = True
        password, file_path = encrypt(file_path)
        filename = filename + '.gpg'
    upload_url = "https://transfer.sh/" + filename
    try:
        it = upload_in_chunks(file_path, 10)
        r = requests.put(url=upload_url, data=IterableToFileAdapter(it))
    except Exception:
        LOG.exception("Failed to upload file")
        return
    finally:
        if remove_file:
            os.unlink(file_path)
        return password, r.text.strip()


def download(args, url):
    password = None
    if '#' in url:
        url, password = url.split('#', 1)
    filename = url.replace("https://transfer.sh", "")
    filename = filename.split("/")[2]
    LOG.info("Saving %r to %r", url, filename)
    r = requests.get(url=url, stream=True)
    with open(filename, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        bar = make_progress_bar()
        bar.start(total_length)
        readsofar = 0
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                readsofar += len(chunk)
                bar.update(readsofar)
                f.write(chunk)
                f.flush()
        bar.finish()
    if password:
        decrypt(filename, password)


def parse_args():
    parser = argparse.ArgumentParser(description='http://transfer.sh')
    parser.add_argument('-c', '--encrypt', action='store_true',
                        help='Encrypt files before uploading')
    parser.add_argument('files', nargs='*', help='Files to upload')
    args = parser.parse_args()
    if not args.files:
        parser.print_help()
        sys.exit(1)
    return args


def process_file(args, file_or_url):
    if "https://transfer.sh" in file_or_url:
        try:
            download(args, file_or_url)
        except Exception:
            LOG.exception("error while downloading %s", file_or_url)
            return
    else:
        if not os.path.exists(file_or_url):
            LOG.warning("File doesn't exist: %r", file_or_url)
            return
        try:
            password, file_url = upload(args, file_or_url) 
        except Exception:
            LOG.exception("error while uploading %s", file_or_url)
            return
        if not file_url:
            LOG.error("Could not get uploaded file url!")
            return
        if password:
            file_url = file_url + '#' + password
        print("\n"+file_url+"\n")	
	clipboard.copy(file_url)
	clipboard.paste()
	print ("Uploaded file link is copied to clipboard, bye")


def main():
    args = parse_args()
    try:
        for file_or_url in args.files:
            process_file(args, file_or_url)
    except KeyboardInterrupt:
        LOG.info('Caught Ctrl+C, cancelled')
    return 0
        

if __name__ == "__main__":
    logging.basicConfig()
    sys.exit(main())