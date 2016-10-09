#!/usr/bin/env python3

from os import scandir, path
from subprocess import PIPE, Popen, DEVNULL
from getopt import getopt, GetoptError
from sys import argv, exit
import time


DICTIONARY_PATH = "/root/dictionaries"
CRACKED_DIR = "/root/cracked"


def list_files_in_path(path_to_list):
    """
    This function returns a sorted list of the files listed from a directory.
    """
    files = [entry.path for entry in scandir(path_to_list) if entry.is_file()]
    return sorted(files)


def run_cmd_with_realtime_output(cmd):
    with Popen(cmd, stdout=PIPE, stderr=PIPE) as process:
        while True:
            line = process.stdout.readline()
            if not line:
                break
            yield line.decode("utf-8").replace("\n", "")


def run_cmd(cmd):
    with Popen(cmd, stdout=DEVNULL, stderr=DEVNULL) as process:
        process.wait()


def build_aircrack_cmd(bssid, cap_file_path, nb_cpu, dictionary_path=None):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    if dictionary_path is not None:
        return [
            'aircrack-ng',
            '-a', '2',
            '-p', str(nb_cpu),
            '-w', dictionary_path,
            '-l', CRACKED_DIR + "/" + "password-" + timestr + ".txt",
            '-b', bssid,
            cap_file_path
        ]
    else:
        return [
            'crunch',
            '2', '8',
            '-f', '/usr/share/crunch/charset.lst', 'mixalpha-numeric-all-space',
            '|',
            'aircrack-ng',
            '-a', '2',
            '-p', str(nb_cpu),
            '-w', '-',
            '-l', CRACKED_DIR + "/" + "password-" + timestr + ".txt",
            '-b', bssid,
            cap_file_path
        ]


def usage():
    print("""
          Usage:
          -h or --help: this help
          -d or --dictionary: use dictionary attack
          -b or --bssid: the BSSID of the wifi network to crack
          -c or --capfile: the path of the *.cap file containing the handshakes to be used.
          """)


def error(msg):
    print("\nError: {}\n".format(msg))


def check_cmdline_parameters(parameters):
    flag = True
    error_msg = ""
    # We check in case capfile is present that it is a real file
    if "capfile" in parameters and not path.isfile(parameters["capfile"]):
        flag = False
        error_msg = "CAP file: \"{}\" is not a valid file or does not exist!".format(parameters["capfile"])
    # We ensure mandatory parameters are set on the command line
    if "capfile" not in parameters or "bssid" not in parameters:
        flag = False
        error_msg = "Both BSSID and cap file must be specified."
    return flag, error_msg


if __name__ == "__main__":
    try:
        opts, args = getopt(argv[1:], "hdb:c:", ["help", "bssid=", "capfile="])
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
            elif opt in ("-d", "--dictionary"):
                parameters["dictionary"] = True
            else:
                assert False, "Unhandled option!"

        # We check the parameters values
        result, error_msg = check_cmdline_parameters(parameters)
        if not result:
            error(error_msg)
            exit(2)

        if "dictionary" in parameters:
            for dictionary in list_files_in_path(DICTIONARY_PATH):
                cmd = build_aircrack_cmd(
                    bssid=parameters["bssid"],
                    cap_file_path=parameters["capfile"],
                    nb_cpu=2,
                    dictionary_path=dictionary
                )
                print("Running command: {}".format(" ".join(cmd)))
                run_cmd(cmd)
        else:
            cmd = build_aircrack_cmd(
                bssid=parameters["bssid"],
                cap_file_path=parameters["capfile"],
                nb_cpu=1
            )
            print("Running command: {}".format(" ".join(cmd)))
            run_cmd(cmd)
