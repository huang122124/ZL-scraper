import json
import re
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException



TOKEN = ''
parms = {'token':TOKEN}
TARGET = ''
results_per_page = 5
domain_list = []
#domain_list = []
email_url_list = []
#LOG Levels
INFO = 0,
WARNING = 1,
LOG_ERROR = 2,
LOG_FATAL = 3.





#Get all the DNS records stored for a domain.
def get_DNS(domain):
    url = 'https://host.io/api/dns/'+ domain
    r = requests.get(url,params=parms)
    dns = json.loads(r.text).get('a')
    return dns


def get_IP(domain):
    url = 'https://host.io/api/web/' + domain
    r = requests.get(url,params=parms)
    ip = json.loads(r.text).get('ip')
    print("get ip:",ip)
    return ip

def get_domains(ip):
    time = get_Total(ip)//results_per_page   #循环次数
    print("time:",time)
    if time>0:
        i = 0
        while i < time + 1:
            parms = {"limit": 1000, "page": i, "token": TOKEN}
            url = 'https://host.io/api/domains/ip/' + ip
            try:
                r = requests.get(url, params=parms)
                domains = json.loads(r.text).get('domains')
                if len(domains) > 0:
                    for domain in domains:
                        domain_list.append(domain)
                        print("appended "+domain)
            except:
                print('Request failed!')
            finally:
                i = i + 1
    else:
        print("Total equals to 0 !!!")





def get_Total(ip):
    parms_domain = {"token": TOKEN}
    url = 'https://host.io/api/domains/ip/' + ip
    total = 0
    try:
        r = requests.get(url, params=parms_domain)
        total = json.loads(r.text).get('total')
    except :
        print('Request failed!')
    return total

def start():
    ip = get_IP(TARGET)
    get_domains(ip)
    if len(domain_list)>0:
        print(domain_list)
        # 打开浏览器
        # service = Service(executable_path="./chromedriver.exe")
        options = webdriver.ChromeOptions()
        # 忽略证书错误
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--ignore-certificate-errors')
        # 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 忽略 DevTools listening on ws://127.0.0.1... 提示
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        for url in domain_list:
            register_url = 'https://'+url+'/register'
            #register_url = url
            print(time.strftime("%m-%d %H:%M:%S", time.localtime()) + "  Start loading ", register_url)
            try:
                driver.get(register_url)
                locator = (By.LINK_TEXT, '邮箱注册')
                WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located(locator),"")
                # soup=BeautifulSoup(driver.page_source,'html.parser')  #driver.page_source可以获取当前源码，用BeautifulSoup解析网页
                email_url_list.append(driver.current_url)
                print("new site support email registeration --> ", driver.current_url)
            except WebDriverException as e:
                print(e.msg)
                continue
        driver.close()
        print("Finish!!! Found following sites:", email_url_list)




if __name__ == '__main__':
    start()

