#!/usr/bin/env python3

import sys
import os
from signal import signal, SIGINT


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

def get_file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def main():
   if len(sys.argv) == 1:
       print("Please specify <diff_file> path. Exiting...\n")
       sys.exit()

   diff_file = sys.argv[1]

   if not os.path.isfile(diff_file):
       print("diff_file {} does not exist. Exiting...\n".format(diff_file))
       sys.exit()

   file_len = get_file_len(diff_file)

   #print("Total {} files".format(file_len))


   # Create gtaglist file
   with open(diff_file) as fp:
       cnt = 0
       for line in fp:
           filepath = os.path.dirname(line[:-1])
           filename = os.path.basename(line[:-1])

           # The -- after cached is forcing the filename to be a file even if it is deleted.
           cmd = "cd " + filepath +"; git difftool -y --cached -- " + filename + "; cd -"
           print( "\n****", cnt+1, "/", file_len, ", ", cmd, "\n");
           os.system(cmd)
           cnt += 1


if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)
    main()
