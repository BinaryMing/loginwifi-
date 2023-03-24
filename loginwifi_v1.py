from base64 import b64decode, b64encode
from random import randint
from time import sleep
from urllib.parse import quote

from lxml import etree
from pywifi import PyWiFi, const, Profile
from requests import Session, get

import GUI


def set_login_data():
    M_Gui = GUI.m_gui()
    user, password, isp, if_encrypt = M_Gui.get_data()
    _ifs = 1  # 默认保存
    password = quote(password)
    _login_data = f"http://172.21.255.105:801/eportal/?c=Portal&a=login&callback=dr1004&login_method=1" \
                  f"&user_account={user}%40{isp}&user_password={password} "
    return _login_data, _ifs, if_encrypt


def get_login_data(login_data_file='logindata.text'):
    try:
        with open(login_data_file, 'r+', encoding='utf-8') as f:
            f_data = f.read()
            if len(f_data) == 0:
                print('未保存登录信息')
                _login_data, ifs, if_encrypt = set_login_data()
                if if_encrypt:
                    _login_data_e = b64encode(_login_data.encode('utf-8'))
                else:
                    _login_data_e = _login_data.encode('utf-8')
                if ifs == 1:
                    f.write(str(if_encrypt) + _login_data_e.decode('utf-8'))
            else:
                if_en = int(f_data[0])
                if if_en:
                    _login_data = b64decode(f_data[1:].encode('utf-8')).decode('utf-8')
                else:
                    _login_data = f_data[1:]
    except FileNotFoundError:
        f = open(login_data_file, 'w', encoding='utf-8')
        print('未保存登录信息')
        _login_data, ifs, if_encrypt = set_login_data()
        if if_encrypt:
            _login_data_e = b64encode(_login_data.encode('utf-8'))
        else:
            _login_data_e = _login_data.encode('utf-8')
        if ifs == 1:
            f.write(str(if_encrypt) + _login_data_e.decode('utf-8'))
        f.close()
    return _login_data


def if_connect_web():
    try:
        get('https://www.baidu.com/', timeout=2)
        return True
    except:
        return False


class connect_wifi_tools:
    def __init__(self, _wifi_ssid):
        self.tmp_profile = None
        self.wifi_ssid = _wifi_ssid
        wifi = PyWiFi()  # 创建一个无线对象
        self.net_card = wifi.interfaces()[0]  # 取一个无限网卡
        profile = Profile()
        profile.ssid = self.wifi_ssid  # wifi名称
        self.tmp_profile = self.net_card.add_network_profile(profile)  # 加载配置文件

    def if_connect_wifi(self):
        return self.net_card.status() == const.IFACE_CONNECTED

    def if_connect_school_wifi(self):
        try:
            return self.net_card.scan_results()[0].ssid == self.wifi_ssid
        except:
            return False

    def wifi_disconnect(self):
        self.net_card.disconnect()  # 断开网卡连接

    def connect_wifi(self):
        self.net_card.disconnect()
        i = 0
        while self.if_connect_wifi() is False:
            self.net_card.connect(self.tmp_profile)  # 连接
            sleep(2)  # 等待2秒后看下是否成功连接了
            i += 1
            if i == 30:
                input('扫描不到ECUT_STUD,请到信号好的位置后按回车运行')  # 连接10次，若无法连接则用input暂停程序
        print('ECUT_STUD连接成功')

    def login_school_wifi(self, _head, _login_data):
        data_page = None
        url_1 = 'http://172.21.255.105/'
        s = Session()

        data_page = s.get(url=url_1, headers=_head, timeout=2)
        v = ''
        for i in range(4):
            v += str(randint(0, 9))
        # try:
        print(data_page.status_code)
        data_page_html_tree = etree.HTML(data_page.text)
        # except:
        #     self.connect_wifi()
        #     self.login_school_wifi(_head, _login_data)
        try:
            now_ip = data_page_html_tree.xpath('/html/head/script[1]/text()')[0].split(';')[6].split('\'')[
                1]  # 获取本次连接ip
        except IndexError:
            now_ip = data_page_html_tree.xpath('/html/head/script[1]/text()')[0].split(';')[13].split('\'')[1]
        url_2 = _login_data + f'&wlan_user_ip={now_ip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name' \
                              f'=&jsVersion=3' \
                              f'.3.3&v={v}'
        while if_connect_web() is False:
            s.get(url=url_2, headers=_head)
            sleep(0.5)
        print('登录成功')
        s.close()
        print('按回车键或者关闭窗口以退出')


if __name__ == '__main__':
    login_data = get_login_data()
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 '
                      'Safari/537.36 SLBrowser/7.0.0.12151 SLBChan/103 '
    }
    wifi_ssid = "ECUT_STUD"
    connect_wifi_tool = connect_wifi_tools(wifi_ssid)
    while True:
        if if_connect_web() is False:
            if connect_wifi_tool.if_connect_school_wifi() and connect_wifi_tool.if_connect_wifi():
                try:
                    connect_wifi_tool.login_school_wifi(head, login_data)
                except:
                    pass
            else:
                try:
                    connect_wifi_tool.connect_wifi()
                    connect_wifi_tool.login_school_wifi(head, login_data)
                except:
                    pass
        else:
            sleep(5)
