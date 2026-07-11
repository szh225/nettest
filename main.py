"""
网络测试工具 - 主程序
"""
from kivy.app import App
from kivy.utils import platform


class NetTestApp(App):
    def build(self):
        from main_screen import MainScreen
        return MainScreen()


if __name__ == '__main__':
    NetTestApp().run()
