#!/usr/bin/env python3

import sys
import os
import argparse


stk1 = {
   "test111" : 1
}

stk2 = {
   "test111" : 1
}

def printSortedStk1():
   sorted_stk = dict(sorted(stk1.items(), key=lambda item: item[1]))
   for x in sorted_stk:
      print(x, stk1[x])

def AddToStk1(nameStr):
   if nameStr in stk1:
      stk1[nameStr] +=1
   else:
      stk1[nameStr] = 1

def printSortedStk2():
   sorted_stk = dict(sorted(stk2.items(), key=lambda item: item[1]))
   for x in sorted_stk:
      print(x, stk2[x])

def printStksDiff():
   sorted_stk1 = dict(sorted(stk1.items(), key=lambda item: item[1]))
   for x in sorted_stk1:
      if not x in stk2:
         print(x, stk1[x], " --> 0")

   sorted_stk2 = dict(sorted(stk2.items(), key=lambda item: item[1]))
   for x in sorted_stk2:
      if not x in stk1:
         print(x, " 0 -->", stk2[x])
      elif stk1[x] != stk2[x]:
         print(x, stk1[x], "->", stk2[x])



def AddToStk2(nameStr):
   if nameStr in stk2:
      stk2[nameStr] +=1
   else:
      stk2[nameStr] = 1



def countNumOfHolderPerSymbol(filepath):
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
              AddToStk1(x)

           cnt += 1

   printSortedStk1()



def countNumOfHolderPerSymbolChange(filepath1, filepath2):
   # Create list for file1
   with open(filepath1) as fp1:
       cnt = 0
       for line in fp1:
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
              AddToStk1(x)
           cnt += 1

   # Create list for file1
   with open(filepath2) as fp2:
       cnt = 0
       for line in fp2:
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
              AddToStk2(x)
           cnt += 1

   printStksDiff()



def main():
   if len(sys.argv) == 1:
       print("Please use the following commands:");
       print(" holders path1 ")
       print(" change path1 path2")
       sys.exit()

   parser = argparse.ArgumentParser()
   parser.add_argument("cmd")
   parser.add_argument("path1")
   parser.add_argument("path2", nargs='?')
   args = parser.parse_args()
   print(args.cmd)
   print(args.path1)
   print(args.path2)
   print("---------------------")

   if args.cmd == "holders":
      countNumOfHolderPerSymbol(args.path1)

   if args.cmd == "change":
      countNumOfHolderPerSymbolChange(args.path1, args.path2)
   sys.exit()


   # Remove old tag files
#   cleanUpOldTags()

   countNumOfHolderPerSymbol(filepath)



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
