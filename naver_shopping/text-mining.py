#패키지 import
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import requests
import re
import pandas as pd
import numpy as np
import os

name=['에어팟 1세대','에어팟 2세대']
category=['음질','품질','성능','기능','배터리 수명','사용성','조작성','디자인','착용감','휴대성']

#에어팟 1세대 검색 
ns_address_airpod="https://search.shopping.naver.com/detail/detail.nhn?nvMid=10776906666&query=%25EC%2597%2590%25EC%2596%25B4%25ED%258C%259F%25201%25EC%2584%25B8%25EB%258C%2580&NaPm=ct%3Dkb3ef8sg%7Cci%3Df7d5699aba286396ee3757965561aa228125c722%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3Da9cfdf21495248f435f4ae3cbea263c694784ae1"
#xpath
shoppingmall_review="/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/ul/li[3]/a/strong"
category1="/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[1]/div[2]/div/ul/li[4]/a/span" #음질
category2="/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[1]/div[2]/div/ul/li[6]/a/span" #품질
category3="/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[1]/div[2]/div/ul/li[7]/a/span" #성능
category4="/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[1]/div[2]/div/ul/li[8]/a/span" #기능
plus="/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[1]/div[2]/div/a" #더보기
category5="/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[1]/div[2]/div/ul/li[16]/a/span"  #배터리 수명
category6="/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[1]/div[2]/div/ul/li[9]/a/span" #사용성
category7="/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[1]/div[2]/div/ul/li[11]/a/span" #조작성
#향상되지않은기능
category8="/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[1]/div[2]/div/ul/li[5]/a/span" #디자인
category9="/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[1]/div[2]/div/ul/li[10]/a/span" #착용감
category10="/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[1]/div[2]/div/ul/li[14]/a/span" #휴대성

header = {'User-Agent': ''}
d = webdriver.Chrome('/Users/hanseungpil/VsCode/실무_셀레니움_크롤링/naver_shopping/chromedriver') # webdriver = chrome
d.implicitly_wait(3)
d.get(ns_address_airpod)
req = requests.get(ns_address_airpod)
html = req.text 
soup = BeautifulSoup(html, "html.parser")

#함수 선언
def add_dataframe(name,category,reviews,stars,cnt):  #데이터 프레임에 저장
    #데이터 프레임생성
    df1=pd.DataFrame(columns=['type','category','review','star'])
    n=1
    if (cnt>0):
        for i in range(0,cnt-1):
            df1.loc[n]=[name,category,reviews[i],stars[i]] #해당 행에 저장
            i+=1
            n+=1
    else:
        df1.loc[n]=[name,category,'null','null']
        n+=1    
    return df1

def save():
    if not os.path.exists('output1.csv'):
        df1.to_csv('output1.csv', encoding='utf-8-sig', mode='w')
    else:
        df1.to_csv('output1.csv',encoding='utf-8-sig', mode='a',header=False)
        
        
#쇼핑몰 리뷰 보기
d.find_element_by_xpath(shoppingmall_review).click()
sleep(2)
        
#"음질" 관련 리뷰 가져오기
d.find_element_by_xpath(category1).click() #스크롤 건드리면 안됨
name_=name[0]  #에어팟 1세대
category_=category[0]
reviews=[]
stars=[]
cnt=1   #리뷰index
page=1
while True:
    j=1
    print ("페이지", page ,"\n") 
    sleep(2)
    while True: #한페이지에 20개의 리뷰, 마지막 리뷰에서 error발생
        try:
            star=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[1]/a/span[2]/strong').text
            stars.append(star)
            review=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]').text
            reviews.append(review)
            if j%2==0: #화면에 2개씩 보이도록 스크롤
                ELEMENT = d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]')
                d.execute_script("arguments[0].scrollIntoView(true);", ELEMENT)       
            j+=1
            print(cnt, review ,star, "\n")
            cnt+=1 
        except: break
            
    sleep(2)
    
    if page<11:#page10까지 적용
        try: #리뷰의 마지막 페이지에서 error발생
            next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page)+']').click() 
            page +=1
        except: break #리뷰의 마지막 페이지에서 process 종료 
            
    else :
        try: #page11부터
            if page%10==0: next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a[12]').click()
            else : next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page%10+2)+']').click()
            page+=1
        except: break 
            
df1=add_dataframe(name_,category_,reviews,stars,cnt)
save()



#"품질" 관련 리뷰 가져오기
up="/html/body/div[2]/a" #맨위로 이동
d.find_element_by_xpath(up).click() #스크롤 건드리면 안됨
d.find_element_by_xpath(category2).click() #스크롤 건드리면 안됨
name_=name[0]  #에어팟 1세대
category_=category[1]
reviews=[]
stars=[]
cnt=1   #리뷰index
page=1
while True:
    j=1
    print ("페이지", page ,"\n") 
    sleep(2)
    while True: #한페이지에 20개의 리뷰, 마지막 리뷰에서 error발생
        try:
            star=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[1]/a/span[2]/strong').text
            stars.append(star)
            review=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]').text
            reviews.append(review)
            if j%2==0: #화면에 2개씩 보이도록 스크롤
                ELEMENT = d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]')
                d.execute_script("arguments[0].scrollIntoView(true);", ELEMENT)       
            j+=1
            print(cnt, review ,star, "\n")
            cnt+=1 
        except: break
            
    sleep(2)
    
    if page<11:#page10까지 적용
        try: #리뷰의 마지막 페이지에서 error발생
            next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page)+']').click() 
            page +=1
        except: break #리뷰의 마지막 페이지에서 process 종료 
            
    else :
        try: #page11부터
            if page%10==0: next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a[12]').click()
            else : next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page%10+2)+']').click()
            page+=1
        except: break 
df1=add_dataframe(name_,category_,reviews,stars,cnt)
save()



#"성능" 관련 리뷰 가져오기
up="/html/body/div[2]/a" #맨위로 이동
d.find_element_by_xpath(up).click() #스크롤 건드리면 안됨
d.find_element_by_xpath(category3).click() #스크롤 건드리면 안됨
name_=name[0]  #에어팟 1세대
category_=category[2]
reviews=[]
stars=[]
cnt=1   #리뷰index
page=1
while True:
    j=1
    print ("페이지", page ,"\n") 
    sleep(2)
    while True: #한페이지에 20개의 리뷰, 마지막 리뷰에서 error발생
        try:
            star=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[1]/a/span[2]/strong').text
            stars.append(star)
            review=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]').text
            reviews.append(review)
            if j%2==0: #화면에 2개씩 보이도록 스크롤
                ELEMENT = d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]')
                d.execute_script("arguments[0].scrollIntoView(true);", ELEMENT)       
            j+=1
            print(cnt, review ,star, "\n")
            cnt+=1 
        except: break
            
    sleep(2)
    
    if page<11:#page10까지 적용
        try: #리뷰의 마지막 페이지에서 error발생
            next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page)+']').click() 
            page +=1
        except: break #리뷰의 마지막 페이지에서 process 종료 
            
    else :
        try: #page11부터
            if page%10==0: next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a[12]').click()
            else : next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page%10+2)+']').click()
            page+=1
        except: break 
df1=add_dataframe(name_,category_,reviews,stars,cnt)
save()

#"기능" 관련 리뷰 가져오기
up="/html/body/div[2]/a" #맨위로 이동
d.find_element_by_xpath(up).click() #스크롤 건드리면 안됨
d.find_element_by_xpath(category4).click() #스크롤 건드리면 안됨
name_=name[0]  #에어팟 1세대
category_=category[3]
reviews=[]
stars=[]
cnt=1   #리뷰index
page=1
while True:
    j=1
    print ("페이지", page ,"\n") 
    sleep(2)
    while True: #한페이지에 20개의 리뷰, 마지막 리뷰에서 error발생
        try:
            star=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[1]/a/span[2]/strong').text
            stars.append(star)
            review=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]').text
            reviews.append(review)
            if j%2==0: #화면에 2개씩 보이도록 스크롤
                ELEMENT = d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]')
                d.execute_script("arguments[0].scrollIntoView(true);", ELEMENT)       
            j+=1
            print(cnt, review ,star, "\n")
            cnt+=1 
        except: break
            
    sleep(2)
    
    if page<11:#page10까지 적용
        try: #리뷰의 마지막 페이지에서 error발생
            next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page)+']').click() 
            page +=1
        except: break #리뷰의 마지막 페이지에서 process 종료 
            
    else :
        try: #page11부터
            if page%10==0: next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a[12]').click()
            else : next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page%10+2)+']').click()
            page+=1
        except: break 
df1=add_dataframe(name_,category_,reviews,stars,cnt)
save()


#"배터리 수명" 관련 리뷰 가져오기
up="/html/body/div[2]/a" #맨위로 이동
d.find_element_by_xpath(up).click() #스크롤 건드리면 안됨
d.find_element_by_xpath(plus).click() #스크롤 건드리면 안됨
d.find_element_by_xpath(category5).click() #스크롤 건드리면 안됨
name_=name[0]  #에어팟 1세대
category_=category[4]
reviews=[]
stars=[]
cnt=1   #리뷰index
page=1
while True:
    j=1
    print ("페이지", page ,"\n") 
    sleep(2)
    while True: #한페이지에 20개의 리뷰, 마지막 리뷰에서 error발생
        try:
            star=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[1]/a/span[2]/strong').text
            stars.append(star)
            review=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]').text
            reviews.append(review)
            if j%2==0: #화면에 2개씩 보이도록 스크롤
                ELEMENT = d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]')
                d.execute_script("arguments[0].scrollIntoView(true);", ELEMENT)       
            j+=1
            print(cnt, review ,star, "\n")
            cnt+=1 
        except: break
            
    sleep(2)
    
    if page<11:#page10까지 적용
        try: #리뷰의 마지막 페이지에서 error발생
            next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page)+']').click() 
            page +=1
        except: break #리뷰의 마지막 페이지에서 process 종료 
            
    else :
        try: #page11부터
            if page%10==0: next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a[12]').click()
            else : next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page%10+2)+']').click()
            page+=1
        except: break 
            
df1=add_dataframe(name_,category_,reviews,stars,cnt)
save()

#"사용성" 관련 리뷰 가져오기
up="/html/body/div[2]/a" #맨위로 이동
d.find_element_by_xpath(up).click() #스크롤 건드리면 안됨
d.find_element_by_xpath(plus).click() #스크롤 건드리면 안됨
d.find_element_by_xpath(category6).click() #스크롤 건드리면 안됨
name_=name[0]  #에어팟 1세대
category_=category[5]
reviews=[]
stars=[]
cnt=1   #리뷰index
page=1
while True:
    j=1
    print ("페이지", page ,"\n") 
    sleep(2)
    while True: #한페이지에 20개의 리뷰, 마지막 리뷰에서 error발생
        try:
            star=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[1]/a/span[2]/strong').text
            stars.append(star)
            review=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]').text
            reviews.append(review)
            if j%2==0: #화면에 2개씩 보이도록 스크롤
                ELEMENT = d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]')
                d.execute_script("arguments[0].scrollIntoView(true);", ELEMENT)       
            j+=1
            print(cnt, review ,star, "\n")
            cnt+=1 
        except: break
            
    sleep(2)
    
    if page<11:#page10까지 적용
        try: #리뷰의 마지막 페이지에서 error발생
            next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page)+']').click() 
            page +=1
        except: break #리뷰의 마지막 페이지에서 process 종료 
            
    else :
        try: #page11부터
            if page%10==0: next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a[12]').click()
            else : next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page%10+2)+']').click()
            page+=1
        except: break 
            


up="/html/body/div[2]/a" #맨위로 이동
d.find_element_by_xpath(up).click() #스크롤 건드리면 안됨
d.find_element_by_xpath(plus).click() #스크롤 건드리면 안됨
d.find_element_by_xpath(category8).click() #스크롤 건드리면 안됨
name_=name[0]  #에어팟 1세대
category_=category[7]
reviews=[]
stars=[]
cnt=1   #리뷰index
page=1
while True:
    j=1
    print ("페이지", page ,"\n") 
    sleep(2)
    while True: #한페이지에 20개의 리뷰, 마지막 리뷰에서 error발생
        try:
            star=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[1]/a/span[2]/strong').text
            stars.append(star)
            review=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]').text
            reviews.append(review)
            if j%2==0: #화면에 2개씩 보이도록 스크롤
                ELEMENT = d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]')
                d.execute_script("arguments[0].scrollIntoView(true);", ELEMENT)       
            j+=1
            print(cnt, review ,star, "\n")
            cnt+=1 
        except: break
            
    sleep(2)
    
    if page<11:#page10까지 적용
        try: #리뷰의 마지막 페이지에서 error발생
            next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page)+']').click() 
            page +=1
        except: break #리뷰의 마지막 페이지에서 process 종료 
            
    else :
        try: #page11부터
            if page%10==0: next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a[12]').click()
            else : next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page%10+2)+']').click()
            page+=1
        except: break
df1=add_dataframe(name_,category_,reviews,stars,cnt)
save()
            
            
up="/html/body/div[2]/a" #맨위로 이동
d.find_element_by_xpath(up).click() #스크롤 건드리면 안됨
d.find_element_by_xpath(plus).click() #스크롤 건드리면 안됨
d.find_element_by_xpath(category9).click() #스크롤 건드리면 안됨
name_=name[0]  #에어팟 1세대
category_=category[8]
reviews=[]
stars=[]
cnt=1   #리뷰index
page=1
while True:
    j=1
    print ("페이지", page ,"\n") 
    sleep(2)
    while True: #한페이지에 20개의 리뷰, 마지막 리뷰에서 error발생
        try:
            star=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[1]/a/span[2]/strong').text
            stars.append(star)
            review=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]').text
            reviews.append(review)
            if j%2==0: #화면에 2개씩 보이도록 스크롤
                ELEMENT = d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]')
                d.execute_script("arguments[0].scrollIntoView(true);", ELEMENT)       
            j+=1
            print(cnt, review ,star, "\n")
            cnt+=1 
        except: break
            
    sleep(2)
    
    if page<11:#page10까지 적용
        try: #리뷰의 마지막 페이지에서 error발생
            next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page)+']').click() 
            page +=1
        except: break #리뷰의 마지막 페이지에서 process 종료 
            
    else :
        try: #page11부터
            if page%10==0: next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a[12]').click()
            else : next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page%10+2)+']').click()
            page+=1
        except: break
df1=add_dataframe(name_,category_,reviews,stars,cnt)
save()
            
up="/html/body/div[2]/a" #맨위로 이동
d.find_element_by_xpath(up).click() #스크롤 건드리면 안됨
d.find_element_by_xpath(plus).click() #스크롤 건드리면 안됨
d.find_element_by_xpath(category10).click() #스크롤 건드리면 안됨
name_=name[0]  #에어팟 1세대
category_=category[9]
reviews=[]
stars=[]
cnt=1   #리뷰index
page=1
while True:
    j=1
    print ("페이지", page ,"\n") 
    sleep(2)
    while True: #한페이지에 20개의 리뷰, 마지막 리뷰에서 error발생
        try:
            star=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[1]/a/span[2]/strong').text
            stars.append(star)
            review=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]').text
            reviews.append(review)
            if j%2==0: #화면에 2개씩 보이도록 스크롤
                ELEMENT = d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/ul/li['+str(j)+']/div/div[2]')
                d.execute_script("arguments[0].scrollIntoView(true);", ELEMENT)       
            j+=1
            print(cnt, review ,star, "\n")
            cnt+=1 
        except: break
            
    sleep(2)
    
    if page<11:#page10까지 적용
        try: #리뷰의 마지막 페이지에서 error발생
            next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page)+']').click() 
            page +=1
        except: break #리뷰의 마지막 페이지에서 process 종료 
            
    else :
        try: #page11부터
            if page%10==0: next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a[12]').click()
            else : next_page=d.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[5]/div[2]/div[2]/a['+str(page%10+2)+']').click()
            page+=1
        except: break 
            
df1=add_dataframe(name_,category_,reviews,stars,cnt)
save()