# VULNHAVEN

VULNHAVEN — Find · Aggregate · Recommend  
Lightweight CLI wrapper for running Xray-based web vulnerability scans, normalizing results, and producing clean human-readable reports. Dibuat untuk pentesters, bug hunters, dan tim security yang ingin workflow scanning yang cepat & terstruktur di lab mereka.

> ⚠️ IMPORTANT: VULNHAVEN **requires** a working installation of **Xray** on the scanning machine (Linux). This README does **not** include instructions to install Xray — pastikan `xray` (atau path ke binary Xray) sudah tersedia dan dikonfigurasi di sistemmu sebelum menggunakan VULNHAVEN.

---

## Fitur utama
- Satu CLI interaktif untuk melakukan scan Xray dengan tiga mode: `Normal`, `Silent`, `Brutal`.
- Menjalankan Xray dari direktori konfigurasi sehingga `xray.yaml`/`module.xray.yaml` dipakai.
- Parser robust untuk normalisasi output Xray → internal JSON schema.
- Deduplication & ranking hasil berdasarkan severity.
- Rekomendasi mitigasi/verifikasi tingkat tinggi (aman — **tidak** berisi langkah eksploitasi).
- Export laporan otomatis: JSON (structured) + Markdown (human friendly).  
- Fallback mock mode apabila Xray tidak tersedia (berguna saat development).

---

## Siapa yang cocok pakai ini?
- Bug bounty hunters yang ingin workflow scanning cepat dan rapi.  
- Pentesters yang ingin mengotomatisasi langkah awal scan web.  
- Tim devsecops yang butuh integrasi scanning ringan ke pipeline testing internal (lab).

---