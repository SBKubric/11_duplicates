import os
import hashlib
import sys

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


def print_duplicates():
    dups = list(filter(lambda entry: len(entry) > 1, duplicates.values()))
    if len(dups) == 0:
        print('No duplicates found!')
        sys.exit()
    for paths in dups:
        print('-----------------------')
        print('These files are duplicates:')
        for path in paths:
            print(path)
    print('Done!')


if __name__ == '__main__':
    print('Enter the existing root directory:')
    root_dir = ''
    while root_dir == '':
        root_dir = input()
    look_for_duplicates(root_dir)
    print_duplicates()
