import os
import hashlib
import sys
import datetime
import argparse
import logging


def parse_args():
    parser = argparse.ArgumentParser(description='The script is designed for locating all duplicates of files'
                                                 'in the given directory.')
    parser.add_argument('-l', '--logfile', default=None,
                        help='The log file with found dups.')
    parser.add_argument('-bl', '--blacklist', default='./password_list', help='The local location of the blacklist'
                                                                              'with passwords.')
    return parser.parse_args()


def path_join(dir, file):
    return os.path.join(dir, file)


def sha256(filepath):
    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def find_dups(root_dir):
    hash_list = {}
    for dir_name, subdir_list, file_list in os.walk(root_dir):
        print('Scanning %s...' % dir_name)
        for fname in file_list:
            fpath = os.path.join(dir_name, fname)
            hash_sha256 = sha256(fpath)
            if hash_sha256 in hash_list:
                hash_list[hash_sha256].append(fpath)
            else:
                hash_list[hash_sha256] = [fpath]
    return list(filter(lambda entry: len(entry) > 1, hash_list.values()))


def configure_logging(args):
    if args.logfile:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=args.logfile,
                            filemode='w')
    else:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s',
                            datefmt='%m-%d %H:%M')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)


def log_duplicates(dups, args):
    logging.info('At %s scanned %s.' % (datetime.datetime.now(), root_dir))
    if args.logfile:
        print('Writing down to %s', args.logfile)
    if dups is None:
        logging.info('No duplicates found!')
        sys.exit()
    for paths in dups:
        logging.info('-----------------------')
        logging.info('These files are duplicates:')
        for path in paths:
            logging.info(path)
    logging.info('Done!')


if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)
    root_dir = input('Enter the existing root directory:\n=> ')
    while not os.path.isdir(root_dir):
        root_dir = input('Oops! Looks like there is no such directory! Enter the existing root directory:\n=> ')
    dups = find_dups(root_dir)
    log_duplicates(dups, args)

