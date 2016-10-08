#!/usr/bin/env python3

from os import scandir, path
from subprocess import PIPE, Popen
from getopt import getopt, GetoptError
from sys import argv, exit


def list_files_in_path(path_to_list):
    """
    This function returns a sorted list of the files listed from a directory.
    """
    files = [entry.path for entry in scandir(path_to_list) if entry.is_file()]
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


def usage():
    print("""
          Usage:
          -h or --help: this help
          -b or --bssid: the BSSID of the wifi network to crack
          -c or --capfile: the path of the *.cap file containing the handshakes to be used.
          """)


def error(msg):
    print("\nError: {}\n".format(msg))


def check_cmdline_parameters(parameters):
    flag = True
    error_msg = ""
    if "capfile" in parameters and not path.isfile(parameters["capfile"]):
        flag = False
        error_msg = "CAP file: \"{}\" is not a valid file or does not exist!".format(parameters["capfile"])
    return flag, error_msg


DICTIONARY_PATH = "/root/dictionaries/custom"

if __name__ == "__main__":
    #    dictionary_files = list_files_in_path(DICTIONARY_PATH)
    #    print(dictionary_files)
    #    for output in run_cmd_with_realtime_output(['htop']):
    #        print(output)
    try:
        opts, args = getopt(argv[1:], "hb:c:", ["help", "bssid=", "capfile="])
    except GetoptError as err:
        print(str(err))
        exit(1)

    if not opts:
        # If there are no command line arguments
        usage()
        exit(0)
    else:
        # We parse the commmand line arguments
        parameters = {}
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                exit(0)
            elif opt in ("-b", "--bssid"):
                parameters["bssid"] = arg
            elif opt in ("-c", "--capfile"):
                parameters["capfile"] = arg
            else:
                assert False, "Unhandled option!"

        # We check the parameters values
        result, error_msg = check_cmdline_parameters(parameters)
        if not result:
            error(error_msg)
            exit(2)

        for dictionary in list_files_in_path(DICTIONARY_PATH):
            print(dictionary)
