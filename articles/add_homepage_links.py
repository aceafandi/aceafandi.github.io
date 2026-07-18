#!/usr/bin/env python3
"""Tambah contextual homepage links ke artikel yang belum punya."""
import re
from pathlib import Path

ARTICLES = Path('.')

# Per artikel: (unique_marker, insert_before_or_after, anchor_html)
# insert_mode: 'before' (link sebelum marker) atau 'replace' (ganti teks dengan link)
PATCHES = {
    'Week_02_apa-itu-din-rail-industrial-switch-dan-mengapa-banyak-dipakai-di-pabrik.html': (
        'pada rel DIN standar 35 mm',
        'after',
        ' <a href="../">distributor industrial switch DIN-rail Scodeno Indonesia</a> menyediakan'
    ),
    'Week_04_industrial-gigabit-switch-vs-fast-ethernet-switch.html': (
        'Lowe (2016): "Jangan pernah memasang kabel di bawah Cat5e."',
        'after',
        ' Bagi yang membutuhkan <a href="../">industrial switch Scodeno</a> dengan port Gigabit,'
    ),
    'Week_06_managed-vs-unmanaged-industrial-switch-mana-yang-tepat.html': (
        'standar minimum',
        'replace',
        'standar minimum — dan <a href="../">Scodeno Indonesia</a> menyediakan kedua opsi dengan dukungan teknis lokal'
    ),
    'Week_07_industrial-switch-dengan-poe-kapan-dibutuhkan.html': (
        'jaringan industri',
        'after',
        ', konsultasikan dengan <a href="../">Scodeno Indonesia</a>'
    ),
    'Week_08_fitur-penting-industrial-ethernet-switch-yang-harus-anda-ketahui.html': (
        'memilih switch industrial yang tepat',
        'replace',
        'memilih <a href="../">industrial switch Scodeno</a> yang tepat'
    ),
    'Week_09_industrial-switch-vs-commercial-switch-apa-perbedaannya.html': (
        'industrial switch, bukan switch komersial, yang menjadi pilihan tepat',
        'replace',
        '<a href="../">Scodeno switch industrial</a>, bukan switch komersial, yang menjadi pilihan tepat'
    ),
    'Week_10_vlan-dalam-industrial-ethernet-network.html': (
        'infrastruktur jaringan industri',
        'after',
        ' — <a href="../">industrial network switch Indonesia</a> yang mendukung VLAN penuh'
    ),
    'Week_12_network-segmentation-pada-jaringan-industri.html': (
        'network segmentation pada jaringan industri',
        'replace',
        'network segmentation pada <a href="../">jaringan industri</a>'
    ),
}


def apply_patch(content, marker, mode, anchor_html):
    if mode == 'after':
        new_str = marker + anchor_html
        if new_str in content:
            return content, False
        if marker not in content:
            return content, False
        return content.replace(marker, new_str, 1), True
    elif mode == 'replace':
        if anchor_html in content:
            return content, False
        if marker not in content:
            return content, False
        return content.replace(marker, anchor_html, 1), True
    return content, False


def main():
    total = 0
    for fname, (marker, mode, anchor) in PATCHES.items():
        fp = ARTICLES / fname
        if not fp.exists():
            print(f"❌ {fname}: not found")
            continue

        html = fp.read_text(encoding='utf-8')

        # Cek apakah sudah ada contextual homepage link di body
        article_match = re.search(r'(<article\b.*?</article>)', html, re.DOTALL | re.IGNORECASE)
        if not article_match:
            print(f"⚠️  {fname}: no article body")
            continue
        body = article_match.group(1)

        # Hitung link ke ../ yang bukan nav/footer
        existing = len(re.findall(r'href="\.\./"(?!.*nav-logo|footer-inner)', body))
        if existing >= 1:
            print(f"⏭️  {fname}: already has {existing} contextual homepage link(s)")
            continue

        new_html, applied = apply_patch(html, marker, mode, anchor)
        if applied:
            fp.write_text(new_html, encoding='utf-8')
            total += 1
            print(f"✅ {fname}: homepage link added")
        else:
            print(f"⚠️  {fname}: marker not found or link exists")

    print(f"\n{'='*50}")
    print(f"Done. Added {total} homepage links.")


if __name__ == '__main__':
    main()
