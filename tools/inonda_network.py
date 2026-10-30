#!/usr/bin/env python3
"""Add crawlable, six-language INONDA journeys without changing existing content.

Run: python tools/inonda_network.py site|org|homes
For inonda.org, build/gen.py also calls enhance_html on every generated page.
"""
import html
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inonda_seo import enhance_seo

ROOT = Path(__file__).resolve().parents[1]
COPY = json.loads(Path(__file__).with_name('network-copy.json').read_text(encoding='utf-8'))
SOCIAL = json.loads(Path(__file__).with_name('social-links.json').read_text(encoding='utf-8'))
VERSION = '20261030-1'
HOSTS = {'site': 'https://www.inonda.site', 'org': 'https://www.inonda.org', 'homes': 'https://www.inonda.homes'}


def journey(page):
    """Map only services actually covered by the estimator; no specialist quote claims."""
    slug = str(page).split('/')[-2] if str(page).endswith('/index.html') else str(page).strip('/').split('/')[-1]
    services = {
        'property-management-services': 'management', 'property-owners': 'management',
        'property-inspections': 'maintenance', 'property-maintenance-repairs': 'maintenance,handyman',
        'maintenance-plans': 'maintenance', 'handyman-services': 'handyman',
        'kitchen-renovation': 'renovation', 'bathroom-renovation': 'renovation',
        'home-renovation': 'renovation', 'painting-plastering-gypsum': 'renovation',
        'flooring-tiling': 'renovation', 'preparing-a-rental-property-in-cyprus': 'cleaning,handyman',
    }.get(slug, '')
    if slug.startswith('property-management-'):
        services = 'management'
    location = next((name for key, name in [('nicosia','Nicosia'),('strovolos','Nicosia'),('limassol','Limassol'),('larnaca','Larnaca'),('ayia-napa','Famagusta district'),('protaras','Famagusta district')] if key in slug), '')
    return services, location


def destinations(lang, page=''):
    services, location = journey(page)
    query = {'lang': lang}
    if services:
        query['services'] = services
    if location:
        query['location'] = location
    return {
        'site': f'{HOSTS["site"]}/{lang}/property-management-services/',
        'org': f'{HOSTS["org"]}/{lang}/services/',
        'homes': f'{HOSTS["homes"]}/?{urlencode(query)}#property',
    }


def bar(site, lang='en', page=''):
    c = COPY[lang]
    urls = destinations(lang, page)
    links = []
    for key, label in [('site','management'),('org','services'),('homes','estimator')]:
        current = ' aria-current="location"' if key == site else ''
        url = '#property' if key == site == 'homes' else f'{HOSTS[key]}/{lang}/' if key == site else urls[key]
        links.append(f'<a href="{html.escape(url, quote=True)}" data-inonda-destination="{key}"{current}><span class="inonda-network-domain" dir="ltr">inonda.{key}</span><span class="inonda-network-role">{html.escape(c[label])}</span></a>')
    return f'<nav class="inonda-network-bar" aria-label="{html.escape(c["nav"])}" data-no-i18n><span class="inonda-network-brand">INONDA LTD</span>{"".join(links)}</nav>'


def section(site, lang='en', page=''):
    c = COPY[lang]
    urls = destinations(lang, page)
    cards = []
    for key, prefix in [('site','site'),('org','org'),('homes','homes')]:
        badge = f'<span class="inonda-network-current">{html.escape(c["current"])}</span>' if key == site else ''
        url = '#property' if key == site == 'homes' else urls[key]
        cards.append(f'<article class="inonda-network-card"><div class="inonda-network-card-top"><span dir="ltr">inonda.{key}</span>{badge}</div><h3>{html.escape(c[prefix+"Title"])}</h3><p>{html.escape(c[prefix+"Text"])}</p><a href="{html.escape(url, quote=True)}" data-inonda-destination="{key}">{html.escape(c[prefix+"Action"])}<span aria-hidden="true"> ↗</span></a></article>')
    people = []
    for name, number, display in [('Irina','35794091616','+357 94 091 616'),('Constantin','35794091613','+357 94 091 613')]:
        people.append(f'<article class="inonda-network-person"><h4>{name}</h4><a class="inonda-network-phone" href="tel:+{number}" dir="ltr">{display}</a><div class="inonda-network-contact-buttons"><a href="https://wa.me/{number}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp · {name} · {display}">WhatsApp</a><a href="viber://chat?number=%2B{number}" aria-label="Viber · {name} · {display}">Viber</a><a href="tel:+{number}" data-network-call>{html.escape(c["call"])}</a></div></article>')
    contacts = f'<div class="inonda-network-contact"><h3 data-network-contact-title>{html.escape(c["contactTitle"])}</h3><div class="inonda-network-people">{"".join(people)}</div><a class="inonda-network-email" href="mailto:inonda2026@outlook.com">inonda2026@outlook.com</a></div>'
    return f'<section id="inonda-network" class="inonda-network-section" aria-labelledby="inonda-network-title" data-no-i18n><div class="inonda-network-heading"><p class="inonda-network-eyebrow">{html.escape(c["eyebrow"])}</p><h2 id="inonda-network-title">{html.escape(c["title"])}</h2><p>{html.escape(c["intro"])}</p></div><div class="inonda-network-cards">{"".join(cards)}</div><p class="inonda-network-note">{html.escape(c["note"])}</p>{contacts}</section>'


def enhance_html(text, site, page=''):
    text = enhance_seo(text, site, page)
    if '<main' not in text or '<header' not in text or 'http-equiv="refresh"' in text:
        return text
    match = re.search(r'<html\b[^>]*\blang=[\"\']([a-z]+)', text, re.I)
    lang = match.group(1) if match and match.group(1) in COPY else 'en'
    if site == 'site':
        # The original site's stylesheet/script URLs were unversioned, so an
        # existing browser could retain older layout code across deployments.
        text = re.sub(r'((?:href|src)=[\"\'][^\"\']*/assets/site\.(?:css|js))(?:\?[^\"\']*)?([\"\'])', lambda m: m.group(1) + '?v=' + VERSION + m.group(2), text)
        def responsive_video(match):
            attrs = match.group(1)
            if 'style=' not in attrs:
                attrs += ' style="display:block;width:100%;max-width:100%;height:auto"'
            return attrs + '>'
        text = re.sub(r'(<video\b(?=[^>]*\bcontrols)[^>]*)(>)', responsive_video, text)
    # Regeneration is idempotent; all original page text stays untouched.
    text = re.sub(r'<!-- INONDA NETWORK (?:ASSETS|BAR|SECTION|SOCIAL) START -->.*?<!-- INONDA NETWORK (?:ASSETS|BAR|SECTION|SOCIAL) END -->', '', text, flags=re.S)
    text = re.sub(r' data-inonda-site="(?:site|org|homes)"', '', text)
    text = re.sub(r'<body\b', f'<body data-inonda-site="{site}"', text, count=1)
    assets = './' if site == 'homes' else '/assets/'
    include = f'<!-- INONDA NETWORK ASSETS START --><link rel="stylesheet" href="{assets}inonda-network.css?v={VERSION}"><link rel="stylesheet" href="{assets}inonda-chat.css?v={VERSION}"><script defer src="{assets}inonda-network.js?v={VERSION}"></script><script defer src="{assets}inonda-chat.js?v={VERSION}"></script><!-- INONDA NETWORK ASSETS END -->'
    text = text.replace('</head>', include + '</head>', 1)
    text = re.sub(r'(<body\b[^>]*>)', lambda m: m.group(1) + '<!-- INONDA NETWORK BAR START -->' + bar(site, lang, page) + '<!-- INONDA NETWORK BAR END -->', text, count=1)
    block = '<!-- INONDA NETWORK SECTION START -->' + section(site, lang, page) + '<!-- INONDA NETWORK SECTION END -->'
    if site == 'homes':
        text = text.replace('<section class="contact-section"', block + '<section class="contact-section"', 1)
    else:
        text = text.replace('</main>', block + '</main>', 1)
    social_links = ''.join(f'<a href="{html.escape(SOCIAL[key], quote=True)}" target="_blank" rel="noopener noreferrer"><img class="inonda-social-icon" src="{assets}{key}-brand.svg?v={VERSION}" alt="" width="28" height="28">{label} · INONDA LTD ↗</a>' for key, label in [('facebook', 'Facebook'), ('instagram', 'Instagram'), ('tiktok', 'TikTok'), ('youtube', 'YouTube')] if SOCIAL.get(key))
    social = f'<!-- INONDA NETWORK SOCIAL START --><nav class="inonda-social-footer" aria-label="{html.escape(COPY[lang]["follow"])}" data-no-i18n><strong>{html.escape(COPY[lang]["follow"])}</strong>{social_links}</nav><!-- INONDA NETWORK SOCIAL END -->'
    footer_end = text.rfind('</footer>')
    if footer_end >= 0:
        text = text[:footer_end] + social + text[footer_end:]
    # Original official brand files, no substitute letters or hand-drawn marks.
    def brand_link(match):
        attrs, inner = match.group(1), match.group(2)
        brand = 'whatsapp' if 'wa.me/' in attrs else 'viber'
        attrs = re.sub(r' data-inonda-brand="[^"]*"', '', attrs)
        inner = re.sub(r'<svg\b.*?</svg>', '', inner, flags=re.S)
        inner = re.sub(r'<img\b[^>]*class="inonda-channel-icon"[^>]*>', '', inner)
        if inner.strip() in ['V', '✆', '☎']:
            inner = ''
        icon = f'<img class="inonda-channel-icon" src="{assets}{brand}-official.svg?v={VERSION}" alt="" width="24" height="24">'
        return f'<a{attrs} data-inonda-brand="{brand}">{icon}{inner}</a>'
    text = re.sub(r'<a\b([^>]*\bhref=[\"\'](?:https://wa\.me/|viber://)[^>]*?)>(.*?)</a>', brand_link, text, flags=re.S)
    return text


CSS = '''/* INONDA LTD: shared navigation and journeys, scoped to avoid site theme collisions. */
body[data-inonda-site]{padding-top:44px}
.inonda-network-bar{box-sizing:border-box;position:fixed;inset:0 0 auto;z-index:120;height:44px;display:flex;align-items:stretch;justify-content:center;gap:0;padding:0 3%;background:#023e8a;color:#fff;font:12px/1.2 Arial,sans-serif;border-bottom:1px solid #6196c3;direction:inherit}
.inonda-network-brand{display:flex;align-items:center;margin-inline-end:auto;font-size:11px;letter-spacing:.08em;white-space:nowrap}
.inonda-network-bar a{box-sizing:border-box;display:flex;align-items:center;gap:10px;padding:0 20px;color:#fff;text-decoration:none;min-width:0;border-inline-start:1px solid #4777ac}
.inonda-network-domain{font-weight:700;white-space:nowrap;unicode-bidi:isolate}
.inonda-network-role{font-size:11px;font-weight:400}
.inonda-network-bar a[aria-current]{background:#0077b6;box-shadow:inset 0 -3px #a6ddf6}
.inonda-network-bar a:hover{background:#005e9f}
.inonda-network-bar a:focus-visible,.inonda-network-section a:focus-visible{outline:3px solid #55c8ff;outline-offset:-4px}
body[data-inonda-site=site]>header{top:56px}
body[data-inonda-site=org]>header.site{top:44px}
body[data-inonda-site=site] .mobile-panel{top:calc(var(--nav-h,76px) + 68px)}
body[data-inonda-site=org] .mobile-panel{top:calc(var(--nav-h,76px) + 44px)}
body[data-inonda-site=org] .hero{padding-top:calc(var(--nav-h,76px) + 104px)}
body[data-inonda-site=site] .hero .wrap{padding-top:calc(var(--nav-h,76px) + 114px)}
.inonda-network-section{box-sizing:border-box;position:relative;clear:both;padding:70px max(5.5%,22px);background:#f3f8fb;color:#102f49;font-family:Arial,sans-serif;text-align:start;border-top:1px solid #d5e3eb;border-bottom:1px solid #d5e3eb;scroll-margin-top:160px}
.inonda-network-section *{box-sizing:border-box}
.inonda-network-heading{max-width:950px;margin:0 0 32px}
.inonda-network-section .inonda-network-eyebrow{color:#0077b6;font-size:11px;letter-spacing:.07em;line-height:1.6;font-weight:700;margin:0 0 18px}
.inonda-network-section h2{font:400 clamp(30px,3.4vw,52px)/1.12 Arial,sans-serif;letter-spacing:-.03em;margin:0 0 22px;color:#023e8a;max-width:none}
.inonda-network-heading>p:last-child{font-size:16px;line-height:1.7;margin:0;max-width:860px;color:#425e70}
.inonda-network-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;max-width:1500px}
.inonda-network-card{display:flex;flex-direction:column;min-width:0;border:1px solid #ccdde7;padding:24px;background:#fff;border-radius:0}
.inonda-network-card-top{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:30px;font-size:12px;color:#0077b6;min-height:25px}
.inonda-network-current{background:#e4f3fb;color:#023e8a;padding:5px 8px;font-size:10px;line-height:1.5}
.inonda-network-section h3{font:400 25px/1.25 Arial,sans-serif;margin:0 0 16px;letter-spacing:-.02em;color:#102f49}
.inonda-network-card>p{font:14px/1.7 Arial,sans-serif;color:#526d7d;margin:0 0 24px;max-width:none}
.inonda-network-card>a{display:block;margin-top:auto;padding:15px 0 0;border-top:1px solid #d5e3eb;font:600 13px/1.6 Arial,sans-serif;color:#023e8a;text-decoration:none;overflow-wrap:anywhere}
.inonda-network-card>a:hover{color:#0077b6;text-decoration:underline}
.inonda-network-section>.inonda-network-note{font:12px/1.7 Arial,sans-serif;color:#526d7d;margin:24px 0 0;max-width:1000px}
.inonda-network-contact{border-top:1px solid #c8dbe6;margin-top:34px;padding-top:30px}
.inonda-network-people{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;max-width:950px}
.inonda-network-person h4{font:600 16px/1.4 Arial,sans-serif;margin:0 0 5px;color:#023e8a}
.inonda-network-person>.inonda-network-phone{display:inline-block;font:400 23px/1.6 Arial,sans-serif;color:#102f49;text-decoration:none;unicode-bidi:isolate}
.inonda-network-contact-buttons{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.inonda-network-contact-buttons a{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:10px 16px;border:1px solid #9bbdd0;color:#023e8a;font:600 13px/1.4 Arial,sans-serif;text-decoration:none}
.inonda-network-contact-buttons a:hover{background:#023e8a;color:#fff}
.inonda-network-email{display:inline-block;margin-top:24px;color:#023e8a;text-decoration:underline;font:14px/1.6 Arial,sans-serif;overflow-wrap:anywhere}
.inonda-social-footer{display:flex;align-items:center;flex-wrap:wrap;gap:16px 30px;padding:26px max(5.5%,22px) 100px;margin:0;border-top:1px solid #85a6ca60;color:inherit;font:13px/1.6 Arial,sans-serif}
.inonda-social-footer strong{font-weight:600;margin-inline-end:auto}
.inonda-social-footer a{display:inline-flex;align-items:center;gap:9px;min-height:44px;color:inherit;text-decoration:none;border-bottom:1px solid #85a6ca}
.inonda-social-icon{width:28px!important;height:28px!important;object-fit:contain;display:block;flex:none;background:#fff;border-radius:5px;padding:4px;filter:none!important;margin:0!important}
.inonda-social-footer a:hover{text-decoration:underline}
.inonda-social-footer a:focus-visible{outline:3px solid #43b9ef;outline-offset:3px}
@media(max-width:700px){.inonda-social-footer{padding:22px 22px 110px;gap:10px 22px}.inonda-social-footer strong{width:100%;margin:0}}
@media(max-width:700px){.inonda-network-people{grid-template-columns:1fr;gap:26px}}
@media(max-width:1000px){.inonda-network-role{display:none}.inonda-network-bar a{padding:0 22px}.inonda-network-card{padding:20px}.inonda-network-section h3{font-size:22px}}
@media(max-width:700px){.inonda-network-brand{display:none}.inonda-network-bar{padding:0;justify-content:stretch}.inonda-network-bar a{justify-content:center;flex:1;padding:0 7px;font-size:12px}.inonda-network-cards{grid-template-columns:1fr}.inonda-network-section{padding:44px 22px}.inonda-network-card-top{margin-bottom:20px}.inonda-network-section h2{font-size:33px}.inonda-network-heading>p:last-child{font-size:14px}.inonda-network-card{padding:22px}.inonda-network-section h3{font-size:25px}}
@media print{.inonda-network-bar,.inonda-network-section{display:none!important}body[data-inonda-site]{padding-top:0}}
'''


def javascript():
    # Static pages are complete without JS; this only keeps the estimator's in-page locale changes in sync.
    return '''/* Shared INONDA website navigation. No analytics, API calls or personal-data transfer. */
(function(){'use strict';
var copy=COPY_DATA;
function esc(v){return String(v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function update(){
 var lang=document.documentElement.lang, c=copy[lang]||copy.en, site=document.body.getAttribute('data-inonda-site');
 var bar=document.querySelector('.inonda-network-bar'); if(!bar)return;
 document.querySelectorAll('.inonda-social-footer').forEach(function(nav){nav.setAttribute('aria-label',c.follow);nav.querySelector('strong').textContent=c.follow;});
 bar.setAttribute('aria-label',c.nav);
 var roles={site:c.management,org:c.services,homes:c.estimator};
 bar.querySelectorAll('[data-inonda-destination]').forEach(function(a){a.querySelector('.inonda-network-role').textContent=roles[a.dataset.inondaDestination];});
 document.querySelectorAll('[data-inonda-destination]').forEach(function(a){if(site==='homes'&&a.dataset.inondaDestination==='homes'){a.setAttribute('href','#property');return;}var u=new URL(a.href);if(a.dataset.inondaDestination==='homes'){u.searchParams.set('lang',lang);}else{u.pathname=u.pathname.replace(/^\\/(el|en|ru|uk|he|ro)\\//,'/'+lang+'/');}a.href=u.href;});
 var section=document.querySelector('.inonda-network-section');if(section){
  section.querySelector('.inonda-network-eyebrow').textContent=c.eyebrow;
  section.querySelector('h2').textContent=c.title;
  section.querySelector('.inonda-network-heading>p:last-child').textContent=c.intro;
  section.querySelector('.inonda-network-note').textContent=c.note;
  section.querySelector('[data-network-contact-title]').textContent=c.contactTitle;
  section.querySelectorAll('[data-network-call]').forEach(function(a){a.textContent=c.call;});
  ['site','org','homes'].forEach(function(key,i){var card=section.querySelectorAll('.inonda-network-card')[i];card.querySelector('h3').textContent=c[key+'Title'];card.querySelector('p').textContent=c[key+'Text'];card.querySelector('a').textContent=c[key+'Action']+' ↗';var badge=card.querySelector('.inonda-network-current');if(badge)badge.textContent=c.current;});
 }
 // Existing menu/footer links must follow the chosen language too; leave media URLs untouched.
 document.querySelectorAll('a[href]').forEach(function(a){if(!/^https:\\/\\/www\\.inonda\\.(site|org)\\/(el|en|ru|uk|he|ro)\\//.test(a.href))return;var u=new URL(a.href);u.pathname=u.pathname.replace(/^\\/(el|en|ru|uk|he|ro)\\//,'/'+lang+'/');a.href=u.href;});
}
document.addEventListener('inonda:language',update);
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',update);else update();
})();
'''.replace('COPY_DATA', json.dumps(COPY, ensure_ascii=False))


def update_site(site):
    folder = ROOT / ('dist' if site == 'homes' else 'public')
    assets = folder if site == 'homes' else folder / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    (assets / 'inonda-network.css').write_text(CSS, encoding='utf-8')
    (assets / 'inonda-network.js').write_text(javascript(), encoding='utf-8')
    (assets / 'inonda-chat.css').write_text(Path(__file__).with_name('inonda_chat.css').read_text(encoding='utf-8'), encoding='utf-8')
    (assets / 'inonda-chat.js').write_text(chat_javascript(), encoding='utf-8')
    count = 0
    for path in folder.rglob('*.html'):
        if path.name.startswith('__'):
            continue
        before = path.read_text(encoding='utf-8')
        after = enhance_html(before, site, path.relative_to(folder).as_posix())
        if before != after:
            path.write_text(after, encoding='utf-8')
            count += 1
    print(f'{site}: connected {count} pages')


def chat_javascript():
    source = Path(__file__).with_name('inonda_chat.js').read_text(encoding='utf-8')
    for marker, filename in [('__INONDA_CHAT_COPY__', 'chat-copy.json'), ('__INONDA_CHAT_UI__', 'chat-ui.json')]:
        data = json.loads(Path(__file__).with_name(filename).read_text(encoding='utf-8'))
        source = source.replace(marker, json.dumps(data, ensure_ascii=False))
    return source


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in HOSTS:
        raise SystemExit('Usage: python tools/inonda_network.py site|org|homes')
    update_site(sys.argv[1])
