[app]

title = NetTest
package.name = nettest
package.domain = org.nettest
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0

requirements = python3,kivy

android.minapi = 21
android.ndk = 25b
android.archs = armeabi-v7a
android.use_androidx = True
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
