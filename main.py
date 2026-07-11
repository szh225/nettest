"""
网络测试工具 - 主程序
"""
from kivy.app import App
from kivy.core.font import FontLoader


class NetTestApp(App):
    def build(self):
        # 使用系统默认字体（支持中文）
        try:
            FontLoader.load_font('sans-serif')
        except:
            pass

        from main_screen import MainScreen
        return MainScreen()


if __name__ == '__main__':
    NetTestApp().run()
