"""Consistent public company identity and search ownership tags; no login secrets."""
import json
from pathlib import Path
import re

CONFIG = json.loads(Path(__file__).with_name('search-config.json').read_text())
SOCIAL = json.loads(Path(__file__).with_name('social-links.json').read_text())
ENTITY = 'https://www.inonda.site/#business'
LANGS = ['el', 'en', 'ru', 'uk', 'he', 'ro']


def business():
    return {
        '@type': 'LocalBusiness', '@id': ENTITY, 'name': 'INONDA LTD',
        'legalName': 'INONDA LTD', 'url': 'https://www.inonda.site/',
        'description': 'Property management, maintenance, renovation and cleaning for residential and commercial properties across Cyprus. Call, inspection, then an agreed written offer.',
        'logo': 'https://www.inonda.site/assets/logo.png',
        'telephone': '+35794091616', 'email': 'inonda2026@outlook.com',
        'identifier': {'@type': 'PropertyValue', 'propertyID': 'Cyprus company registration', 'value': 'HE490415'},
        # The owner visits clients. Do not turn the registered flat into a storefront.
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Strovolos', 'addressRegion': 'Nicosia', 'addressCountry': 'CY'},
        'areaServed': {'@type': 'Country', 'name': 'Cyprus'},
        'sameAs': ['https://www.inonda.org/', 'https://www.inonda.homes/'] + [SOCIAL[k] for k in ['facebook', 'instagram', 'tiktok', 'youtube'] if SOCIAL.get(k)],
        'contactPoint': [
            {'@type': 'ContactPoint', 'name': 'Irina', 'telephone': '+35794091616', 'contactType': 'customer service', 'availableLanguage': ['Greek', 'English', 'Russian']},
            {'@type': 'ContactPoint', 'name': 'Constantin', 'telephone': '+35794091613', 'contactType': 'customer service', 'availableLanguage': ['Greek', 'English', 'Romanian']}
        ]
    }


def enhance_seo(text, site, page=''):
    if '<head' not in text or re.search(r'<meta[^>]*(?:content=["\']noindex|name=["\']robots["\'][^>]*content=["\']noindex)', text, re.I):
        return text
    # These are deliberately public ownership tokens, not passwords or API secrets.
    tags = []
    for name, value in CONFIG['verification'].get(site, {}).items():
        text = re.sub(r'<meta\b(?=[^>]*\bname=["\']' + re.escape(name) + r'["\'])[^>]*>\s*', '', text, flags=re.I)
        tags.append(f'<meta name="{name}" content="{value}">\n')
    old_ids = ['https://www.inonda.org/#business', 'https://www.inonda.homes/#business']
    def schema(match):
        data = json.loads(match.group(1))
        graph = data.get('@graph', [data])
        for node in graph:
            if node.get('@type') in ['LocalBusiness', 'HomeAndConstructionBusiness']:
                # Keep page-specific offers, images and established service detail.
                node.update(business())
        encoded = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        for old in old_ids:
            encoded = encoded.replace(old, ENTITY)
        return '<script type="application/ld+json">' + encoded + '</script>'
    pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    text = re.sub(pattern, schema, text, flags=re.S)
    if site == 'homes' and 'application/ld+json' not in text:
        data = {'@context': 'https://schema.org', '@graph': [business(),
            {'@type': 'WebSite', '@id': 'https://www.inonda.homes/#website', 'name': 'INONDA LTD service estimator', 'url': 'https://www.inonda.homes/', 'publisher': {'@id': ENTITY}, 'inLanguage': LANGS},
            {'@type': 'WebApplication', '@id': 'https://www.inonda.homes/#estimator', 'name': 'INONDA LTD property service estimator', 'url': 'https://www.inonda.homes/', 'applicationCategory': 'BusinessApplication', 'operatingSystem': 'Web browser', 'isAccessibleForFree': True, 'publisher': {'@id': ENTITY}, 'inLanguage': LANGS, 'description': 'Configure residential or commercial property service combinations and editable planning assumptions. All displayed prices include 19% VAT. Illustrative budget ranges require inspection and an agreed written offer.'}]}
        text = text.replace('</head>', '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '</script>\n</head>', 1)
    # Make the existing language controls crawlable without running JavaScript.
    if site == 'site' and re.match(r'^(el|en|ru|uk|he|ro)/', page):
        suffix = page.split('/', 1)[1].removesuffix('index.html')
        def lang_link(match):
            tag = match.group(0)
            lang = re.search(r'data-golang=["\']([a-z]+)', tag).group(1)
            return re.sub(r'href=["\'][^"\']*["\']', f'href="/{lang}/{suffix}"', tag)
        text = re.sub(r'<a\b(?=[^>]*data-golang=["\'](?:el|en|ru|uk|he|ro)["\'])[^>]*>', lang_link, text)
    return text.replace('</head>', ''.join(tags) + '</head>', 1)
