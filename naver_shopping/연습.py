import csv
from lib2to3.pgen2 import driver
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 브라우저 생성
browser = webdriver.Chrome(executable_path= '/Users/hanseungpil/VsCode/실무_셀레니움_크롤링/naver_shopping/chromedriver')

# 웹사이트 열기
browser.get('https://www.naver.com')

# 쇼핑 메뉴 클릭
browser.find_element_by_css_selector('a.nav.shop').click()
time.sleep(2)

# 검색창 클릭
search = browser.find_element_by_css_selector('input.co_srh_input._input')
search.click()

# 검색어 입력
search.send_keys('대용량 제습기')
search.send_keys(Keys.ENTER)

browser.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/div[3]/a').click()
browser.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/div[1]/div/div[2]/div[3]/ul/li[4]/a').click()