# Threads Auto Post

Aplikasi web untuk login/menyambungkan akun Threads dan memposting ke Threads, termasuk auto-post alert saham gorengan (aplikasi web, bukan APK).

## Fitur aplikasi web
- Panel koneksi akun Threads (tautan resmi Meta Accounts Center; aplikasi tidak meminta password/token)
- Composer postingan Threads: penghitung 500 karakter, URL media HTTPS opsional, penjadwalan
- Antrean postingan: Siap posting / Terjadwal / Draf / Riwayat, dengan salin teks, edit, dan tandai terposting
- Auto-post alert saham: toggle on/off, pilihan 4 jenis alert (VWAP, AKUM + SCALPING, ARA HUNTER, SCALPING AWAL), dedup otomatis maksimal 1x per saham per jenis alert per hari WIB, format ≤500 karakter berisi kode, harga, sinyal, entry, cut, dan disclaimer screening
- Panel Ekspor untuk repository

## Skrip di repo ini
- `threads_auto_post.py` — contoh skrip API resmi Meta Threads (bukan library unofficial/reverse-engineered).
  - Izin yang dibutuhkan: `threads_basic` dan `threads_content_publish`
  - Alur: buat media container, lalu `threads_publish`. Teks bisa memakai `auto_publish_text=true`.
  - Batas: 500 karakter, 250 post per akun per 24 jam. API tidak punya penjadwalan bawaan.

## Setup skrip (penting)
1. Buat Meta Developer App dengan use case Threads API.
2. Otorisasi akun Threads-mu sendiri, tukarkan token 1 jam menjadi token panjang (60 hari).
3. Simpan token di GitHub Secrets sebagai `THREADS_ACCESS_TOKEN` (dan `THREADS_USER_ID` bila perlu). **Jangan pernah commit token ke repo.**
4. Jalankan: `python3 threads_auto_post.py "teks postingan"`

## Catatan
- Akun Threads harus tertaut dulu; penerbitan sungguhan butuh persetujuan per postingan sesuai aturan Meta, atau skrip ini dengan token di GitHub Secrets.
- Postingan alert saham adalah hasil screening, bukan rekomendasi pasti, dan selalu disertai disclaimer.
- Repo ini berisi skrip API resmi dan deskripsi proyek; versi web lengkapnya tidak diekspor sebagai kode sumber dari repo ini.
