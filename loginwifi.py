from pywifi import PyWiFi, const, Profile
from time import sleep
from requests import Session
from lxml import etree
from random import randint
from urllib.parse import quote
from sys import executable


def get_which():
    w = input('请选择您的运营商：\n1、中国移动\n2、中国联通\n3、中国电信\n')
    try:
        w = int(w)
    except ValueError:
        print('输入有误,请重新选择运营商')
        get_which()
    which = '-1'
    if w == 1:
        which = 'cmcc'
    elif w == 2:
        which = 'unicom'
    elif w == 3:
        which = 'telecom'

    return which


def get_user():
    user = input('请输入您的账号：')
    try:
        user = int(user)
    except ValueError:
        print('账号输入非纯数字请重新输入')
        get_user()
    return user


def get_ifs():
    _ifs = input('是否要保存登录内容？(如果保存以后登录自动都将使用本次登录信息)\n1、是\n2、否\n')
    try:
        _ifs = int(_ifs)
    except ValueError:
        print('输入有误请重新选择')
        get_ifs()
    return _ifs


def set_login_data():
    user = get_user()
    password_table = input('请输入您的密码：')
    password = quote(password_table)
    which = get_which()

    _ifs = get_ifs()
    _login_data = f"http://172.21.255.105:801/eportal/?c=Portal&a=login&callback=dr1004&login_method=1" \
                  f"&user_account={user}%40{which}&user_password={password} "
    return _login_data, _ifs


# exe_path = executable
# b = exe_path.split('\\')
# b.pop()
# f_path = '\\'.join(b)+'\\'+'logindata.text'

try:
    with open('logindata.text', 'r+', encoding='utf-8') as f:
        t = f.read()
        if len(t) == 0:
            print('未保存登录信息')
            login_data, ifs = set_login_data()
            if ifs == 1:
                f.write(login_data)
            t = login_data
        f.close()
except FileNotFoundError:
    f = open('logindata.text', 'w', encoding='utf-8')
    print('未保存登录信息')
    login_data, ifs = set_login_data()
    if ifs == 1:
        f.write(login_data)
    t = login_data
    f.close()

wifi = PyWiFi()  # 创建一个无线对象
ifaces = wifi.interfaces()[0]  # 取一个无限网卡
ifaces.disconnect()  # 断开网卡连接
sleep(0.5)  # 缓冲0.5秒
i = 0
while ifaces.status() != const.IFACE_CONNECTED:
    profile = Profile()  # 配置文件
    profile.ssid = "ECUT_STUD"  # wifi名称
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件
    ifaces.connect(tmp_profile)  # 连接
    sleep(0.5)  # 等待0.5秒后看下是否成功连接了
    i += 1
    if i == 10:
        raise Exception('扫描不到ECUT_STUD,请到信号好的位置再运行')  # 连接10次，若无法连接则抛出错误
print('ECUT_STUD连接成功')

s = Session()
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 '
                  'Safari/537.36 SLBrowser/7.0.0.12151 SLBChan/103 '
}
url_1 = 'http://172.21.255.105/'
data_page = s.get(url=url_1, headers=head)
v = ''
for i in range(4):
    v += f'{randint(0, 9)}'
data_page_html_tree = etree.HTML(data_page.text)
try:
    now_ip = data_page_html_tree.xpath('/html/head/script[1]/text()')[0].split(';')[6].split('\'')[1]  # 获取本次连接ip
except IndexError:
    now_ip = data_page_html_tree.xpath('/html/head/script[1]/text()')[0].split(';')[13].split('\'')[1]
url_2 = t + f'&wlan_user_ip={now_ip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3' \
            f'.3.3&v={v}'
p = s.get(url=url_2, headers=head)
if p.status_code == 200:
    print('登录成功')
s.close()
print('按回车键或者关闭窗口以退出')
input()
