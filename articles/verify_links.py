import re
from pathlib import Path

total_links = 0
for f in sorted(Path('.').glob('Week_*.html')):
    html = f.read_text()
    m = re.search(r'<article\b.*?</article>', html, re.DOTALL)
    if m:
        body = m.group(0)
        links = re.findall(r'href="\.\./"', body)
        total_links += len(links)
        status = '✅' if len(links) >= 1 else '❌'
        print(f'{status} {f.name}: {len(links)} contextual homepage link(s)')
    else:
        print(f'  {f.name}: no article body')

print(f'\nTotal contextual homepage links: {total_links}')
