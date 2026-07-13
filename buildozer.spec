[app]
title = Wireless Security Auditor
package.name = wirelessauditor
package.domain = org.graduation
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,pyjnius
android.permissions = ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_WIFI_STATE, CHANGE_WIFI_STATE
android.features = android.hardware.wifi, android.hardware.location.gps
android.api = 34
android.minapi = 21
android.enable_androidx = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
