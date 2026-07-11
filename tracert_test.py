"""
Tracert (路由追踪) 测试模块
"""
import subprocess
import threading
import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock


class TracertTestWidget(BoxLayout):
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
        self.max_hops_input = TextInput(
            hint_text='最大跳数',
            multiline=False,
            font_size='16sp',
            size_hint_x=0.3,
            text='30'
        )
        input_layout.add_widget(self.host_input)
        input_layout.add_widget(self.max_hops_input)
        self.add_widget(input_layout)

        # 按钮区域
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height='48dp')
        self.tracert_btn = Button(text='开始 Tracert', font_size='16sp', bold=True)
        self.tracert_btn.bind(on_press=self.start_tracert)
        self.stop_btn = Button(text='停止', font_size='16sp', state='disabled')
        self.stop_btn.bind(on_press=self.stop_tracert)
        btn_layout.add_widget(self.tracert_btn)
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
        self._process = None

    def update_height(self, *args):
        lines = len(self.result_label.text.split('\n'))
        self.result_label.height = max(50, lines * 20)

    def start_tracert(self, instance):
        host = self.host_input.text.strip()
        if not host:
            self.result_label.text = '⚠️ 请输入主机名或IP地址'
            self.result_label.color = (1, 0.3, 0.3, 1)
            return

        max_hops = 30
        try:
            max_hops = int(self.max_hops_input.text)
            if max_hops < 1 or max_hops > 64:
                max_hops = 30
        except ValueError:
            pass

        self._running = True
        self.tracert_btn.state = 'disabled'
        self.stop_btn.state = 'normal'
        self.progress.show()
        self.progress.value = 0
        self.result_label.text = f'正在追踪到 {host} 的路由...'
        self.result_label.color = (0.2, 0.6, 0.2, 1)

        thread = threading.Thread(target=self._run_tracert, args=(host, max_hops))
        thread.daemon = True
        thread.start()

    def stop_tracert(self, instance):
        self._running = False
        if self._process:
            try:
                self._process.terminate()
            except Exception:
                pass

    def _run_tracert(self, host, max_hops):
        try:
            is_windows = platform.system() == 'Windows'
            cmd_args = []
            
            if is_windows:
                cmd_args = ['tracert', '-h', str(max_hops), host]
            else:
                # Android/Linux 使用 traceroute
                cmd_args = ['traceroute', '-m', str(max_hops), host]
            
            self._process = subprocess.Popen(
                cmd_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            output_lines = []
            total_lines = max_hops + 4
            
            for line in self._process.stdout:
                if not self._running:
                    break
                output_lines.append(line.rstrip())
                progress_value = min(95, len(output_lines) / total_lines * 100)
                Clock.schedule_once(lambda dt, v=progress_value: self.progress.set_value(v), 0)
                Clock.schedule_once(lambda dt, lines=output_lines[:]: self.update_result(lines), 0)

            self._process.wait()
            returncode = self._process.returncode

            if returncode == 0:
                summary = '\n✅ Tracert 测试完成'
            else:
                summary = '\n❌ Tracert 测试失败'

            final_output = '\n'.join(output_lines) + summary
            Clock.schedule_once(lambda dt: self.finish_tracert(final_output, returncode == 0), 0)

        except FileNotFoundError:
            error_msg = '❌ 错误: 未找到 traceroute 命令，请确保设备已安装'
            Clock.schedule_once(lambda dt: self.finish_tracert(error_msg, False), 0)
        except Exception as e:
            error_msg = f'❌ 错误: {str(e)}'
            Clock.schedule_once(lambda dt: self.finish_tracert(error_msg, False), 0)

    def update_result(self, lines):
        self.result_label.text = '\n'.join(lines)

    def progress_set_value(self, value):
        self.progress.value = value

    def finish_tracert(self, result, success):
        self.result_label.text = result
        if success:
            self.result_label.color = (0.2, 0.6, 0.2, 1)
        else:
            self.result_label.color = (1, 0.3, 0.3, 1)
        self.tracert_btn.state = 'normal'
        self.stop_btn.state = 'disabled'
        self.progress.hide()
        self._running = False
        self._process = None
