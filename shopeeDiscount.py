from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from bs4 import BeautifulSoup
import pprint
import time
from categorize import product_with_discount
from highestDiscount import highest_discount


search = str(input("What are you searching for?\n:"))
print('searching ...')
searchurl = search.replace(' ', '%20')
url = 'https://shopee.com.my/search?keyword={}&page=0'.format(searchurl)

driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(30)
try:
    driver.find_element_by_xpath('//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]/button').click()
except:
    Exception()

page = 0
while page != 5:
    driver.implicitly_wait(3)
    driver.execute_script("window.scrollTo(0,(document.body.scrollHeight)/4)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,(document.body.scrollHeight)/2)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,3*(document.body.scrollHeight)/4)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'#main > div > div._1Bj1VS > div.container._2_Y1cV > div.jrLh5s > div.shopee-search-item-result > div.row.shopee-search-item-result__items')))
    except:
        break
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('div', {'class':'col-xs-2-4 shopee-search-item-result__item'})


    print(str(len(products)) + ' products on this page...')
    prod_list = []
    for product in products:
        discount = ''
        try:
            discount = product.find('span', {'class':'percent'}).text
            prod = product_with_discount(discount)
        except:
            Exception()
    
        if len(discount) > 0:
            try:
                name = product.find('div', {'class':'_1NoI8_ _1JBBaM'})
                prod['Name'] = name.text
            except:
                Exception()
            try:
                name = product.find('div', {'class':'_1NoI8_ _16BAGk'})
                prod['Name'] = name.text
            except:
                Exception()
        
            right_item = True
            for word in search:
                if word.lower() not in prod['Name'].lower():
                    right_item = False
            if right_item == False: break

            prices = product.find_all('span', {'class':'_341bF0'})
            if len(prices) == 2:
                prod['Price_lowest'] = 'RM' + prices[0].text
                prod['Price_highest'] = 'RM' + prices[1].text
            else:
                prod['Price_lowest'] = 'RM' + prices[0].text
        
            try:
                link = product.find('a', href=True)
                prod['Link'] = link['href']
                prod_list.append(prod)
            except:
                Exception()
    page += 1
    print('page ' + str(page))
    if page != 5:
        try:
            driver.get(driver.current_url[:-1] +  str(page))
        except:
            break

#pprint.pprint(prod_list)
print(str(len(prod_list)) + ' products found with discounts')
print('The best offer is...')

buy_now = highest_discount(prod_list)
pprint.pprint(buy_now)
try:
    driver.get('https://shopee.com.my/' + buy_now['Link'])
except:
    Exception()
