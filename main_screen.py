"""
网络测试工具 - 主界面（完整功能版）
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import subprocess
import socket
import threading


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10

        # 标题
        title = Label(
            text='NetTest Tool v1.0',
            font_size='22sp',
            bold=True,
            size_hint=(1, None),
            height=50
        )
        self.add_widget(title)

        # 按钮容器 - 增加高度
        btn_box = BoxLayout(
            orientation='vertical',
            spacing=12,
            size_hint=(1, None),
            height=280  # 4 buttons * 70 height
        )

        btn_ping = Button(text='[ Ping Test ]', font_size='18sp', size_hint_y=None, height=70, background_color=[0.2, 0.6, 0.2, 1])
        btn_ping.bind(on_press=self.show_ping_popup)
        btn_box.add_widget(btn_ping)

        btn_tracert = Button(text='[ Tracert Test ]', font_size='18sp', size_hint_y=None, height=70, background_color=[0.2, 0.2, 0.6, 1])
        btn_tracert.bind(on_press=self.show_tracert_popup)
        btn_box.add_widget(btn_tracert)

        btn_telnet = Button(text='[ Telnet Test ]', font_size='18sp', size_hint_y=None, height=70, background_color=[0.6, 0.2, 0.2, 1])
        btn_telnet.bind(on_press=self.show_telnet_popup)
        btn_box.add_widget(btn_telnet)

        btn_ssh = Button(text='[ SSH Test ]', font_size='18sp', size_hint_y=None, height=70, background_color=[0.5, 0.5, 0.2, 1])
        btn_ssh.bind(on_press=self.show_ssh_popup)
        btn_box.add_widget(btn_ssh)

        self.add_widget(btn_box)

        # 结果展示区域
        self.result_label = Label(
            text='Ready. Tap a button to start test.',
            font_size='14sp',
            size_hint=(1, 1),
            halign='left',
            valign='top'
        )
        self.add_widget(self.result_label)

    # ============ Ping 测试 ============
    def show_ping_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='IP / Host:', size_hint_y=None, height=30))
        ip_input = TextInput(hint_text='e.g. 8.8.8.8', multiline=False, font_size='16sp')
        content.add_widget(ip_input)
        
        btn = Button(text='Start Ping', size_hint_y=None, height=50)
        btn.bind(on_press=lambda x: self.do_ping(ip_input.text, popup))
        content.add_widget(btn)

        popup = Popup(title='Ping Test', content=content, size_hint=(0.8, 0.4))
        popup.open()

    def do_ping(self, ip, popup):
        popup.dismiss()
        self.result_label.text = 'Pinging ' + ip + '...\n\nRunning...'
        
        def run():
            try:
                result = subprocess.run(['ping', '-c', '4', ip], capture_output=True, text=True, timeout=10)
                output = result.stdout + result.stderr
                Clock.schedule_once(lambda dt: self.show_result(output, 'Ping'))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_result('Error: ' + str(e), 'Ping'))
        
        threading.Thread(target=run, daemon=True).start()

    # ============ Tracert 测试 ============
    def show_tracert_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='IP / Host:', size_hint_y=None, height=30))
        ip_input = TextInput(hint_text='e.g. 8.8.8.8', multiline=False, font_size='16sp')
        content.add_widget(ip_input)
        
        btn = Button(text='Start Tracert', size_hint_y=None, height=50)
        btn.bind(on_press=lambda x: self.do_tracert(ip_input.text, popup))
        content.add_widget(btn)

        popup = Popup(title='Tracert Test', content=content, size_hint=(0.8, 0.4))
        popup.open()

    def do_tracert(self, ip, popup):
        popup.dismiss()
        self.result_label.text = 'Tracing route to ' + ip + '...\n\nRunning...'
        
        def run():
            try:
                result = subprocess.run(['traceroute', ip, '-m', '10'], capture_output=True, text=True, timeout=30)
                output = result.stdout + result.stderr
                Clock.schedule_once(lambda dt: self.show_result(output, 'Tracert'))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_result('Error: ' + str(e), 'Tracert'))
        
        threading.Thread(target=run, daemon=True).start()

    # ============ Telnet 测试 ============
    def show_telnet_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='IP / Host:', size_hint_y=None, height=30))
        ip_input = TextInput(hint_text='e.g. 192.168.1.1', multiline=False, font_size='16sp')
        content.add_widget(ip_input)
        
        content.add_widget(Label(text='Port:', size_hint_y=None, height=30))
        port_input = TextInput(hint_text='e.g. 23', text='23', multiline=False, font_size='16sp')
        content.add_widget(port_input)
        
        btn = Button(text='Start Telnet', size_hint_y=None, height=50)
        btn.bind(on_press=lambda x: self.do_telnet(ip_input.text, port_input.text, popup))
        content.add_widget(btn)

        popup = Popup(title='Telnet Test', content=content, size_hint=(0.8, 0.5))
        popup.open()

    def do_telnet(self, ip, port, popup):
        popup.dismiss()
        self.result_label.text = 'Testing Telnet ' + ip + ':' + port + '...\n\nRunning...'
        
        def run():
            try:
                port_num = int(port)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((ip, port_num))
                sock.close()
                if result == 0:
                    msg = 'SUCCESS!\n\n' + ip + ':' + str(port_num) + ' is OPEN\nTelnet connection established.'
                else:
                    msg = 'FAILED!\n\n' + ip + ':' + str(port_num) + ' is CLOSED\nCannot establish Telnet connection.'
                Clock.schedule_once(lambda dt: self.show_result(msg, 'Telnet'))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_result('Error: ' + str(e), 'Telnet'))
        
        threading.Thread(target=run, daemon=True).start()

    # ============ SSH 测试 ============
    def show_ssh_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='IP / Host:', size_hint_y=None, height=30))
        ip_input = TextInput(hint_text='e.g. 192.168.1.1', multiline=False, font_size='16sp')
        content.add_widget(ip_input)
        
        content.add_widget(Label(text='Port:', size_hint_y=None, height=30))
        port_input = TextInput(hint_text='e.g. 22', text='22', multiline=False, font_size='16sp')
        content.add_widget(port_input)
        
        btn = Button(text='Start SSH', size_hint_y=None, height=50)
        btn.bind(on_press=lambda x: self.do_ssh(ip_input.text, port_input.text, popup))
        content.add_widget(btn)

        popup = Popup(title='SSH Test', content=content, size_hint=(0.8, 0.5))
        popup.open()

    def do_ssh(self, ip, port, popup):
        popup.dismiss()
        self.result_label.text = 'Testing SSH ' + ip + ':' + port + '...\n\nRunning...'
        
        def run():
            try:
                port_num = int(port)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((ip, port_num))
                sock.close()
                if result == 0:
                    msg = 'SUCCESS!\n\n' + ip + ':' + str(port_num) + ' is OPEN\nSSH port is reachable.'
                else:
                    msg = 'FAILED!\n\n' + ip + ':' + str(port_num) + ' is CLOSED\nSSH port is not reachable.'
                Clock.schedule_once(lambda dt: self.show_result(msg, 'SSH'))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_result('Error: ' + str(e), 'SSH'))
        
        threading.Thread(target=run, daemon=True).start()

    # ============ 通用结果显示 ============
    def show_result(self, output, test_type):
        max_len = 2000
        if len(output) > max_len:
            output = output[:max_len] + '\n\n... (truncated)'
        self.result_label.text = '[' + test_type + ' Result]\n\n' + output
