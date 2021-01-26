#!/usr/bin/env python3

import sys
import os
import numbers
from signal import signal, SIGINT


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

def print_help(num):
    print("Please specify <firstFile> <lineNum> <secFile> <lineNum>. Exiting...\n")
    print("{}".format(num))
    print("This will generate firstFile_num and secondFile_num \n")

def main():
   if len(sys.argv) != 5:
       print_help(1)
       sys.exit()

   firstFile = sys.argv[1]
   firstLineNum = sys.argv[2]
   secFile = sys.argv[3]
   secLineNum = sys.argv[4]

   try:
       val = int(firstLineNum)
   except ValueError:
       print_help(2)
       sys.ext()

   try:
       val = int(secLineNum)
   except ValueError:
       print_help(3)
       sys.ext()

   newFirstFile = firstFile + '_' + firstLineNum;
   #print("\nfrist ******  {}\n".format(newFirstFile))

   newSecFile = secFile + '_' + secLineNum;
   #print("\nsecond ******  {}\n".format(newSecFile))

   # generate first new file
   cmd1 = "tail -n +" + firstLineNum + ' ' + firstFile + ' > ' +  newFirstFile
   #print("\n******  {}\n".format(cmd1))
   os.system(cmd1)

   #generate second new file
   cmd2 = "tail -n +" + secLineNum + ' ' + secFile + ' > ' +  newSecFile
   #print("\n******  {}\n".format(cmd2))
   os.system(cmd2)

   # compare new files
   cmd = "meld "+ newFirstFile + ' ' + newSecFile
   #print("\n******  {}\n".format(cmd))
   os.system(cmd)



if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)
    main()
