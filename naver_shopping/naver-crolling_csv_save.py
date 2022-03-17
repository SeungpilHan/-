import csv
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
search.send_keys('에어렉스 대용량 제습기')
search.send_keys(Keys.ENTER)

#80개씩 보기
browser.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/div[3]/a').click()
time.sleep(1)
browser.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/div[3]/ul/li[4]/a').click()

# 스크롤 전 높이
before_h = browser.execute_script("return window.scrollY")

# 무한 스크롤
while True:
    # 맨 아래로 스크롤을 내린다.
    browser.find_element_by_css_selector("body").send_keys(Keys.END)

    # 스크롤 사이 페이지 로딩 시간
    time.sleep(2)

    # 스크롤 후 높이
    after_h = browser.execute_script("return window.scrollY")

    if after_h == before_h:
        break
    before_h = after_h

# 파일 생성
f = open(r"/Users/hanseungpil/VsCode/실무_셀레니움_크롤링/naver_shopping/data.csv", 'w', encoding='CP949', newline='')
csvWriter = csv.writer(f)

# 상품 정보 div
items = browser.find_elements_by_css_selector(".basicList_item__2XT81")

for item in items:
    name = item.find_element_by_css_selector(".basicList_title__3P9Q7").text
    try:
        price = item.find_element_by_css_selector(".price_num__2WUXn").text
    except:
        price = "판매중단"
    link = item.find_element_by_css_selector(".basicList_title__3P9Q7 > a").get_attribute('href')
    img_src = item.find_element_by_css_selector(".thumbnail_thumb__3Agq6 > img").get_attribute('src')
    print(name, price, link, img_src)

    #데이터쓰기
    csvWriter.writerow([name, price, link, img_src])

#파일닫기
f.close()