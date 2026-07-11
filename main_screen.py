"""
网络测试工具 - 主界面（完整功能版 v2）
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import socket
import threading
import os


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 5

        # 标题 - 固定在最上方
        title = Label(
            text='NetTest Tool v1.0',
            font_size='20sp',
            bold=True,
            size_hint=(1, None),
            height=45
        )
        self.add_widget(title)

        # 分隔线
        sep = Label(text='─' * 40, size_hint=(1, None), height=10)
        self.add_widget(sep)

        # 按钮容器 - 再增加50%高度 (70 * 1.5 = 105px)
        btn_box = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(1, None),
            height=460  # 4 buttons * 105 + spacing
        )

        btn_ping = Button(text='[ Ping Test ]', font_size='18sp', size_hint_y=None, height=105)
        btn_ping.bind(on_press=self.show_ping_popup)
        btn_box.add_widget(btn_ping)

        btn_tracert = Button(text='[ Tracert Test ]', font_size='18sp', size_hint_y=None, height=105)
        btn_tracert.bind(on_press=self.show_tracert_popup)
        btn_box.add_widget(btn_tracert)

        btn_telnet = Button(text='[ Telnet Test ]', font_size='18sp', size_hint_y=None, height=105)
        btn_telnet.bind(on_press=self.show_telnet_popup)
        btn_box.add_widget(btn_telnet)

        btn_ssh = Button(text='[ SSH Test ]', font_size='18sp', size_hint_y=None, height=105)
        btn_ssh.bind(on_press=self.show_ssh_popup)
        btn_box.add_widget(btn_ssh)

        self.add_widget(btn_box)

        # 分隔线
        sep2 = Label(text='─' * 40, size_hint=(1, None), height=10)
        self.add_widget(sep2)

        # 结果展示区域 - 填充剩余空间
        self.result_label = Label(
            text='Ready. Tap a button to start test.',
            font_size='13sp',
            size_hint=(1, 1),
            halign='left',
            valign='top'
        )
        self.add_widget(self.result_label)

    # ============ Popup 创建 ============
    def create_popup(self, title, fields, btn_text, callback):
        """通用 Popup 创建方法"""
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        inputs = []
        for field in fields:
            content.add_widget(Label(text=field['label'], size_hint_y=None, height=30, font_size='15sp'))
            inp = TextInput(
                hint_text=field.get('hint', ''),
                text=field.get('default', ''),
                multiline=False,
                font_size='16sp'
            )
            inputs.append(inp)
            content.add_widget(inp)
        
        btn = Button(text=btn_text, size_hint_y=None, height=55, font_size='18sp')
        
        def on_press(instance):
            values = [inp.text.strip() for inp in inputs]
            popup.dismiss()
            callback(values)
        
        btn.bind(on_press=on_press)
        content.add_widget(btn)

        popup = Popup(title=title, content=content, size_hint=(0.85, None), height=250)
        popup.open()

    # ============ Ping 测试 ============
    def show_ping_popup(self, instance):
        def callback(values):
            ip = values[0]
            if not ip:
                self.result_label.text = '[Ping] Error: IP/Host cannot be empty!'
                return
            self.do_ping(ip)
        
        self.create_popup(
            'Ping Test',
            [{'label': 'IP / Host:', 'hint': 'e.g. 8.8.8.8'}],
            'Start Ping',
            callback
        )

    def do_ping(self, ip):
        self.result_label.text = '[Ping] Testing ' + ip + '...\n\nPlease wait...'
        
        def run():
            try:
                # 使用 Python socket 实现 ping（ICMP 需要 root，用 TCP 替代）
                output = self.ping_using_socket(ip)
                Clock.schedule_once(lambda dt: self.show_result(output, 'Ping'))
            except Exception as e:
                import traceback
                err_msg = traceback.format_exc()
                Clock.schedule_once(lambda dt: self.show_result('Error:\n' + err_msg, 'Ping'))
        
        threading.Thread(target=run, daemon=True).start()

    def ping_using_socket(self, ip):
        """使用 TCP socket 模拟 ping（不需要 root 权限）"""
        import time
        
        # 尝试解析主机名
        try:
            resolved_ip = socket.gethostbyname(ip)
        except socket.gaierror:
            return '[Ping] FAILED\n\nCannot resolve hostname: ' + ip
        
        results = []
        results.append('Ping test for ' + ip + ' (' + resolved_ip + ')')
        results.append('Using TCP port 80 as ICMP requires root\n')
        
        success_count = 0
        for i in range(4):
            start = time.time()
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((resolved_ip, 80))
                elapsed = (time.time() - start) * 1000
                sock.close()
                
                if result == 0:
                    results.append('Packet ' + str(i+1) + ': time=' + '{:.1f}'.format(elapsed) + 'ms (port 80 OPEN)')
                    success_count += 1
                else:
                    results.append('Packet ' + str(i+1) + ': time=' + '{:.1f}'.format(elapsed) + 'ms (port 80 CLOSED)')
            except socket.timeout:
                results.append('Packet ' + str(i+1) + ': Timeout (>3000ms)')
            except Exception as e:
                results.append('Packet ' + str(i+1) + ': Error - ' + str(e))
            time.sleep(0.1)
        
        results.append('')
        results.append('--- Ping statistics ---')
        results.append('4 packets sent, ' + str(success_count) + ' reached (port 80 open)')
        if success_count == 4:
            results.append('Status: SUCCESS - Host is reachable')
        elif success_count > 0:
            results.append('Status: PARTIAL - Host responded but port 80 may be blocked')
        else:
            results.append('Status: FAILED - Host unreachable or all ports blocked')
        
        return '\n'.join(results)

    # ============ Tracert 测试 ============
    def show_tracert_popup(self, instance):
        def callback(values):
            ip = values[0]
            if not ip:
                self.result_label.text = '[Tracert] Error: IP/Host cannot be empty!'
                return
            self.do_tracert(ip)
        
        self.create_popup(
            'Tracert Test',
            [{'label': 'IP / Host:', 'hint': 'e.g. 8.8.8.8'}],
            'Start Tracert',
            callback
        )

    def do_tracert(self, ip):
        self.result_label.text = '[Tracert] Tracing route to ' + ip + '...\n\nPlease wait (may take 30s)...'
        
        def run():
            try:
                output = self.trace_route(ip)
                Clock.schedule_once(lambda dt: self.show_result(output, 'Tracert'))
            except Exception as e:
                import traceback
                err_msg = traceback.format_exc()
                Clock.schedule_once(lambda dt: self.show_result('Error:\n' + err_msg, 'Tracert'))
        
        threading.Thread(target=run, daemon=True).start()

    def trace_route(self, ip):
        """使用 UDP 实现 traceroute（不需要 root）"""
        import time
        
        try:
            target_ip = socket.gethostbyname(ip)
        except socket.gaierror:
            return '[Tracert] FAILED\n\nCannot resolve hostname: ' + ip
        
        results = []
        results.append('Tracing route to ' + ip + ' (' + target_ip + ')')
        results.append('Max 10 hops, using UDP\n')
        
        for ttl in range(1, 11):
            hop_result = '  ' + str(ttl) + '.  '
            hop_found = False
            
            for port in range(33434, 33434 + 3):  # 3 tries
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.settimeout(3)
                    # Android 上设置 TTL 可能受限，尝试设置
                    try:
                        import struct
                        sock.setsockopt(socket.IPPROTO_IP, 0x07, ttl)  # IP_TTL
                    except:
                        pass
                    
                    start = time.time()
                    try:
                        sock.sendto(b'\x00', (target_ip, port))
                    except:
                        pass
                    
                    try:
                        data, addr = sock.recvfrom(1024)
                        elapsed = (time.time() - start) * 1000
                        hop_result += addr[0] + ' (' + '{:.0f}'.format(elapsed) + 'ms) '
                        hop_found = True
                    except socket.timeout:
                        hop_result += '* '
                    except Exception:
                        hop_result += '* '
                    finally:
                        sock.close()
                        
                except Exception:
                    hop_result += '* '
            
            if not hop_found:
                hop_result += 'Request timeout'
            
            results.append(hop_result)
            
            # 如果到达了目标，停止
            if hop_found:
                try:
                    last_ip = hop_result.split('(')[0].strip().split()[-1]
                    if last_ip == target_ip and last_ip != '*':
                        results.append('\nRoute trace complete.')
                        break
                except:
                    pass
        
        results.append('')
        results.append('Note: UDP traceroute may be limited on Android without root.')
        return '\n'.join(results)

    # ============ Telnet 测试 ============
    def show_telnet_popup(self, instance):
        def callback(values):
            ip = values[0]
            port = values[1]
            if not ip or not port:
                self.result_label.text = '[Telnet] Error: IP and Port cannot be empty!'
                return
            try:
                int(port)
            except ValueError:
                self.result_label.text = '[Telnet] Error: Port must be a number!'
                return
            self.do_telnet(ip, port)
        
        self.create_popup(
            'Telnet Test',
            [
                {'label': 'IP / Host:', 'hint': 'e.g. 192.168.1.1'},
                {'label': 'Port:', 'hint': 'e.g. 23', 'default': '23'}
            ],
            'Start Telnet',
            callback
        )

    def do_telnet(self, ip, port):
        self.result_label.text = '[Telnet] Testing ' + ip + ':' + port + '...\n\nPlease wait...'
        
        def run():
            try:
                output = self.test_telnet(ip, port)
                Clock.schedule_once(lambda dt: self.show_result(output, 'Telnet'))
            except Exception as e:
                import traceback
                err_msg = traceback.format_exc()
                Clock.schedule_once(lambda dt: self.show_result('Error:\n' + err_msg, 'Telnet'))
        
        threading.Thread(target=run, daemon=True).start()

    def test_telnet(self, ip, port):
        """测试 Telnet 端口连通性"""
        import time
        
        results = []
        results.append('Telnet Test')
        results.append('Target: ' + ip + ':' + port)
        results.append('')
        
        try:
            resolved_ip = socket.gethostbyname(ip)
            results.append('Resolved IP: ' + resolved_ip)
        except socket.gaierror:
            results.append('ERROR: Cannot resolve hostname: ' + ip)
            return '\n'.join(results)
        
        port_num = int(port)
        start = time.time()
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(8)
            result = sock.connect_ex((resolved_ip, port_num))
            elapsed = (time.time() - start) * 1000
            sock.close()
            
            results.append('')
            results.append('Connection time: {:.0f}ms'.format(elapsed))
            
            if result == 0:
                results.append('Status: SUCCESS')
                results.append('')
                results.append('Port ' + str(port_num) + ' is OPEN')
                results.append('Telnet connection can be established.')
                results.append('')
                results.append('You can use a Telnet client to connect.')
            else:
                results.append('Status: FAILED')
                results.append('')
                results.append('Port ' + str(port_num) + ' is CLOSED or FILTERED')
                results.append('Cannot establish Telnet connection.')
                results.append('')
                results.append('Possible reasons:')
                results.append('1. Telnet service not running on target')
                results.append('2. Firewall blocking the port')
                results.append('3. Wrong port number')
                
        except socket.timeout:
            results.append('')
            results.append('Status: TIMEOUT')
            results.append('')
            results.append('Connection timed out after 8 seconds.')
            results.append('Target may be unreachable or firewall is blocking.')
        except Exception as e:
            results.append('')
            results.append('Status: ERROR')
            results.append('')
            results.append('Error: ' + str(e))
        
        return '\n'.join(results)

    # ============ SSH 测试 ============
    def show_ssh_popup(self, instance):
        def callback(values):
            ip = values[0]
            port = values[1]
            if not ip or not port:
                self.result_label.text = '[SSH] Error: IP and Port cannot be empty!'
                return
            try:
                int(port)
            except ValueError:
                self.result_label.text = '[SSH] Error: Port must be a number!'
                return
            self.do_ssh(ip, port)
        
        self.create_popup(
            'SSH Test',
            [
                {'label': 'IP / Host:', 'hint': 'e.g. 192.168.1.1'},
                {'label': 'Port:', 'hint': 'e.g. 22', 'default': '22'}
            ],
            'Start SSH',
            callback
        )

    def do_ssh(self, ip, port):
        self.result_label.text = '[SSH] Testing ' + ip + ':' + port + '...\n\nPlease wait...'
        
        def run():
            try:
                output = self.test_ssh(ip, port)
                Clock.schedule_once(lambda dt: self.show_result(output, 'SSH'))
            except Exception as e:
                import traceback
                err_msg = traceback.format_exc()
                Clock.schedule_once(lambda dt: self.show_result('Error:\n' + err_msg, 'SSH'))
        
        threading.Thread(target=run, daemon=True).start()

    def test_ssh(self, ip, port):
        """测试 SSH 端口连通性"""
        import time
        
        results = []
        results.append('SSH Test')
        results.append('Target: ' + ip + ':' + port)
        results.append('')
        
        try:
            resolved_ip = socket.gethostbyname(ip)
            results.append('Resolved IP: ' + resolved_ip)
        except socket.gaierror:
            results.append('ERROR: Cannot resolve hostname: ' + ip)
            return '\n'.join(results)
        
        port_num = int(port)
        start = time.time()
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(8)
            result = sock.connect_ex((resolved_ip, port_num))
            elapsed = (time.time() - start) * 1000
            sock.close()
            
            results.append('')
            results.append('Connection time: {:.0f}ms'.format(elapsed))
            
            if result == 0:
                results.append('Status: SUCCESS')
                results.append('')
                results.append('Port ' + str(port_num) + ' is OPEN')
                results.append('SSH port is reachable.')
                results.append('')
                results.append('Note: This only tests port connectivity.')
                results.append('Actual SSH login requires username/password.')
            else:
                results.append('Status: FAILED')
                results.append('')
                results.append('Port ' + str(port_num) + ' is CLOSED or FILTERED')
                results.append('SSH port is not reachable.')
                results.append('')
                results.append('Possible reasons:')
                results.append('1. SSH service (sshd) not running')
                results.append('2. Firewall blocking port 22')
                results.append('3. Wrong port number')
                
        except socket.timeout:
            results.append('')
            results.append('Status: TIMEOUT')
            results.append('')
            results.append('Connection timed out after 8 seconds.')
        except Exception as e:
            results.append('')
            results.append('Status: ERROR')
            results.append('')
            results.append('Error: ' + str(e))
        
        return '\n'.join(results)

    # ============ 通用结果显示 ============
    def show_result(self, output, test_type):
        self.result_label.text = output
