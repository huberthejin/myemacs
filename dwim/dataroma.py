#!/usr/bin/env python3

import sys
import os
import argparse
import requests
from bs4 import BeautifulSoup
from datetime import date
import json
import time
import gc
import operator
import re
import numpy_financial as npf
import traceback

#debug_level: 0 - nodebug
#             1 - most important debug
#             2 - normal debug
debug_level = 1

wait_sec = 2

stk1 = {}


def mydbg1(*arg):
   if debug_level >= 1:
      print(arg)

def mydbg2(*arg):
   if debug_level >= 2:
      print(arg)

def AddAndIncreateOneToStk1(nameStr):
   if nameStr in stk1:
      stk1[nameStr] +=1
   else:
      stk1[nameStr] = 1

def AddPairToStk1(nameStr, val):
   if nameStr not in stk1:
      stk1[nameStr] = val

def printSortedStk1():
   sorted_stk = dict(sorted(stk1.items(), key=lambda item: item[1]))
   for x in sorted_stk:
      print(x, stk1[x])

def printSortedStk2():
   for x in stk1:
      print(x, stk1[x], type(x), type(stk1[x]))

def get_file_suffix():
   today = date.today()
   suffix = today.strftime("%y%m%d")
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
         AddAndIncreateOneToStk1(sym1)
      printSortedStk1()




#### acqm

tick_count = 0

def convert_num_to_Million(numStr):
   mydbg2("numStr", numStr)
   if "B" in numStr:
      numInBill = numStr[:-1]
      numInMill = float(numInBill) *  1000
   elif "T" in numStr:
      numInBill = numStr[:-1]
      numInMill = float(numInBill) *  1000000
   elif "M" in numStr:
      numInMill = float(numStr[:-1])
   elif "-" in numStr:
      numInMill = float(0)
   elif "N/A" in numStr:
      numInMill = float(0)
   else:
      if "(" in numStr:
         numInMill = float(numStr.replace('(','').replace(')','').replace(',','')) * -1
      else:
         numInMill = float(numStr.replace(',',''))

   mydbg2("numInmill", numInMill)
   return numInMill

def convert_num_to_unit(numStr):
   mydbg2("numStr", numStr)
   if "k" in numStr:
      numNoK = numStr[:-1]
      numInUnit = float(numNoK) *  1000
   elif "N/A" in numStr:
      numInUnit = float(0)
   elif "-" in numStr:
      numInUnit = float(0)
   else:
      if "(" in numStr:
         numInUnit = float(numStr.replace('(','').replace(')','').replace(',','').replace('$','')) * -1
      else:
         numInUnit = float(numStr.replace(',','').replace('$',''))

   mydbg2("numInUnit", numInUnit)
   return numInUnit



def old_count_acqm(tick, outfp):
   # Initialize the variables.
   global tick_count
   tick_count+=1
   market_cap = 0
   total_cash = 0
   total_debt = 0

   tot_rev = 0
   cost_of_rev = 0
   sga = 0
   depreciation = 0

   market_cap_str = total_cash_str = total_debt_str = total_revenues_str = \
      cost_of_revenue_str = sga_str = depreciation_str = "0"

   # seekingalpha -- cashflow
   sc_cookie = "machine_cookie=3043358740123; LAST_VISITED_PAGE=%7B%22pathname%22%3A%22https%3A%2F%2Fseekingalpha.com%2Fsymbol%2FFDX%22%2C%22pageKey%22%3A%226b081633-5704-43ac-9525-a3499d875a2b%22%7D; session_id=359b95c6-13c3-40e8-9324-4fd9c47e887c; __tbc=%7Bkpbx%7DF-inOuBb7onTMxBtnfKoRHwjL633E-knaQ8qJ7ls9j_5I7llaR0ChqeafNTeDBMKDP83pVbTLEpQOKVBrGjfk0lx2FmQlDd2_-RRoBLzAu8; __pat=-18000000; __pvi=%7B%22id%22%3A%22v-2022-01-03-21-57-15-368-FmMmlTqEHX4rubJq-eab022edb31c73ccc1a75a24e3f894de%22%2C%22domain%22%3A%22.seekingalpha.com%22%2C%22time%22%3A1641265082244%7D; xbc=%7Bkpbx%7D17GMJyZl-q9yJCCRqU_rdWwnsWWughOqJJRQgdIgu-VONLUUyaK8eful4YGDryK2fIzndfJqA0nn9dycxA5-nymOmlIxhG0ukFUwt3SxeYmnhdUNZp9rM7EF2H0XwkaeGQAkExim4a1C90mGcz1LZvvW2EYCLl50udCLO_YdQK0oElIAPWxEhQoqBNA49x7vBhBFYRCKLb61f98jWrMHxrb98zYwqti3S_2wf2m8mGM; sailthru_pageviews=1; prism_25946650=a421fb3d-13dc-4ec1-956f-f91cda1d154a; _gcl_au=1.1.1484803624.1641265037; pxcts=07268bf0-6d0a-11ec-88e8-63504f71bccc; _pxvid=07261b94-6d0a-11ec-b560-796a69584a50; _pxde=de4986f2d80b13ced84e2d17c7ba4eec4d6d1de5d04d596a6f0e5d013305b3d9:eyJ0aW1lc3RhbXAiOjE2NDEyNjU4MDE1MzMsImZfa2IiOjB9; _ga=GA1.2.226011785.1641265038; _gid=GA1.2.1758972647.1641265038; _fbp=fb.1.1641265038078.1805296611; ga_clientid=226011785.1641265038; _uetsid=06b6f5106d0a11ecbf3247c0bc90a86a; _uetvid=06b6e0006d0a11eca0f049c77dd6bd9e; _px2=eyJ1IjoiMWRiNjI2YTAtNmQwYS0xMWVjLTg5ZWYtNDcwYTkwOTRjMmU3IiwidiI6IjA3MjYxYjk0LTZkMGEtMTFlYy1iNTYwLTc5NmE2OTU4NGE1MCIsInQiOjE2NDEyNjYzMDE1MzMsImgiOiI3ZTFjNDdiODY2NDdiMzQ4NjFkZTMwZjNhYmFjZDJiNDJkZWU3MzJkMTAwNjI3YjM3YzBmMTNkMTI0NzU5NjczIn0=; _px=SZCeewKAxfbQbjnTVj1VeUni5+ipCsKKziIbKcFQgaeYdA6xe77lIlQI5zeLbX+ZS7dW5xj0Udxmd95QOXNjoQ==:1000:aD6fdWqfOT09QNSoaq7WOuQKUMicSnR5X35/rdS/FJpNgold02wR60nMo4dWZcql0c2QgzLIoHqgodh7r2dsXO+GzyIbNcDmPfrBvFzuN0kMajO9fMcuJbIuCBk+pOmp5WUSww35/Jwb3dPrtP8mlhj17ELYzfgdzv7vEspB9k277qkPawmHM38KtuNMq/buHloH609iJ7NlfeXZlFTYy9LMD9HIhIinLVWQ32YaLox2WcKavxxKLmCOeKnuAibi88pYlxLrLqejK2ZKNBdKUA==; h_px=1"

   sc_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0", \
                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", \
                 "Accept-Encoding": "gzip, deflate, br", \
                 "Accept-Language": "en-US,en;q=0.5", \
                 "Cookie": sc_cookie}
   sk_url_cash = "https://seekingalpha.com/symbol/" + tick + "/financials-data?period_type=annual&statement_type=cash-flow-statement&order_type=latest_right&is_pro=false"
   mydbg1(sk_url_cash)
   sc_reqs = requests.get(sk_url_cash, headers=sc_headers)
   #print(sc_reqs.text)
   dataCash = json.loads(sc_reqs.text)
   # I call it : table, section, entry, column
   # dataCash[table][section][entry][column]
   sc_col_len = len(dataCash["data"][1][0])
   for entry_idx in range(len(dataCash["data"][1])):
      if (dataCash["data"][1][entry_idx][0]["value"] == "Depreciation & Amortization, Total"):
         if (dataCash["data"][1][entry_idx][sc_col_len-1]["name"] == "TTM"):
            depreciation_str = dataCash["data"][1][entry_idx][sc_col_len-1]["value"]
            depreciation = convert_num_to_Million(depreciation_str)
            print(depreciation_str, depreciation)
         if( depreciation == 0.0):
            print(tick_count,tick, 0.0)
            return tick, float(0.0)

         mydbg1("depreciation", depreciation)


   # yahoo
   tick1 = tick.replace(".", "-")
   yaurl= "https://finance.yahoo.com/quote/" + tick1 + "/key-statistics?p=" + tick1
   mydbg1(yaurl)
   yareqs = requests.get(yaurl, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv)"})
   ya_soup = BeautifulSoup(yareqs.text, 'html.parser')

   ya_tbody = ya_soup.find_all('tbody')
   for tbdy in ya_tbody:
      for entry in tbdy.find_all('tr'):
         mytd = entry.find_all('td')
         spanStr = mytd[0].find('span').text
         if "Market Cap (intraday)" in spanStr:
            market_cap_str = mytd[1].text
            market_cap = convert_num_to_Million(market_cap_str)
            mydbg1("market_cap", market_cap)
         elif "Total Cash" in spanStr:
            if "Total Cash Per Share" not in spanStr:
               total_cash_str = mytd[1].text
               total_cash = convert_num_to_Million(total_cash_str)
               mydbg1("total_cash", total_cash)
         elif "Total Debt" in spanStr:
            if "Total Debt/Equity" not in spanStr:
               total_debt_str = mytd[1].text
               total_debt = convert_num_to_Million(total_debt_str)
               mydbg1("total_debt", total_debt)
   enterprice_value = market_cap - total_cash + total_debt
   mydbg1("enterprice_value", enterprice_value)

   time.sleep(wait_sec)

   # seekingalpha -- income
   sk_url_income = "https://seekingalpha.com/symbol/" + tick + "/financials-data?period_type=annual&statement_type=income-statement&order_type=latest_right&is_pro=false"
   mydbg1(sk_url_income)
   #si_reqs = requests.get(sk_url_income, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"})
   si_reqs = requests.get(sk_url_income, headers=sc_headers)
   #print(si_reqs.text)
   dataIncm = json.loads(si_reqs.text)
   si_col_len = len(dataIncm["data"][0][1])
   print( si_col_len, "****")
   for list1 in dataIncm["data"]:
      for sec_entry in list1:
         if (sec_entry[0]["value"] == "Total Revenues"):
            if (sec_entry[si_col_len-1]["name"] == "TTM"):
               total_revenues_str = sec_entry[si_col_len-1]["value"]
            tot_rev = convert_num_to_Million(total_revenues_str)
            mydbg1("tot_rev", tot_rev)

         if (sec_entry[0]["value"] == "Cost Of Revenues"):
            if (dataIncm["data"][0][3][si_col_len-1]["name"] == "TTM"):
               cost_of_revenue_str = dataIncm["data"][0][3][si_col_len-1]["value"]
            cost_of_rev = convert_num_to_Million(cost_of_revenue_str)
            mydbg1("cost_of_rev", cost_of_rev)
         if (sec_entry[0]["value"] == "Selling General & Admin Expenses"):
            if (dataIncm["data"][1][0][si_col_len-1]["name"] == "TTM"):
               sga_str = dataIncm["data"][1][0][si_col_len-1]["value"]
            sga = convert_num_to_Million(sga_str)
            mydbg1("sga", sga)

   operating_earnings = tot_rev - cost_of_rev - sga - depreciation

   acq_multple = enterprice_value/operating_earnings
   acq_multple_fmt = "{:.6f}".format(acq_multple)
   print(tick_count, tick, acq_multple_fmt,market_cap, total_cash, total_debt, 0, 0, enterprice_value,tot_rev, cost_of_rev, sga, depreciation, operating_earnings)
   print("       ", market_cap_str, total_cash_str, total_debt_str, total_revenues_str, cost_of_revenue_str, sga_str, depreciation_str)
   numList1 = ["#", str(tick_count), str(tick), str(acq_multple_fmt), str(market_cap), str(total_cash), str(total_debt), "0", "0", str(enterprice_value), str(tot_rev), str(cost_of_rev), str(sga), str(depreciation), str(operating_earnings)]
   numList1_str = ', '.join(numList1)+"\n"
   outfp.write(numList1_str)
   numList2 = ["#       ", market_cap_str, total_cash_str, total_debt_str, total_revenues_str, cost_of_revenue_str, sga_str, depreciation_str]
   numList2_str = ', '.join(numList2)+"\n"
   outfp.write(numList2_str)

   # garbage collect
   del ya_soup
   gc.collect()

   return tick, float(acq_multple_fmt)



def count_acqm1():
   with open('/home/hjin/test/aapl.json') as f:
      dataIncm = json.load(f)

      if (dataIncm["data"][0][2][0]["value"] == "Total Revenues") and \
         (dataIncm["data"][0][2][11]["name"] == "TTM"):
         print(dataIncm["data"][0][2][11]["value"])
      if (dataIncm["data"][0][3][0]["value"] == "Cost Of Revenues") and \
         (dataIncm["data"][0][3][11]["name"] == "TTM"):
         print(dataIncm["data"][0][3][11]["value"])
      if (dataIncm["data"][1][0][0]["value"] == "Selling General & Admin Expenses") and \
         (dataIncm["data"][1][0][11]["name"] == "TTM"):
         print(dataIncm["data"][1][0][11]["value"])

   with open('/home/hjin/test/aapl-cash.json') as f1:
      dataCash = json.load(f1)

   if (dataCash["data"][1][2][0]["value"] == "Depreciation & Amortization, Total") and \
      (dataCash["data"][1][2][11]["name"] == "TTM"):
      print(dataCash["data"][1][2][11]["value"])

   print(dataCash["data"][1][2][0]["value"])
   print(dataCash["data"][1][2][11]["name"])


def old_count_all_acqms():
   outputfile = "/home/hjin/test/acqm_results"
   outfp = open(outputfile, 'a+')
   filepath = "/home/hjin/test/all-ticks"
   with open(filepath) as fp:
       cnt = 0
       for line in fp:
          tick = line[:-1]
          mydbg2(tick, "--------")
          result = old_count_acqm(tick, outfp)
          combinStr = result[0] + ", "+ str(result[1])+ "\n"
          outfp.write(combinStr)
          outfp.flush()
          AddPairToStk1(result[0], result[1])
          time.sleep(wait_sec)

   print("---------------------")
   printSortedStk2()
   print("=====================")
   printSortedStk1()

##### trailing PEs

def old_get_tpe_from_ya(tick, outfp):
   # Initialize the variables.
   global tick_count
   tick_count+=1

   trailing_pe = 0
   market_cap = 0
   trailing_pe_str = "0"
   market_cap_str = "0"
   ret_val = 0


   # yahoo
   tick1 = tick.replace(".", "-")
   yaurl= "https://finance.yahoo.com/quote/" + tick1 + "/key-statistics?p=" + tick1
   mydbg1(yaurl)
   yareqs = requests.get(yaurl, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv)"})
   ya_soup = BeautifulSoup(yareqs.text, 'html.parser')

   ya_tbody = ya_soup.find_all('tbody')
   for tbdy in ya_tbody:
      for entry in tbdy.find_all('tr'):
         mytd = entry.find_all('td')
         spanStr = mytd[0].find('span').text
         if "Market Cap (intraday)" in spanStr:
            market_cap_str = mytd[1].text
            market_cap = convert_num_to_Million(market_cap_str)
            mydbg1("market_cap", market_cap)
         if "Trailing P/E" in spanStr:
            trailing_pe_str = mytd[1].text
            trailing_pe = convert_num_to_unit(trailing_pe_str)
            mydbg1("trailing_pe", trailing_pe)

   # debug code
   if market_cap == 0:
      ret_val = 1
      #print(yareqs.text)

   print(tick_count, tick, trailing_pe, trailing_pe_str)
   numList1 = ["#", str(tick_count), str(tick), str(trailing_pe), str(trailing_pe_str)]
   numList1_str = ', '.join(numList1)+"\n"
   outfp.write(numList1_str)

   # garbage collect
   del ya_soup
   del yareqs
   del yaurl
   del ya_tbody

   return ret_val, tick, float(trailing_pe)



def old_count_all_trailing_pe():
   outputfile = "/home/hjin/test/tpe_results"
   outfp = open(outputfile, 'a+')
   filepath = "/home/hjin/test/all-ticks"
   with open(filepath) as fp:
       cnt = 0
       for line in fp:
          tick = line[:-1]
          mydbg2(tick, "--------")

          while True:
             result = old_get_tpe_from_ya(tick, outfp)
             if result[0] != 0:
                # wait for the server to retrieve the data.
                time.sleep(20)
             else:
                break

          combinStr = result[1] + ", "+ str(result[2])+ "\n"
          outfp.write(combinStr)
          outfp.flush()
          AddPairToStk1(result[1], result[2])
          gc.collect()
          time.sleep(wait_sec)

   print("---------------------")
   printSortedStk2()
   print("=====================")
   printSortedStk1()

## save to json file

def get_dict_values_from_yh(tick, company):
   # Initialize the variables.
   global tick_count
   ret_val = 0
   tick_count+=1

   market_cap = 0
   trailing_pe = 0
   total_cash = 0
   total_debt = 0
   forward_pe = 0
   ps_ratio = 0
   pb_ratio = 0
   share_num = 0
   share_num_imp = 0
   close_price = 0

   market_cap_str = "0"
   trailing_pe_str = "0"
   total_cash_str = "0"
   total_debt_str = "0"
   forward_pe_str = "0"
   ps_ratio_str = "0"
   pb_ratio_str = "0"
   share_num_str = "0"
   share_num_imp_str = "0"
   close_price_str = "0"

   # yahoo
   tick1 = tick.replace(".", "-")
   yaurl= "https://finance.yahoo.com/quote/" + tick1 + "/key-statistics?p=" + tick1
   mydbg1(yaurl)
   yareqs = requests.get(yaurl, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv)"})
   ya_soup = BeautifulSoup(yareqs.text, 'html.parser')
   ya_tbody = ya_soup.find_all('tbody')
   for tbdy in ya_tbody:
      for entry in tbdy.find_all('tr'):
         mytd = entry.find_all('td')
         spanStr = mytd[0].find('span').text
         if "Market Cap (intraday)" in spanStr:
            market_cap_str = mytd[1].text
            market_cap = convert_num_to_Million(market_cap_str)
            mydbg1("market_cap", market_cap)
         elif "Trailing P/E" in spanStr:
            trailing_pe_str = mytd[1].text
            trailing_pe = convert_num_to_unit(trailing_pe_str)
            mydbg1("trailing_pe", trailing_pe)
         elif "Total Cash" in spanStr:
            if "Total Cash Per Share" not in spanStr:
               total_cash_str = mytd[1].text
               total_cash = convert_num_to_Million(total_cash_str)
               mydbg1("total_cash", total_cash)
         elif "Total Debt" in spanStr:
            if "Total Debt/Equity" not in spanStr:
               total_debt_str = mytd[1].text
               total_debt = convert_num_to_Million(total_debt_str)
               mydbg1("total_debt", total_debt)
         elif "Forward P/E" in spanStr:
            forward_pe_str = mytd[1].text
            forward_pe = convert_num_to_unit(forward_pe_str)
            mydbg1("forward_pe", forward_pe)
         elif "Price/Sales" in spanStr:
            ps_ratio_str = mytd[1].text
            ps_ratio = convert_num_to_unit(ps_ratio_str)
            mydbg1("ps_ratio", ps_ratio)
         elif "Price/Book" in spanStr:
            pb_ratio_str = mytd[1].text
            pb_ratio = convert_num_to_unit(pb_ratio_str)
            mydbg1("pb_ratio", pb_ratio)
         elif "Shares Outstanding" == spanStr:
            share_num_str = mytd[1].text
            share_num = convert_num_to_Million(share_num_str)
            mydbg1("share_num", share_num)
         elif "Implied Shares Outstanding" == spanStr:
            share_num_imp_str = mytd[1].text
            share_num_imp = convert_num_to_Million(share_num_imp_str)
            mydbg1("share_num_imp", share_num_imp)

   # debug code
   if market_cap == 0:
      ret_val = 1
      #print(yareqs.text)

   company["trailing_pe"] = trailing_pe
   company["market_cap"] = market_cap
   company["total_cash"] = total_cash
   company["total_debt"] = total_debt
   company["forward_pe"] = forward_pe
   company["ps_ratio"] = ps_ratio
   company["pb_ratio"] = pb_ratio
   if share_num_imp != 0:
      company["share_num"] = share_num_imp
   else:
      company["share_num"] = share_num

   yaurl2= "https://finance.yahoo.com/quote/" + tick1 + "/history?p=" + tick1
   mydbg1(yaurl2)
   yareqs2 = requests.get(yaurl2, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv)"})
   ya_soup2 = BeautifulSoup(yareqs2.text, 'html.parser')
   ya_tbody2 = ya_soup2.find_all('tbody')
   entry2 = ya_tbody2[0].find('tr')
   mytds = entry2.find_all('td')
   close_price_str = mytds[4].find('span').text
   close_price = convert_num_to_Million(close_price_str)
   mydbg1("close_price", close_price)
   company["close_price"] = close_price


   # garbage collect
   del ya_soup
   del yareqs
   del yaurl
   del ya_tbody
   del ya_soup2
   del yareqs2
   del yaurl2
   del ya_tbody2

   return ret_val, company

def do_save_yh_to_json_file():
   # load partial data from existing file
   if os.path.exists("./yh/yh_data") and \
      os.path.getsize("./yh/yh_data") != 0:
      infile = "./yh/yh_data"
      infp = open(infile)
      companylist = json.load(infp)
   else:
      # Get empty dict if no file exits
      companylist = dict()

   outputfile = "./yh/yh_data"
   outfp = open(outputfile, 'w+')
   filepath = "../all-ticks"
   company = dict()

   with open(filepath) as fp:
       cnt = 0
       for line in fp:
          tick = line[:-1]
          mydbg2(tick, "--------")

          while True:
             # company is changed in the called function
             result = get_dict_values_from_yh(tick, company)
             if result[0] != 0:
                # wait for the server to retrieve the data.
                time.sleep(20)
             else:
                break

          companylist[tick] = company
          gc.collect()
          time.sleep(wait_sec)

   outfp.write(json.dumps(companylist, indent=4, sort_keys=True))


# The idx is 1 for TTM, 2 for this year, ...
def get_dict_values_from_ska(tick, company, idx):
   # Initialize the variables.
   global tick_count
   tick_count+=1
   ret_val = 0

   mydbg1(tick_count, tick)

   tot_rev = 0
   cost_of_rev = 0
   sga = 0
   net_income = 0
   income_tax = 0
   depreciation = 0
   receivable_chg = 0
   payable_chg = 0
   capexp = 0
   sale_property = 0
   cash_from_operations = 0


   total_revenues_str = "0"
   cost_of_revenue_str = "0"
   sga_str = "0"
   net_income_str = "0"
   income_tax_str = "0"
   depreciation_str = "0"
   receivable_chg_str = "0"
   payable_chg_str = "0"
   capexp_str = "0"
   sale_property_str = "0"
   cash_from_operations_str = "0"

   # seekingalpha -- cashflow
   # firefox, income-statement/GET
   sc_cookie = "machine_cookie=8619160637441; LAST_VISITED_PAGE=%7B%22pathname%22%3A%22https%3A%2F%2Fseekingalpha.com%2Fsymbol%2FASML%22%2C%22pageKey%22%3A%22301f9740-c80d-4722-96a9-f19475ce35bc%22%7D; session_id=45d1209c-24a1-4666-80eb-2113debc170b; __tbc=%7Bkpbx%7Dp7BENTc0p2VRd8xZTpU9kRJIo8GDGMUP_ts6Hv_qVvUk5DcMrlOg5x2g5PL1cC2AbN6dfixX1ezw-Q5Lx5MiFcC08N3DeiGmrIQtcfXxyh4; __pat=-18000000; __pvi=%7B%22id%22%3A%22v-2022-01-15-21-20-54-660-hZiPMtA3DcNbiy1k-fff2441e8a69239afb4222daac45a33b%22%2C%22domain%22%3A%22.seekingalpha.com%22%2C%22time%22%3A1642299670964%7D; xbc=%7Bkpbx%7D17GMJyZl-q9yJCCRqU_rdWwnsWWughOqJJRQgdIgu-VONLUUyaK8eful4YGDryK2fIzndfJqA0nn9dycxA5-n_mlYAm6eHG7Pq1LZgIR4zWUkv2RKy3rJd9Qsk8cHLPlvjhuRmx_t1ZjQa7IsxW7_xvU1RNUaiZg9avridxRXM4oElIAPWxEhQoqBNA49x7vBhBFYRCKLb61f98jWrMHxrb98zYwqti3S_2wf2m8mGM; sailthru_pageviews=1; _gcl_au=1.1.1700814452.1642299656; prism_25946650=38bdf2fc-70a6-4fd0-a066-3067e88d9be4; _ga=GA1.2.672133721.1642299657; _gid=GA1.2.603671983.1642299657; _gat_UA-142576245-4=1; _dc_gtm_UA-142576245-1=1; _clck=ressaa|1|ey6|0; _px2=eyJ1IjoiZjc5MDQ3ZTAtNzY3Mi0xMWVjLTkwMDEtNjdlNTBjOTc0NTdiIiwidiI6ImYwNjE4YzE3LTc2NzItMTFlYy04MTQ0LTY1NjU1NjVhNjY0MyIsInQiOjE2NDIzMDAxNzE3NjEsImgiOiIwOGU4OGMyMTYzOTNjMjczODMwOWJlZDhmYmI2ZTY4MjM0NmI4NWUzM2Y1MjJhMGQzMzliOWM1OTJkNzYzNGM5In0=; _px=e9p/0sY9pHFjEkq+Sxp/l/4bdx1wfhhW5ds3GGYPHWVKofEt2Ioh9EKyqXebD2ODmaO5sFTH9EEW+fgGZnshVA==:1000:e5nO6dmUksp1IFMsH1dx5keCeeSYwN+aTV5xOWJNrmGIQ6RmYCQ4Yabi03fEGOCGVp50LJO2KpEEk73EzD9L34SeQg2D3zYdMLklBGMdpm2fTggRZUcPN8eQj0OfHw8VRnJykE1HqXEkd+iY5awmF5ADzyjPotmdKc/vT4LXwSoke+pIgYRGprNs3tauaO7SNrQ8nCXolZg70PRF+/h5wiV7QLIgZ2VOjilF/hpij0m4EuQhKOMJm9RoXjVP8dWhe1ru/5p30o6vAl2ambbCtQ==; pxcts=f061e6e0-7672-11ec-b777-31aa06aaba58; _pxvid=f0618c17-7672-11ec-8144-6565565a6643; _pxde=9a85660e07caa29e651a00d07cb2ac2a6031a5e6d3c0fe21d182ab991e3d1c52:eyJ0aW1lc3RhbXAiOjE2NDIyOTk2NzE3NjEsImZfa2IiOjB9; _clsk=e0nd9v|1642299671456|3|0|e.clarity.ms/collect; _fbp=fb.1.1642299657556.1756000643; _uetsid=efc3c5b0767211ec8eecb745aa9ac1ea; _uetvid=efc3dc60767211ecbd940db587b46b5d; ga_clientid=672133721.1642299657; h_px=1; __adblocker=false"

   sc_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0", \
                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", \
                 "Accept-Encoding": "gzip, deflate, br", \
                 "Accept-Language": "en-US,en;q=0.5", \
                 "Cookie": sc_cookie}

   rev_list = []
   grosspft_list = []
   eps_list = []
   bvps_list = []
   fcf_list = []

   # seekingalpha -- income
   sk_url_income = "https://seekingalpha.com/symbol/" + tick + "/financials-data?period_type=annual&statement_type=income-statement&order_type=latest_right&is_pro=false"
   mydbg1(sk_url_income)
   #si_reqs = requests.get(sk_url_income, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"})
   si_reqs = requests.get(sk_url_income, headers=sc_headers)
   if "been denied" in si_reqs.text:
      ret_val = 1
      print("It is denied ****")
      return ret_val, company
   #print(si_reqs.text)
   dataIncm = json.loads(si_reqs.text)
   print(len(dataIncm["data"]))
   print(len(dataIncm["data"][0]))
   if len(dataIncm["data"]) == 0 or len(dataIncm["data"][0]) == 0 or len(dataIncm["data"][0][0]) == 0:
      ret_val = 2
      print("It is nodata ***")
      return ret_val, company
   si_col_len = len(dataIncm["data"][0][1])
   for list1 in dataIncm["data"]:
      for sec_entry in list1:
         if (sec_entry[0]["value"] == "Total Revenues"):
            for lidx in range(2, si_col_len):
               if "svg" not in sec_entry[lidx]["value"]:
                  rev_lstr = sec_entry[lidx]["value"]
                  rev_list.append(convert_num_to_Million(rev_lstr))
         if (sec_entry[0]["value"] == "Gross Profit"):
            for lidx in range(2, si_col_len):
               if "svg" not in sec_entry[lidx]["value"]:
                  grosspft_lstr = sec_entry[lidx]["value"]
                  grosspft_list.append(convert_num_to_Million(grosspft_lstr))
         if (sec_entry[0]["value"] == "Diluted EPS"):
            for lidx in range(2, si_col_len):
               if "svg" not in sec_entry[lidx]["value"]:
                  eps_lstr = sec_entry[lidx]["value"]
                  eps_list.append(convert_num_to_unit(eps_lstr))

         if (sec_entry[0]["value"] == "Total Revenues"):
            if (sec_entry[si_col_len-1]["name"] == "TTM"):
               total_revenues_str = sec_entry[si_col_len-idx]["value"]
            tot_rev = convert_num_to_Million(total_revenues_str)
            mydbg1("tot_rev", tot_rev)

         if (sec_entry[0]["value"] == "Cost Of Revenues"):
            if (sec_entry[si_col_len-1]["name"] == "TTM"):
               cost_of_revenue_str = sec_entry[si_col_len-idx]["value"]
            cost_of_rev = convert_num_to_Million(cost_of_revenue_str)
            mydbg1("cost_of_rev", cost_of_rev)
         if (sec_entry[0]["value"] == "Selling General & Admin Expenses"):
            if (sec_entry[si_col_len-1]["name"] == "TTM"):
               sga_str = sec_entry[si_col_len-idx]["value"]
            sga = convert_num_to_Million(sga_str)
            mydbg1("sga", sga)
         if (sec_entry[0]["value"] == "Net Income"):
            if (sec_entry[si_col_len-1]["name"] == "TTM"):
               net_income_str = sec_entry[si_col_len-idx]["value"]
            net_income = convert_num_to_Million(net_income_str)
            mydbg1("net_income", net_income)
         if (sec_entry[0]["value"] == "Income Tax Expense"):
            if (sec_entry[si_col_len-1]["name"] == "TTM"):
               income_tax_str = sec_entry[si_col_len-idx]["value"]
            income_tax = convert_num_to_Million(income_tax_str)
            mydbg1("income_tax", income_tax)

   company["rev_list"] = rev_list
   company["grosspft_list"] = grosspft_list
   company["eps_list"] = eps_list
   company["tot_rev"] = tot_rev
   company["cost_of_rev"] = cost_of_rev
   company["sga"] = sga
   company["net_income"] = net_income
   company["income_tax"] = income_tax

   time.sleep(wait_sec)

   #seekingalpha -- balance
   sk_url_balance = "https://seekingalpha.com/symbol/" + tick + "/financials-data?period_type=annual&statement_type=balance-sheet&order_type=latest_right&is_pro=false"
   mydbg1(sk_url_balance)
   sb_reqs = requests.get(sk_url_balance, headers=sc_headers)
   #print(sb_reqs.text)
   balSheet = json.loads(sb_reqs.text)
   # I call it : table, section, entry, column
   # dataCash[table][section][entry][column]
   sb_col_len = len(balSheet["data"][0][0])
   for list1 in balSheet["data"]:
      for sec_entry in list1:
         if (sec_entry[0]["value"] == "Book Value / Share"):
            for lidx in range(2, sb_col_len):
               if "svg" not in sec_entry[lidx]["value"]:
                  bvps_lstr = sec_entry[lidx]["value"]
                  bvps_list.append(convert_num_to_unit(bvps_lstr))

   company["bvps_list"] = bvps_list

   time.sleep(wait_sec)

   # seekingalpha -- cashflow
   sk_url_cash = "https://seekingalpha.com/symbol/" + tick + "/financials-data?period_type=annual&statement_type=cash-flow-statement&order_type=latest_right&is_pro=false"
   mydbg1(sk_url_cash)
   sc_reqs = requests.get(sk_url_cash, headers=sc_headers)
   #print(sc_reqs.text)
   dataCash = json.loads(sc_reqs.text)
   # I call it : table, section, entry, column
   # dataCash[table][section][entry][column]
   sc_col_len = len(dataCash["data"][1][0])
   for list1 in dataCash["data"]:
      for sec_entry in list1:
         if (sec_entry[0]["value"] == "Levered Free Cash Flow"):
            for lidx in range(2, sc_col_len):
               if "svg" not in sec_entry[lidx]["value"]:
                  fcf_lstr = sec_entry[lidx]["value"]
                  fcf_list.append(convert_num_to_Million(fcf_lstr))
         if (sec_entry[0]["value"] == "Depreciation & Amortization, Total"):
            if (sec_entry[sc_col_len-1]["name"] == "TTM"):
               depreciation_str = sec_entry[sc_col_len-idx]["value"]
               depreciation = convert_num_to_Million(depreciation_str)
               mydbg1(depreciation_str, depreciation)
               mydbg1("depreciation", depreciation)
         if (sec_entry[0]["value"] == "Change In Accounts Receivable"):
            if (sec_entry[sc_col_len-1]["name"] == "TTM"):
               receivable_chg_str = sec_entry[sc_col_len-idx]["value"]
               receivable_chg = convert_num_to_Million(receivable_chg_str)
               mydbg1(receivable_chg_str, receivable_chg)
               mydbg1("receivable_chg", receivable_chg)
         if (sec_entry[0]["value"] == "Change In Accounts Payable"):
            if (sec_entry[sc_col_len-1]["name"] == "TTM"):
               payable_chg_str = sec_entry[sc_col_len-idx]["value"]
               payable_chg = convert_num_to_Million(payable_chg_str)
               mydbg1(payable_chg_str, payable_chg)
               mydbg1("payable_chg", payable_chg)
         if (sec_entry[0]["value"] == "Capital Expenditure"):
            if (sec_entry[sc_col_len-1]["name"] == "TTM"):
               capexp_str = sec_entry[sc_col_len-idx]["value"]
               capexp = convert_num_to_Million(capexp_str)
               mydbg1(capexp_str, capexp)
               mydbg1("capexp", capexp)
         if (sec_entry[0]["value"] == "Sale of Property, Plant, and Equipment"):
            if (sec_entry[sc_col_len-1]["name"] == "TTM"):
               sale_property_str = sec_entry[sc_col_len-idx]["value"]
               sale_property = convert_num_to_Million(sale_property_str)
               mydbg1(sale_property_str, sale_property)
               mydbg1("sale_property", sale_property)
         if (sec_entry[0]["value"] == "Cash from Operations"):
            if (sec_entry[sc_col_len-1]["name"] == "TTM"):
               cash_from_operations_str = sec_entry[sc_col_len-idx]["value"]
               cash_from_operations = convert_num_to_Million(cash_from_operations_str)
               mydbg1(cash_from_operations_str, cash_from_operations)
               mydbg1("cash_from_operations", cash_from_operations)
   company["depreciation"] = depreciation
   company["receivable_chg"] = receivable_chg
   company["payable_chg"] = payable_chg
   company["cash_from_operations"] = cash_from_operations
   company["capexp"] = capexp
   company["sale_property"] = sale_property
   company["fcf_list"] = fcf_list

   return ret_val, company

def do_save_ska_to_json_file():
   # load partial data from existing file
   if os.path.exists("./ska/ska_data") and \
      os.path.getsize("./ska/ska_data") != 0:
      infile = "./ska/ska_data"
      infp = open(infile)
      companylist = json.load(infp)
   else:
      companylist = dict()

   outputfile = "./ska/ska_data"
   outfp = open(outputfile, 'w+')
   filepath = "../all-ticks"
   #companylist = dict()
   company = dict()
   with open(filepath) as fp:
       cnt = 0
       do_exit = 0
       for line in fp:
          tick = line[:-1]
          mydbg2(tick,"--------")
          if tick in companylist.keys():
             print(tick, " exists")
          else:
             # company is changed in the called function.
             try:
                result = get_dict_values_from_ska(tick, company, 1)
                # something wrong, go save the current result
                if result[0] == 1:
                   break
                if result[0] == 2:
                   continue
             except Exception as e:
                print("Something is wrong, save and exit")
                tb = traceback.format_exc()
                print(tb)
                break

             companylist[tick] = company
             gc.collect()
             time.sleep(wait_sec)

   # The data is recorded at the very end.
   outfp.write(json.dumps(companylist, indent=4, sort_keys=True))


# Add file2 entries to file1
# The same entries in file1 will get overwritten by file2
def do_merge_file2_to_file1(file1, file2, outputfile):
   print(file1)
   print(file2)

   with open(file1) as f1:
      cplist1 = json.load(f1)

   with open(file2) as f2:
      cplist2 = json.load(f2)

   print(cplist1)
   print(cplist2)
   # loop through file2
   for key in cplist2:
      for itm in cplist2[key]:
         cplist1[key][itm] = cplist2[key][itm]

   outfp = open(outputfile, 'w+')
   outfp.write(json.dumps(cplist1, indent=4, sort_keys=True))



def sort_all_trailing_pe(file1):

   with open(file1) as f1:
      cplist1 = json.load(f1)

   cplist2 = dict()
   for key in cplist1:
      cplist2[key] = float(cplist1[key]["trailing_pe"])

   #print(cplist2)
   sorted_cplist2 = dict(sorted(cplist2.items(), key=operator.itemgetter(1), reverse=True) )
   print(sorted_cplist2)
   print(json.dumps(sorted_cplist2, indent=4))

def calc_sort_all_acqms(file1):
   with open(file1) as f1:
      cplist1 = json.load(f1)

   cplist2 = dict()
   for key in cplist1:

      tot_rev = cplist1[key]["tot_rev"]
      cost_of_rev = cplist1[key]["cost_of_rev"]
      sga = cplist1[key]["sga"]
      depreciation = cplist1[key]["depreciation"]
      operating_earnings = tot_rev - cost_of_rev - sga - depreciation

      if operating_earnings < 0:
         continue

      market_cap = cplist1[key]["market_cap"]
      total_cash = cplist1[key]["total_cash"]
      total_debt = cplist1[key]["total_debt"]
      enterprice_value = market_cap - total_cash + total_debt

      acqm = enterprice_value/operating_earnings
      acqm_fmt = "{:.4f}".format(acqm)
      cplist2[key] = float(acqm_fmt)

   sorted_cplist2 = dict(sorted(cplist2.items(), key=operator.itemgetter(1), reverse=True) )
   print(json.dumps(sorted_cplist2, indent=4))


def do_calc_growth_rate(data_list):
   start_idx = -1
   end_idx = -1
   compound_rate = 0
   compound_rate_fmt = 0.0

   # printout raw data
   print("raw: ", end=" ")
   for item in data_list:
      print(item, end=" ")
   print("")

   size = len(data_list)
   for idx in range(0,size):
      if data_list[idx] > 0:
         start_idx = idx
         break

   if start_idx != -1:
      for idx in reversed(range(0,size)):
         if data_list[idx] > 0 and data_list[idx] >= data_list[start_idx]:
            end_idx = idx
            break
   if start_idx != -1 and end_idx > start_idx:
      compound_rate = (data_list[end_idx]/data_list[start_idx])**(1/(end_idx-start_idx))-1
      compound_rate_fmt = round(compound_rate, 4)
   mydbg1("compound_rate", round(compound_rate_fmt*100, 2), start_idx, end_idx, data_list[start_idx], data_list[end_idx])
   return compound_rate_fmt



def do_one_tick_calculation(company):
   ## ?? not working.
   output = json.dumps(company, indent=4, sort_keys=False)
   re_output = re.sub(r'",\s+', '", ', output)
   print(re_output)

   print(f"======= {company['name']} ======")
   rev_growth = do_calc_growth_rate(company["rev_list"])
   print("rev_growth: ", rev_growth)
   grosspft_growth = do_calc_growth_rate(company["grosspft_list"])
   print("grosspft_growth: ", grosspft_growth)
   eps_growth = do_calc_growth_rate(company["eps_list"])
   print("eps_growth: ", eps_growth)
   bvps_growth = do_calc_growth_rate(company["bvps_list"])
   print("bvps_growth: ", bvps_growth)
   fcf_growth = do_calc_growth_rate(company["fcf_list"])
   print("fcs_growth: ", fcf_growth)


   # tencap calculation
   net_income = company["net_income"]
   income_tax = company["income_tax"]
   depreciation = company["depreciation"]
   receivable_chg = company["receivable_chg"]
   payable_chg = company["payable_chg"]
   capexp = company["capexp"]
   sale_property = company["sale_property"]
   share_num = company["share_num"]
   close_price = company["close_price"]

   owner_earnings = net_income + income_tax + depreciation + receivable_chg + \
                    payable_chg + capexp + sale_property

   tencap_price = (owner_earnings*10)/share_num
   tencap_price_fmt = "{:.2f}".format(tencap_price)
   price_ratio = close_price/tencap_price
   price_ratio_fmt = "{:.2f}".format(price_ratio)

   print("===========")
   print(f"{'*close_price: ' :<20} {close_price}")
   print(f"{'*tencap_price:' :<20} {tencap_price_fmt :<10} [ {price_ratio_fmt} ]")

   # pabriDcf

   growth_rate = 0
   growth_rate_name = ""
   if (bvps_growth != 0):
      growth_rate = bvps_growth
      growth_rate_name = "bvps_growth"
   elif (eps_growth != 0):
      growth_rate = eps_growth
      growth_rate_name = "eps_growth"
   elif (grosspft_growth != 0):
      growth_rate = grosspft_growth
      growth_rate_name = "grosspft_growth"
   elif (rev_growth != 0):
      growth_rate = rev_growth
      growth_rate_name = "rev_growth"

   print(f"{'*growth_rate:' :<20} {growth_rate :<10} [{growth_rate_name}] ")
   cash_from_operations = company["cash_from_operations"]
   capexp = company["capexp"]
   sale_property = company["sale_property"]
   total_cash = company["total_cash"]
   total_debt = company["total_debt"] *-1
   share_num = company["share_num"]

   fcf_y0 = cash_from_operations + capexp + sale_property
   discount_rate = 0.1
   fcf_y1 = fcf_y0 * (1 + growth_rate)
   fcf_y2 = fcf_y1 * (1 + growth_rate)
   fcf_y3 = fcf_y2 * (1 + growth_rate)
   fcf_y4 = fcf_y3 * (1 + growth_rate)
   fcf_y5 = fcf_y4 * (1 + growth_rate)
   fcf_y6 = fcf_y5 * (1 + growth_rate)
   fcf_y7 = fcf_y6 * (1 + growth_rate)
   fcf_y8 = fcf_y7 * (1 + growth_rate)
   fcf_y9 = fcf_y8 * (1 + growth_rate)
   fcf_y10 = fcf_y9 * (1 + growth_rate)

   fcf_y1_dcf =  npf.pv(discount_rate, 1, 0, fcf_y1)*-1
   fcf_y2_dcf =  npf.pv(discount_rate, 2, 0, fcf_y2)*-1
   fcf_y3_dcf =  npf.pv(discount_rate, 3, 0, fcf_y3)*-1
   fcf_y4_dcf =  npf.pv(discount_rate, 4, 0, fcf_y4)*-1
   fcf_y5_dcf =  npf.pv(discount_rate, 5, 0, fcf_y5)*-1
   fcf_y6_dcf =  npf.pv(discount_rate, 6, 0, fcf_y6)*-1
   fcf_y7_dcf =  npf.pv(discount_rate, 7, 0, fcf_y7)*-1
   fcf_y8_dcf =  npf.pv(discount_rate, 8, 0, fcf_y8)*-1
   fcf_y9_dcf =  npf.pv(discount_rate, 9, 0, fcf_y9)*-1
   fcf_y10_dcf =  npf.pv(discount_rate, 10, 0, fcf_y10)*-1
   termination_value = fcf_y10_dcf *10
   current_npv = fcf_y1_dcf + fcf_y2_dcf + fcf_y3_dcf + fcf_y4_dcf + fcf_y5_dcf + \
                 fcf_y6_dcf + fcf_y7_dcf + fcf_y8_dcf + fcf_y9_dcf + fcf_y10_dcf + \
                 termination_value+ total_cash + total_debt

   mydbg2(fcf_y1, fcf_y1_dcf)
   mydbg2(fcf_y8, fcf_y8_dcf)
   #print(current_npv)

   intrinsic_value_per_share = current_npv/share_num
   intrinsic_price_ratio = close_price/intrinsic_value_per_share
   intrinsic_price_ratio_fmt = "{:.2f}".format(intrinsic_price_ratio)

   pabridcf_price = intrinsic_value_per_share/2
   pabridcf_price_ratio = close_price/pabridcf_price
   pabridcf_price_ratio_fmt = "{:.2f}".format(pabridcf_price_ratio)

   print(f"{'*pabDcf_price:' :<20} {round(pabridcf_price, 2):<10} [ {pabridcf_price_ratio_fmt} ]")
   print(f"{'==pabIntrinsic:' :<20} {round(intrinsic_value_per_share, 2):<10} [ {intrinsic_price_ratio_fmt} ]" )

   # payback (eight years)
   payback_sum = fcf_y1 + fcf_y2 + fcf_y3 + fcf_y4 + fcf_y5 + \
                 fcf_y6 + fcf_y7 + fcf_y8

   payback_price = payback_sum/share_num
   payback_price_ratio = close_price/payback_price
   payback_price_ratio_fmt = "{:.2f}".format(payback_price_ratio)

   print(f"{'*payback_price:' :<20} {round(payback_price):<10} [ {payback_price_ratio_fmt} ]" )


## This will evaluate one stock
def do_evaluate_one_tick(tick, idx):
   company = dict()
   company["name"] = tick
   result = get_dict_values_from_ska(tick, company, idx)
   if result[0] != 0:
      return

   company["dash"] = "------"

   result = get_dict_values_from_yh(tick, company)
   if result[0] != 0:
      return

   outputfile = "/home/hjin/test/one_tick"
   outfp = open(outputfile, 'w+')
   outfp.write(json.dumps(company, indent=4, sort_keys=False))

   do_one_tick_calculation(company)


def do_evaluate_file_one_tick():
   infile = "/home/hjin/test/one_tick"
   with open(infile) as f1:
      company = json.load(f1)

   do_one_tick_calculation(company)



# https://seekingalpha.com/symbol/FDX/financials-data?period_type=annual&statement_type=income-statement&order_type=latest_right&is_pro=false
# https://seekingalpha.com/symbol/AAPL/financials-data?period_type=annual&statement_type=cash-flow-statement&order_type=latest_right&is_pro=false
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36
# Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0
#  Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36


def get_ticks():
   url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
   reqs = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv)"})
   #print(reqs.text)
   soup = BeautifulSoup(reqs.text, 'html.parser')

   tbody = soup.find_all('tbody')
   for entry in tbody[0].find_all('tr'):
      mytds = entry.find_all('td')
      if mytds:
         name = mytds[0].find('a').text
         print(name)



def main():
   if len(sys.argv) == 1:
       print("Please use the following commands in subdir:");
       print("    check-date -- print the submit date")
       print("    holders -- print the whole holder-symbols table")
       print("    count-symbols -- count how many holders for a symbol")
       print("    acqm -- acquirer's multiple")
       print("         eg: python -u ./dataroma.py acqm merge_data")
       print("    get-ticks -- save ticks to all-ticks ")
       print("              eg: ./dataroma.py get-ticks | tee all-ticks ")
       print("    tpe -- sort the trailing PEs")
       print("         eg: python -u ./dataroma.py tpe merge_data")
       print("    yh-to-file -- save yahoo data to file. Needs yh subdir")
       print("         eg: python -u ./dataroma.py yh-to-file")
       print("    ska-to-file -- save seekalpha data to file. Needs ska subdir")
       print("         eg: python -u ./dataroma.py ska-to-file")
       print("    merge-json-files file1 file2 -- add file2 json contents to file1")
       print("         eg: python -u ../dataroma.py merge-json-files ./yh/yh_data ./ska/ska_data ./merge_data ")
       print("    eval-one tick idx -- evaluate one tick (1 - TTM, 2 - last year etc)")
       print("         eg: python -u ./dataroma.py eval-one 1 FB")
       print("    eval-one-file -- evaluate one_tick file")
       print("         eg: python -u ./dataroma.py eval-one-file")
       print("    change path1 path2")
       sys.exit()

   parser = argparse.ArgumentParser()
   parser.add_argument("cmd")
   parser.add_argument("path1", nargs='?')
   parser.add_argument("path2", nargs='?')
   parser.add_argument("path3", nargs='?')
   args = parser.parse_args()
   mydbg1(args.cmd)
   mydbg1(args.path1)
   mydbg1(args.path2)
   mydbg1(args.path3)
   mydbg1("---------------------")


   sfx = get_file_suffix()
   #print(sfx)

   if args.cmd == "check-date":
      check_date()
   elif args.cmd == "holders":
      check_holders()
   elif args.cmd == "count-symbols":
      count_symbols()
   elif args.cmd == "acqm":
      calc_sort_all_acqms(args.path1)
   elif args.cmd == "get-ticks":
      get_ticks()
   elif args.cmd == "tpe":
      sort_all_trailing_pe(args.path1)
   elif args.cmd == "yh-to-file":
      do_save_yh_to_json_file()
   elif args.cmd == "ska-to-file":
      do_save_ska_to_json_file()
   elif args.cmd == "merge-json-files":
      do_merge_file2_to_file1(args.path1, args.path2, args.path3)
   elif args.cmd == "eval-one":
      do_evaluate_one_tick(args.path2.upper(), int(args.path1))
   elif args.cmd == "eval-one-file":
      do_evaluate_file_one_tick()



if __name__ == '__main__':
   main()
