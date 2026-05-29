"""
wifiscan.py
Script untuk scan WiFi dan upload ke Firebase.
"""

import pywifi
from pywifi import const
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json
import os

# ─────────────────────────────────────────
# Inisialisasi Firebase
# ─────────────────────────────────────────
def init_firebase():
    if firebase_admin._apps:
        return firestore.client()
    
    key_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
    if not os.path.exists(key_path):
        print(f"❌ Error: {key_path} tidak ditemukan!")
        return None
    
    try:
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase connected!")
        return firestore.client()
    except Exception as e:
        print(f"❌ Firebase error: {e}")
        return None

# ─────────────────────────────────────────
# Scan WiFi networks
# ─────────────────────────────────────────
def scan_wifi():
    """Scan semua WiFi network yang tersedia."""
    try:
        wifi = pywifi.PyWiFi()
        ifaces = wifi.interfaces()
        
        if not ifaces:
            print("❌ Tidak ada WiFi interface ditemukan!")
            return []
        
        iface = ifaces[0]
        print(f"🔍 Scanning dengan interface: {iface.name}")
        
        iface.scan()
        import time
        time.sleep(3)  # Tunggu hasil scan
        
        results = iface.scan_results()
        networks = []
        
        for bss in results:
            # Tentukan band
            freq = bss.freq
            if 2400 <= freq <= 2500:
                band = "2.4 GHz"
            elif 5000 <= freq <= 6000:
                band = "5 GHz"
            else:
                band = "Unknown"
            
            # Tentukan channel dari frequency
            channel = freq_to_channel(freq)
            
            # Hitung quality/signal strength
            rssi = bss.signal
            quality = rssi_to_quality(rssi)
            
            networks.append({
                "ssid": bss.ssid or "[Hidden]",
                "bssid": bss.bssid,
                "rssi": rssi,
                "channel": channel,
                "band": band,
                "quality": quality,
                "freq": freq,
                "timestamp": datetime.now().isoformat(),
            })
        
        return networks
    
    except Exception as e:
        print(f"❌ Scan error: {e}")
        return []

# ─────────────────────────────────────────
# Utility functions
# ─────────────────────────────────────────
def freq_to_channel(freq):
    """Konversi frequency (MHz) ke channel number."""
    if 2412 <= freq <= 2472:
        return (freq - 2407) // 5
    elif 5180 <= freq <= 5825:
        return (freq - 5000) // 5
    return 0

def rssi_to_quality(rssi):
    """Konversi RSSI ke kualitas sinyal."""
    if rssi >= -50:
        return "Excellent"
    elif rssi >= -60:
        return "Good"
    elif rssi >= -70:
        return "Fair"
    else:
        return "Poor"

# ─────────────────────────────────────────
# Upload ke Firebase
# ─────────────────────────────────────────
def upload_to_firebase(db, networks):
    """Upload hasil scan ke Firestore."""
    if db is None or not networks:
        print("❌ Database tidak tersedia atau tidak ada network!")
        return False
    
    try:
        scan_data = {
            "timestamp": datetime.now().isoformat(),
            "networks": networks,
            "total": len(networks),
        }
        
        db.collection("wifi_scans").add(scan_data)
        print(f"✅ Upload sukses! {len(networks)} jaringan tersimpan di Firebase")
        return True
    
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

# ─────────────────────────────────────────
# Main
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("📡 WiFi Scanner — Kelompok 10 ET3204")
    print("=" * 50)
    
    db = init_firebase()
    if db is None:
        print("\n⚠️  Tidak bisa connect ke Firebase.")
        print("Pastikan serviceAccountKey.json ada di folder ini!")
        input("Tekan Enter untuk keluar...")
        exit(1)
    
    print("\n🔍 Scanning WiFi networks...")
    networks = scan_wifi()
    
    if networks:
        print(f"\n📊 Ditemukan {len(networks)} jaringan:")
        for net in networks:
            print(f"  • {net['ssid']:30s} | Ch {net['channel']:3d} ({net['band']}) | RSSI {net['rssi']} | {net['quality']}")
        
        print("\n📤 Uploading ke Firebase...")
        upload_to_firebase(db, networks)
    else:
        print("\n❌ Tidak ada jaringan ditemukan!")
    
    print("\n✅ Selesai! Buka dashboard di browser (lihat instruksi berikutnya)")
    input("Tekan Enter untuk keluar...")