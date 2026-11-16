#!/usr/bin/env python3
"""Validate INONDA LTD's generated, localized Carpentry service pages.

Run after: python3 build/check_content.py && python3 build/gen.py
No deployment or GitHub credentials required.
"""
import json,re,sys
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
sys.path.insert(0,str(Path(__file__).resolve().parent))
import carpentry_pages as C

ROOT=Path(__file__).resolve().parent.parent
PUBLIC=ROOT/'public'
assert C.validate()
assert (PUBLIC/'assets/carpentry.css').is_file()
assert len(C.routes())==11
all_urls=set()
titles=set()

for lang in C.LANGUAGES:
    assert lang in C.DETAILS
    for route in C.routes():
        page=PUBLIC/lang/route/'index.html'
        assert page.is_file(),str(page)
        content=page.read_text(encoding='utf-8')
        expected='https://www.inonda.org/'+lang+'/'+route+'/'
        assert expected not in all_urls,expected
        all_urls.add(expected)
        assert '<html lang="'+lang+'"' in content,expected
        assert 'dir="'+('rtl' if lang=='he' else 'ltr')+'"' in content,expected
        assert '<link rel="canonical" href="'+expected+'">' in content,expected
        for other in C.LANGUAGES:
            other_url='https://www.inonda.org/'+other+'/'+route+'/'
            assert 'hreflang="'+other+'" href="'+other_url+'"' in content,expected+':'+other
        assert 'name="robots" content="index, follow' in content,expected
        assert '<h1>' in content and '<h2>' in content,expected
        assert '/assets/carpentry.css?' in content,expected
        assert 'https://www.inonda.homes/?lang='+lang+'#bp-carpentry-section' in content,expected
        assert 'wa.me/35794091616?text=' in content,expected
        # The existing form must label the requested Carpentry service without sending anything.
        assert 'name="Carpentry category"' in content,expected
        assert '#quote' in content,expected
        assert not re.search(r'wasmer(?:\.io|\.app)?|hosted by|powered by (?:github|netlify|vercel)',content,re.I),expected
        assert 'HE 490415' in content,expected
        title=re.search(r'<title>([^<]+)</title>',content)
        assert title,title
        key=(lang,unescape(title.group(1)))
        assert key not in titles,key
        titles.add(key)
        scripts=re.findall(r'<script type="application/ld\+json">([^<]+)</script>',content)
        assert scripts,expected
        graph=json.loads(scripts[0])['@graph']
        types=[x.get('@type') for x in graph]
        assert 'BreadcrumbList' in types,expected
        if route=='carpentry':
            assert content.count('inonda-wood-card')>=10,expected
            assert 'ItemList' in types,expected
            for cat in C.CATEGORIES:
                assert C.SLUGS[cat['id']] in content,expected
        else:
            assert 'Service' in types and 'FAQPage' in types,expected
            faq=next(x for x in graph if x.get('@type')=='FAQPage')
            assert len(faq['mainEntity'])>=4,expected
            assert content.count('<details class="rv">')>=4,expected
            cat=next((c for c in C.CATEGORIES if route.endswith('/'+C.SLUGS[c['id']])),None)
            assert cat is not None,expected
            entry=C.DETAILS[lang]['entries'][cat['id']]
            assert all(unescape(part[:32]) in unescape(content) for part in entry['scope']),expected

    for old in ['services','doors-windows-carpentry']:
        source=PUBLIC/lang/old/'index.html'
        assert source.is_file()
        html=source.read_text(encoding='utf-8')
        assert 'carpentry-services-promo' in html,lang+':'+old
        assert '../carpentry/' in html,lang+':'+old
        assert '/'+lang+'/doors-windows-carpentry/' in html,lang+':'+old

sitemap=(PUBLIC/'sitemap.xml').read_text(encoding='utf-8')
for url in all_urls:
    assert '<loc>'+url+'</loc>' in sitemap,url
    assert sitemap.count('<loc>'+url+'</loc>')==1,url
assert len(all_urls)==66
llms=(PUBLIC/'llms.txt').read_text(encoding='utf-8')
assert 'carpentry/doors-frames/' in llms and 'carpentry/custom-projects/' in llms
print('PASS: 66 localized carpentry pages, ten unique sections, source mapping, four FAQs per subsection,')
print('canonical/hreflang, JSON-LD, related services, WhatsApp draft links, RTL, indexability and no host attribution.')
