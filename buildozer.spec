[app]
# (str) Title of your application
title = Wireless Security Auditor

# (str) Package name
package.name = wirelessauditor

# (str) Package domain (needed for android packaging)
package.domain = org.security

# (str) Source code directory where main.py is located
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy,zxcvbn

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# =============================================================================
# Android specific configuration
# =============================================================================

# (list) Permissions required by the app for scanning networks
android.permissions = INTERNET, ACCESS_WIFI_STATE, CHANGE_WIFI_STATE, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip cleanup after hit
android.skip_cleanup = False

# (str) Format used to package the app for release/debug mode
android.release_artifact = apk
android.debug_artifact = apk

[buildozer]
# (int) Log level (2 = debug with full command output)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
