# BRIEF: Visual Overhaul Scodeno Landing Page
## Untuk: AURA
## Dari: ADING (udah beresin backend + struktur)
## Status: SIAP DIKERJAIN

---

## LOKASI FILE
Semua file di `/home/ace_a/projects/scodeno-landing/`
- `index.html` — halaman utama (sudah bersih, link semua internal)
- `articles/Week_01_*.html` s/d `Week_12_*.html` — 12 artikel (10 full, 2 placeholder)

Server lokal udah nyala: `localhost:8080`

---

## YANG SUDAH BERES (jangan disentuh struktur HTML-nya)
1. Semua link eksternal scodeno.com sudah diganti ke file lokal — jangan tambah link eksternal lagi
2. Navigasi antar artikel (prev/next/breadcrumb) sudah jalan
3. Filter artikel di index (JS hash-based) sudah jalan
4. About section, products grid, footer sudah ada
5. Artikel Week_01-10 konten utuh, Week_11-12 masih placeholder (biarin dulu, ARIS yang isi)

---

## YANG PERLU KAMU KERJAIN (Visual & Copywriting)
1. **Hero section** — ganti headline + subheadline biar lebih punchy, engaging
2. **Product cards** — styling lebih bold, tambahin visual hierarchy
3. **Article cards** — bikin lebih menarik, mungkin tambahin thumbnail/icon
4. **Color scheme** — sekarang mostly biru (#0068B4), lo bisa explore palette yang lebih hidup
5. **Typography** — font Inter udah dipake, lo bisa adjust spacing/sizing
6. **CTA** — bikin lebih prominent, konversi-focused
7. **Konsistensi visual antar halaman** — index + 12 artikel harus satu vibe

---

## BATASAN (ini serius, jangan dilanggar)
- JANGAN ubah struktur navigasi internal — link antar halaman sudah bener semua
- JANGAN tambah link ke scodeno.com atau domain eksternal lain
- JANGAN hapus konten artikel yang sudah ada
- CSS inline/internal styling aja, satu file per halaman (no external CSS dependencies selain Google Fonts Inter)
- Tetep support mobile responsive

---

## KARAKTER YANG DIHARAPKAN
- Industrial tapi modern — bukan pabrik jadul, tapi Industry 4.0
- Clean, bold, percaya diri
- Target audience: engineer pabrik, system integrator, IT manager
- Bukan template generic — harus ada personality

---

## CARA TES
Buka `http://localhost:8080/index.html` di browser, cek semua halaman.
Commit kalo udah ok: `git add -A && git commit -m "Visual overhaul by AURA"`
Push: `GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519_aura_backup" git push origin scodeno-landing`
