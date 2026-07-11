"""
NetTest - Network Testing Tool
"""
from kivy.app import App


class NetTestApp(App):
    def build(self):
        from kivy.uix.label import Label
        return Label(text='NetTest', font_size='24sp')


if __name__ == '__main__':
    NetTestApp().run()
