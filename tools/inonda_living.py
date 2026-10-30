"""Approved Living Blueprint presentation; existing content and routes are retained."""
from html import escape as e

VERSION = '20261031-living-1'
COPY = {
 'el': ('Μία ομάδα για το ακίνητό σας. Λευκωσία και όλη η Κύπρος.', 'Ενδεικτική αρχιτεκτονική απεικόνιση · Εξερευνήστε τις υπηρεσίες', 'Δείτε τις υπηρεσίες', 'Επιλέξτε υπηρεσία'),
 'en': ('One team for your property. Nicosia and all of Cyprus.', 'Concept architectural illustration · Explore our services', 'Explore services', 'Choose a service'),
 'ru': ('Одна команда для вашей недвижимости. Никосия и весь Кипр.', 'Концептуальная архитектурная иллюстрация · Наши услуги', 'Посмотреть услуги', 'Выберите услугу'),
 'uk': ('Одна команда для вашої нерухомості. Нікосія та весь Кіпр.', 'Концептуальна архітектурна ілюстрація · Наші послуги', 'Переглянути послуги', 'Виберіть послугу'),
 'he': ('צוות אחד לנכס שלכם. ניקוסיה וכל קפריסין.', 'הדמיה אדריכלית להמחשה · גלו את השירותים שלנו', 'לצפייה בשירותים', 'בחרו שירות'),
 'ro': ('O singură echipă pentru proprietatea dvs. Nicosia și tot Ciprul.', 'Ilustrație arhitecturală conceptuală · Explorați serviciile', 'Descoperiți serviciile', 'Alegeți un serviciu'),
}
GROUPS = [('maintenance', 'calendar', 'maintenance-plans'), ('repairs', 'home', 'plumbing-services'), ('transformation', 'roller', 'home-renovation')]

def living_assets(home=False):
    preload = f'<link rel="preload" as="image" href="/assets/living-blueprint-house.webp?v={VERSION}" imagesrcset="/assets/living-blueprint-house-sm.webp?v={VERSION} 760w, /assets/living-blueprint-house.webp?v={VERSION} 1386w" imagesizes="(max-width: 760px) 100vw, 65vw" fetchpriority="high">' if home else ''
    return preload + f'<link rel="stylesheet" href="/assets/living-blueprint.css?v={VERSION}"><script defer src="/assets/living-blueprint.js?v={VERSION}"></script>'

def living_hero(T, ic, note):
    lang=T['lang']; H=T['home']; u=T['ui']; c=COPY[lang]
    tabs=[]; panels=[]
    for i,(group,icon,slug) in enumerate(GROUPS):
        G=T['groups'][group]; selected='true' if i==0 else 'false'
        tabs.append(f'<button type="button" role="tab" id="living-tab-{group}" aria-controls="living-panel-{group}" aria-selected="{selected}" tabindex="{0 if i==0 else -1}" data-living-tab="{group}"><span class="living-tab-icon">{ic(icon)}</span><span>{e(G["name"])}</span>{ic("arrow")}</button>')
        panels.append(f'<div class="living-panel" id="living-panel-{group}" role="tabpanel" aria-labelledby="living-tab-{group}" tabindex="0"{ " hidden" if i else ""}><p>{e(G["desc"])}</p><a href="{slug}/">{e(c[2])} {ic("arrow")}</a></div>')
    spots=''.join(f'<a class="living-hotspot living-hotspot-{i}" href="{slug}/" aria-label="{e(T["svc"][slug]["name"])}" title="{e(T["svc"][slug]["name"])}">{ic(icon)}</a>' for i,(slug,icon) in enumerate([('bathroom-renovation','bath'),('kitchen-renovation','kitchen'),('maintenance-plans','calendar')]))
    return f'''<section class="living-hero" aria-labelledby="living-title">
<div class="living-stage"><img class="living-house" src="/assets/living-blueprint-house.webp?v={VERSION}" srcset="/assets/living-blueprint-house-sm.webp?v={VERSION} 760w, /assets/living-blueprint-house.webp?v={VERSION} 1386w" sizes="(max-width: 760px) 100vw, 65vw" alt="{e(c[1])}" width="1386" height="1135" fetchpriority="high" decoding="async">{spots}<p class="living-caption">{e(c[1])}</p></div>
<div class="wrap living-hero-layout"><div class="living-hero-copy"><p class="eyebrow">{e(H['eyebrow'])}</p><h1 id="living-title">{e(H['h1'])}</h1><p class="living-subtitle">{e(c[0])}</p>{note}<div class="btns"><a class="btn btn-primary" href="contact/#quote">{ic('calendar')}{e(u['cta_visit'])}</a><a class="btn btn-ghost" href="https://wa.me/35794091616" target="_blank" rel="noopener" aria-label="{e(u['cta_wa'])}">WhatsApp</a></div></div>
<div class="living-selector"><div role="tablist" aria-label="{e(c[3])}" aria-orientation="vertical">{''.join(tabs)}</div>{''.join(panels)}<noscript><a href="services/">{e(c[2])}</a></noscript></div></div></section>'''
