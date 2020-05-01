#!/usr/bin/env python3

import sys
import os
from signal import signal, SIGINT


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


def main():
   if len(sys.argv) == 3:
       print("Please specify <old_dir> <new_dir> <diff_file> path. Exiting...\n")
       sys.exit()

   olddir = sys.argv[1]
   newdir = sys.argv[2]
   diff_file = sys.argv[3]

   if not os.path.isfile(diff_file):
       print("diff_file {} does not exist. Exiting...\n".format(diff_file))
       sys.exit()


   # Create gtaglist file
   with open(diff_file) as fp:
       cnt = 0
       for line in fp:
           cmd = "meld "+ olddir +'/'+line[:-1] + ' ' + newdir + '/' + line[:-1]
           print("\n******  {}\n".format(cmd))
           os.system(cmd)
           cnt += 1


if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)
    main()
