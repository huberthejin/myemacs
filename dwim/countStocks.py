#!/usr/bin/env python3

import sys
import os


stk = {
   "test" : 1,
   "test1" : 2
}

def printSortedStk():
   sorted_stk = dict(sorted(stk.items(), key=lambda item: item[1]))
   for x in sorted_stk:
      print(x, stk[x])

def AddToStk(nameStr):
   if nameStr in stk:
      stk[nameStr] +=1
   else:
      stk[nameStr] = 1

def main():
   if len(sys.argv) == 1:
       print("Please specify file path. Exiting...\n")
       sys.exit()

   filepath = sys.argv[1]
   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...\n".format(filepath))
       sys.exit()

   # Remove old tag files
#   cleanUpOldTags()

   # Create gtaglist file
   with open(filepath) as fp:
       cnt = 0
       for line in fp:
           #print("1--{}".format(line[:-1]))
           offset = line.find('$')
           line1 = line[offset:-1]
           #print("{}".format(line1[:]))
           # remove the first spaces
           offset2 = line1.find(' ')
           line2 = line1[offset2:]
           #print("{}".format(line2[:]))
           line3 = line2.lstrip()
           #print("2--{}".format(line3[:]))
           # remove the second spaces
           offset3 = line3.find('\t')
           #print(offset3)
           line4 = line3[offset3:]
           #print("{}".format(line4[:]))
           line5 = line4.lstrip()
           #print("{}".format(line5[:]))
           # remove the third spaces
           offset6 = line5.find('\t')
           #print(offset6)
           line6 = line5[offset6:]
           #print("{}".format(line6[:]))
           line7 = line6.lstrip()
           #print("{}".format(line7[:]))
           listOfWords = line7.split()
           for x in listOfWords:
              AddToStk(x)

           cnt += 1

   printSortedStk()



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
