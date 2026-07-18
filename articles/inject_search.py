#!/usr/bin/env python3
"""Inject search bar into all scodenoindonesia.com article HTML files."""
import re
from pathlib import Path

articles_dir = Path('/home/ace_a/projects/scodeno-landing/articles')

SEARCH_CSS = '''
    /* ===== SEARCH ===== */
    .nav-search{position:relative;display:flex;align-items:center}
    .search-toggle{background:none;border:none;cursor:pointer;padding:8px;display:flex;align-items:center;justify-content:center;border-radius:4px;transition:background 0.15s}
    .search-toggle:hover{background:rgba(255,255,255,0.06)}
    .search-toggle svg{width:18px;height:18px;stroke:var(--gray-300);stroke-width:2;fill:none;transition:stroke 0.15s}
    .search-toggle:hover svg{stroke:var(--white)}
    .search-panel{position:absolute;top:100%;right:0;width:420px;max-width:90vw;background:var(--dark-card);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:0;display:none;box-shadow:0 16px 48px rgba(0,0,0,0.45);z-index:200}
    .search-panel.active{display:block}
    .search-input-wrap{display:flex;align-items:center;padding:12px 16px;border-bottom:1px solid rgba(255,255,255,0.06)}
    .search-input-wrap svg{width:16px;height:16px;stroke:var(--gray-400);stroke-width:2;fill:none;flex-shrink:0;margin-right:10px}
    .search-input{flex:1;background:none;border:none;color:var(--white);font-size:0.9375rem;font-family:inherit;outline:none}
    .search-input::placeholder{color:var(--gray-400)}
    .search-results{max-height:420px;overflow-y:auto;padding:8px 0}
    .search-result{display:block;padding:10px 16px;text-decoration:none;transition:background 0.1s;border-bottom:1px solid rgba(255,255,255,0.03)}
    .search-result:last-child{border-bottom:none}
    .search-result:hover{background:rgba(255,255,255,0.04)}
    .search-result-title{font-size:0.875rem;font-weight:600;color:var(--white);margin-bottom:3px;line-height:1.3}
    .search-result-title mark{background:rgba(0,149,224,0.25);color:var(--blue-light);border-radius:2px;padding:0 1px}
    .search-result-snippet{font-size:0.75rem;color:var(--gray-400);line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
    .search-result-meta{display:flex;align-items:center;gap:8px;margin-top:4px}
    .search-result-cat{font-size:0.625rem;font-weight:600;text-transform:uppercase;letter-spacing:0.04em;padding:2px 6px;border-radius:2px}
    .cat-artikel{background:rgba(0,149,224,0.12);color:var(--blue-light)}
    .cat-produk{background:rgba(0,180,120,0.12);color:#00B478}
    .search-empty{padding:24px 16px;text-align:center;color:var(--gray-400);font-size:0.875rem}
    .search-overlay{position:fixed;top:0;left:0;right:0;bottom:0;z-index:150;display:none}
    .search-overlay.active{display:block}
    @media(max-width:768px){.search-panel{position:fixed;top:64px;left:0;right:0;max-width:100vw;border-radius:0;border-left:none;border-right:none}}
'''

SEARCH_HTML = '''
      <div class="nav-search">
        <button class="search-toggle" onclick="toggleSearch()" aria-label="Search">
          <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="17" y1="17" x2="22" y2="22"/></svg>
        </button>
        <div class="search-panel" id="searchPanel">
          <div class="search-input-wrap">
            <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="17" y1="17" x2="22" y2="22"/></svg>
            <input type="text" class="search-input" id="searchInput" placeholder="Cari artikel atau produk..." oninput="doSearch()" onkeydown="if(event.key==='Escape')closeSearch()">
          </div>
          <div class="search-results" id="searchResults"></div>
        </div>
      </div>
      <div class="search-overlay" id="searchOverlay" onclick="closeSearch()"></div>
'''

SEARCH_JS = '''
<script>
let searchIndex=[];
fetch('search-index.json').then(r=>r.json()).then(d=>{searchIndex=d});

function toggleSearch(){
  const panel=document.getElementById('searchPanel');
  const overlay=document.getElementById('searchOverlay');
  const input=document.getElementById('searchInput');
  const active=panel.classList.contains('active');
  if(active){closeSearch()}else{
    panel.classList.add('active');
    overlay.classList.add('active');
    setTimeout(()=>input.focus(),100);
    doSearch();
  }
}

function closeSearch(){
  document.getElementById('searchPanel').classList.remove('active');
  document.getElementById('searchOverlay').classList.remove('active');
  document.getElementById('searchInput').value='';
  document.getElementById('searchResults').innerHTML='';
}

function doSearch(){
  const q=document.getElementById('searchInput').value.toLowerCase().trim();
  const container=document.getElementById('searchResults');
  if(!q){showDefaultResults(container);return}
  const results=searchIndex.filter(item=>{
    const haystack=(item.title+' '+item.snippet+' '+item.tag+' '+item.category).toLowerCase();
    return haystack.includes(q);
  }).slice(0,12);
  if(results.length===0){
    container.innerHTML='<div class="search-empty">Tidak ditemukan. Coba kata kunci lain.</div>';
    return
  }
  container.innerHTML=results.map(r=>{
    const title=highlight(r.title,q);
    const snip=r.snippet.substring(0,100);
    const catClass=r.category==='Artikel'?'cat-artikel':'cat-produk';
    return `<a href="${r.url}" class="search-result">
      <div class="search-result-title">${title}</div>
      <div class="search-result-snippet">${snip}</div>
      <div class="search-result-meta"><span class="search-result-cat ${catClass}">${r.category}</span><span style="font-size:0.625rem;color:var(--gray-500)">${r.tag}</span></div>
    </a>`;
  }).join('');
}

function showDefaultResults(container){
  const shuffled=searchIndex.sort(()=>Math.random()-0.5).slice(0,6);
  container.innerHTML=shuffled.map(r=>{
    const catClass=r.category==='Artikel'?'cat-artikel':'cat-produk';
    return `<a href="${r.url}" class="search-result">
      <div class="search-result-title">${r.title}</div>
      <div class="search-result-snippet">${r.snippet.substring(0,100)}</div>
      <div class="search-result-meta"><span class="search-result-cat ${catClass}">${r.category}</span><span style="font-size:0.625rem;color:var(--gray-500)">${r.tag}</span></div>
    </a>`;
  }).join('');
}

function highlight(text,q){
  const regex=new RegExp(`(${q.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')})`,'gi');
  return text.replace(regex,'<mark>$1</mark>');
}

document.addEventListener('keydown',function(e){if(e.key==='Escape')closeSearch()});
</script>
'''

def inject_search(filepath):
    html = filepath.read_text(encoding='utf-8')
    modified = html

    # 1. Add search CSS before </style>
    if SEARCH_CSS.strip() not in modified:
        modified = modified.replace('  </style>', SEARCH_CSS + '\n  </style>', 1)

    # 2. Add search HTML before the "Request Quote" CTA in the nav
    # Pattern: the Request Quote link is the last element before </div></nav>
    old_cta = '<a href="../#contact" class="nav-cta">Request Quote</a></div></nav>'
    new_cta = SEARCH_HTML + '\n    <a href="../#contact" class="nav-cta">Request Quote</a></div></nav>'
    if old_cta in modified:
        modified = modified.replace(old_cta, new_cta, 1)
    else:
        # Minified version
        old_cta2 = '<a href="../#contact" class="nav-cta">Request Quote</a>'
        if old_cta2 in modified:
            modified = modified.replace(old_cta2, SEARCH_HTML.replace('\n', '') + old_cta2, 1)
        else:
            print(f'  ⚠️  {filepath.name}: nav CTA not found')
            return False, modified

    # 3. Add search JS before </body>
    if 'searchIndex' not in modified:
        modified = modified.replace('</body>', SEARCH_JS + '\n</body>', 1)

    return True, modified


def main():
    count = 0
    for f in sorted(articles_dir.glob('Week_*.html')):
        ok, new_html = inject_search(f)
        if ok:
            f.write_text(new_html, encoding='utf-8')
            count += 1
            print(f'  ✅ {f.name}')

    print(f'\n✅ Injected search into {count} articles')

if __name__ == '__main__':
    main()
