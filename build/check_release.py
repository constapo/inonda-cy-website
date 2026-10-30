"""Release checks for crawlability, generated links, metadata and approved presentation."""
import json
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
PUB=ROOT/'public'
BASE='https://www.inonda.org/'
errors=[]
pages={}
for p in PUB.rglob('*.html'):
    if p.name.startswith('__'):continue
    soup=BeautifulSoup(p.read_text(), 'html.parser')
    pages[p.resolve()]=soup

def check(ok, reason):
    if not ok:errors.append(reason)

def target(page, value):
    u=urlsplit(value)
    if u.scheme not in ['', 'https','http'] or (u.netloc and u.netloc!='www.inonda.org'):return None
    if not u.path:return page.resolve(),u.fragment
    p=(PUB/unquote(u.path).lstrip('/')) if u.path.startswith('/') or u.netloc else page.parent/unquote(u.path)
    if u.path.endswith('/'):p=p/'index.html'
    return p.resolve(),u.fragment

count=0
for p,soup in pages.items():
    if not soup.select_one('main') or p == (PUB/'index.html').resolve():continue
    count+=1
    rel=p.relative_to(PUB.resolve()).as_posix()
    expected=BASE+rel.removesuffix('index.html')
    check(len(soup.select('h1'))==1,f'{rel}: single H1')
    check(bool(soup.title and soup.title.string),f'{rel}: title')
    check(bool(soup.select_one('meta[name=description]')['content']),f'{rel}: description')
    check(soup.select_one('link[rel=canonical]')['href']==expected,f'{rel}: canonical')
    check('noindex' not in soup.select_one('meta[name=robots]')['content'],f'{rel}: indexable')
    alternates=soup.select('link[hreflang]')
    check(any(x['hreflang']=='x-default' for x in alternates),f'{rel}: x-default')
    for a in alternates:
        dest=target(p,a['href'])
        check(dest is not None and dest[0].exists(),f'{rel}: alternate {a["href"]}')
    ids=[x['id'] for x in soup.select('[id]')]
    check(len(ids)==len(set(ids)),f'{rel}: unique IDs')
    graph=[]
    for script in soup.select('script[type="application/ld+json"]'):
        data=json.loads(script.string)
        graph+=data.get('@graph',[data])
    check(any(x.get('@type')=='WebPage' and x.get('url')==expected for x in graph),f'{rel}: WebPage schema')
    check(len(soup.select('.inonda-social-footer'))==1,f'{rel}: one social footer')
    for href in json.loads((ROOT/'tools/social-links.json').read_text()).values():
        check(soup.select_one(f'.inonda-social-footer a[href="{href}"]') is not None,f'{rel}: social {href}')
    for el,attr in [(x,'href') for x in soup.select('a[href]')]+[(x,'src') for x in soup.select('img[src],script[src],source[src]')]+[(x,'href') for x in soup.select('link[rel=stylesheet]')]:
        dest=target(p,el[attr])
        if dest:
            check(dest[0].exists(),f'{rel}: missing {el[attr]}')
            if dest[1] and dest[0] in pages:check(pages[dest[0]].find(id=dest[1]) is not None,f'{rel}: missing anchor {el[attr]}')
    if rel.count('/')==1:
        check(len(soup.select('[role=tab]'))==3,f'{rel}: service selector')
        check(soup.select_one('.living-house')['fetchpriority']=='high',f'{rel}: hero priority')
    check(soup.html['dir']==('rtl' if rel.startswith('he/') else 'ltr'),f'{rel}: direction')

sitemap=ET.parse(PUB/'sitemap.xml')
urls=[node.text for node in sitemap.findall('{*}url/{*}loc')]
check(len(urls)==count==186,'186 canonical sitemap URLs')
check(len(urls)==len(set(urls)),'Unique sitemap URLs')
for url in urls:
    check((PUB/url.removeprefix(BASE)/'index.html').exists(),'Sitemap target '+url)
check('Allow: /' in (PUB/'robots.txt').read_text(),'robots allows crawling')
check('20261031-living-2' in (PUB/'el/index.html').read_text(),'versioned presentation')
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {count} pages; sitemap, canonical/hreflang, JSON-LD, social links, all local links/assets/anchors and six-language direction checked.')
