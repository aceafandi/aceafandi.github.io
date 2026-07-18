#!/usr/bin/env python3
"""Generate HTML for Week 13 — Network Downtime"""
import re
from pathlib import Path

md_file = Path('/mnt/d/Dokumen/Konexindo/4-SEO-Konten/artikel/Week_13_network-downtime-pabrik.md')
out_dir = Path('/home/ace_a/projects/scodeno-landing/articles')
out_file = out_dir / 'Week_13_network-downtime-pabrik.html'

md = md_file.read_text(encoding='utf-8')

lines = md.strip().split('\n')
title = "Cara Mencegah Network Downtime di Pabrik"
meta_desc = "Lima lapis pertahanan mencegah network downtime di pabrik: redundant power, uplink ganda, ring topology, segmentasi, dan monitoring proaktif."

body_parts = []
in_table = False
in_list = None
current_lines = []
skipped_meta = False

def flush_paragraph():
    global current_lines
    if current_lines:
        text = ' '.join(current_lines).strip()
        if text:
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
            body_parts.append(f'<p>{text}</p>')
        current_lines = []

def flush_table():
    global current_lines, in_table
    if current_lines:
        rows_html = []
        for i, line in enumerate(current_lines):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if i == 0:
                rows_html.append('<thead>\n<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>\n</thead>')
            elif '---' in line:
                continue
            else:
                rows_html.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
        body_parts.append('<div class="table-wrap"><table>\n' + '\n'.join(rows_html) + '\n</table></div>')
        current_lines = []
    in_table = False

for i, line in enumerate(lines):
    # Skip meta comment
    if line.startswith('<!--') or (not skipped_meta and i < 5):
        if '-->' in line:
            skipped_meta = True
        continue
    if not skipped_meta:
        continue

    # Skip H1
    if line.startswith('# '):
        continue

    if not line.strip():
        if in_table: flush_table()
        elif in_list: body_parts.append(f'</{in_list}>'); in_list = None
        else: flush_paragraph()
        continue

    if line.strip() == '---':
        if in_table: flush_table()
        if in_list: body_parts.append(f'</{in_list}>'); in_list = None
        flush_paragraph()
        body_parts.append('<hr>')
        continue

    if line.startswith('## '):
        if in_table: flush_table()
        if in_list: body_parts.append(f'</{in_list}>'); in_list = None
        flush_paragraph()
        h2 = line[3:].strip()
        h2 = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', h2)
        body_parts.append(f'<h2>{h2}</h2>')
        continue

    if line.startswith('### '):
        if in_table: flush_table()
        if in_list: body_parts.append(f'</{in_list}>'); in_list = None
        flush_paragraph()
        h3 = line[4:].strip()
        h3 = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', h3)
        body_parts.append(f'<h3>{h3}</h3>')
        continue

    if line.strip().startswith('|') and line.strip().endswith('|'):
        if in_list: body_parts.append(f'</{in_list}>'); in_list = None
        flush_paragraph()
        if not in_table: in_table = True
        current_lines.append(line.strip())
        continue

    if line.strip().startswith('- '):
        if in_table: flush_table()
        flush_paragraph()
        if in_list != 'ul':
            if in_list: body_parts.append(f'</{in_list}>')
            body_parts.append('<ul>')
            in_list = 'ul'
        item = line.strip()[2:]
        item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
        item = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', item)
        body_parts.append(f'<li>{item}</li>')
        continue

    if re.match(r'^\d+\.\s', line.strip()):
        if in_table: flush_table()
        flush_paragraph()
        if in_list != 'ol':
            if in_list: body_parts.append(f'</{in_list}>')
            body_parts.append('<ol>')
            in_list = 'ol'
        item = re.sub(r'^\d+\.\s', '', line.strip())
        item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
        item = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', item)
        body_parts.append(f'<li>{item}</li>')
        continue

    current_lines.append(line.strip())

if in_table: flush_table()
if in_list: body_parts.append(f'</{in_list}>')
flush_paragraph()

# Add homepage contextual link in the conclusion
for j, part in enumerate(body_parts):
    if 'lima langkah di atas bisa memastikan jaringan' in part:
        body_parts[j] = part.replace(
            'lima langkah di atas bisa memastikan jaringan',
            'lima langkah di atas — dengan <a href="../">switch industrial Scodeno</a> yang mendukung redundant power, ERPS, dan SNMP — bisa memastikan jaringan'
        )
        break

article_body = '\n'.join(body_parts)
words = len(md.split())
read_time = max(1, round(words / 160))

html = f'''<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Scodeno Indonesia</title>
  <meta name="description" content="{meta_desc}">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --blue: #0068B4; --blue-light: #0095E0; --blue-dark: #004A82; --blue-bg: #E7F3FB;
      --blue-glow: rgba(0,104,180,0.20);
      --black: #0A0E14; --near-black: #141A22; --dark-card: #1A202A;
      --white: #FFFFFF; --off-white: #F5F7FA; --gray-50: #F9FAFB; --gray-100: #E8ECF0;
      --gray-200: #C8CDD4; --gray-300: #9BA2AB; --gray-400: #6B7280; --gray-500: #4B5563;
      --text-dark: #1A1A1A; --text-light: #E2E8F0; --text-muted: #9BA2AB;
      --content-max: 780px; --radius-sm: 2px; --radius-md: 4px;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family:'Inter',system-ui,sans-serif; color:var(--text-dark); background:var(--white); line-height:1.7; }}
    .nav {{ position:fixed; top:0; left:0; right:0; z-index:100; background:rgba(10,14,20,0.94); backdrop-filter:blur(12px); border-bottom:1px solid rgba(255,255,255,0.06); }}
    .nav-inner {{ max-width:1200px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; padding:0 24px; height:64px; }}
    .nav-left {{ display:flex; align-items:center; gap:32px; }}
    .nav-logo {{ display:flex; align-items:center; gap:10px; text-decoration:none; }}
    .nav-logo-img {{ height:28px; width:auto; }}
    .nav-logo-text {{ font-weight:800; font-size:1.0625rem; color:var(--white); letter-spacing:-0.01em; }}
    .nav-logo-indonesia {{ color:var(--blue-light); margin-left:2px; }}
    .nav-links {{ display:flex; align-items:center; gap:4px; list-style:none; }}
    .nav-links a {{ color:var(--gray-300); text-decoration:none; font-size:0.8125rem; font-weight:500; padding:8px 12px; border-radius:4px; }}
    .nav-links a:hover {{ color:var(--white); background:rgba(255,255,255,0.06); }}
    .nav-dropdown {{ position:relative; }}
    .nav-dropdown>a::after {{ content:'▾'; font-size:0.625rem; margin-left:2px; }}
    .nav-dropdown-menu {{ position:absolute; top:100%; left:0; min-width:200px; background:var(--dark-card); border:1px solid rgba(255,255,255,0.08); border-radius:6px; padding:6px 0; opacity:0; visibility:hidden; transform:translateY(4px); transition:all 0.18s; box-shadow:0 12px 32px rgba(0,0,0,0.35); }}
    .nav-dropdown:hover .nav-dropdown-menu {{ opacity:1; visibility:visible; transform:translateY(0); }}
    .nav-dropdown-menu a {{ display:block; padding:8px 16px!important; font-size:0.8125rem!important; color:var(--gray-300)!important; border-radius:0!important; }}
    .nav-dropdown-menu a:hover {{ background:rgba(255,255,255,0.06)!important; color:var(--white)!important; }}
    .nav-cta {{ background:var(--blue); color:var(--white)!important; padding:8px 18px!important; border-radius:4px!important; font-weight:600!important; }}
    .nav-cta:hover {{ background:var(--blue-light)!important; }}
    .article-header {{ background:var(--black); color:var(--white); padding:calc(64px + 64px) 24px 64px; position:relative; overflow:hidden; }}
    .article-header::before {{ content:''; position:absolute; top:-30%; right:-20%; width:500px; height:500px; background:radial-gradient(circle,var(--blue-glow) 0%,transparent 70%); pointer-events:none; }}
    .article-header-inner {{ max-width:var(--content-max); margin:0 auto; position:relative; z-index:1; }}
    .article-tag {{ display:inline-block; background:rgba(0,149,224,0.15); color:var(--blue-light); font-size:0.75rem; font-weight:600; padding:4px 12px; border-radius:2px; margin-bottom:16px; text-transform:uppercase; letter-spacing:0.06em; }}
    .article-header h1 {{ font-size:clamp(1.75rem,4vw,2.5rem); font-weight:800; line-height:1.15; letter-spacing:-0.02em; margin-bottom:16px; }}
    .article-header .article-meta {{ color:var(--text-muted); font-size:0.875rem; display:flex; gap:20px; }}
    .article-body {{ max-width:var(--content-max); margin:0 auto; padding:64px 24px; }}
    .article-body h2 {{ font-size:1.5rem; font-weight:700; color:var(--near-black); margin:48px 0 16px; letter-spacing:-0.01em; }}
    .article-body h3 {{ font-size:1.25rem; font-weight:600; color:var(--near-black); margin:32px 0 12px; }}
    .article-body p {{ color:var(--gray-500); font-size:1.0625rem; margin-bottom:20px; line-height:1.8; }}
    .article-body ul,.article-body ol {{ color:var(--gray-500); font-size:1.0625rem; margin-bottom:20px; padding-left:24px; }}
    .article-body li {{ margin-bottom:8px; line-height:1.7; }}
    .article-body strong {{ color:var(--text-dark); font-weight:600; }}
    .article-body a {{ color:var(--blue); text-decoration:underline; }}
    .article-body a:hover {{ color:var(--blue-light); }}
    .article-body hr {{ border:none; border-top:1px solid var(--gray-100); margin:48px 0; }}
    .table-wrap {{ overflow-x:auto; margin:28px 0; border-radius:6px; border:1px solid var(--gray-100); box-shadow:0 1px 3px rgba(0,0,0,0.04); }}
    .article-body table {{ width:100%; border-collapse:collapse; font-size:0.875rem; line-height:1.5; min-width:600px; }}
    .article-body thead th {{ background:linear-gradient(180deg,#E8F0F8 0%,#D4E4F2 100%); color:var(--blue-dark); font-weight:600; font-size:0.8125rem; text-transform:uppercase; letter-spacing:0.03em; padding:12px 14px; text-align:left; border-bottom:2px solid #B8D0E8; border-right:1px solid #C8D8E8; }}
    .article-body thead th:last-child {{ border-right:none; }}
    .article-body tbody td {{ padding:10px 14px; border-bottom:1px solid var(--gray-100); border-right:1px solid var(--gray-100); color:var(--gray-500); }}
    .article-body tbody td:last-child {{ border-right:none; }}
    .article-body tbody tr:nth-child(even) td {{ background:var(--gray-50); }}
    .article-body tbody tr:hover td {{ background:var(--blue-bg); }}
    .article-body tbody td:first-child {{ font-weight:500; color:var(--text-dark); }}
    .related-section {{ background:var(--off-white); padding:64px 24px; }}
    .related-inner {{ max-width:var(--content-max); margin:0 auto; }}
    .related-inner h2 {{ font-size:1.5rem; font-weight:700; margin-bottom:24px; letter-spacing:-0.01em; }}
    .related-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:16px; }}
    .related-card {{ background:var(--white); border:1px solid var(--gray-100); border-radius:var(--radius-md); padding:20px; text-decoration:none; transition:box-shadow 0.2s; }}
    .related-card:hover {{ box-shadow:0 4px 16px rgba(0,0,0,0.06); }}
    .related-card h3 {{ font-size:0.9375rem; font-weight:600; color:var(--text-dark); margin-bottom:4px; }}
    .related-card .tag {{ font-size:0.6875rem; color:var(--blue); font-weight:600; text-transform:uppercase; letter-spacing:0.04em; }}
    .article-nav {{ max-width:var(--content-max); margin:0 auto; padding:0 24px; }}
    .article-nav-inner {{ display:flex; justify-content:space-between; align-items:flex-start; padding:32px 0; border-top:1px solid var(--gray-100); }}
    .article-nav-inner a {{ display:flex; align-items:center; gap:8px; color:var(--gray-500); text-decoration:none; font-size:0.875rem; max-width:45%; }}
    .article-nav-inner a:hover {{ color:var(--blue); }}
    .article-nav-inner .nav-label {{ color:var(--gray-400); font-size:0.6875rem; display:block; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:2px; }}
    .article-nav-inner .nav-title {{ color:var(--text-dark); font-weight:600; line-height:1.3; }}
    .article-nav-back {{ text-align:center; padding-bottom:40px; }}
    .article-nav-back a {{ color:var(--blue); text-decoration:none; font-weight:600; }}
    .footer {{ background:var(--near-black); color:var(--text-muted); padding:48px 24px 32px; border-top:1px solid rgba(255,255,255,0.06); }}
    .footer-inner {{ max-width:1200px; margin:0 auto; display:flex; justify-content:space-between; align-items:center; font-size:0.8125rem; }}
    .footer-inner a {{ color:var(--blue-light); text-decoration:none; }}
    @media(max-width:768px){{ .article-header{{padding:calc(64px + 40px) 16px 40px;}} .article-body{{padding:40px 16px;}} .nav-links{{display:none;}} }}
  </style>
</head>
<body>
<nav class="nav"><div class="nav-inner"><div class="nav-left"><a href="../" class="nav-logo"><img src="../logo.png" alt="Scodeno" class="nav-logo-img"><span class="nav-logo-text">Scodeno<span class="nav-logo-indonesia">Indonesia</span></span></a><ul class="nav-links"><li class="nav-dropdown"><a href="../#products">Products</a><div class="nav-dropdown-menu"><a href="../#products">Unmanaged Switches</a><a href="../#products">Managed Switches</a><a href="../#products">PoE Switches</a><a href="../#products">Data Center</a><a href="../#products">xPON / Fiber</a><a href="../#products">Smart Box &amp; IoT</a></div></li><li class="nav-dropdown"><a href="../#articles">Articles</a><div class="nav-dropdown-menu"><a href="../#articles">Fundamental</a><a href="../#articles">Selection Guide</a><a href="../#articles">Technology</a><a href="../#articles">Deployment</a><a href="../#articles">Network Design</a></div></li><li><a href="../#about">About</a></li></ul></div><a href="../#contact" class="nav-cta">Request Quote</a></div></nav>
<header class="article-header"><div class="article-header-inner"><span class="article-tag">Network Design</span><h1>{title}</h1><div class="article-meta"><span>{read_time} min read</span></div></div></header>
<article class="article-body">
{article_body}
</article>
<nav class="article-nav"><div class="article-nav-inner"><a href="Week_12_network-segmentation-pada-jaringan-industri.html"><span><span class="nav-label">Previous</span><span class="nav-title">Network Segmentation pada Jaringan Industri</span></span></a><a href="Week_14_industrial-network-monitoring-system-memantau-jaringan-ot-tanpa-henti.html"><span><span class="nav-label">Next</span><span class="nav-title">Industrial Network Monitoring System</span></span></a></div><div class="article-nav-back"><a href="../#articles">← Kembali ke Semua Artikel</a></div></nav>
<section class="related-section"><div class="related-inner"><h2>Artikel Terkait</h2><div class="related-grid">
<a href="Week_10_vlan-dalam-industrial-ethernet-network.html" class="related-card"><span class="tag">Technology</span><h3>VLAN dalam Industrial Ethernet Network</h3></a>
<a href="Week_11_qos-dalam-industrial-network.html" class="related-card"><span class="tag">Technology</span><h3>QoS dalam Industrial Network</h3></a>
<a href="Week_14_industrial-network-monitoring-system-memantau-jaringan-ot-tanpa-henti.html" class="related-card"><span class="tag">Network Design</span><h3>Industrial Network Monitoring System</h3></a>
<a href="Week_06_managed-vs-unmanaged-industrial-switch-mana-yang-tepat.html" class="related-card"><span class="tag">Selection Guide</span><h3>Managed vs Unmanaged Industrial Switch</h3></a>
</div></div></section>
<footer class="footer"><div class="footer-inner"><span>&copy; 2024 Scodeno Indonesia</span><span>Didistribusikan oleh <a href="../">PT Konexindo Unitama</a></span></div></footer>
</body>
</html>'''

out_file.write_text(html, encoding='utf-8')
print(f"✅ Week 13 HTML: {out_file}")
print(f"   Words: {words}, Read time: {read_time} min")
