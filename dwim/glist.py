#!/usr/bin/env python3

import sys
import os

def main():
   if len(sys.argv) == 1:
       print("Please specify file path. Exiting...\n")
       sys.exit()

   filepath = sys.argv[1]
   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...\n".format(filepath))
       sys.exit()

   # Remove old tag files
   cleanUpOldTags()

   # Create gtaglist file
   with open(filepath) as fp:
       cnt = 0
       for line in fp:
           print("line {} contents {}".format(cnt, line[:-1]))
           if line[0] == '#':
               print("skip comments")
               continue

           if cnt == 0:
               cmd = "find " + line[:-1] + " -type f -print > ./gtaglist"
           else:
               cmd = "find " + line[:-1] + " -type f -print >> ./gtaglist"
           print("{}\n".format(cmd))
           os.system(cmd)
           cnt += 1

   # Run gtags command
   cmd = "gtags -f ./gtaglist"
   print("{}\n".format(cmd))
   os.system(cmd)


def cleanUpOldTags():
    mycmd = "rm -rf ./gtaglist"
    os.system(mycmd)
    mycmd = "rm -rf ./GPATH"
    os.system(mycmd)
    mycmd = "rm -rf ./GRTAGS"
    os.system(mycmd)
    mycmd = "rm -rf ./GTAGS"
    os.system(mycmd)


if __name__ == '__main__':
   main()
