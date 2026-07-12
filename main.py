# -*- coding: utf-8 -*-
"""
GRADUATION PROJECT: WIRELESS SECURITY AUDITOR PROFESSIONAL
MODIFIED FOR GITHUB ACTIONS (CLI ONLY & CI ENVIRONMENT FRIENDLY)
"""
import os
import sys
import subprocess
from datetime import datetime

try:
    from zxcvbn import zxcvbn
    ZXCVBN_AVAILABLE = True
except ImportError:
    ZXCVBN_AVAILABLE = False

class WirelessSecurityAuditor:
    def __init__(self):
        self.vault = {}
        self.nearby_networks = []
        self.total_vulns = 0

    def analyze_password_strength(self, password):
        if password == "[Open Network]":
            return "OPEN", ["No password"], 0, ["Open"]
        if ZXCVBN_AVAILABLE:
            res = zxcvbn(password)
            score = res['score']
            strength = ["VERY WEAK", "WEAK", "FAIR", "GOOD", "STRONG"][score]
            feedback = res['feedback']['suggestions'] or ["No suggestions"]
            if res['feedback']['warning']:
                feedback.insert(0, "⚠ " + res['feedback']['warning'])
            return strength, feedback, score, [f"zxcvbn: {score}/4"]
        else:
            score = 0
            feedback = []
            if len(password) >= 12: score += 3; feedback.append("Good length")
            elif len(password) >= 8: score += 2
            else: feedback.append("Short")
            if any(c.isupper() for c in password): score += 1
            else: feedback.append("No uppercase")
            if any(c.islower() for c in password): score += 1
            else: feedback.append("No lowercase")
            if any(c.isdigit() for c in password): score += 1
            else: feedback.append("No numbers")
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?/~"
            if any(c in symbols for c in password): score += 1
            else: feedback.append("No special chars")
            strength = "STRONG" if score >= 6 else "MEDIUM" if score >= 4 else "WEAK"
            return strength, feedback, score, ["Basic analysis"]

    def get_all_saved_profiles(self):
        if os.getenv("GITHUB_ACTIONS") == "true":
            print("[CI Mode] Simulating saved profiles extraction...")
            self.vault = {
                "test_home_wifi": {"ssid": "Test_Home_WiFi", "password": "password123", "auth": "WPA2-Personal", "cipher": "CCMP", "strength": "WEAK", "score": 1, "feedback": ["Short", "Common password"]}
            }
            return self.vault

        self.vault = {}
        try:
            out = subprocess.check_output("netsh wlan show profiles", shell=True, text=True, errors='ignore', timeout=10)
            profiles = []
            for line in out.split('\n'):
                if "All User Profile" in line:
                    parts = line.split(":")
                    if len(parts) > 1: profiles.append(parts[1].strip())
            for ssid in profiles:
                try:
                    info = subprocess.check_output(f'netsh wlan show profile name="{ssid}" key=clear', shell=True, text=True, errors='ignore', timeout=10)
                    password, auth, cipher = "[Open Network]", "Unknown", "Unknown"
                    for line in info.split('\n'):
                        if "Authentication" in line and len(line.split(":")) > 1: auth = line.split(":")[1].strip()
                        elif "Cipher" in line and len(line.split(":")) > 1: cipher = line.split(":")[1].strip()
                        elif "Key Content" in line and len(line.split(":")) > 1: password = line.split(":")[1].strip()
                    strength, fb, score, _ = self.analyze_password_strength(password)
                    self.vault[ssid.lower()] = {"ssid": ssid, "password": password, "auth": auth, "cipher": cipher, "strength": strength, "score": score, "feedback": fb}
                except: pass
        except: pass
        return self.vault

    def scan_nearby_networks(self):
        if os.getenv("GITHUB_ACTIONS") == "true":
            print("[CI Mode] Simulating nearby networks scan...")
            self.nearby_networks = [
                {"ssid": "Unsecure_Coffee_Shop", "auth": "Open", "encrypt": "None", "vulnerabilities": [], "fixes": []}
            ]
            for net in self.nearby_networks:
                vulns, fixes = self.detect_vulnerabilities(net)
                net['vulnerabilities'] = vulns
                net['fixes'] = fixes
            return self.nearby_networks

        self.nearby_networks = []
        try:
            out = subprocess.check_output("netsh wlan show networks mode=bssid", shell=True, text=True, errors='ignore', timeout=15)
            cur = {}
            for line in out.split('\n'):
                line = line.strip()
                if line.startswith("SSID"):
                    if cur and cur.get('ssid'): self.nearby_networks.append(cur); cur = {}
                    parts = line.split(":", 1)
                    if len(parts) > 1 and parts[1].strip():
                        cur['ssid'] = parts[1].strip(); cur['bssids'] = []; cur['auth'] = "Unknown"; cur['encrypt'] = "Unknown"
                elif "Authentication" in line and len(line.split(":", 1)) > 1: cur['auth'] = line.split(":", 1)[1].strip()
                elif "Encryption" in line and len(line.split(":", 1)) > 1: cur['encrypt'] = line.split(":", 1)[1].strip()
            if cur and cur.get('ssid'): self.nearby_networks.append(cur)
            for net in self.nearby_networks:
                vulns, fixes = self.detect_vulnerabilities(net)
                net['vulnerabilities'] = vulns; net['fixes'] = fixes
        except: pass
        return self.nearby_networks

    def detect_vulnerabilities(self, net):
        vulns, fixes = [], []
        ssid = net.get('ssid', '')
        auth = net.get('auth', '').lower()
        encrypt = net.get('encrypt', '').lower()
        ssid_lower = ssid.lower()
        
        if "open" in auth or "open" in encrypt:
            vulns.append({"type": "Open Network", "severity": "CRITICAL", "description": f"'{ssid}' is OPEN", "risk": "Anyone can connect and sniff traffic."})
            fixes.append({"action": "Enable Encryption", "steps": ["Enable WPA2/WPA3 Personal", "Set a strong password"]})
        elif "wep" in encrypt or "wep" in auth:
            vulns.append({"type": "WEP Encryption", "severity": "CRITICAL", "description": f"'{ssid}' uses WEP", "risk": "WEP encryption can be cracked in minutes."})
            fixes.append({"action": "Upgrade to WPA2/WPA3", "steps": ["Change security mode to WPA2-PSK (AES)"]})
        
        if ssid_lower in self.vault:
            saved_profile = self.vault[ssid_lower]
            if saved_profile.get("strength") in ["VERY WEAK", "WEAK"]:
                vulns.append({"type": "Weak Saved Password", "severity": "HIGH", "description": f"Saved password for '{ssid}' is weak", "risk": "Brute-force risk."})
                fixes.append({"action": "Change Wi-Fi Password", "steps": ["Generate a unique password longer than 12 chars"]})
        return vulns, fixes

if __name__ == "__main__":
    print(f"--- Wireless Security Auditor CLI v1.0 ({datetime.now()}) ---")
    auditor = WirelessSecurityAuditor()
    
    print("\n[+] Extracting Saved Profiles...")
    profiles = auditor.get_all_saved_profiles()
    for ssid, data in profiles.items():
        print(f" -> SSID: {data['ssid']} | Auth: {data['auth']} | Password Strength: {data['strength']}")

    print("\n[+] Scanning Nearby Networks...")
    networks = auditor.scan_nearby_networks()
    for net in networks:
        print(f" -> SSID: {net['ssid']} | Auth: {net.get('auth')} | Vulns Found: {len(net.get('vulnerabilities', []))}")
        for v in net.get('vulnerabilities', []):
            print(f"    [!] {v['type']} ({v['severity']}): {v['description']}")
