from tkinter import Label, Tk, Entry, StringVar, IntVar, Radiobutton, Button


def set_y_value(n):
    y_start = 40
    y_interval = 30
    return y_start + n * y_interval


class m_gui:
    def __init__(self):
        self.user_name = None
        self.password = None
        self.isp = None
        self.if_encrypt = None
        self.win = Tk()
        self.win.title('登录')
        # 设置窗口宽度和高度
        self.win.geometry('330x220')

        # label_height, label_width =

        Label(text='账号:').place(x=50, y=set_y_value(0))
        self._user_name = Entry(self.win)
        self._user_name.place(x=100, y=set_y_value(0))

        Label(text='密码:').place(x=50, y=set_y_value(1))
        # 使用show="*"，在文本框输入的内容就全部显示为*
        self.pwd = Entry(self.win, show='*')
        self.pwd.place(x=100, y=set_y_value(1))

        isp_dict = {
            'cmcc': '移动',
            'unicom': '联通',
            'telecom': '电信'
        }
        self._isp = StringVar()
        n = 0
        for key in isp_dict:
            Radiobutton(self.win, text=isp_dict[key], variable=self._isp, value=key).place(x=60 + 80 * n,
                                                                                           y=set_y_value(2))
            n += 1

        if_encrypts = [(0, '数据不加密'), (1, '数据加密')]
        self._if_encrypt = IntVar()
        for index, v in if_encrypts:
            Radiobutton(self.win, text=v, variable=self._if_encrypt, value=index).place(x=60 + 120 * index,
                                                                                        y=set_y_value(3))

        # 创建注册按钮，点击按钮时调用register函数
        Button(text='登录', command=self.register).place(x=100, y=180, width=190)
        self.win.mainloop()

    def register(self):
        self.user_name = self._user_name.get()
        self.password = self.pwd.get()
        self.isp = self._isp.get()
        self.if_encrypt = self._if_encrypt.get()
        self.win.destroy()

    def get_data(self):
        return self.user_name, self.password, self.isp, self.if_encrypt
