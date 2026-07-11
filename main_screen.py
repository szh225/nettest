"""
网络测试工具 - 极简主界面
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        self.add_widget(Label(text='NetTest 网络测试工具', font_size='24sp', bold=True, size_hint_y=None, height=50))

        btn_ping = Button(text='Ping 测试', font_size='18sp')
        btn_ping.bind(on_press=lambda x: self.show_result('Ping 功能开发中...'))
        self.add_widget(btn_ping)

        btn_tracert = Button(text='Tracert 测试', font_size='18sp')
        btn_tracert.bind(on_press=lambda x: self.show_result('Tracert 功能开发中...'))
        self.add_widget(btn_tracert)

        btn_telnet = Button(text='Telnet 测试', font_size='18sp')
        btn_telnet.bind(on_press=lambda x: self.show_result('Telnet 功能开发中...'))
        self.add_widget(btn_telnet)

        btn_ssh = Button(text='SSH 测试', font_size='18sp')
        btn_ssh.bind(on_press=lambda x: self.show_result('SSH 功能开发中...'))
        self.add_widget(btn_ssh)

        self.result_label = Label(text='点击按钮开始测试', font_size='16sp', size_hint_y=None, height=50)
        self.add_widget(self.result_label)

    def show_result(self, text):
        self.result_label.text = text


def build():
    return MainScreen()
