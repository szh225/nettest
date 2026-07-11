[app]

# (str) Title of your application
title = 网络测试工具

# (str) Package name
package.name = nettest

# (str) Package domain (needed for android/ios packaging)
package.domain = org.nettest

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application icon filename
icon.filename = @misc/icon.png

# (str) Application icon Android
android.icon = @misc/icon.png

# (str) Application icon iOS
ios.icon = @misc/icon.png

# (str) Application display name
display_name = 网络测试工具

# (list) Application requirements
# Comma-separated list of requirements for the application
requirements = python3,kivy

# (int) Minimum Android API version to support
android.minapi = 21

# (int) Target Android API version
android.maxapi = 33

# (int) Android SDK version to use
android.sdk = 33

# (int) Android NDK version to use
android.ndk = 22b

# (str) The Android arch to build for
android.archs = armeabi-v7a

# (bool) Enables AndroidX support
android.use_androidx = True

# (str) Orientation of the app
orientation = portrait

# (bool) Allow to save camera images into a temporary (writable) folder
android.allow_backup = True

# (str) The Android windowSoftInputMode
android.windowSoftInputMode = adjustResize

# (list) Android permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
bin_dir = ./bin
