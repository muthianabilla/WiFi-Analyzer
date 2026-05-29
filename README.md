# 📡 WiFi Analyzer Dashboard

WiFi Analyzer adalah aplikasi untuk menganalisis jaringan WiFi dan memberikan rekomendasi channel optimal.

## 🎯 Fitur

- 📊 Dashboard interaktif dengan Streamlit
- 🔍 Analisis interferensi WiFi (2.4 GHz & 5 GHz)
- 📈 Visualisasi grafik sinyal dan channel map
- ☁️ Simpan hasil scan di Firebase Cloud
- 🎨 UI modern dan user-friendly

## 🚀 Quick Start

### Prerequisite
- Python 3.12+
- Windows 10/11
- Internet connection

### Installation

```bash
# Clone repository
git clone https://github.com/USERNAME/WiFi-Analyzer.git
cd WiFi-Analyzer

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download serviceAccountKey.json dari Firebase
# (Letakkan di folder WiFi-Analyzer)

# Jalankan WiFi Scanner
python wifiscan.py

# Di terminal lain, jalankan Dashboard
streamlit run app.py
```

## 📋 Cara Pakai

1. **Jalankan WiFi Scanner** di laptop Anda:
```bash
   python wifiscan.py
```
   Scanner akan otomatis mendeteksi WiFi networks dan upload ke Firebase.

2. **Buka Dashboard** di browser:
```bash
   streamlit run app.py
```
   Akses di `http://localhost:8501`

3. **Lihat Visualisasi**:
   - Channel recommendation untuk 2.4 GHz & 5 GHz
   - RSSI strength chart
   - Channel map
   - Daftar semua networks yang terdeteksi

## 🔧 Requirements

- streamlit>=1.32.0
- pywifi>=1.1.12
- firebase-admin>=6.4.0
- plotly>=5.20.0
- pandas>=2.0.0
- matplotlib>=3.8.0
- comtypes>=1.1.14

## 📝 Catatan

- `serviceAccountKey.json` tidak di-push ke GitHub (security)
- Virtual environment (`venv/`) diabaikan
- Jalankan scanner **sebagai Administrator** untuk hasil optimal

## 👥 Tim Pengembang

Kelompok 10 - ET3204 Layanan Tersambung dan Komputasi Awan

## 📄 License

MIT License