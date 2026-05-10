#!/usr/bin/env python3
"""Convert all Scodeno article MD files to HTML pages with dropdown nav and Excel-style tables."""
import os, re

ARTICLES_DIR = "/home/ace_a/.hermes/profiles/apus/output/artikel"
OUT_DIR = "/home/ace_a/projects/scodeno-landing/articles"

TEMPLATE = r'''<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Scodeno Indonesia</title>
  <meta name="description" content="{description}">
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
    body {{
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      color: var(--text-dark); background: var(--white);
      line-height: 1.7; -webkit-font-smoothing: antialiased;
    }}

    /* ===== NAVIGATION ===== */
    .nav {{
      position: fixed; top: 0; left: 0; right: 0; z-index: 100;
      background: rgba(10,14,20,0.94); backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255,255,255,0.06);
    }}
    .nav-inner {{
      max-width: 1200px; margin: 0 auto;
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 24px; height: 64px;
    }}
    .nav-left {{ display: flex; align-items: center; gap: 32px; }}
    .nav-logo {{ display: flex; align-items: center; gap: 10px; text-decoration: none; }}
    .nav-logo-img {{ height: 28px; width: auto; }}
    .nav-logo-text {{ font-weight: 800; font-size: 1.0625rem; color: var(--white); letter-spacing: -0.01em; white-space: nowrap; }}
    .nav-logo-indonesia {{ color: var(--blue-light); margin-left: 2px; }}
    .nav-links {{ display: flex; align-items: center; gap: 4px; list-style: none; }}
    .nav-links a {{ color: var(--gray-300); text-decoration: none; font-size: 0.8125rem; font-weight: 500; padding: 8px 12px; border-radius: 4px; transition: all 0.15s; white-space: nowrap; }}
    .nav-links a:hover {{ color: var(--white); background: rgba(255,255,255,0.06); }}

    /* Dropdown */
    .nav-dropdown {{ position: relative; }}
    .nav-dropdown > a {{ display: flex; align-items: center; gap: 4px; }}
    .nav-dropdown > a::after {{ content: '▾'; font-size: 0.625rem; margin-left: 2px; }}
    .nav-dropdown-menu {{
      position: absolute; top: 100%; left: 0; min-width: 200px;
      background: var(--dark-card); border: 1px solid rgba(255,255,255,0.08);
      border-radius: 6px; padding: 6px 0; opacity: 0; visibility: hidden;
      transform: translateY(4px); transition: all 0.18s ease;
      box-shadow: 0 12px 32px rgba(0,0,0,0.35);
    }}
    .nav-dropdown:hover .nav-dropdown-menu {{ opacity: 1; visibility: visible; transform: translateY(0); }}
    .nav-dropdown-menu a {{
      display: block; padding: 8px 16px !important; font-size: 0.8125rem !important;
      color: var(--gray-300) !important; border-radius: 0 !important;
    }}
    .nav-dropdown-menu a:hover {{ background: rgba(255,255,255,0.06) !important; color: var(--white) !important; }}
    .nav-dropdown-menu .dropdown-label {{
      font-size: 0.625rem; text-transform: uppercase; letter-spacing: 0.06em;
      color: var(--gray-400); padding: 6px 16px 2px; font-weight: 600;
    }}

    .nav-cta {{
      background: var(--blue); color: var(--white) !important;
      padding: 8px 18px !important; border-radius: 4px !important;
      font-weight: 600 !important; font-size: 0.8125rem !important;
    }}
    .nav-cta:hover {{ background: var(--blue-light) !important; }}

    /* ===== ARTICLE HEADER ===== */
    .article-header {{
      background: var(--black); color: var(--white);
      padding: calc(64px + 64px) 24px 64px;
      position: relative; overflow: hidden;
    }}
    .article-header::before {{
      content: ''; position: absolute; top: -30%; right: -20%;
      width: 500px; height: 500px;
      background: radial-gradient(circle, var(--blue-glow) 0%, transparent 70%);
      pointer-events: none;
    }}
    .article-header-inner {{ max-width: var(--content-max); margin: 0 auto; position: relative; z-index: 1; }}
    .article-tag {{
      display: inline-block; background: rgba(0,149,224,0.15); color: var(--blue-light);
      font-size: 0.75rem; font-weight: 600; padding: 4px 12px;
      border-radius: 2px; margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.06em;
    }}
    .article-header h1 {{
      font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 800;
      line-height: 1.15; letter-spacing: -0.02em; margin-bottom: 16px;
    }}
    .article-header .article-meta {{ color: var(--text-muted); font-size: 0.875rem; display: flex; gap: 20px; }}

    /* ===== ARTICLE BODY ===== */
    .article-body {{
      max-width: var(--content-max); margin: 0 auto;
      padding: 64px 24px;
    }}
    .article-body h2 {{
      font-size: 1.5rem; font-weight: 700; color: var(--near-black);
      margin: 48px 0 16px; letter-spacing: -0.01em;
    }}
    .article-body h3 {{
      font-size: 1.25rem; font-weight: 600; color: var(--near-black);
      margin: 32px 0 12px;
    }}
    .article-body h4 {{
      font-size: 1.0625rem; font-weight: 600; color: var(--gray-500);
      margin: 24px 0 8px;
    }}
    .article-body p {{
      color: var(--gray-500); font-size: 1.0625rem;
      margin-bottom: 20px; line-height: 1.8;
    }}
    .article-body ul, .article-body ol {{
      color: var(--gray-500); font-size: 1.0625rem;
      margin-bottom: 20px; padding-left: 24px;
    }}
    .article-body li {{ margin-bottom: 8px; line-height: 1.7; }}
    .article-body strong {{ color: var(--text-dark); font-weight: 600; }}
    .article-body a {{ color: var(--blue); text-decoration: underline; }}
    .article-body a:hover {{ color: var(--blue-light); }}
    .article-body hr {{ border: none; border-top: 1px solid var(--gray-100); margin: 48px 0; }}
    .article-body blockquote {{
      border-left: 3px solid var(--blue); padding-left: 20px;
      margin: 24px 0; color: var(--gray-500); font-style: italic;
    }}

    /* ===== EXCEL-STYLE TABLE ===== */
    .table-wrap {{
      overflow-x: auto; margin: 28px 0; border-radius: 6px;
      border: 1px solid var(--gray-100);
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .article-body table {{
      width: 100%; border-collapse: collapse;
      font-size: 0.875rem; line-height: 1.5;
      min-width: 600px;
    }}
    .article-body thead th {{
      background: linear-gradient(180deg, #E8F0F8 0%, #D4E4F2 100%);
      color: var(--blue-dark); font-weight: 600; font-size: 0.8125rem;
      text-transform: uppercase; letter-spacing: 0.03em;
      padding: 12px 14px; text-align: left;
      border-bottom: 2px solid #B8D0E8;
      border-right: 1px solid #C8D8E8;
      white-space: nowrap; position: sticky; top: 0;
    }}
    .article-body thead th:last-child {{ border-right: none; }}
    .article-body tbody td {{
      padding: 10px 14px; border-bottom: 1px solid var(--gray-100);
      border-right: 1px solid var(--gray-100); color: var(--gray-500);
      vertical-align: top;
    }}
    .article-body tbody td:last-child {{ border-right: none; }}
    .article-body tbody tr:nth-child(even) td {{
      background: var(--gray-50);
    }}
    .article-body tbody tr:hover td {{
      background: var(--blue-bg);
    }}
    .article-body tbody td:first-child {{
      font-weight: 500; color: var(--text-dark);
    }}

    /* ===== RELATED ARTICLES ===== */
    .related-section {{
      background: var(--off-white); padding: 64px 24px;
    }}
    .related-inner {{ max-width: var(--content-max); margin: 0 auto; }}
    .related-inner h2 {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 24px; letter-spacing: -0.01em; }}
    .related-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }}
    .related-card {{
      background: var(--white); border: 1px solid var(--gray-100);
      border-radius: var(--radius-md); padding: 20px; text-decoration: none;
      transition: box-shadow 0.2s;
    }}
    .related-card:hover {{ box-shadow: 0 4px 16px rgba(0,0,0,0.06); }}
    .related-card h3 {{ font-size: 0.9375rem; font-weight: 600; color: var(--text-dark); margin-bottom: 4px; }}
    .related-card .tag {{ font-size: 0.6875rem; color: var(--blue); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }}

    /* ===== FOOTER ===== */
    .footer {{
      background: var(--near-black); color: var(--text-muted);
      padding: 48px 24px 32px; border-top: 1px solid rgba(255,255,255,0.06);
    }}
    .footer-inner {{
      max-width: 1200px; margin: 0 auto;
      display: flex; justify-content: space-between; align-items: center;
      font-size: 0.8125rem;
    }}
    .footer-inner a {{ color: var(--blue-light); text-decoration: none; }}
    .footer-inner a:hover {{ color: var(--white); }}

    @media (max-width: 768px) {{
      .article-header {{ padding: calc(64px + 40px) 16px 40px; }}
      .article-body {{ padding: 40px 16px; }}
      .nav-links {{ display: none; }}
    }}
  </style>
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <div class="nav-left">
      <a href="../index.html" class="nav-logo">
        <img src="../logo.png" alt="Scodeno" class="nav-logo-img">
        <span class="nav-logo-text">Scodeno<span class="nav-logo-indonesia">Indonesia</span></span>
      </a>
      <ul class="nav-links">
        <li class="nav-dropdown">
          <a href="../index.html#products">Products</a>
          <div class="nav-dropdown-menu">
            <a href="../index.html#products">Unmanaged Switches</a>
            <a href="../index.html#products">Managed Switches</a>
            <a href="../index.html#products">PoE Switches</a>
            <a href="../index.html#products">Data Center</a>
            <a href="../index.html#products">xPON / Fiber</a>
            <a href="../index.html#products">Smart Box &amp; IoT</a>
          </div>
        </li>
        <li class="nav-dropdown">
          <a href="../index.html#articles">Articles</a>
          <div class="nav-dropdown-menu">
            <a href="../index.html#articles">Fundamental</a>
            <a href="../index.html#articles">Selection Guide</a>
            <a href="../index.html#articles">Technology</a>
            <a href="../index.html#articles">Deployment</a>
            <a href="../index.html#articles">Network Design</a>
          </div>
        </li>
        <li><a href="../index.html#about">About</a></li>
      </ul>
    </div>
    <a href="../index.html#contact" class="nav-cta">Request Quote</a>
  </div>
</nav>

<header class="article-header">
  <div class="article-header-inner">
    <span class="article-tag">{tag}</span>
    <h1>{title}</h1>
    <div class="article-meta">
      <span>{read_time} min read</span>
    </div>
  </div>
</header>

<article class="article-body">
{content}
</article>

<section class="related-section">
  <div class="related-inner">
    <h2>Artikel Terkait</h2>
    <div class="related-grid">
{related}
    </div>
  </div>
</section>

<footer class="footer">
  <div class="footer-inner">
    <span>&copy; 2024 Scodeno Indonesia</span>
    <span>Didistribusikan oleh <a href="../index.html">PT Konexindo Unitama</a></span>
  </div>
</footer>

</body>
</html>'''


def md_to_html(text):
    """Convert markdown to HTML, auto-wrapping tables with .table-wrap."""
    lines = text.split('\n')
    result = []
    i = 0
    in_list = False
    list_type = None
    in_table = False
    table_rows = []
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Empty lines
        if not stripped:
            if in_list:
                result.append(f'</{list_type}>')
                in_list = False
                list_type = None
            if in_table:
                result.append(format_table(table_rows))
                table_rows = []
                in_table = False
            i += 1
            continue
        
        # Table detection: lines with | that are not just inline
        if '|' in stripped and not stripped.startswith(('#', '>', '- ', '* ')):
            pipe_count = stripped.count('|')
            if pipe_count >= 2:
                if not in_table:
                    if in_list:
                        result.append(f'</{list_type}>')
                        in_list = False
                    in_table = True
                    table_rows = []
                table_rows.append(stripped)
                i += 1
                continue
        
        # If we were in a table and this line isn't one, close it
        if in_table:
            result.append(format_table(table_rows))
            table_rows = []
            in_table = False
        
        # Headers
        if stripped.startswith('#### '):
            if in_list: result.append(f'</{list_type}>'); in_list = False
            result.append(f'<h4>{stripped[5:]}</h4>')
        elif stripped.startswith('### '):
            if in_list: result.append(f'</{list_type}>'); in_list = False
            result.append(f'<h3>{stripped[4:]}</h3>')
        elif stripped.startswith('## '):
            if in_list: result.append(f'</{list_type}>'); in_list = False
            result.append(f'<h2>{stripped[3:]}</h2>')
        elif stripped.startswith('# '):
            if in_list: result.append(f'</{list_type}>'); in_list = False
        elif stripped == '---':
            if in_list: result.append(f'</{list_type}>'); in_list = False
            result.append('<hr>')
        elif stripped.startswith('> '):
            if in_list: result.append(f'</{list_type}>'); in_list = False
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            result.append('<blockquote>' + ' '.join(quote_lines) + '</blockquote>')
            continue
        elif stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list or list_type != 'ul':
                if in_list: result.append(f'</{list_type}>')
                result.append('<ul>')
                in_list = True; list_type = 'ul'
            result.append(f'<li>{inline_md(stripped[2:])}</li>')
        elif re.match(r'^\d+\.\s', stripped):
            if not in_list or list_type != 'ol':
                if in_list: result.append(f'</{list_type}>')
                result.append('<ol>')
                in_list = True; list_type = 'ol'
            content = re.sub(r'^\d+\.\s', '', stripped)
            result.append(f'<li>{inline_md(content)}</li>')
        else:
            if in_list: result.append(f'</{list_type}>'); in_list = False; list_type = None
            para_lines = [stripped]
            j = i + 1
            while j < len(lines) and lines[j].strip() and not lines[j].strip().startswith(('#', '-', '*', '>', '|')) and lines[j].strip() != '---' and not re.match(r'^\d+\.\s', lines[j].strip()) and '|' not in lines[j].strip():
                para_lines.append(lines[j].strip())
                j += 1
            para = ' '.join(para_lines)
            result.append(f'<p>{inline_md(para)}</p>')
            i = j - 1
        
        i += 1
    
    if in_list: result.append(f'</{list_type}>')
    if in_table: result.append(format_table(table_rows))
    
    return '\n'.join(result)


def format_table(rows):
    """Format table rows into proper HTML with thead/tbody."""
    if len(rows) < 2:
        return '<p><em>Table data incomplete</em></p>'
    
    # Parse each row
    parsed = []
    for row in rows:
        cells = [c.strip() for c in row.strip().strip('|').split('|')]
        parsed.append(cells)
    
    # Detect separator row (e.g. |---|---|)
    sep_idx = None
    for idx, row in enumerate(parsed):
        if all(re.match(r'^:?-{3,}:?$', c) for c in row):
            sep_idx = idx
            break
    
    if sep_idx is not None:
        header_rows = parsed[:sep_idx]
        body_rows = parsed[sep_idx + 1:]
    else:
        header_rows = [parsed[0]]
        body_rows = parsed[1:]
    
    html = ['<div class="table-wrap"><table>']
    
    # thead
    html.append('<thead>')
    for row in header_rows:
        html.append('<tr>' + ''.join(f'<th>{inline_md(c)}</th>' for c in row) + '</tr>')
    html.append('</thead>')
    
    # tbody
    html.append('<tbody>')
    for row in body_rows:
        html.append('<tr>' + ''.join(f'<td>{inline_md(c)}</td>' for c in row) + '</tr>')
    html.append('</tbody>')
    
    html.append('</table></div>')
    return '\n'.join(html)


def inline_md(text):
    """Handle inline markdown: bold, italic, links, code."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text


# Article metadata
articles = [
    {"file": "Week_01_kenapa-industrial-switch-menggunakan-desain-fanless.md", "tag": "Fundamental", "read_time": 10},
    {"file": "Week_02_apa-itu-din-rail-industrial-switch-dan-mengapa-banyak-dipakai-di-pabrik.md", "tag": "Fundamental", "read_time": 12},
    {"file": "Week_03_ip-rating-pada-industrial-ethernet-switch-apa-artinya.md", "tag": "Fundamental", "read_time": 8},
    {"file": "Week_04_industrial-gigabit-switch-vs-fast-ethernet-switch.md", "tag": "Selection Guide", "read_time": 7},
    {"file": "Week_05_industrial-switch-dengan-sfp-port-fungsi-dan-kegunaannya.md", "tag": "Technology", "read_time": 7},
    {"file": "Week_06_managed-vs-unmanaged-industrial-switch-mana-yang-tepat.md", "tag": "Selection Guide", "read_time": 12},
    {"file": "Week_07_industrial-switch-dengan-poe-kapan-dibutuhkan.md", "tag": "Deployment", "read_time": 7},
    {"file": "Week_08_fitur-penting-industrial-ethernet-switch-yang-harus-anda-ketahui.md", "tag": "Selection Guide", "read_time": 14},
    {"file": "Week_09_industrial-switch-vs-commercial-switch-apa-perbedaannya.md", "tag": "Technology", "read_time": 11},
    {"file": "Week_10_vlan-dalam-industrial-ethernet-network.md", "tag": "Network Design", "read_time": 9},
    {"file": "Week_11_qos-dalam-industrial-network.md", "tag": "Network Design", "read_time": 8},
    {"file": "Week_12_network-segmentation-pada-jaringan-industri.md", "tag": "Network Design", "read_time": 8},
]

all_info = []
for a in articles:
    filepath = os.path.join(ARTICLES_DIR, a["file"])
    with open(filepath, 'r') as f:
        raw = f.read()
    title_match = re.search(r'\*\*Judul Artikel:\s*(.+?)\*\*', raw)
    if title_match:
        title = title_match.group(1)
    else:
        title = raw.split('\n')[0].lstrip('# ').strip()
    slug = a["file"].replace('.md', '.html')
    all_info.append({"title": title, "tag": a["tag"], "slug": slug})

os.makedirs(OUT_DIR, exist_ok=True)

for i, a in enumerate(articles):
    filepath = os.path.join(ARTICLES_DIR, a["file"])
    with open(filepath, 'r') as f:
        raw = f.read()
    
    title_match = re.search(r'\*\*Judul Artikel:\s*(.+?)\*\*', raw)
    title = title_match.group(1) if title_match else raw.split('\n')[0].lstrip('# ').strip()
    
    hr_idx = raw.find('\n---\n')
    body = raw[hr_idx + 5:] if hr_idx > 0 else raw.split('\n', 1)[1] if '\n' in raw else raw
    body_lines = body.split('\n')
    if body_lines and body_lines[0].strip().startswith('**Judul'):
        body = '\n'.join(body_lines[1:])
    
    content_html = md_to_html(body)
    
    related_html = '\n'.join([
        f'      <a href="{r["slug"]}" class="related-card"><span class="tag">{r["tag"]}</span><h3>{r["title"]}</h3></a>'
        for r in [ai for j, ai in enumerate(all_info) if j != i][:4]
    ])
    
    html = TEMPLATE.format(
        title=title, description=title,
        tag=a["tag"], read_time=a["read_time"],
        content=content_html, related=related_html
    )
    
    slug = a["file"].replace('.md', '.html')
    with open(os.path.join(OUT_DIR, slug), 'w') as f:
        f.write(html)
    print(f"  OK  {slug}")

print(f"\nDone. {len(articles)} articles written to {OUT_DIR}/")
