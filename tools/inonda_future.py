"""Apply the owner's approved architectural interface without rewriting content."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = '20261030-2'
MARKER = r'<!-- INONDA FUTURE ASSETS START -->.*?<!-- INONDA FUTURE ASSETS END -->'


def write_assets(site):
    folder = ROOT / ('dist' if site == 'homes' else 'public/assets')
    folder.mkdir(parents=True, exist_ok=True)
    for name in ['future-design.css', 'future-ui.js']:
        source = Path(__file__).with_name(name).read_bytes()
        target = folder / name
        if not target.exists() or target.read_bytes() != source:
            target.write_bytes(source)


def enhance_future(text, site):
    if '<main' not in text or '</head>' not in text or 'http-equiv="refresh"' in text:
        return text
    write_assets(site)
    assets = './' if site == 'homes' else '/assets/'
    include = f'<!-- INONDA FUTURE ASSETS START --><link rel="stylesheet" href="{assets}future-design.css?v={VERSION}"><script defer src="{assets}future-ui.js?v={VERSION}"></script><!-- INONDA FUTURE ASSETS END -->'
    text = re.sub(r'((?:href|src)=["\'][^"\']*\.(?:css|js|svg)\?v=)20261030-1', lambda match: match.group(1) + VERSION, text)
    text = re.sub(MARKER, '', text, flags=re.S)
    return text.replace('</head>', include + '</head>', 1)


def update_site(site):
    write_assets(site)
    folder = ROOT / ('dist' if site == 'homes' else 'public')
    count = 0
    for path in folder.rglob('*.html'):
        source = path.read_text(encoding='utf-8')
        updated = enhance_future(source, site)
        if updated != source:
            path.write_text(updated, encoding='utf-8')
            count += 1
    print(f'{site}: architectural interface applied to {count} pages')


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ['site', 'org', 'homes']:
        raise SystemExit('Usage: python tools/inonda_future.py site|org|homes')
    update_site(sys.argv[1])
