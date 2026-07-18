#!/usr/bin/env python3
"""Optimasi internal link scodenoindonesia.com — tambah contextual body link ke homepage & cross-link."""
import re
from pathlib import Path

ARTICLES = Path('/home/ace_a/projects/scodeno-landing/articles')

# === DEFINISI LINK BARU PER ARTIKEL ===
# Format: {filename: [(anchor_text, target_url, insertion_after_text), ...]}
# insertion_after_text = substring unik setelah mana link disisipkan

OPTIMIZATIONS = {
    # Week 01: Fanless → tambah homepage link + cross-link ke Fitur Penting & Industrial vs Commercial
    'Week_01_kenapa-industrial-switch-menggunakan-desain-fanless.html': [
        # Homepage link — setelah "desain fanless adalah fondasi keandalan jangka panjang"
        ('<a href="../">Scodeno industrial switch</a>',
         'desain fanless adalah fondasi keandalan'),
        # Cross-link ke Week 08 Fitur Penting
        ('<a href="Week_08_fitur-penting-industrial-ethernet-switch-yang-harus-anda-ketahui.html">fitur penting</a>',
         'fanless bukan satu-satunya'),
    ],

    # Week 02: DIN-Rail → homepage link + cross-link ke Fitur Penting
    'Week_02_apa-itu-din-rail-industrial-switch-dan-mengapa-banyak-dipakai-di-pabrik.html': [
        ('<a href="../">industrial switch DIN-rail Scodeno</a>',
         'DIN-rail adalah standar'),
        ('<a href="Week_08_fitur-penting-industrial-ethernet-switch-yang-harus-anda-ketahui.html">fitur penting industrial switch</a>',
         'memilih switch'),
    ],

    # Week 03: IP Rating → homepage link + cross-link ke Industrial vs Commercial
    'Week_03_ip-rating-pada-industrial-ethernet-switch-apa-artinya.html': [
        ('<a href="../">industrial ethernet switch Scodeno</a>',
         'IP rating'),
        ('<a href="Week_09_industrial-switch-vs-commercial-switch-apa-perbedaannya.html">industrial vs commercial switch</a>',
         'perlindungan enclosure'),
    ],

    # Week 04: Gigabit vs Fast → homepage link + cross-link ke Monitoring
    'Week_04_industrial-gigabit-switch-vs-fast-ethernet-switch.html': [
        ('<a href="../">Scodeno Indonesia</a>',
         'memilih switch industrial'),
        ('<a href="Week_14_industrial-network-monitoring-system-memantau-jaringan-ot-tanpa-henti.html">monitoring jaringan</a>',
         'kebutuhan bandwidth'),
    ],

    # Week 05: SFP Port → homepage link + cross-link ke VLAN
    'Week_05_industrial-switch-dengan-sfp-port-fungsi-dan-kegunaannya.html': [
        ('<a href="../">industrial switch Indonesia</a>',
         'SFP port'),
        ('<a href="Week_10_vlan-dalam-industrial-ethernet-network.html">VLAN pada jaringan industri</a>',
         'segmentasi'),
    ],

    # Week 06: Managed vs Unmanaged → homepage + monitoring
    'Week_06_managed-vs-unmanaged-industrial-switch-mana-yang-tepat.html': [
        ('<a href="../">distributor industrial switch Indonesia</a>',
         'Scodeno Indonesia'),
        ('<a href="Week_14_industrial-network-monitoring-system-memantau-jaringan-ot-tanpa-henti.html">monitoring jaringan OT</a>',
         'SNMP traps'),
    ],

    # Week 07: PoE → homepage + cross-link ke SFP & Fitur Penting
    'Week_07_industrial-switch-dengan-poe-kapan-dibutuhkan.html': [
        ('<a href="../">Scodeno Indonesia</a>',
         'PoE industrial switch'),
        ('<a href="Week_05_industrial-switch-dengan-sfp-port-fungsi-dan-kegunaannya.html">SFP port pada industrial switch</a>',
         'gigabit'),
    ],

    # Week 08: Fitur Penting → homepage + cross-links ke Fanless, DIN-Rail, IP Rating
    'Week_08_fitur-penting-industrial-ethernet-switch-yang-harus-anda-ketahui.html': [
        ('<a href="../">industrial switch Scodeno</a>',
         'fitur penting'),
        ('<a href="Week_01_kenapa-industrial-switch-menggunakan-desain-fanless.html">desain fanless</a>',
         'keandalan'),
        ('<a href="Week_03_ip-rating-pada-industrial-ethernet-switch-apa-artinya.html">rating IP</a>',
         'proteksi enclosure'),
    ],

    # Week 09: Industrial vs Commercial → homepage + Fanless + IP Rating
    'Week_09_industrial-switch-vs-commercial-switch-apa-perbedaannya.html': [
        ('<a href="../">Scodeno switch industrial</a>',
         'industrial switch'),
        ('<a href="Week_01_kenapa-industrial-switch-menggunakan-desain-fanless.html">kenapa industrial switch pakai desain fanless</a>',
         'fanless'),
    ],

    # Week 10: VLAN → homepage + Managed
    'Week_10_vlan-dalam-industrial-ethernet-network.html': [
        ('<a href="../">industrial network switch Indonesia</a>',
         'VLAN pada industrial switch'),
        ('<a href="Week_06_managed-vs-unmanaged-industrial-switch-mana-yang-tepat.html">managed switch</a>',
         'managed'),
    ],

    # Week 11: QoS → homepage + Managed
    'Week_11_qos-dalam-industrial-network.html': [
        ('<a href="../">Scodeno Indonesia</a>',
         'jaringan industri'),
        ('<a href="Week_06_managed-vs-unmanaged-industrial-switch-mana-yang-tepat.html">managed switch industrial</a>',
         'managed switch'),
    ],

    # Week 12: Segmentation → homepage + Managed + VLAN
    'Week_12_network-segmentation-pada-jaringan-industri.html': [
        ('<a href="../">industrial switch distributor Indonesia</a>',
         'segmentasi jaringan'),
        ('<a href="Week_10_vlan-dalam-industrial-ethernet-network.html">VLAN</a>',
         'memisahkan'),
    ],

    # Week 14: Monitoring → homepage + Fitur Penting
    'Week_14_industrial-network-monitoring-system-memantau-jaringan-ot-tanpa-henti.html': [
        ('<a href="../">Scodeno industrial networking</a>',
         'monitoring'),
        ('<a href="Week_08_fitur-penting-industrial-ethernet-switch-yang-harus-anda-ketahui.html">fitur penting industrial switch</a>',
         'SNMP'),
    ],
}


def apply_optimization(filepath: Path, rules: list):
    """Apply rules to a single HTML file."""
    html = filepath.read_text(encoding='utf-8')
    modified = html
    applied = 0

    for anchor_html, marker in rules:
        # Cari marker dalam konten artikel (bukan di nav/footer)
        # marker harus muncul di body — cari di bagian antara <article> dan </article>
        article_match = re.search(r'(<article\b.*?</article>)', modified, re.DOTALL)
        if not article_match:
            print(f"  ⚠️  Article body not found in {filepath.name}")
            continue

        article_body = article_match.group(1)

        # Cek apakah marker ada dan link yang sama belum ada
        if marker not in article_body:
            print(f"  ⚠️  Marker '{marker[:50]}...' not found in article body")
            continue

        if anchor_html in article_body:
            print(f"  ⏭️  Link '{anchor_html[:50]}...' already exists")
            continue

        # Sisipkan link setelah kemunculan pertama marker di article body
        # Strategi: cari marker, lalu sisipkan link 10-30 karakter setelahnya dalam konteks natural
        idx = article_body.find(marker)
        # Cari akhir kalimat/klausa yang mengandung marker
        # Ambil teks dari marker sampai koma atau titik berikutnya
        snippet = article_body[idx:idx+200]
        # Cari posisi natural untuk insert — setelah kata benda/frasa lengkap
        # Gunakan heuristik: cari 'adalah', 'merupakan', ',' atau '.' setelah marker
        end_markers = ['. ', ', ', ' — ', '.</p>', '.\n']
        insert_offset = len(marker)
        for em in end_markers:
            pos = snippet.find(em, len(marker))
            if 0 < pos < 80:
                insert_offset = pos + len(em.rstrip('.'))
                break

        # Bangun teks baru dengan link disisipkan
        insert_pos = idx + insert_offset
        new_text = modified[:insert_pos] + ' ' + anchor_html + ' ' + modified[insert_pos:]

        # Hindari double space
        new_text = re.sub(r'  +', ' ', new_text)

        modified = new_text
        applied += 1
        print(f"  ✅ Added: {anchor_html[:70]}...")

    return modified, applied


def main():
    total_added = 0
    for filename, rules in OPTIMIZATIONS.items():
        filepath = ARTICLES / filename
        if not filepath.exists():
            print(f"❌ File not found: {filename}")
            continue

        print(f"\n📝 {filename}")
        new_html, applied = apply_optimization(filepath, rules)
        if applied > 0:
            filepath.write_text(new_html, encoding='utf-8')
            total_added += applied
        else:
            print(f"  ⚠️  No links added — skipping write")

    print(f"\n{'='*60}")
    print(f"✅ Done. Total contextual links added: {total_added}")

if __name__ == '__main__':
    main()
