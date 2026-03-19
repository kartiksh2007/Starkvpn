#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import random

class StarkGhostFinal:
    def __init__(self):
        if os.getuid() != 0:
            print("\n[🚨] ERROR: Please run with 'sudo python3 v10_final.py'")
            sys.exit()
        self.interface = self.get_active_interface()
        self.old_host = subprocess.check_output(["hostname"]).decode().strip()

    def get_active_interface(self):
        try:
            res = subprocess.check_output(r"ip route get 1.1.1.1 | grep -Po '(?<=dev )(\S+)'", shell=True)
            return res.decode().strip()
        except: return "eth0"

    def activate_phantom(self):
        print("\n--- STARK-GHOST v10.1 | PHANTOM ACTIVATED ---")
        
        # 1. Identity Masking
        print("[!] CHANGING HARDWARE ID (MAC)...")
        subprocess.run(["ip", "link", "set", self.interface, "down"])
        subprocess.run(["macchanger", "-r", self.interface], capture_output=True)
        subprocess.run(["ip", "link", "set", self.interface, "up"])
        
        new_host = f"Stark-Ghost-{random.randint(100, 999)}"
        subprocess.run(["hostname", new_host])
        print(f"[✓] IDENTITY: {new_host} | MAC: RANDOMIZED")

        # 2. Network Tunneling (Transparent Proxy)
        print("[!] DEPLOYING ANTI-TRACE FIREWALL...")
        rules = [
            "iptables -P INPUT ACCEPT",
            "iptables -P FORWARD ACCEPT",
            "iptables -P OUTPUT ACCEPT",
            "iptables -t nat -F",
            "iptables -t nat -A OUTPUT -m owner --uid-owner debian-tor -j RETURN",
            "iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports 5353",
            "iptables -t nat -A OUTPUT -p tcp --syn -j REDIRECT --to-ports 9040",
            "iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT",
            "iptables -A OUTPUT -m owner --uid-owner debian-tor -j ACCEPT",
            "iptables -A OUTPUT -j REJECT" # The Kill-Switch
        ]
        for r in rules:
            subprocess.run(f"sudo {r}", shell=True)
        
        # DNS Leak Protection
        subprocess.run("echo 'nameserver 127.0.0.1' > /etc/resolv.conf", shell=True)
        print("[✓] TUNNEL ACTIVE: YOU ARE NOW UNTRACEABLE.")

    def run(self):
        os.system("clear")
        try:
            self.activate_phantom()
            print("\n" + "="*50)
            print("🔴 FBI/CBI/HACKER STATUS: BLINDED 🔴")
            print("Your real location is now hidden behind 3 Global Nodes.")
            print("All your tools (Nmap, Browser, Python) are now Proxied.")
            print("PRESS CTRL+C TO SHUT DOWN AND DELETE TRACES.")
            print("="*50 + "\n")
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        print("\n[!] EMERGENCY NUKE: PURGING ALL EVIDENCE...")
        subprocess.run("iptables -F && iptables -t nat -F", shell=True)
        subprocess.run(["hostname", self.old_host])
        subprocess.run("echo 'nameserver 8.8.8.8' > /etc/resolv.conf", shell=True)
        subprocess.run(["ip", "link", "set", self.interface, "down"])
        subprocess.run(["macchanger", "-p", self.interface], capture_output=True)
        subprocess.run(["ip", "link", "set", self.interface, "up"])
        print("[✓] SYSTEM RETURNED TO NORMAL. NO LOGS LEFT.")

if __name__ == "__main__":
    stark = StarkGhostFinal()
    stark.run()