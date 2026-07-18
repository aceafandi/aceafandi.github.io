#!/usr/bin/env python3
"""Build search index for scodenoindonesia.com — articles + products"""
import json, re
from pathlib import Path

articles_dir = Path('/home/ace_a/projects/scodeno-landing/articles')

index = []

# === ARTICLES ===
for f in sorted(articles_dir.glob('Week_*.html')):
    html = f.read_text(encoding='utf-8')
    # Extract title
    title_m = re.search(r'<title>(.*?)(?: — Scodeno Indonesia)?</title>', html)
    title = title_m.group(1).strip() if title_m else f.stem
    
    # Extract first paragraph as snippet
    body_m = re.search(r'<article\b.*?<p>(.*?)</p>', html, re.DOTALL)
    snippet = ''
    if body_m:
        snippet = re.sub(r'<[^>]+>', '', body_m.group(1)).strip()[:120]
    
    # Extract tag
    tag_m = re.search(r'<span class="article-tag">(.*?)</span>', html)
    tag = tag_m.group(1) if tag_m else 'Article'
    
    index.append({
        'title': title,
        'url': f'articles/{f.name}',
        'snippet': snippet,
        'category': 'Artikel',
        'tag': tag
    })

# === PRODUCTS ===
# Scodeno product categories from homepage
products = [
    # Unmanaged Switches
    {'title': 'S200 Series Unmanaged Switch — Non-PoE', 'url': '#products', 'snippet': 'Industrial unmanaged switch, plug-and-play, DIN-rail, fanless design.', 'category': 'Produk', 'tag': 'Unmanaged'},
    {'title': 'S200 Series Unmanaged Switch — PoE', 'url': '#products', 'snippet': 'Unmanaged PoE industrial switch dengan PoE Watchdog dan DIP switch.', 'category': 'Produk', 'tag': 'Unmanaged'},
    {'title': 'XPTN-9000-45 Series Unmanaged', 'url': '#products', 'snippet': 'Industrial Ethernet switch 4-port 100Mbps, DIN-rail, IP40, fanless.', 'category': 'Produk', 'tag': 'Unmanaged'},
    {'title': 'XPTN-9000-65 Series Unmanaged', 'url': '#products', 'snippet': '6 Series industrial switch dengan DIP switch: VLAN, QoS, Port Isolation.', 'category': 'Produk', 'tag': 'Unmanaged'},
    # Managed Switches
    {'title': 'S200 Series Layer 2+ Managed Switch', 'url': '#products', 'snippet': 'Managed industrial switch dengan VLAN 802.1Q, QoS, SNMP, ring redundancy.', 'category': 'Produk', 'tag': 'Managed'},
    {'title': 'XPTN-9000-77 Series Layer 2+ Managed', 'url': '#products', 'snippet': 'Layer 2+ managed switch industrial, ERPS ring, dual power, wide temp.', 'category': 'Produk', 'tag': 'Managed'},
    {'title': 'XPTN-9000-85 Series Layer 2 Managed — Rack Mount', 'url': '#products', 'snippet': 'Rack-mount managed industrial switch 24-port, 10G uplink, redundancy.', 'category': 'Produk', 'tag': 'Managed'},
    # Specialty
    {'title': 'S200 Series 2.5G Unmanaged Switch', 'url': '#products', 'snippet': 'Industrial 2.5 Gigabit switch, multi-gig, fanless, DIN-rail.', 'category': 'Produk', 'tag': 'Unmanaged'},
    {'title': 'S200 Series 2.5G Layer 3 Switch', 'url': '#products', 'snippet': 'Layer 3 managed industrial switch 2.5G, 10G uplink.', 'category': 'Produk', 'tag': 'Managed'},
    {'title': 'Industrial PoE Switch — XPTN-9000 Series', 'url': '#products', 'snippet': 'PoE industrial switch, 802.3af/at, PoE Watchdog, VIP Power Port.', 'category': 'Produk', 'tag': 'PoE'},
    {'title': 'Industrial Switch dengan SFP Port', 'url': '#products', 'snippet': 'Fiber-ready industrial switch, multimode/single-mode SFP modules.', 'category': 'Produk', 'tag': 'Fiber'},
    {'title': 'Data Center Switch — Scodeno', 'url': '#products', 'snippet': 'Data center and cloud computing switch, high-density 10G/25G/100G.', 'category': 'Produk', 'tag': 'Data Center'},
]

index.extend(products)

out = articles_dir / 'search-index.json'
out.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'✅ Index: {len(index)} items ({len(index)-len(products)} articles + {len(products)} products)')
