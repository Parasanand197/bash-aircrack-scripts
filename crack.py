#!/usr/bin/env python3

from os import scandir
from subprocess import PIPE, Popen


def list_files_in_path(path):
    """
    This function returns a sorted list of the files listed from a directory.
    """
    files = [entry.path for entry in scandir(path) if entry.is_file()]
    return sorted(files)


def run_cmd_with_realtime_output(cmd):
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line


def build_aircrack_cmd(dictionary_path, bssid, cap_file_path, pwd_file_path):
    return [
        'aircrack-ng',
        '-w',
        dictionary_path,
        '-b',
        bssid,
        '-l',
        pwd_file_path,
        cap_file_path,
    ]

DICTIONARY_PATH = "/root/dictionaries/custom"

if __name__ == "__main__":
    dictionary_files = list_files_in_path(DICTIONARY_PATH)
    print(dictionary_files)
    for output in run_cmd_with_realtime_output(['htop']):
        print(output)
