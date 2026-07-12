[app]
title = Wireless Security Auditor
package.name = wirelessauditor
package.domain = org.security
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# المتطلبات الأساسية والمكتبات للتطبيق
requirements = python3,kivy,zxcvbn

orientation = portrait
fullscreen = 1

# الصلاحيات الأمنية المطلوبة للوصول الصارم لأجهزة الراديو والواي فاي بالهاتف
android.permissions = INTERNET, ACCESS_WIFI_STATE, CHANGE_WIFI_STATE, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION
android.api = 33
android.minapi = 21
android.ndk = 25b
android.skip_cleanup = False
android.release_artifact = apk
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
