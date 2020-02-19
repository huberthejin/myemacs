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
               cmd = 'find -L ${PWD}/' + line[:-1] + ' -type f | egrep -i "\.(c|h|cpp|cc|hpp|enum|bag)$" > ./cscope.files'
           else:
               cmd = 'find -L ${PWD}/' + line[:-1] + ' -type f | egrep -i "\.(c|h|cpp|cc|hpp|enum|bag)$" >> ./cscope.files'
           print("{}\n".format(cmd))
           os.system(cmd)
           cnt += 1

   # Run gtags command
   cmd = "cat ./cscope.files | xargs etags -a"
   print("{}\n".format(cmd))
   os.system(cmd)


def cleanUpOldTags():
    mycmd = "rm -rf ./tags"
    os.system(mycmd)
    mycmd = "rm -rf ./TAGS"
    os.system(mycmd)
    mycmd = "rm -rf ./scope.files"
    os.system(mycmd)
    mycmd = "rm -rf ./cscope.out"
    os.system(mycmd)


if __name__ == '__main__':
   main()
