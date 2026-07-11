"""
网络测试工具 - 主界面
包含 Tab 切换：Ping / Tracert / Telnet / SSH
"""
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

from ping_test import PingTestWidget
from tracert_test import TracertTestWidget
from telnet_test import TelnetTestWidget
from ssh_test import SSHTestWidget


class MainScreen(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.tab_height = '40dp'
        self.tab_font_size = '14sp'

        # 添加各个测试 Tab
        self.add_widget(TabbedPanelItem(text='📡 Ping', child=PingTestWidget()))
        self.add_widget(TabbedPanelItem(text='🔍 Tracert', child=TracertTestWidget()))
        self.add_widget(TabbedPanelItem(text='🔌 Telnet', child=TelnetTestWidget()))
        self.add_widget(TabbedPanelItem(text='🔐 SSH', child=SSHTestWidget()))
