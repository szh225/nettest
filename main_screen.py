"""
网络测试工具 - 主界面
包含 Tab 切换：Ping / Tracert / Telnet / SSH
"""
import traceback
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.logger import Logger


class MainScreen(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.tab_height = '40dp'
        self.tab_font_size = '14sp'

        try:
            Logger.info("MainScreen: Loading PingTestWidget")
            from ping_test import PingTestWidget
            self.add_widget(TabbedPanelItem(text='Ping', child=PingTestWidget()))
            
            Logger.info("MainScreen: Loading TracertTestWidget")
            from tracert_test import TracertTestWidget
            self.add_widget(TabbedPanelItem(text='Tracert', child=TracertTestWidget()))
            
            Logger.info("MainScreen: Loading TelnetTestWidget")
            from telnet_test import TelnetTestWidget
            self.add_widget(TabbedPanelItem(text='Telnet', child=TelnetTestWidget()))
            
            Logger.info("MainScreen: Loading SSHTestWidget")
            from ssh_test import SSHTestWidget
            self.add_widget(TabbedPanelItem(text='SSH', child=SSHTestWidget()))
            
            Logger.info("MainScreen: All tabs loaded successfully")
        except Exception as e:
            Logger.error(f"MainScreen: Failed to load tabs: {e}")
            Logger.error(traceback.format_exc())
            raise
