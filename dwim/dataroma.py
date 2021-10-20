#!/usr/bin/env python3

import sys
import os
import argparse
import requests
from bs4 import BeautifulSoup
from datetime import date


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

def main():
   if len(sys.argv) == 1:
       print("Please use the following commands:");
       print("check-date")
       print(" holders path1 ")
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




if __name__ == '__main__':
   main()
