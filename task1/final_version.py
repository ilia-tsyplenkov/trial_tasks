#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Execute test task.

Tested on Ubuntu 14.04
Python version 2.7.6 and 2.7.11
"""

import sys
import os
from datetime import datetime

LOG = 'process.log'


def print_progress(cur_step, max_step):
    """Show process progress."""
    sys.stdout.write('\r')
    sys.stdout.write("[%-100s] %d%%" %
                     ('=' * (100 * (cur_step + 1) / max_step),
                      100 * (cur_step + 1) / max_step))
    sys.stdout.flush()


def make_dirs(dir_num):
    """Create directories."""
    has_fails = False
    for x in xrange(1, dir_num + 1):
        if os.system("mkdir dir_%s 2>>%s" % (x, LOG)):
            has_fails = True
        print_progress(x, dir_num + 1)
    if has_fails:
        print("\tFAILED")
        os.system("cat %s" % LOG)
        sys.exit(1)
    else:
        print("\tOK")


def make_files(path, k_size):
    """Create 1000 files with specified size in Kilobytes."""
    amount = 1001
    KILO = 1024
    has_fails = False
    for x in xrange(1, amount):
        f_name = "%s_%s_%s" % (KILO * k_size,
                               datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
                               x)
        f_path = "%s/%s" % (path, f_name)
        if os.system("dd if=/dev/urandom of=%s bs=1k count=%s\
 status=none 2>>%s" %
                     (f_path, k_size, LOG)):
            has_fails = True

        print_progress(x, amount)
    if has_fails:
        print("\tFAILED")
        os.system("cat %s" % LOG)
    else:
        print("\tOK")

if __name__ == '__main__':

    print("Removing dirs and files from the previous launch")
    os.system("rm -rf dir* %s" % LOG)

    print("Creating original directories")
    os.system("cp /dev/null %s" % LOG)
    make_dirs(5)
    for x in xrange(1, 6):
        print("Generating files in ./dir_%s with %sK size" % (x, x))
        os.system("cp /dev/null %s" % LOG)
        make_files("./dir_%s" % x, x)

    print("Creating checksums for created files")
    os.system("cp /dev/null %s" % LOG)
    has_fails = False
    for x in xrange(1, 6):
        if os.system("md5sum ./dir_%s/* 1>dir_%s.chk 2>>%s" % (x, x, LOG)):
            has_fails = True
        print_progress(x, 6)
    if has_fails:
        print("\tFAILED")
        os.system("cat %s" % LOG)
    else:
        print("\tOK")

    copy_dir = "dir_cp"
    if os.system("mkdir %s" % copy_dir):
        print("Cannot create a directory for copying")
        sys.exit(1)

    print("Copying original folders to %s" % copy_dir)
    has_fails = False
    os.system("cp /dev/null %s" % LOG)
    for x in xrange(1, 6):
        if os.system("cp -R ./dir_%s ./%s/ 2>>%s" % (x, copy_dir, LOG)):
            has_fails = True
        print_progress(x, 6)

    if has_fails:
        print("\tFAILED")
        os.system("cat %s" % LOG)
    else:
        print("\tOK")

    move_dir = "dir_mv"
    if os.system("mkdir %s" % move_dir):
        print("Cannot create a directory for moving")
        sys.exit(1)
    print("Moving %s directory to %s" % (copy_dir, move_dir))
    has_fails = False
    os.system("cp /dev/null %s" % LOG)
    if os.system("mv ./%s ./%s/ 2>%s" % (copy_dir, move_dir, LOG)):
        has_fails = True
    print_progress(99, 100)

    if has_fails:
        print("\tFAILED")
        os.system("cat %s" % LOG)
    else:
        print("\tOK")

    print("Removing original directories")
    has_fails = False
    os.system("cp /dev/null %s" % LOG)
    for x in xrange(1, 6):
        if os.system("rm -rf dir_%s 2>>%s" % (x, LOG)):
            has_fails = False
        print_progress(x, 6)

    if has_fails:
        print("\tFAILED")
        os.system("cat %s" % LOG)
    else:
        print("\tOK")

    print("Creating symlinks for directories in ./%s/%s/"
          % (move_dir, copy_dir))
    has_fails = False
    os.system("cp /dev/null %s" % LOG)
    for x in xrange(1, 6):
        if os.system("ln -s ./%s/%s/dir_%s dir_%s 2>>%s" %
                     (move_dir, copy_dir, x, x, LOG)):
            has_fails = True
        print_progress(x, 6)

    if has_fails:
        print("\tFAILED")
        os.system("cat %s" % LOG)
    else:
        print("\tOK")

    print("Checking files")
    has_fails = False
    os.system("cp /dev/null %s" % LOG)
    for x in xrange(1, 6):
        if os.system("md5sum -c --quiet dir_%s.chk 2>>%s" % (x, LOG)):
            has_fails = True
        print_progress(x, 6)

    if has_fails:
        print("\tFAILED")
        os.system("cat %s" % LOG)
    else:
        print("\tOK")

    print("Removing ood files from even folders")
    has_fails = False
    os.system("cp /dev/null %s" % LOG)
    # os.system("rm ./%s/%s/dir_{2,4}/*{1,3,5,7,9}" % (move_dir, copy_dir))
    # This works from bash but doesn't work from Python in Linux
    for x in [2, 4]:
        for root, _, files in os.walk("./%s/%s/dir_%s" %
                                      (move_dir, copy_dir, x)):
            for f in files:
                if f[-1] in "13579":
                    if os.system("rm %s/%s 2>>%s" % (root, f, LOG)):
                        has_fails = True
    print_progress(99, 100)

    if has_fails:
        print("\tFAILED")
        os.system("cat %s" % LOG)
    else:
        print("\tOK")
