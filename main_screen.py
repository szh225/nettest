"""
网络测试工具 - 主界面
"""
import os
import traceback

LOG_FILE = os.path.join(os.environ.get('HOME', '/'), 'nettest.log')

def log(msg):
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(str(msg) + '\n')
    except:
        pass

from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem


class MainScreen(TabbedPanel):
    def __init__(self, **kwargs):
        log("MainScreen.__init__ called")
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.tab_height = 40
        self.tab_font_size = 14

        try:
            log("Importing PingTestWidget")
            from ping_test import PingTestWidget
            self.add_widget(TabbedPanelItem(text='Ping', child=PingTestWidget()))
            log("Ping tab added")

            log("Importing TracertTestWidget")
            from tracert_test import TracertTestWidget
            self.add_widget(TabbedPanelItem(text='Tracert', child=TracertTestWidget()))
            log("Tracert tab added")

            log("Importing TelnetTestWidget")
            from telnet_test import TelnetTestWidget
            self.add_widget(TabbedPanelItem(text='Telnet', child=TelnetTestWidget()))
            log("Telnet tab added")

            log("Importing SSHTestWidget")
            from ssh_test import SSHTestWidget
            self.add_widget(TabbedPanelItem(text='SSH', child=SSHTestWidget()))
            log("SSH tab added")

            log("All tabs loaded successfully")
        except Exception as e:
            log(f"Failed to load tabs: {e}")
            log(traceback.format_exc())
            raise
