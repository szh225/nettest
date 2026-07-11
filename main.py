"""
网络测试工具 - 主程序入口
支持 Ping, Tracert, Telnet, SSH 测试
"""
import traceback
import sys

from kivy.app import App
from kivy.utils import platform
from kivy.logger import Logger


class NetTestApp(App):
    def build(self):
        try:
            Logger.info(f"NetTest: Starting on {platform}")
            from main_screen import MainScreen
            self.title = 'NetTest'
            self.root = MainScreen()
            Logger.info("NetTest: MainScreen created successfully")
            return self.root
        except Exception as e:
            Logger.error(f"NetTest: Failed to build app: {e}")
            Logger.error(traceback.format_exc())
            raise


if __name__ == '__main__':
    try:
        NetTestApp().run()
    except Exception as e:
        print(f"FATAL: {e}")
        print(traceback.format_exc())
        sys.exit(1)
