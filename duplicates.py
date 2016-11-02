import os
import hashlib
import sys
import datetime

files = {}
duplicates = {}


def sha256(filepath):
    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def look_for_duplicates(root_dir):
    for dir_name, subdir_list, file_list in os.walk(root_dir):
        print('Scanning %s...' % dir_name)
        for fname in file_list:
            hash_sha256 = sha256(os.path.join(dir_name, fname))
            if hash_sha256 in duplicates:
                duplicates[hash_sha256].append(os.path.join(dir_name, fname))
            else:
                duplicates[hash_sha256] = [os.path.join(dir_name, fname)]


def log_it(string, *, mode='a'):
    with open('LOGFILE', mode) as logfile:
        logfile.write(' %s\n' % string)
    return string


def print_duplicates():
    dups = list(filter(lambda entry: len(entry) > 1, duplicates.values()))
    if len(dups) == 0:
        print(log_it('No duplicates found!'))
        sys.exit()
    for paths in dups:
        print(log_it('-----------------------'))
        print(log_it('These files are duplicates:'))
        for path in paths:
            print(log_it(path))
    print(log_it('Done!'))


if __name__ == '__main__':
    root_dir = input('Enter the existing root directory:\n=> ')
    while not os.path.isdir(root_dir):
        root_dir = input('Oops! Looks like there is no such directory! Enter the existing root directory:\n=> ')
    log_it('%s ======> %s.' % (datetime.datetime.now(), root_dir))
    look_for_duplicates(root_dir)
    print_duplicates()
