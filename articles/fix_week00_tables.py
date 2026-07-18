#!/usr/bin/env python3
"""Fix the two broken tables in Week 00 HTML"""
from pathlib import Path

f = Path('/home/ace_a/projects/scodeno-landing/articles/Week_00_scodeno-switch-panduan-lengkap.html')
html = f.read_text()

# Problem 1: Replace broken decision framework table 
# (currently only one thead row) with correct full table
old_table1 = '<div class="table-wrap"><table>\n<thead>\n<tr><th>Anggaran terbatas, tapi butuh isolasi port/VLAN/QoS?</th><th>**DIP Switch Scodeno** — *sweet spot*</th><th>—</th></tr>\n</thead>\n</table></div>'

new_table1 = '''<div class="table-wrap"><table>
<thead>
<tr><th>Pertanyaan</th><th>Jika "Ya"</th><th>Jika "Tidak"</th></tr>
</thead>
<tbody>
<tr><td>Jaringan punya &gt;1 jenis trafik (kontrol + video + SCADA)?</td><td>Butuh VLAN → <strong>Managed</strong> atau <strong>DIP Switch</strong></td><td>Unmanaged cukup</td></tr>
<tr><td>Ada kamera/AP/sensor tanpa akses listrik?</td><td><strong>PoE Switch</strong></td><td>Non-PoE</td></tr>
<tr><td>Jarak antar perangkat &gt;100m?</td><td><strong>Switch dengan SFP port</strong> + fiber</td><td>RJ45 cukup</td></tr>
<tr><td>Butuh failover &lt;1 detik jika kabel putus?</td><td><strong>Managed</strong> dengan ring redundancy</td><td>—</td></tr>
<tr><td>Jaringan akan berkembang dalam 2-3 tahun?</td><td><strong>Managed</strong> dari awal</td><td>Unmanaged bisa</td></tr>
<tr><td>Butuh monitoring real-time (SNMP/syslog)?</td><td><strong>Managed</strong></td><td>Unmanaged</td></tr>
<tr><td>Anggaran terbatas, tapi butuh isolasi port/VLAN/QoS?</td><td><strong>DIP Switch Scodeno</strong> — <em>sweet spot</em></td><td>—</td></tr>
</tbody>
</table></div>'''

html = html.replace(old_table1, new_table1)

# Problem 2: Fix the "Panduan Mendalam" table — currently broken into <p> tags
# Find the pattern: bunch of <p>| ... |</p> lines between two headings
old_articles_section = '<p>| Topik | Artikel | Waktu Baca |</p>\n<p>|-------|---------|-----------|</p>\n<p>| Desain Fanless | <a href="Week_01_kenapa-industrial-switch-menggunakan-desain-fanless.html">Kenapa Industrial Switch Menggunakan Desain Fanless</a> | 10 menit |</p>\n<p>| DIN-Rail Mounting | <a href="Week_02_apa-itu-din-rail-industrial-switch-dan-mengapa-banyak-dipakai-di-pabrik.html">Apa Itu DIN-Rail Industrial Switch</a> | 12 menit |</p>\n<p>| IP Rating | <a href="Week_03_ip-rating-pada-industrial-ethernet-switch-apa-artinya.html">IP Rating pada Industrial Ethernet Switch</a> | 8 menit |</p>\n<p>| Gigabit vs Fast | <a href="Week_04_industrial-gigabit-switch-vs-fast-ethernet-switch.html">Industrial Gigabit Switch vs Fast Ethernet Switch</a> | 7 menit |</p>\n<p>| SFP & Fiber | <a href="Week_05_industrial-switch-dengan-sfp-port-fungsi-dan-kegunaannya.html">Industrial Switch dengan SFP Port</a> | 7 menit |</p>\n<p>| Managed vs Unmanaged | <a href="Week_06_managed-vs-unmanaged-industrial-switch-mana-yang-tepat.html">Managed vs Unmanaged Industrial Switch</a> | 8 menit |</p>\n<p>| PoE | <a href="Week_07_industrial-switch-dengan-poe-kapan-dibutuhkan.html">Industrial Switch dengan PoE: Kapan Dibutuhkan?</a> | 7 menit |</p>\n<p>| Buyer\'s Guide | <a href="Week_08_fitur-penting-industrial-ethernet-switch-yang-harus-anda-ketahui.html">11 Fitur Penting Industrial Ethernet Switch</a> | 14 menit |</p>\n<p>| Industrial vs Commercial | <a href="Week_09_industrial-switch-vs-commercial-switch-apa-perbedaannya.html">Industrial Switch vs Commercial Switch</a> | 7 menit |</p>\n<p>| VLAN | <a href="Week_10_vlan-dalam-industrial-ethernet-network.html">VLAN dalam Industrial Ethernet Network</a> | 7 menit |</p>\n<p>| QoS | <a href="Week_11_qos-dalam-industrial-network.html">QoS dalam Industrial Network</a> | 8 menit |</p>\n<p>| Network Segmentation | <a href="Week_12_network-segmentation-pada-jaringan-industri.html">Network Segmentation pada Jaringan Industri</a> | 7 menit |</p>\n<div class="table-wrap"><table>\n<thead>\n<tr><th>Monitoring</th><th>[Industrial Network Monitoring System](Week_14_industrial-network-monitoring-system-memantau-jaringan-ot-tanpa-henti.html)</th><th>10 menit</th></tr>\n</thead>\n</table></div>'

new_articles_table = '''<div class="table-wrap"><table>
<thead>
<tr><th>Topik</th><th>Artikel</th><th>Waktu Baca</th></tr>
</thead>
<tbody>
<tr><td>Desain Fanless</td><td><a href="Week_01_kenapa-industrial-switch-menggunakan-desain-fanless.html">Kenapa Industrial Switch Menggunakan Desain Fanless</a></td><td>10 menit</td></tr>
<tr><td>DIN-Rail Mounting</td><td><a href="Week_02_apa-itu-din-rail-industrial-switch-dan-mengapa-banyak-dipakai-di-pabrik.html">Apa Itu DIN-Rail Industrial Switch</a></td><td>12 menit</td></tr>
<tr><td>IP Rating</td><td><a href="Week_03_ip-rating-pada-industrial-ethernet-switch-apa-artinya.html">IP Rating pada Industrial Ethernet Switch</a></td><td>8 menit</td></tr>
<tr><td>Gigabit vs Fast</td><td><a href="Week_04_industrial-gigabit-switch-vs-fast-ethernet-switch.html">Industrial Gigabit Switch vs Fast Ethernet Switch</a></td><td>7 menit</td></tr>
<tr><td>SFP &amp; Fiber</td><td><a href="Week_05_industrial-switch-dengan-sfp-port-fungsi-dan-kegunaannya.html">Industrial Switch dengan SFP Port</a></td><td>7 menit</td></tr>
<tr><td>Managed vs Unmanaged</td><td><a href="Week_06_managed-vs-unmanaged-industrial-switch-mana-yang-tepat.html">Managed vs Unmanaged Industrial Switch</a></td><td>8 menit</td></tr>
<tr><td>PoE</td><td><a href="Week_07_industrial-switch-dengan-poe-kapan-dibutuhkan.html">Industrial Switch dengan PoE: Kapan Dibutuhkan?</a></td><td>7 menit</td></tr>
<tr><td>Buyer\'s Guide</td><td><a href="Week_08_fitur-penting-industrial-ethernet-switch-yang-harus-anda-ketahui.html">11 Fitur Penting Industrial Ethernet Switch</a></td><td>14 menit</td></tr>
<tr><td>Industrial vs Commercial</td><td><a href="Week_09_industrial-switch-vs-commercial-switch-apa-perbedaannya.html">Industrial Switch vs Commercial Switch</a></td><td>7 menit</td></tr>
<tr><td>VLAN</td><td><a href="Week_10_vlan-dalam-industrial-ethernet-network.html">VLAN dalam Industrial Ethernet Network</a></td><td>7 menit</td></tr>
<tr><td>QoS</td><td><a href="Week_11_qos-dalam-industrial-network.html">QoS dalam Industrial Network</a></td><td>8 menit</td></tr>
<tr><td>Network Segmentation</td><td><a href="Week_12_network-segmentation-pada-jaringan-industri.html">Network Segmentation pada Jaringan Industri</a></td><td>7 menit</td></tr>
<tr><td>Monitoring</td><td><a href="Week_14_industrial-network-monitoring-system-memantau-jaringan-ot-tanpa-henti.html">Industrial Network Monitoring System</a></td><td>10 menit</td></tr>
</tbody>
</table></div>'''

if old_articles_section in html:
    html = html.replace(old_articles_section, new_articles_table)
    print("✅ Articles table fixed")
else:
    print("❌ Could not find articles table section")

f.write_text(html)
print("✅ Week 00 HTML repaired")
