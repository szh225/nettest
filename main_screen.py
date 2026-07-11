"""
网络测试工具 - 主界面
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # 标题 - 使用英文避免字体问题
        title = Label(
            text='NetTest Tool',
            font_size='24sp',
            bold=True,
            size_hint=(1, None),
            height=50
        )
        self.add_widget(title)

        # 按钮容器
        btn_box = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(1, None),
            height=200  # 4 buttons * 50 height
        )

        btn_ping = Button(text='[Ping Test]', font_size='18sp', size_hint_y=None, height=50)
        btn_ping.bind(on_press=self.on_ping)
        btn_box.add_widget(btn_ping)

        btn_tracert = Button(text='[Tracert Test]', font_size='18sp', size_hint_y=None, height=50)
        btn_tracert.bind(on_press=self.on_tracert)
        btn_box.add_widget(btn_tracert)

        btn_telnet = Button(text='[Telnet Test]', font_size='18sp', size_hint_y=None, height=50)
        btn_telnet.bind(on_press=self.on_telnet)
        btn_box.add_widget(btn_telnet)

        btn_ssh = Button(text='[SSH Test]', font_size='18sp', size_hint_y=None, height=50)
        btn_ssh.bind(on_press=self.on_ssh)
        btn_box.add_widget(btn_ssh)

        self.add_widget(btn_box)

        # 结果展示区域 - 使用 ScrollView 填充剩余空间
        scroll = ScrollView(size_hint=(1, 1))
        self.result_label = Label(
            text='Tap a button to start test...',
            font_size='14sp',
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        scroll.add_widget(self.result_label)
        self.add_widget(scroll)

    def on_ping(self, instance):
        self.result_label.text = 'Ping test...\n\nFeature coming soon.'

    def on_tracert(self, instance):
        self.result_label.text = 'Tracert test...\n\nFeature coming soon.'

    def on_telnet(self, instance):
        self.result_label.text = 'Telnet test...\n\nFeature coming soon.'

    def on_ssh(self, instance):
        self.result_label.text = 'SSH test...\n\nFeature coming soon.'
