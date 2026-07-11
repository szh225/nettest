@echo off
REM 网络测试工具 - Windows 测试启动脚本
echo ======================================
echo   网络测试工具 - 桌面测试模式
echo ======================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3
    pause
    exit /b 1
)

echo [信息] Python 版本:
python --version
echo.

REM 检查 Kivy 是否安装
python -c "import kivy" >nul 2>&1
if errorlevel 1 (
    echo [信息] 正在安装 Kivy...
    pip install kivy
    echo.
)

echo [信息] 启动网络测试工具...
echo.

cd /d "%~dp0"
python main.py

pause
