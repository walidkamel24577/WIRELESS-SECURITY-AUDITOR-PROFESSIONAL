# -*- coding: utf-8 -*-
"""
GRADUATION PROJECT: WIRELESS SECURITY AUDITOR PROFESSIONAL
FINAL COMPREHENSIVE SUITE - SAVED PASSWORDS & LIVE SCANNER
"""
import os
import sys
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
from kivy.clock import Clock

if platform == 'android':
    from android.permissions import request_permissions, Permission
    from jnius import autoclass, cast

class WirelessSecurityAuditor:
    def __init__(self):
        pass

    def get_real_android_saved_passwords(self):
        """القسم الأول: استخراج كلمات المرور للشبكات المحفوظة مسبقاً داخل الهاتف"""
        saved_list = {}
        if platform != 'android':
            return {
                "Home_Network": {"ssid": "Home_Network", "password": "SuperPassword2026", "auth": "WPA2"},
                "Starbucks_Guest": {"ssid": "Starbucks_Guest", "password": "[Open Network]", "auth": "Open"}
            }
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            Context = autoclass('android.content.Context')
            wifi_manager = activity.getSystemService(Context.WIFI_SERVICE)
            configured_networks = wifi_manager.getConfiguredNetworks()
            
            if configured_networks is not None:
                for i in range(configured_networks.size()):
                    config = configured_networks.get(i)
                    if not config.SSID:
                        continue
                    ssid = config.SSID.replace('"', '')
                    password = "[Protected]"
                    if hasattr(config, 'preSharedKey') and config.preSharedKey:
                        password = config.preSharedKey.replace('"', '')
                    
                    auth = "WPA/WPA2"
                    if "NONE" in str(config.allowedKeyManagement):
                        auth = "Open"
                        password = "[Open Network]"

                    saved_list[ssid.lower()] = {"ssid": ssid, "password": password, "auth": auth}
        except Exception as e:
            print(f"Error: {str(e)}")
        return saved_list

    def scan_live_nearby_networks(self):
        """القسم الثاني: إرسال أمر فحص فوري وجلب الشبكات المحيطة بك"""
        networks_list = []
        if platform != 'android':
            return [
                {"ssid": "Nearby_Unsecured_Net", "auth": "Open", "level": -45},
                {"ssid": "Target_Router_Private", "auth": "WPA3", "level": -85}
            ]
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            Context = autoclass('android.content.Context')
            wifi_manager = activity.getSystemService(Context.WIFI_SERVICE)
            
            # تفعيل عملية الفحص بشكل نشط
            wifi_manager.startScan()
            
            scan_results = wifi_manager.getScanResults()
            if scan_results is not None:
                for i in range(scan_results.size()):
                    result = scan_results.get(i)
                    ssid = result.SSID
                    capabilities = result.capabilities
                    level = result.level
                    
                    if ssid:
                        auth_type = "WPA/WPA2"
                        if "WEP" in capabilities: auth_type = "WEP"
                        elif "OPEN" in capabilities or ("NOT" in capabilities and "WPA" not in capabilities): auth_type = "Open"
                        
                        networks_list.append({"ssid": ssid, "auth": auth_type, "level": level})
        except Exception as e:
            print(f"Scan Error: {str(e)}")
        return networks_list

class AuditorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(AuditorWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        if platform == 'android':
            request_permissions([Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION])

        self.title_label = Label(
            text="[b]WIRELESS AUDITOR & PASSWORDS VAULT[/b]", 
            markup=True, font_size='18sp', size_hint_y=None, height=50
        )
        self.add_widget(self.title_label)

        # أزرار التحكم والعمليات
        self.btn_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        
        self.vault_btn = Button(text="Show Saved Keys", font_size='14sp', background_color=(0.8, 0.2, 0.2, 1))
        self.vault_btn.bind(on_press=self.display_saved)
        self.btn_layout.add_widget(self.vault_btn)
        
        self.scan_btn = Button(text="Scan Active Air", font_size='14sp', background_color=(0.2, 0.6, 0.4, 1))
        self.scan_btn.bind(on_press=self.display_live)
        self.btn_layout.add_widget(self.scan_btn)
        
        self.add_widget(self.btn_layout)

        # تصحيح الـ ScrollView بالكامل وإدراج النص داخله بشكل مرن
        self.scroll = ScrollView(size_hint=(1, 1))
        self.result_label = Label(
            text="• Select 'Show Saved Keys' to look inside the device vault.\n• Select 'Scan Active Air' to sniff networks currently in range.", 
            font_size='14sp', halign='left', valign='top', size_hint_y=None
        )
        self.result_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value))
        self.result_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        
        self.scroll.add_widget(self.result_label)
        self.add_widget(self.scroll)

    def display_saved(self, instance):
        auditor = WirelessSecurityAuditor()
        data = auditor.get_real_android_saved_passwords()
        output = f"--- DEVICE PASSWORDS VAULT REPORT ({datetime.now().strftime('%H:%M')}) ---\n\n"
        if not data:
            output += "No saved networks found or execution blocked by System API restrictions.\n"
        else:
            for k, v in data.items():
                output += f" 🔐 SSID: {v['ssid']}\n 🔑 Key: {v['password']}\n 🛡️ Proto: {v['auth']}\n" + "-"*35 + "\n"
        self.result_label.text = output

    def display_live(self, instance):
        auditor = WirelessSecurityAuditor()
        data = auditor.scan_live_nearby_networks()
        output = f"--- LIVE WIRELESS ENVIRONMENTS DETECTED ({datetime.now().strftime('%H:%M')}) ---\n\n"
        output += "Note: Real-time air passwords can't be fetched without brute-force.\n\n"
        if not data:
            output += "No networks detected. Please ensure that Location services (GPS) are turned ON."
        else:
            for net in data:
                output += f" 📡 Network: {net['ssid']}\n   Security: {net['auth']} | Signal: {net['level']} dBm\n\n"
        self.result_label.text = output

class WirelessAuditorApp(App):
    def build(self):
        return AuditorWindow()

if __name__ == "__main__":
    WirelessAuditorApp().run()
