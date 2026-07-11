"""
Ping 测试模块
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
from kivy.core.window import Window


class PingTestWidget(BoxLayout):
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
        self.count_input = TextInput(
            hint_text='次数',
            multiline=False,
            font_size='16sp',
            size_hint_x=0.3,
            text='4'
        )
        input_layout.add_widget(self.host_input)
        input_layout.add_widget(self.count_input)
        self.add_widget(input_layout)

        # 按钮区域
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height='48dp')
        self.ping_btn = Button(text='开始 Ping', font_size='16sp', bold=True)
        self.ping_btn.bind(on_press=self.start_ping)
        self.stop_btn = Button(text='停止', font_size='16sp', state='disabled')
        self.stop_btn.bind(on_press=self.stop_ping)
        btn_layout.add_widget(self.ping_btn)
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
        # 根据文本内容动态调整高度
        lines = len(self.result_label.text.split('\n'))
        self.result_label.height = max(50, lines * 20)

    def start_ping(self, instance):
        host = self.host_input.text.strip()
        if not host:
            self.result_label.text = '⚠️ 请输入主机名或IP地址'
            self.result_label.color = (1, 0.3, 0.3, 1)
            return

        count = 4
        try:
            count = int(self.count_input.text)
            if count < 1 or count > 100:
                count = 4
        except ValueError:
            pass

        self._running = True
        self.ping_btn.state = 'disabled'
        self.stop_btn.state = 'normal'
        self.progress.show()
        self.progress.value = 0
        self.result_label.text = f'正在 Ping {host} ...'
        self.result_label.color = (0.2, 0.6, 0.2, 1)

        # 在新线程中执行
        thread = threading.Thread(target=self._run_ping, args=(host, count))
        thread.daemon = True
        thread.start()

    def stop_ping(self, instance):
        self._running = False
        if self._process:
            try:
                self._process.terminate()
            except Exception:
                pass

    def _run_ping(self, host, count):
        try:
            is_android = platform.system() == 'Android' or platform.system() == 'Linux'
            cmd_args = []
            
            if is_android:
                # Android/Linux 系统
                cmd_args = ['ping', '-c', str(count), host]
            else:
                # Windows 系统
                cmd_args = ['ping', '-n', str(count), host]
            
            self._process = subprocess.Popen(
                cmd_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            output_lines = []
            total_lines = count + 4  # 预估总行数
            
            for line in self._process.stdout:
                if not self._running:
                    break
                output_lines.append(line.rstrip())
                progress_value = len(output_lines) / total_lines * 100
                Clock.schedule_once(lambda dt, v=progress_value: self.progress.set_value(v), 0)
                Clock.schedule_once(lambda dt, lines=output_lines[:] : self.update_result(lines), 0)

            self._process.wait()
            returncode = self._process.returncode

            if returncode == 0:
                summary = '\n✅ Ping 测试成功'
            else:
                summary = '\n❌ Ping 测试失败'

            final_output = '\n'.join(output_lines) + summary
            Clock.schedule_once(lambda dt: self.finish_ping(final_output, returncode == 0), 0)

        except Exception as e:
            error_msg = f'❌ 错误: {str(e)}'
            Clock.schedule_once(lambda dt: self.finish_ping(error_msg, False), 0)

    def update_result(self, lines):
        self.result_label.text = '\n'.join(lines)

    def progress_set_value(self, value):
        self.progress.value = value

    def finish_ping(self, result, success):
        self.result_label.text = result
        if success:
            self.result_label.color = (0.2, 0.6, 0.2, 1)
        else:
            self.result_label.color = (1, 0.3, 0.3, 1)
        self.ping_btn.state = 'normal'
        self.stop_btn.state = 'disabled'
        self.progress.hide()
        self._running = False
        self._process = None
