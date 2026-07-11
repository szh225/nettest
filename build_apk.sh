#!/bin/bash
# 网络测试工具 - APK 打包脚本
# 使用方法：chmod +x build_apk.sh && ./build_apk.sh

echo "======================================"
echo "  网络测试工具 - APK 打包脚本"
echo "======================================"

# 检查是否在 Linux/WSL 环境下运行
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo "❌ 错误：请在 Linux 或 WSL 环境下运行此脚本"
    exit 1
fi

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python 3，请先安装 Python 3"
    exit 1
fi

echo "✅ Python 3 已安装: $(python3 --version)"

# 检查 Buildozer 是否安装
if ! command -v buildozer &> /dev/null; then
    echo "⚠️  Buildozer 未安装，正在安装..."
    pip3 install buildozer
fi

echo "✅ Buildozer 已安装: $(buildozer --version 2>/dev/null || echo '未知版本')"

# 安装系统依赖（如果需要）
echo ""
echo "检查系统依赖..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y python3-pip python3-venv \
        zip unzip openjdk-17-jdk autoconf libtool pkg-config \
        zlib1g-dev libncurses5-dev libgncursesw5-dev \
        libfreetype6-dev libpng-dev libffi-dev liblzma-dev
elif command -v yum &> /dev/null; then
    sudo yum groupinstall -y "Development Tools"
    sudo yum install -y python3 python3-pip zip unzip java-17-openjdk-devel
fi

echo ""
echo "开始打包 APK..."
echo ""

# 执行打包
buildozer android debug

# 检查打包结果
if [ -f ".bin/*.apk" ]; then
    echo ""
    echo "======================================"
    echo "✅ 打包成功！"
    echo "======================================"
    echo "APK 文件位置: .bin/"
    ls -lh .bin/*.apk
    echo ""
    echo "安装到手机："
    echo "  adb install .bin/*.apk"
else
    echo ""
    echo "❌ 打包失败，请检查错误信息"
    exit 1
fi
