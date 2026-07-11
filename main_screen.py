"""
网络测试工具 - 主界面（带日志查看功能）
"""
import os
import traceback

LOG_DIR = os.path.join(os.environ.get('HOME', '/'), '.nettest')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'nettest.log')

def log(msg):
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(str(msg) + '\n')
    except:
        pass

from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class LogViewer(BoxLayout):
    """日志查看页面"""
    def __init__(self, log_file, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.log_file = log_file

        # 标题
        title = Label(text='=== 启动日志 ===', font_size=16, bold=True, size_hint_y=None, height=30)
        self.add_widget(title)

        # 日志内容（可滚动）
        scroll = ScrollView(size_hint=(1, 0.85))
        self.log_label = Label(
            text='加载中...',
            font_size=12,
            halign='left',
            valign='top',
            markup=False,
            size_hint_y=None
        )
        self.log_label.bind(text=lambda *args: setattr(self.log_label, 'height', max(100, len(self.log_label.text) * 0.5)))
        scroll.add_widget(self.log_label)
        self.add_widget(scroll)

        # 刷新按钮
        refresh_btn = Button(text='刷新日志', size_hint_y=None, height=40)
        refresh_btn.bind(on_press=self.refresh_log)
        self.add_widget(refresh_btn)

        self.refresh_log()

    def refresh_log(self, *args):
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.log_label.text = content
            else:
                self.log_label.text = '日志文件不存在'
        except Exception as e:
            self.log_label.text = f'读取失败: {e}'


class MainScreen(TabbedPanel):
    def __init__(self, log_file=None, **kwargs):
        log("MainScreen.__init__ called")
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.tab_height = 40
        self.tab_font_size = 14
        self.log_file = log_file or LOG_FILE

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

            # 添加日志查看 Tab
            log("Adding LogViewer tab")
            self.add_widget(TabbedPanelItem(text='日志', child=LogViewer(self.log_file)))
            log("LogViewer tab added")

            log("All tabs loaded successfully")
        except Exception as e:
            log(f"Failed to load tabs: {e}")
            log(traceback.format_exc())
            raise
