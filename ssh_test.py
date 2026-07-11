"""
SSH 测试模块
"""
import socket
import threading
import time
import ssl
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock


class SSHTestWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # 输入区域
        input_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height='48dp')
        self.host_input = TextInput(
            hint_text='输入主机名或IP地址',
            multiline=False,
            font_size='16sp',
            size_hint_x=0.7
        )
        self.port_input = TextInput(
            hint_text='端口',
            multiline=False,
            font_size='16sp',
            size_hint_x=0.3,
            text='22'
        )
        input_layout.add_widget(self.host_input)
        input_layout.add_widget(self.port_input)
        self.add_widget(input_layout)

        # 超时设置
        timeout_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height='48dp')
        timeout_label = Label(text='超时(秒):', font_size='14sp', size_hint_x=0.3)
        self.timeout_input = TextInput(
            hint_text='超时时间',
            multiline=False,
            font_size='16sp',
            size_hint_x=0.7,
            text='10'
        )
        timeout_layout.add_widget(timeout_label)
        timeout_layout.add_widget(self.timeout_input)
        self.add_widget(timeout_layout)

        # 按钮区域
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height='48dp')
        self.ssh_btn = Button(text='开始 SSH 测试', font_size='16sp', bold=True)
        self.ssh_btn.bind(on_press=self.start_ssh)
        self.stop_btn = Button(text='停止', font_size='16sp', state='disabled')
        self.stop_btn.bind(on_press=self.stop_ssh)
        btn_layout.add_widget(self.ssh_btn)
        btn_layout.add_widget(self.stop_btn)
        self.add_widget(btn_layout)

        # 进度条
        self.progress = ProgressBar(size_hint_y=None, height='20dp')
        self.progress.hide()
        self.add_widget(self.progress)

        # 结果输出区域
        result_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        result_layout.bind(minimum_height=result_layout.setter('height'))
        self.result_label = Label(
            text='等待测试...',
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.result_label.bind(text=self.update_height)
        result_layout.add_widget(self.result_label)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(result_layout)
        self.add_widget(scroll)

        # 控制变量
        self._running = False
        self._socket = None

    def update_height(self, *args):
        lines = len(self.result_label.text.split('\n'))
        self.result_label.height = max(50, lines * 20)

    def start_ssh(self, instance):
        host = self.host_input.text.strip()
        if not host:
            self.result_label.text = '⚠️ 请输入主机名或IP地址'
            self.result_label.color = (1, 0.3, 0.3, 1)
            return

        port = 22
        try:
            port = int(self.port_input.text)
            if port < 1 or port > 65535:
                port = 22
        except ValueError:
            pass

        timeout = 10
        try:
            timeout = int(self.timeout_input.text)
            if timeout < 1 or timeout > 60:
                timeout = 10
        except ValueError:
            pass

        self._running = True
        self.ssh_btn.state = 'disabled'
        self.stop_btn.state = 'normal'
        self.progress.show()
        self.progress.value = 0
        self.result_label.text = f'正在测试 SSH 连接 {host}:{port} ...'
        self.result_label.color = (0.2, 0.6, 0.2, 1)

        thread = threading.Thread(target=self._run_ssh, args=(host, port, timeout))
        thread.daemon = True
        thread.start()

    def stop_ssh(self, instance):
        self._running = False
        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass

    def _run_ssh(self, host, port, timeout):
        try:
            start_time = time.time()
            output_lines = [f'尝试 SSH 连接 {host}:{port} ...']
            
            Clock.schedule_once(lambda dt, lines=output_lines[:]: self.update_result(lines), 0)

            # 创建 socket 连接
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(timeout)

            # 解析 DNS
            dns_start = time.time()
            try:
                ip_address = socket.gethostbyname(host)
                dns_time = (time.time() - dns_start) * 1000
                output_lines.append(f'DNS 解析: {host} -> {ip_address} ({dns_time:.2f} ms)')
                Clock.schedule_once(lambda dt, lines=output_lines[:]: self.update_result(lines), 0)
            except socket.gaierror as e:
                output_lines.append(f'❌ DNS 解析失败: {str(e)}')
                Clock.schedule_once(lambda dt: self.finish_ssh('\n'.join(output_lines), False), 0)
                return

            # 连接测试
            conn_start = time.time()
            try:
                self._socket.connect((ip_address, port))
                conn_time = (time.time() - conn_start) * 1000
                
                output_lines.append(f'✅ TCP 连接成功! ({conn_time:.2f} ms)')
                output_lines.append(f'本地地址: {self._socket.getsockname()[0]}')
                
                # 尝试读取 SSH Banner
                try:
                    self._socket.settimeout(3)
                    banner = self._socket.recv(1024).decode('utf-8', errors='ignore').strip()
                    if banner:
                        output_lines.append(f'SSH Banner: {banner}')
                        # 解析 banner 信息
                        if 'SSH-' in banner:
                            parts = banner.split(' ')
                            if len(parts) >= 2:
                                output_lines.append(f'SSH 版本: {parts[0]}')
                                output_lines.append(f'SSH 软件: {parts[1]}')
                except socket.timeout:
                    output_lines.append('⚠️ 未收到 SSH Banner (可能正常)')
                except Exception as e:
                    output_lines.append(f'⚠️ 读取 Banner 失败: {str(e)}')

                total_time = (time.time() - start_time) * 1000
                output_lines.append(f'总耗时: {total_time:.2f} ms')
                output_lines.append('\n✅ SSH 端口测试成功 - 端口可达')
                output_lines.append('提示: 此测试仅验证端口连通性，不进行实际 SSH 认证')

                Clock.schedule_once(lambda dt: self.progress.set_value(100), 0)
                Clock.schedule_once(lambda dt: self.finish_ssh('\n'.join(output_lines), True), 0)

            except socket.timeout:
                conn_time = (time.time() - conn_start) * 1000
                output_lines.append(f'❌ 连接超时 ({conn_time:.0f} ms)')
                output_lines.append('SSH 端口可能关闭或被防火墙阻止')
                Clock.schedule_once(lambda dt: self.finish_ssh('\n'.join(output_lines), False), 0)
            except ConnectionRefusedError:
                conn_time = (time.time() - conn_start) * 1000
                output_lines.append(f'❌ 连接被拒绝 ({conn_time:.2f} ms)')
                output_lines.append('SSH 服务未运行或端口未开放')
                Clock.schedule_once(lambda dt: self.finish_ssh('\n'.join(output_lines), False), 0)
            except OSError as e:
                output_lines.append(f'❌ 网络错误: {str(e)}')
                Clock.schedule_once(lambda dt: self.finish_ssh('\n'.join(output_lines), False), 0)

        except Exception as e:
            error_msg = f'❌ 错误: {str(e)}'
            Clock.schedule_once(lambda dt: self.finish_ssh(error_msg, False), 0)
        finally:
            if self._socket:
                try:
                    self._socket.close()
                except Exception:
                    pass

    def update_result(self, lines):
        self.result_label.text = '\n'.join(lines)

    def progress_set_value(self, value):
        self.progress.value = value

    def finish_ssh(self, result, success):
        self.result_label.text = result
        if success:
            self.result_label.color = (0.2, 0.6, 0.2, 1)
        else:
            self.result_label.color = (1, 0.3, 0.3, 1)
        self.ssh_btn.state = 'normal'
        self.stop_btn.state = 'disabled'
        self.progress.hide()
        self._running = False
        self._socket = None
