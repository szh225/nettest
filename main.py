"""
网络测试工具 - 主程序入口
支持 Ping, Tracert, Telnet, SSH 测试
"""
from kivy.app import App
from kivy.utils import platform

from main_screen import MainScreen


class NetTestApp(App):
    def build(self):
        self.title = '网络测试工具'
        self.root = MainScreen()
        return self.root


if __name__ == '__main__':
    NetTestApp().run()
