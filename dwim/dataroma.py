#!/usr/bin/env python3

import sys
import os
import argparse
import requests
from bs4 import BeautifulSoup
from datetime import date

stk1 = {
   "test111" : 1
}


def AddToStk1(nameStr):
   if nameStr in stk1:
      stk1[nameStr] +=1
   else:
      stk1[nameStr] = 1

def printSortedStk1():
   sorted_stk = dict(sorted(stk1.items(), key=lambda item: item[1]))
   for x in sorted_stk:
      print(x, stk1[x])

def get_file_suffix():
   today = date.today()
   suffix = today.strftime("%y%d%m")
   return suffix



def get_company_info(url):
   reqs = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv)"})
   soup = BeautifulSoup(reqs.text, 'html.parser')

   name = soup.find_all('div',id='f_name')[0].text
   offset = name.find('\n')
   name1 = name[0:offset]
   releaseDate = soup.find_all('p',id='p2')[0].find_all('span')[1].text
   print(releaseDate, " : ", name1)

def check_date():
   weburl = "https://dataroma.com"
   url = "https://dataroma.com/m/managers.php"
   reqs = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv)"})
   soup = BeautifulSoup(reqs.text, 'html.parser')

   tbody = soup.find_all('tbody')
   for entry in tbody[0].find_all('tr'):
      link = entry.find('a').get('href')
      complink = weburl+link
      get_company_info(complink)

def check_holders():
   url = "https://dataroma.com/m/managers.php"
   reqs = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv)"})
   soup = BeautifulSoup(reqs.text, 'html.parser')

   tbody = soup.find_all('tbody')
   for entry in tbody[0].find_all('tr'):
      companyStr=""
      for companyName in entry.find_all('td', class_='man'):
         name1 = companyName.find('a').text
         offset1 = name1.find(' ')
         offset2 = name1.find(' ', offset1+1)  # find second occurence
         #print(offset1, offset2)
         name2 = name1[0:offset2]
         companyStr = companyStr +name2
         #print(name2)
      for symbols in entry.find_all('td', class_='sym'):
         sym1 = symbols.find('a').text
         companyStr = companyStr + ":"+sym1
         #print(sym1)
      print(companyStr)

def count_symbols():
   url = "https://dataroma.com/m/managers.php"
   reqs = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv)"})
   soup = BeautifulSoup(reqs.text, 'html.parser')

   tbody = soup.find_all('tbody')
   for entry in tbody[0].find_all('tr'):
      companyStr=""
      for companyName in entry.find_all('td', class_='man'):
         name1 = companyName.find('a').text
         offset1 = name1.find(' ')
         offset2 = name1.find(' ', offset1+1)  # find second occurence
         #print(offset1, offset2)
         name2 = name1[0:offset2]
         companyStr = companyStr +name2
         #print(name2)
      for symbols in entry.find_all('td', class_='sym'):
         sym1 = symbols.find('a').text
         AddToStk1(sym1)
      printSortedStk1()

def main():
   if len(sys.argv) == 1:
       print("Please use the following commands:");
       print(" check-date -- print the submit date")
       print(" holders -- print the whole holder-symbols table")
       print(" count-symbols -- count how many holders for a symbol")
       print(" change path1 path2")
       sys.exit()

   parser = argparse.ArgumentParser()
   parser.add_argument("cmd")
   parser.add_argument("path1", nargs='?')
   parser.add_argument("path2", nargs='?')
   args = parser.parse_args()
   print(args.cmd)
   print(args.path1)
   print(args.path2)
   print("---------------------")


   sfx = get_file_suffix()
   print(sfx)

   if args.cmd == "check-date":
      check_date()
   elif args.cmd == "holders":
      check_holders()
   elif args.cmd == "count-symbols":
      count_symbols()






if __name__ == '__main__':
   main()
