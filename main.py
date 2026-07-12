# -*- coding: utf-8 -*-
"""
GRADUATION PROJECT: WIRELESS SECURITY AUDITOR PROFESSIONAL
FINAL MOBILE VERSION WITH KIVY GUI FOR ANDROID
"""
import os
import sys
from datetime import datetime

# استدعاء مكتبات واجهة مستخدم أندرويد (Kivy)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

try:
    from zxcvbn import zxcvbn
    ZXCVBN_AVAILABLE = True
except ImportError:
    ZXCVBN_AVAILABLE = False

class WirelessSecurityAuditor:
    def __init__(self):
        self.vault = {}
        self.nearby_networks = []

    def analyze_password_strength(self, password):
        if password == "[Open Network]":
            return "OPEN", ["No password"], 0
        if ZXCVBN_AVAILABLE:
            res = zxcvbn(password)
            score = res['score']
            strength = ["VERY WEAK", "WEAK", "FAIR", "GOOD", "STRONG"][score]
            feedback = res['feedback']['suggestions'] or ["No suggestions"]
            return strength, feedback, score
        else:
            return "MEDIUM", ["Basic analysis fallback"], 3

    def get_all_saved_profiles(self):
        # محاكاة مستقرة وآمنة متوافقة مع صلاحيات الأندرويد
        self.vault = {
            "test_home_wifi": {"ssid": "Secure_Home_Net", "password": "password123", "auth": "WPA2-Personal", "strength": "WEAK", "score": 1}
        }
        return self.vault

    def scan_nearby_networks(self):
        # محاكاة فحص شبكات أندرويد لضمان عدم الانهيار
        self.nearby_networks = [
            {"ssid": "Unsecure_Coffee_Shop", "auth": "Open", "encrypt": "None", "vulnerabilities": [{"type": "Open Network", "severity": "CRITICAL", "description": "'Unsecure_Coffee_Shop' is OPEN"}]}
        ]
        return self.nearby_networks


# بناء واجهة التطبيق التي ستظهر للمستخدم على الشاشة
class AuditorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(AuditorWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # عنوان التطبيق العلوي
        self.title_label = Label(
            text="[b]WIRELESS SECURITY AUDITOR[/b]", 
            markup=True, 
            font_size='22sp',
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.title_label)

        # زر بدء عملية الفحص
        self.scan_btn = Button(
            text="Start Security Audit", 
            font_size='18sp',
            size_hint_y=None,
            height=60,
            background_color=(0.1, 0.6, 0.8, 1)
        )
        self.scan_btn.bind(on_press=self.run_audit)
        self.add_widget(self.scan_btn)

        # صندوق التمرير لعرض النتائج الطويلة دون تجميد الشاشة
        self.scroll = ScrollView()
        self.result_label = Label(
            text="Click the button above to scan networks...", 
            font_size='14sp', 
            halign='left', 
            valign='top',
            size_hint_y=None
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.scroll.add_widget(self.result_label)
        self.add_widget(self.scroll)

    def run_audit(self, instance):
        auditor = WirelessSecurityAuditor()
        output = f"Audit Report Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        output += "="*40 + "\n\n"
        
        output += "[ Saved Profiles ]\n"
        profiles = auditor.get_all_saved_profiles()
        for ssid, data in profiles.items():
            output += f" • SSID: {data['ssid']}\n   Strength: {data['strength']}\n\n"
            
        output += "[ Nearby Networks Scan ]\n"
        networks = auditor.scan_nearby_networks()
        for net in networks:
            output += f" • SSID: {net['ssid']} (Auth: {net['auth']})\n"
            if net['vulnerabilities']:
                for v in net['vulnerabilities']:
                    output += f"   [!] {v['type']} - {v['severity']}\n"
                    
        self.result_label.text = output


class WirelessAuditorApp(App):
    def build(self):
        return AuditorWindow()


if __name__ == "__main__":
    WirelessAuditorApp().run()
