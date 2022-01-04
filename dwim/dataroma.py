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

#debug_level: 0 - nodebug
#             1 - most important debug
#             2 - normal debug
debug_level = 2

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



def count_acqm(tick, outfp):
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
   print( sc_col_len, "**")
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


def count_all_acqms():
   outputfile = "/home/hjin/test/acqm_results"
   outfp = open(outputfile, 'a+')
   filepath = "/home/hjin/test/all-ticks"
   with open(filepath) as fp:
       cnt = 0
       for line in fp:
          tick = line[:-1]
          mydbg2(tick, "--------")
          result = count_acqm(tick, outfp)
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

def convert_num_to_unit(numStr):
   mydbg2("numStr", numStr)
   if "k" in numStr:
      numNoK = numStr[:-1]
      numInUnit = float(numNoK) *  1000
   elif "N/A" in numStr:
      numInUnit = float(0)
   else:
      if "(" in numStr:
         numInUnit = float(numStr.replace('(','').replace(')','').replace(',','')) * -1
      else:
         numInUnit = float(numStr.replace(',',''))

   mydbg2("numInUnit", numInUnit)
   return numInUnit

def count_tpe(tick, outfp):
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



def count_all_trailing_pe():
   outputfile = "/home/hjin/test/tpe_results"
   outfp = open(outputfile, 'a+')
   filepath = "/home/hjin/test/all-ticks"
   with open(filepath) as fp:
       cnt = 0
       for line in fp:
          tick = line[:-1]
          mydbg2(tick, "--------")

          while True:
             result = count_tpe(tick, outfp)
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

def get_dict_values_from_yh(tick):
   # Initialize the variables.
   global tick_count
   tick_count+=1

   market_cap = 0
   trailing_pe = 0
   total_cash = 0
   total_debt = 0
   forward_pe = 0
   ps_ratio = 0
   pb_ratio = 0

   market_cap_str = "0"
   trailing_pe_str = "0"
   total_cash_str = "0"
   total_debt_str = "0"
   forward_pe_str = "0"
   ps_ratio_str = "0"
   pb_ratio_str = "0"
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

   # debug code
   if market_cap == 0:
      ret_val = 1
      #print(yareqs.text)

   print(tick_count, tick, trailing_pe, trailing_pe_str)
   company = dict()
   company["trailing_pe"] = trailing_pe
   company["market_cap"] = market_cap
   company["total_cash"] = total_cash
   company["total_debt"] = total_debt
   company["forward_pe"] = forward_pe
   company["ps_ratio"] = ps_ratio
   company["pb_ratio"] = pb_ratio

   # garbage collect
   del ya_soup
   del yareqs
   del yaurl
   del ya_tbody

   return ret_val, company

def do_save_yh_to_json_file():
   outputfile = "/home/hjin/test/yh_data"
   outfp = open(outputfile, 'w+')
   filepath = "/home/hjin/test/all-ticks"
   companylist = dict()
   with open(filepath) as fp:
       cnt = 0
       for line in fp:
          tick = line[:-1]
          mydbg2(tick, "--------")

          while True:
             result = get_dict_values_from_yh(tick)
             if result[0] != 0:
                # wait for the server to retrieve the data.
                time.sleep(20)
             else:
                break

          companylist[tick] = result[1]
          gc.collect()
          time.sleep(wait_sec)

   outfp.write(json.dumps(companylist, indent=4, sort_keys=True))


def get_dict_values_from_ska(tick):
   # Initialize the variables.
   global tick_count
   tick_count+=1
   ret_val = 0

   tot_rev = 0
   cost_of_rev = 0
   sga = 0
   depreciation = 0

   total_revenues_str = "0"
   cost_of_revenue_str = "0"
   sga_str = "0"
   depreciation_str = "0"

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
   print( sc_col_len, "**")
   for entry_idx in range(len(dataCash["data"][1])):
      if (dataCash["data"][1][entry_idx][0]["value"] == "Depreciation & Amortization, Total"):
         if (dataCash["data"][1][entry_idx][sc_col_len-1]["name"] == "TTM"):
            depreciation_str = dataCash["data"][1][entry_idx][sc_col_len-1]["value"]
            depreciation = convert_num_to_Million(depreciation_str)
            print(depreciation_str, depreciation)

         mydbg1("depreciation", depreciation)

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

   company = dict()
   company["tot_rev"] = tot_rev
   company["cost_of_rev"] = cost_of_rev
   company["sga"] = sga
   company["depreciation"] = depreciation

   return ret_val, company

def do_save_ska_to_json_file():
   outputfile = "/home/hjin/test/ska_data"
   outfp = open(outputfile, 'w+')
   filepath = "/home/hjin/test/all-ticks"
   companylist = dict()
   with open(filepath) as fp:
       cnt = 0
       for line in fp:
          tick = line[:-1]
          mydbg2(tick, "--------")

          while True:
             result = get_dict_values_from_ska(tick)
             if result[0] != 0:
                # wait for the server to retrieve the data.
                time.sleep(20)
             else:
                break

          companylist[tick] = result[1]
          gc.collect()
          time.sleep(wait_sec)

   outfp.write(json.dumps(companylist, indent=4, sort_keys=True))


def get_dict_values_from_yh2(tick):
   # Initialize the variables.
   global tick_count
   tick_count+=1

   forward_pe = 0
   market_cap = 0
   ps_ratio = 0
   pb_ratio = 0
   forward_pe_str = "0"
   market_cap_str = "0"
   ps_ratio_str = "0"
   pb_ratio_str = "0"
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
         if "Forward P/E" in spanStr:
            forward_pe_str = mytd[1].text
            forward_pe = convert_num_to_unit(forward_pe_str)
            mydbg1("forward_pe", forward_pe)
         if "Price/Sales" in spanStr:
            ps_ratio_str = mytd[1].text
            ps_ratio = convert_num_to_unit(ps_ratio_str)
            mydbg1("ps_ratio", ps_ratio)
         if "Price/Book" in spanStr:
            pb_ratio_str = mytd[1].text
            pb_ratio = convert_num_to_unit(pb_ratio_str)
            mydbg1("pb_ratio", pb_ratio)

   # debug code
   if market_cap == 0:
      ret_val = 1
      #print(yareqs.text)

   print(tick_count, tick, forward_pe, forward_pe_str)
   company = dict()
   company["forward_pe"] = forward_pe
   company["ps_ratio"] = ps_ratio
   company["pb_ratio"] = pb_ratio

   # garbage collect
   del ya_soup
   del yareqs
   del yaurl
   del ya_tbody

   return ret_val, company

def do_save_yh_to_json_file2():
   outputfile = "/home/hjin/test/yh_data2"
   outfp = open(outputfile, 'w+')
   filepath = "/home/hjin/test/all-ticks"
   companylist = dict()
   with open(filepath) as fp:
       cnt = 0
       for line in fp:
          tick = line[:-1]
          mydbg2(tick, "--------")

          while True:
             result = get_dict_values_from_yh2(tick)
             if result[0] != 0:
                # wait for the server to retrieve the data.
                time.sleep(20)
             else:
                break

          companylist[tick] = result[1]
          gc.collect()
          time.sleep(wait_sec)

   outfp.write(json.dumps(companylist, indent=4, sort_keys=True))


# Add file2 entries to file1
# The same entries in file1 will get overwritten by file2
def do_merge_file2_to_file1(file1, file2):
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

   outputfile = "/home/hjin/test/merge_data"
   outfp = open(outputfile, 'w+')
   outfp.write(json.dumps(cplist1, indent=4, sort_keys=True))


#      print(json.dumps(data, indent=4, sort_keys=False))


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
       print("Please use the following commands:");
       print(" check-date -- print the submit date")
       print(" holders -- print the whole holder-symbols table")
       print(" count-symbols -- count how many holders for a symbol")
       print(" acqm -- acquirer's multiple")
       print("         eg: python -u ./dataroma.py acqm | tee acqm_traces")
       print(" get-ticks -- save ticks to all-ticks ")
       print("              eg: ./dataroma.py get-ticks | tee all-ticks ")
       print(" tpe -- sort the trailing PEs")
       print("         eg: python -u ./dataroma.py tpe | tee tpe_traces")
       print(" yh-to-file -- save yahoo data to file")
       print("         eg: python -u ./dataroma.py yh-to-file")
       print(" yh-to-file2 -- save yahoo data to file2")
       print(" ska-to-file -- save seekalpha data to file")
       print("         eg: python -u ./dataroma.py ska-to-file")
       print(" merge-json-files file1 file2 -- add file2 json contents to file1")
       print("         eg: python -u ./dataroma.py merge-json-files ./yh_data ./ska_data ")
       print(" change path1 path2")
       sys.exit()

   parser = argparse.ArgumentParser()
   parser.add_argument("cmd")
   parser.add_argument("path1", nargs='?')
   parser.add_argument("path2", nargs='?')
   args = parser.parse_args()
   mydbg1(args.cmd)
   mydbg1(args.path1)
   mydbg1(args.path2)
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
      count_all_acqms()
   elif args.cmd == "get-ticks":
      get_ticks()
   elif args.cmd == "tpe":
      count_all_trailing_pe()
   elif args.cmd == "yh-to-file":
      do_save_yh_to_json_file()
   elif args.cmd == "yh-to-file2":
      do_save_yh_to_json_file2()
   elif args.cmd == "ska-to-file":
      do_save_ska_to_json_file()
   elif args.cmd == "merge-json-files":
      do_merge_file2_to_file1(args.path1, args.path2)



if __name__ == '__main__':
   main()
