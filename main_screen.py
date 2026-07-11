"""
网络测试工具 - 主界面
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # 标题
        title = Label(
            text='NetTest',
            font_size='24sp',
            size_hint=(1, None),
            height=50
        )
        self.add_widget(title)

        # Ping 按钮
        btn_ping = Button(text='Ping', size_hint=(1, None), height=50)
        btn_ping.bind(on_press=self.on_ping)
        self.add_widget(btn_ping)

        # Tracert 按钮
        btn_tracert = Button(text='Tracert', size_hint=(1, None), height=50)
        btn_tracert.bind(on_press=self.on_tracert)
        self.add_widget(btn_tracert)

        # Telnet 按钮
        btn_telnet = Button(text='Telnet', size_hint=(1, None), height=50)
        btn_telnet.bind(on_press=self.on_telnet)
        self.add_widget(btn_telnet)

        # SSH 按钮
        btn_ssh = Button(text='SSH', size_hint=(1, None), height=50)
        btn_ssh.bind(on_press=self.on_ssh)
        self.add_widget(btn_ssh)

        # 结果
        self.result_label = Label(
            text='Ready',
            size_hint=(1, 1)
        )
        self.add_widget(self.result_label)

    def on_ping(self, instance):
        self.result_label.text = 'Ping test'

    def on_tracert(self, instance):
        self.result_label.text = 'Tracert test'

    def on_telnet(self, instance):
        self.result_label.text = 'Telnet test'

    def on_ssh(self, instance):
        self.result_label.text = 'SSH test'
