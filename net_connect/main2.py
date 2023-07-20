from selenium import webdriver
import time
import os
import requests
import re

class Login:
    # 初始化
    def __init__(self, name, key, driver_path):
        # 检测间隔时间，单位为秒
        self.every = 60
        self.user_name = name
        self.key = key
        self.driver_path = driver_path

    # 模拟登录
    def login(self):
        print(self.getCurrentTime(), u"拼命连网中...")
        try:
            driver = webdriver.Edge(self.driver_path)
            driver.maximize_window()
            driver.get('http://192.168.200.2/')
            flag = True
            try:
                driver.find_element_by_xpath('//*[@id="edit_body"]/div[3]/div[1]/div/div[2]/div[1]/div/div[5]/span[3]/input')
            except Exception:
                flag = False
            if flag:
                driver.find_element_by_xpath('//*[@id="edit_body"]/div[3]/div[1]/div/div[2]/div[1]/div/div[5]/span[3]/input').click()
                driver.find_element_by_xpath('//*[@id="edit_body"]/div[3]/div[1]/div/div[2]/div[1]/div/form/input[3]').send_keys(self.user_name)
                driver.find_element_by_xpath('//*[@id="edit_body"]/div[3]/div[1]/div/div[2]/div[1]/div/form/input[4]').send_keys(self.key)
                driver.find_element_by_xpath('//*[@id="edit_body"]/div[3]/div[1]/div/div[2]/div[1]/div/form/input[2]').click()
                time.sleep(1)
                driver.close()
                print(u'连接成功...')
        except Exception:
            print(u'连接失败...')

    # 判断当前是否可以连网
    def canConnect(self):
        try:
            q = requests.get("http://www.baidu.com", timeout=5)
            m = re.search(r'STATUS OK', q.text)
            if m:
                return True
            else:
                return False
        except:
            print('error')
            return False

    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    # 主函数
    def main(self):
        print(self.getCurrentTime(), u"Hi，欢迎使用自动登陆系统")
        while True:
            while True:
                can_connect = self.canConnect()
                if not can_connect:
                    print(self.getCurrentTime(), u"断网了...")
                    self.login()
                else:
                    print(self.getCurrentTime(), u"一切正常...")
                time.sleep(self.every)
            time.sleep(self.every)


if __name__ == '__main__':
    if os.path.exists('./user.txt') and os.path.exists('./driver.txt'):
        user = open('./user.txt', 'r').readlines()
        driver = open('./driver.txt', 'r').readline().strip('\n')
        name = user[0].strip('\n')
        key = user[1].strip('\n')
        print('User name:', name)
        print('Key:', key)
        print('检测间隔:60(s)')
        if os.path.exists(driver):
            login = Login(name, key, driver)
            login.main()
        else:
            raise Exception('ERROR(1): Edge driver is not ready.')
    else:
        raise Exception('ERROR(0): The configuration files are not exist.')


