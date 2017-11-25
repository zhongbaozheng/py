# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 11:39:42 2016

@author: Administrator
"""

import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests

# 直接登陆新浪微博
url = 'http://weibo.com/login.php'
binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary,executable_path='D:/py/selenium/geckodriver.exe')
driver.get(url)
print('开始登陆')

# 定位到账号密码表单
login_tpye = driver.find_element_by_class_name('info_header').find_element_by_xpath('//a[2]')
login_tpye.click()
time.sleep(3)

name_field = driver.find_element_by_id('loginname')
name_field.clear()
name_field.send_keys('weizongchensipu@163.com')

password_field = driver.find_element_by_class_name('password').find_element_by_name('password')
password_field.clear()
password_field.send_keys('tttt5555')


submit = driver.find_element_by_class_name('W_login_form').find_element_by_link_text('登录')
submit.click()

# 等待页面刷新，完成登陆
time.sleep(5)
print('登陆完成')
sina_cookies = driver.get_cookies()

cookie = [item["name"] + "=" + item["value"] for item in sina_cookies]
cookiestr = '; '.join(item for item in cookie)

# 验证cookie是否有效
driver.get('http://weibo.com/p/1005051921017243/info?mod=pedit_more')
"""
redirect_url = 'http://weibo.com/p/1005051921017243/info?mod=pedit_more'
headers = {'cookie': cookiestr}
html = requests.get(redirect_url, headers=headers).text
print(html)
"""