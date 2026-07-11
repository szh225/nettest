# 网络测试工具 (NetTest)

一款功能强大的 Android 网络测试工具，支持 Ping、Tracert、Telnet 和 SSH 测试。

## 功能特性

### 📡 Ping 测试
- 支持自定义 Ping 次数
- 实时显示 Ping 结果
- 显示往返时延统计

### 🔍 Tracert 路由追踪
- 追踪网络路由路径
- 自定义最大跳数
- 显示每跳延迟

### 🔌 Telnet 测试
- 测试端口连通性
- 自定义端口号（默认 23）
- 显示 DNS 解析时间和连接时间
- 自动读取 Banner 信息

### 🔐 SSH 测试
- 测试 SSH 端口连通性（默认 22）
- 显示 SSH Banner 和版本信息
- 详细的连接诊断信息

## 项目结构

```
nettest_app/
├── main.py              # 主程序入口
├── main_screen.py       # 主界面（Tab 切换）
├── ping_test.py         # Ping 测试模块
├── tracert_test.py      # Tracert 测试模块
├── telnet_test.py       # Telnet 测试模块
├── ssh_test.py          # SSH 测试模块
├── style.kv             # Kivy 样式文件
├── buildozer.spec       # Buildozer 打包配置
└── README.md            # 本文件
```

## 快速开始

### 方法一：在电脑上运行测试

1. 安装依赖：
```bash
pip install kivy
```

2. 运行程序：
```bash
cd nettest_app
python main.py
```

### 方法二：GitHub Actions 云端打包（推荐）

**无需本地 Linux 环境，自动打包 APK！**

1. 在 GitHub 上创建新仓库（公开或私有均可）
2. 将 `nettest_app` 目录下所有文件推送到仓库：
   ```bash
   cd nettest_app
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/nettest.git
   git push -u origin main
   ```
3. 等待 GitHub Actions 自动执行打包（约 15-25 分钟）
4. 打包完成后，在仓库的 **Actions** → 对应 workflow → **Artifacts** 下载 APK
5. 或者在 **Releases** 中下载自动发布的 APK

> 💡 每次推送代码到 main 分支都会自动重新打包

### 方法三：本地 Linux/WSL 打包

#### 环境准备（需要 Linux 或 WSL）

1. 安装 Buildozer：
```bash
pip install buildozer
```

2. 安装系统依赖（Ubuntu/Debian）：
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv \
    zip unzip openjdk-17-jdk autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libgncursesw5-dev \
    libfreetype6-dev libpng-dev libffi-dev liblzma-dev
```

3. 进入项目目录并打包：
```bash
cd nettest_app
buildozer android debug
```

4. 打包完成后，APK 文件位于 `.bin/` 目录下

5. 将 APK 传输到手机并安装：
```bash
adb install .bin/*.apk
```

#### 使用 Termux（直接在 Android 上打包）

1. 安装 Termux（从 F-Droid 下载）
2. 在 Termux 中执行：
```bash
pkg update
pkg install python build-essential rust openssl clang
pip install buildozer
```

3. 复制项目文件到 Termux，执行打包

## 使用说明

### Ping 测试
1. 切换到 "📡 Ping" 标签页
2. 输入目标主机名或 IP 地址
3. 可选：修改 Ping 次数（默认 4 次）
4. 点击 "开始 Ping" 按钮
5. 查看测试结果

### Tracert 测试
1. 切换到 "🔍 Tracert" 标签页
2. 输入目标主机名或 IP 地址
3. 可选：修改最大跳数（默认 30）
4. 点击 "开始 Tracert" 按钮
5. 查看路由追踪结果

### Telnet 测试
1. 切换到 "🔌 Telnet" 标签页
2. 输入目标主机名或 IP 地址
3. 输入端口号（默认 23）
4. 设置超时时间（默认 10 秒）
5. 点击 "开始 Telnet" 按钮
6. 查看连接测试结果

### SSH 测试
1. 切换到 "🔐 SSH" 标签页
2. 输入目标主机名或 IP 地址
3. 输入端口号（默认 22）
4. 设置超时时间（默认 10 秒）
5. 点击 "开始 SSH 测试" 按钮
6. 查看连接测试结果和 SSH 版本信息

## 注意事项

1. **权限要求**：应用需要网络权限
2. **Android 限制**：Android 系统可能限制 ping/traceroute 命令，部分功能可能需要 root 权限
3. **SSH 测试**：本工具仅测试 SSH 端口连通性，不进行实际 SSH 认证连接
4. **防火墙**：某些网络环境可能阻止 ICMP 或特定端口访问

## 技术栈

- **Python 3** - 编程语言
- **Kivy** - 跨平台 UI 框架
- **Buildozer** - Android 打包工具
- **socket** - 网络通信
- **subprocess** - 系统命令调用

## 许可证

MIT License

## 作者

孙智辉 (s00839528)
