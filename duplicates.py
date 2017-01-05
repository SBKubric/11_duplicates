import os
import hashlib
import collections
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


def get_file_hash(filepath):
    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as source_file:
        for chunk in iter(lambda: source_file.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def find_dups(root_dir):
    hashes_list = collections.defaultdict(list)
    for dir_name, subdir_list, file_list in os.walk(root_dir):
        for fname in file_list:
            fpath = os.path.join(dir_name, fname)
            hash_sha256 = get_file_hash(fpath)
            hashes_list[hash_sha256].append(fpath)
    return list(filter(lambda entry: len(entry) > 1, hashes_list.values()))


def configure_logging(args):
    if args.logfile:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(message)s',
                            filename=args.logfile,
                            filemode='w')
    else:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(message)s')


def log_duplicates(dups, args):
    logging.info('At %s scanned %s.' % (datetime.datetime.now(), root_dir))
    if args.logfile:
        print('Writing down to %s', args.logfile)
    if dups is None:
        logging.info('No duplicates found!')
        return None
    for paths in dups:
        logging.info('\n\nThese files are duplicates:')
        for path in paths:
            logging.info(path)


if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)
    root_dir = input('Enter the existing root directory:\n=> ')
    while not os.path.isdir(root_dir):
        root_dir = input('Oops! Looks like there is no such directory! Enter the existing root directory:\n=> ')
    print('Scanning the directory...')
    dups = find_dups(root_dir)
    log_duplicates(dups, args)

