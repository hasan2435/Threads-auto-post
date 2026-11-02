#!/usr/bin/env python3
"""
Threads Auto Post — skrip API resmi Meta Threads.

Cara pakai:
  1. Buat Meta Developer App dengan use case Threads API.
  2. Beri izin threads_basic dan threads_content_publish.
  3. Otorisasi akun Threads-mu sendiri, tukarkan token 1 jam menjadi
     token panjang (60 hari), simpan sebagai variabel lingkungan
     THREADS_ACCESS_TOKEN (jangan pernah commit token ke repo).
  4. Jalankan: python3 threads_auto_post.py "Teks postingan maksimal 500 karakter"

Untuk gambar/video, Threads membutuhkan URL HTTPS publik, bukan upload
file lokal langsung. Alur resmi: buat media container dulu, lalu publish.

  POST https://graph.threads.net/v1.0/{user_id}/threads
    media_type=TEXT|IMAGE|VIDEO|CAROUSEL, text=..., image_url=... (bila ada)
  -> creation_id
  POST https://graph.threads.net/v1.0/{user_id}/threads_publish
    creation_id=...

Untuk teks saja bisa memakai auto_publish_text=true pada langkah pertama.
Batas: 500 karakter per post, 250 post per akun per 24 jam.
API tidak punya penjadwalan bawaan — jadwalkan pemanggilan skrip ini
dengan cron atau GitHub Actions (lihat .github/workflows/threads-daily.yml).

Skrip ini adalah contoh resmi, bukan library unofficial/reverse-engineered.
Hasil screening saham yang diposting lewat skrip ini wajib menyertakan
disclaimer bahwa itu screening, bukan rekomendasi pasti.
"""
import os
import sys
import time
import urllib.parse
import urllib.request

API_BASE = "https://graph.threads.net/v1.0"


def _post(path, data):
    token = os.environ.get("THREADS_ACCESS_TOKEN", "")
    user_id = os.environ.get("THREADS_USER_ID", "me")
    if not token:
        raise SystemExit("THREADS_ACCESS_TOKEN belum di-set (simpan di GitHub Secrets, jangan di-commit).")
    body = urllib.parse.urlencode({**data, "access_token": token}).encode()
    req = urllib.request.Request(f"{API_BASE}/{user_id}{path}", data=body, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode()


def publish_text(text, image_url=None):
    if len(text) > 500:
        raise SystemExit(f"Teks {len(text)} karakter, melebihi batas Threads 500 karakter.")
    data = {"media_type": "TEXT", "text": text}
    if image_url:
        data = {"media_type": "IMAGE", "text": text, "image_url": image_url}
        # Untuk media: buat container, tunggu, lalu publish.
        import json
        creation_id = json.loads(_post("/threads", data))["id"]
        time.sleep(30)
        return _post("/threads_publish", {"creation_id": creation_id})
    data["auto_publish_text"] = "true"
    return _post("/threads", data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Pakai: python3 threads_auto_post.py "teks postingan"')
    print(publish_text(sys.argv[1], os.environ.get("THREADS_IMAGE_URL") or None))
