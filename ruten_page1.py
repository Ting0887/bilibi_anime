# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 14:15:10 2020

@author: user
"""

import requests
from selenium import webdriver
import selenium.webdriver.support.ui as ui 
import json
import time
import pandas as pd
mylist = [] #空陣列
myexcel = []
driverPath = 'C:\\Users\\user\\chromedriver.exe'
browser = webdriver.Chrome(driverPath)
url = 'https://rtapi.ruten.com.tw/api/search/v3/index.php/core/prod?q=%E8%BE%B2%E6%9E%97&type=direct&sort=rnk%2Fdc&offset=1&limit=80&2666611'
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}

res = requests.get(url,headers=headers)
response = json.loads(res.text.encode('utf8'))
count = 0
for item in response['Rows']:
    count += 1
    link = 'https://www.ruten.com.tw/item/show?' + item['Id']
    browser.get(link) #進入連結
    time.sleep(1)
    wait = ui.WebDriverWait(browser,10)
    
    title = wait.until(lambda browser: browser.find_element_by_xpath("//span[@class='vmiddle']").text) #商品名稱
    price = wait.until(lambda browser: browser.find_element_by_xpath("//strong[@class='rt-text-xx-large rt-text-important']").text) #價格
    payway = browser.find_element_by_xpath("//ul[@class='detail-list']").text.replace('\n','、') #付款方式
    diliverway = browser.find_elements_by_xpath("//ul[@class='detail-list']")[1].text.replace('\n','、') #運送方式
    try:
        seller_board = browser.find_element_by_xpath("//div[@class='seller-board']").text.replace('\n',' ')
    except:
        seller_board = None
        
    mylist.append({'商品名稱':title,
                   '連結':link,
                   '價格':price,
                   '付款方式':payway,
                   '運送方式':diliverway,
                   '賣家的版':seller_board})
    
    mydata = pd.DataFrame([{'商品名稱':title,
                            '連結':link,
                            '價格':price,
                            '付款方式':payway,
                            '運送方式':diliverway,
                            '賣家的版':seller_board}])
    myexcel.append(mydata)
    
    print('第{}筆資料完成!'.format(count))
file = 'ruten_農林.json'

with open(file,'w',encoding='utf-8') as data:
    json.dump(mylist, data, ensure_ascii=False,indent=2)
    
data.close()

df = pd.concat(myexcel,ignore_index=True)
df.to_excel('ruten_農林.xlsx',index=0)    
    