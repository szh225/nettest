"""
网络测试工具 - 主界面（逐步添加功能）
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

        # 标题
        self.add_widget(Label(
            text='NetTest 网络测试工具',
            font_size='24sp',
            bold=True,
            size_hint_y=None,
            height=50
        ))

        # Ping 按钮
        btn_ping = Button(text='Ping 测试', font_size='18sp', size_hint_y=None, height=50)
        btn_ping.bind(on_press=self.on_ping)
        self.add_widget(btn_ping)

        # Tracert 按钮
        btn_tracert = Button(text='Tracert 测试', font_size='18sp', size_hint_y=None, height=50)
        btn_tracert.bind(on_press=self.on_tracert)
        self.add_widget(btn_tracert)

        # Telnet 按钮
        btn_telnet = Button(text='Telnet 测试', font_size='18sp', size_hint_y=None, height=50)
        btn_telnet.bind(on_press=self.on_telnet)
        self.add_widget(btn_telnet)

        # SSH 按钮
        btn_ssh = Button(text='SSH 测试', font_size='18sp', size_hint_y=None, height=50)
        btn_ssh.bind(on_press=self.on_ssh)
        self.add_widget(btn_ssh)

        # 结果展示区域
        self.result_label = Label(
            text='点击按钮开始测试',
            font_size='16sp',
            size_hint_y=None,
            height=100
        )
        self.add_widget(self.result_label)

    def on_ping(self, instance):
        self.result_label.text = 'Ping 测试功能开发中...'

    def on_tracert(self, instance):
        self.result_label.text = 'Tracert 测试功能开发中...'

    def on_telnet(self, instance):
        self.result_label.text = 'Telnet 测试功能开发中...'

    def on_ssh(self, instance):
        self.result_label.text = 'SSH 测试功能开发中...'


def build():
    return MainScreen()
