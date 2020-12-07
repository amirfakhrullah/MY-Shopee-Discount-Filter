from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from bs4 import BeautifulSoup


def product_with_discount(discount):
    prod = {
        'Discount': '',
        'Name': '',
        'Price_lowest': '',
        'Price_highest': '',
        'Link': ''
    }

    prod['Discount'] = discount
    return prod