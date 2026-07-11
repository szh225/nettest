"""
网络测试工具 - 主程序入口
"""
import os
import sys
import traceback

# Set up logging to file for debugging
LOG_FILE = os.path.join(os.environ.get('HOME', '/'), 'nettest.log')

def log(msg):
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(str(msg) + '\n')
    except:
        pass

log("=== NetTest starting ===")
log(f"Platform: {sys.platform}")
log(f"Python: {sys.version}")

try:
    from kivy.utils import platform
    log(f"Kivy platform: {platform}")
except Exception as e:
    log(f"Failed to import kivy.utils: {e}")
    raise

try:
    from kivy.app import App
    log("Kivy App imported successfully")
except Exception as e:
    log(f"Failed to import kivy.app: {e}")
    log(traceback.format_exc())
    raise


class NetTestApp(App):
    def build(self):
        log("NetTestApp.build() called")
        try:
            from main_screen import MainScreen
            log("MainScreen imported")
            self.title = 'NetTest'
            self.root = MainScreen()
            log("MainScreen created, returning root")
            return self.root
        except Exception as e:
            log(f"build() failed: {e}")
            log(traceback.format_exc())
            raise


if __name__ == '__main__':
    log("Starting main block")
    try:
        NetTestApp().run()
    except Exception as e:
        log(f"FATAL in main: {e}")
        log(traceback.format_exc())
        raise
