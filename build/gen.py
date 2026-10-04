#!/usr/bin/env python3
"""Build the inonda.org static site into ../public.

Usage:  python3 build/gen.py

Content lives in build/content/<lang>.py (one dict T per language).
Photos:  drop JPG/PNG files named after an image key (hero, kitchen, bathroom, plumbing,
         electrical, roof, painting, outdoor, ac, tiling, carpentry, handyman, emergency,
         maintenance) into build/source-images/ and rebuild; they are converted to WebP.
Video:   put hero.mp4 (and optionally hero-sm.mp4 for phones) in public/assets/video/.
"""
import html, importlib.util, json, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
SRC_IMG = os.path.join(ROOT, "build", "source-images")
BASE = "https://www.inonda.org"
LANGS = ["el", "en", "ru", "uk", "he", "ro"]
PHONE1, PHONE1_TXT = "+35794091616", "+357 94 091 616"   # Irina, main line (WhatsApp, form, call button)
PHONE2, PHONE2_TXT = "+35794091613", "+357 94 091 613"   # Constantin
WA = "35794091616"
# name, phone, display, whatsapp, language codes they answer in
PEOPLE = [("Irina", PHONE1, PHONE1_TXT, "35794091616", ["ru", "el", "en"]),
          ("Constantin", PHONE2, PHONE2_TXT, "35794091613", ["ro", "el", "en"])]
EMAIL = "inonda2026@outlook.com"
REG = "HE 490415"
ADDR = {"street": "29 Charalampou Mouskou", "locality": "Strovolos, Nicosia", "postal": "2014"}
TODAY = datetime.date.today().isoformat()
GSC_TOKEN = "ADV3fYCmHBO56b8IEcEpqdFcPNTT8Wj4_rADsPaRq3M"  # Google Search Console (https://www.inonda.org/)

GROUPS = ["maintenance", "repairs", "transformation"]
# slug, group, icon, image key
SERVICES = [
    ("maintenance-plans", "maintenance", "calendar", "maintenance"),
    ("air-conditioning-services", "maintenance", "snow", "ac"),
    ("roof-waterproofing-damp", "maintenance", "roof", "roof"),
    ("plumbing-services", "repairs", "drop", "plumbing"),
    ("electrical-services", "repairs", "bolt", "electrical"),
    ("handyman-services", "repairs", "hammer", "handyman"),
    ("emergency-repairs", "repairs", "siren", "emergency"),
    ("kitchen-renovation", "transformation", "kitchen", "kitchen"),
    ("bathroom-renovation", "transformation", "bath", "bathroom"),
    ("home-renovation", "transformation", "home", "hero"),
    ("painting-plastering-gypsum", "transformation", "roller", "painting"),
    ("flooring-tiling", "transformation", "tiles", "tiling"),
    ("doors-windows-carpentry", "transformation", "door", "carpentry"),
    ("outdoor-works", "transformation", "sun", "outdoor"),
]
SVC = {s[0]: s for s in SERVICES}
PAGES = ["", "services", "how-we-work", "service-areas", "about", "faq", "contact", "privacy-policy", "terms-of-service"]

# ---------------------------------------------------------------- icons (24px stroke)
I = {
 "calendar": '<rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4M8.5 15l2.3 2.3L15.5 13"/>',
 "snow": '<path d="M12 2v20M4.9 6.5l14.2 11M19.1 6.5L4.9 17.5M9 3.5l3 2.5 3-2.5M9 20.5l3-2.5 3 2.5"/>',
 "roof": '<path d="M2.5 11.5L12 4l9.5 7.5"/><path d="M5 10v10h14V10"/><path d="M9.5 20v-5.5h5V20"/><path d="M15.5 6.8V3.5h2.5v5.2"/>',
 "drop": '<path d="M12 2.8s6.5 7 6.5 11.7A6.5 6.5 0 0 1 5.5 14.5C5.5 9.8 12 2.8 12 2.8z"/><path d="M9 15a3 3 0 0 0 3 3"/>',
 "bolt": '<path d="M13 2.5L4.5 13.5H12l-1 8 8.5-11H12z"/>',
 "hammer": '<path d="M14.5 6.5l3 3M13 4.5l2-2 6 6-2 2"/><path d="M15.5 8.5L5 19a2 2 0 0 1-2.8-2.8L12.7 5.7"/>',
 "siren": '<path d="M6.5 18v-5a5.5 5.5 0 0 1 11 0v5"/><path d="M4 21h16v-3H4zM12 2.5v2M3.5 6l1.5 1.3M20.5 6L19 7.3"/>',
 "kitchen": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 10h18M7.5 6.5h2M14.5 6.5h2M12 10v11M8 14v3M16 14v3"/>',
 "bath": '<path d="M3 12h18v2.5A5.5 5.5 0 0 1 15.5 20h-7A5.5 5.5 0 0 1 3 14.5z"/><path d="M6 12V5.5A2.5 2.5 0 0 1 10.5 4M7 20l-1 2M17 20l1 2"/>',
 "home": '<path d="M3 11l9-7.5 9 7.5"/><path d="M5 9.5V20h14V9.5"/><path d="M10 20v-6h4v6"/>',
 "roller": '<rect x="3" y="3" width="15" height="6" rx="1.5"/><path d="M18 6h2.5v5.5H11v3"/><rect x="9.5" y="14.5" width="3" height="7" rx="1"/>',
 "tiles": '<rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="8" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1"/>',
 "door": '<path d="M5 21V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v17M3 21h18"/><path d="M15 12.5h.01"/>',
 "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "shield": '<path d="M12 2.5l8 3v6c0 5-3.4 8.6-8 10-4.6-1.4-8-5-8-10v-6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 "doc": '<path d="M14 2.5H6.5a2 2 0 0 0-2 2v15a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V8z"/><path d="M14 2.5V8h5.5M8.5 13h7M8.5 17h5"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "broom": '<path d="M19.5 2.5l-7 7M9.5 9l5.5 5.5-2.5 7-10-10z"/><path d="M6 15l-2 2M9 18l-1.5 1.5"/>',
 "award": '<circle cx="12" cy="9" r="6"/><path d="M8.5 13.8L7 21.5l5-3 5 3-1.5-7.7"/>',
 "pin": '<path d="M12 21.5s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9.5" r="2.5"/>',
 "phone": '<path d="M21 16.5v3a2 2 0 0 1-2.2 2A19.5 19.5 0 0 1 2.5 5.2 2 2 0 0 1 4.5 3h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.5 10.8a16 16 0 0 0 4.7 4.7l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 "mail": '<rect x="2.5" y="4.5" width="19" height="15" rx="2"/><path d="M3 6l9 7 9-7"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M21.5 20a6.5 6.5 0 0 0-4-6"/>',
 "camera": '<path d="M3 8a2 2 0 0 1 2-2h2.5l1.5-2.5h6L16.5 6H19a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><circle cx="12" cy="13" r="3.5"/>',
 "euro": '<path d="M17.5 6.5A7 7 0 1 0 17.5 17.5M4 10.5h9M4 13.5h9"/>',
}
WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.5-.3z"/></svg>'

def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[name]}</svg>'

def e(s):
    return html.escape(str(s), quote=True)

# ---------------------------------------------------------------- images
def prepare_images():
    if not os.path.isdir(SRC_IMG):
        return
    try:
        from PIL import Image
    except ImportError:
        print("Pillow missing: pip install pillow"); return
    out = os.path.join(PUB, "assets", "img")
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(SRC_IMG):
        key, ext = os.path.splitext(f)
        if ext.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        src = os.path.join(SRC_IMG, f)
        dst = os.path.join(out, key + ".webp")
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
            continue
        im = Image.open(src).convert("RGB")
        for w, suffix in ((1800, ""), (900, "-sm")):
            r = im.copy()
            if r.width > w:
                r = r.resize((w, round(r.height * w / r.width)), Image.LANCZOS)
            r.save(os.path.join(out, key + suffix + ".webp"), "WEBP", quality=80, method=6)
        if key == "hero":
            og = im.copy()
            og = og.resize((1200, round(og.height * 1200 / og.width)), Image.LANCZOS)
            top = max(0, (og.height - 630) // 2)
            og.crop((0, top, 1200, top + 630)).save(os.path.join(PUB, "assets", "og-image.jpg"), "JPEG", quality=84)
        print("image:", key)

def has_img(key):
    return bool(key) and os.path.exists(os.path.join(PUB, "assets", "img", key + ".webp"))

def has_video(name="hero.mp4"):
    return os.path.exists(os.path.join(PUB, "assets", "video", name))

def picture(key, alt, up, eager=False, icon="home"):
    if has_img(key):
        load = 'fetchpriority="high"' if eager else 'loading="lazy"'
        return (f'<img src="{up}assets/img/{key}.webp" srcset="{up}assets/img/{key}-sm.webp 900w, {up}assets/img/{key}.webp 1800w" '
                f'sizes="(max-width: 960px) 100vw, 50vw" alt="{e(alt)}" width="1800" height="1350" decoding="async" {load}>')
    return f'<div class="art">{ic(icon)}</div>'

# ---------------------------------------------------------------- content loading
def load(lang):
    spec = importlib.util.spec_from_file_location(lang, os.path.join(ROOT, "build", "content", lang + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.T

def url(lang, page):
    return f"{BASE}/{lang}/" + (page + "/" if page else "")

# ---------------------------------------------------------------- layout
FONTS = "https://fonts.googleapis.com/css2?family=Commissioner:wght@600;700;800&family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap"
FONTS_HE = "https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap"

def business_ld(T):
    u = T["ui"]
    return {
        "@type": "HomeAndConstructionBusiness", "@id": BASE + "/#business",
        "name": "Inonda LTD", "legalName": "INONDA LTD", "url": BASE + "/",
        "description": u["org_desc"], "logo": BASE + "/assets/logo.png", "image": BASE + "/assets/og-image.jpg",
        "telephone": PHONE1, "email": EMAIL, "priceRange": "€€",
        "identifier": {"@type": "PropertyValue", "propertyID": "Cyprus company registration", "value": REG},
        "address": {"@type": "PostalAddress", "streetAddress": ADDR["street"], "addressLocality": "Strovolos",
                    "addressRegion": "Nicosia", "postalCode": ADDR["postal"], "addressCountry": "CY"},
        "areaServed": [{"@type": "City", "name": n} for n in ("Nicosia", "Larnaca", "Limassol", "Paralimni")] + [{"@type": "Country", "name": "Cyprus"}],
        "knowsLanguage": ["el", "en", "ru", "ro"],
        "contactPoint": [{"@type": "ContactPoint", "telephone": ph, "name": n, "contactType": "customer service",
                          "availableLanguage": [{"ru": "Russian", "el": "Greek", "en": "English", "ro": "Romanian"}[c] for c in langs]}
                         for n, ph, _, _, langs in PEOPLE],
    }

def ver(name):
    import hashlib
    with open(os.path.join(PUB, "assets", name), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

def head(T, page, title, desc, ld_extra=None, up="../"):
    lang = T["lang"]
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{url(l, page)}">' for l in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{url("en", page)}">'
    loc_alt = "".join(f'<meta property="og:locale:alternate" content="{ALL[l]["locale"]}">' for l in LANGS if l != lang)
    graph = [business_ld(T), {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "Inonda LTD",
             "inLanguage": LANGS, "publisher": {"@id": BASE + "/#business"}}]
    if ld_extra:
        graph += ld_extra
    fonts = FONTS_HE if lang == "he" else FONTS
    return f'''<!DOCTYPE html>
<html lang="{lang}" dir="{T["dir"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="google-site-verification" content="{GSC_TOKEN}">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url(lang, page)}">
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Inonda LTD">
<meta property="og:locale" content="{T["locale"]}">{loc_alt}
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url(lang, page)}">
<meta property="og:image" content="{BASE}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0B1530">
<link rel="icon" href="{up}../favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="{up}../assets/favicon.png">
<link rel="apple-touch-icon" href="{up}../assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{fonts}"></noscript>
<link rel="stylesheet" href="{up}../assets/site.css?v={ver("site.css")}">
<script defer src="{up}../assets/site.js?v={ver("site.js")}"></script>
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
</head>'''

def nav_items(T):
    u = T["ui"]["nav"]
    return [("services", u["services"]), ("how-we-work", u["process"]), ("service-areas", u["areas"]),
            ("about", u["about"]), ("faq", u["faq"]), ("contact", u["contact"])]

def header(T, page, up):
    u = T["ui"]
    home = up if up else "./"
    links = "".join(f'<a href="{up}{p}/"' + (' aria-current="page"' if p == page else "") + f'>{e(n)}</a>' for p, n in nav_items(T))
    opts = "".join(f'<option value="{l}">{ALL[l]["label"]} {ALL[l]["name"]}</option>' for l in LANGS)
    mob_l = "".join(f'<a href="{up}../{l}/' + (page + "/" if page else "") + f'" hreflang="{l}" lang="{l}" data-golang="{l}">{ALL[l]["label"]}</a>' for l in LANGS)
    return f'''<body class="{'home' if page == '' else 'inner'}">
<a class="skip" href="#main">{e(u["skip"])}</a>
<header class="site"><div class="wrap bar">
<a class="brand" href="{home}"><img src="{up}../assets/logo-68.png" alt="Inonda LTD logo" width="38" height="30"><span>Inonda LTD<small>{e(u["tagline_short"])}</small></span></a>
<nav class="links" aria-label="{e(u["menu"])}">{links}</nav>
<div class="nav-right">
<select class="langsel" aria-label="Language">{opts}</select>
<a class="btn btn-primary btn-sm" href="{up}contact/#quote">{e(u["cta_quote"])}</a>
<button class="menu-toggle" id="menuToggle" aria-controls="mobilePanel" aria-expanded="false" aria-label="{e(u["menu"])}">☰</button>
</div></div></header>
<div class="mobile-panel" id="mobilePanel">{links.replace(' aria-current="page"', '')}<a class="btn btn-primary" href="{up}contact/#quote">{e(u["cta_quote"])}</a><div class="mobile-langs" aria-label="Language">{mob_l}</div></div>
<main id="main">'''

def footer(T, up):
    u = T["ui"]; S = T["svc"]
    def col(g):
        return "".join(f'<a href="{up}{s[0]}/">{e(S[s[0]]["name"])}</a>' for s in SERVICES if s[1] == g)
    return f'''</main>
<footer class="site"><div class="wrap">
<div class="fgrid4">
<div><a class="brand" href="{up}"><img src="{up}../assets/logo-68.png" alt="" width="38" height="30"><span>Inonda LTD<small>{e(u["tagline_short"])}</small></span></a>
<p>{e(u["footer_about"])}</p>
<p>INONDA LTD · {e(u["reg_no"])} {REG}<br>{ADDR["street"]}, {ADDR["postal"]} {ADDR["locality"]}, {e(u["cyprus"])}</p></div>
<div><p class="fh">{e(T["groups"]["maintenance"]["name"])} &amp; {e(T["groups"]["repairs"]["name"])}</p>{col("maintenance")}{col("repairs")}</div>
<div><p class="fh">{e(T["groups"]["transformation"]["name"])}</p>{col("transformation")}</div>
<div><p class="fh">{e(u["nav"]["contact"])}</p>
<a href="tel:{PHONE1}">{PHONE1_TXT}</a><a href="tel:{PHONE2}">{PHONE2_TXT}</a>
<a href="https://wa.me/{WA}" rel="noopener" target="_blank">WhatsApp</a><a href="mailto:{EMAIL}">{EMAIL}</a>
<p class="fh" style="margin-top:22px">{e(u["company"])}</p>
<a href="{up}how-we-work/">{e(u["nav"]["process"])}</a><a href="{up}service-areas/">{e(u["nav"]["areas"])}</a><a href="{up}about/">{e(u["nav"]["about"])}</a><a href="{up}faq/">{e(u["nav"]["faq"])}</a></div>
</div>
<div class="legal"><span>© {datetime.date.today().year} INONDA LTD. {e(u["rights"])}</span>
<span><a href="{up}privacy-policy/">{e(u["privacy"])}</a> · <a href="{up}terms-of-service/">{e(u["terms"])}</a> · <a href="https://www.inonda.site/{T["lang"]}/" rel="noopener">{e(u["sister"])}</a></span></div>
</div></footer>
<div class="float-stack">
<a class="float-btn wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_SVG}</a>
<a class="float-btn tel" href="tel:{PHONE1}" aria-label="{e(u["call"])}">{ic("phone")}</a>
</div>
<div class="cookie" id="cookieBanner"><span>{e(u["cookie"])} <a href="{up}privacy-policy/">{e(u["privacy"])}</a></span><button class="btn btn-primary btn-sm" id="cookieAccept" type="button">OK</button></div>
</body>
</html>
'''

# ---------------------------------------------------------------- blocks
def team(T, compact=False):
    t = T["ui"]["team"]; out = []
    for (name, ph, txt, wa, langs), (role, ) in zip(PEOPLE, [(r,) for r in t["roles"]]):
        ln = " · ".join(t["langs"][c] for c in langs)
        if compact:
            out.append(f'<div class="person-line"><span class="pn">{e(name)} <small>{e(role)}</small></span><span class="pl">{ic("users")}{e(ln)}</span>'
                       f'<span class="pa"><a href="tel:{ph}">{ic("phone")}{txt}</a><a href="https://wa.me/{wa}" target="_blank" rel="noopener" aria-label="WhatsApp {e(name)}">{WA_SVG}</a></span></div>')
        else:
            out.append(f'<div class="person rv"><div class="avatar" aria-hidden="true">{name[0]}</div><div><h3>{e(name)}</h3><p class="role">{e(role)}</p>'
                       f'<p class="langs"><strong>{e(t["speaks"])}:</strong> {e(ln)}</p><div class="btns"><a class="btn btn-dark btn-sm" href="tel:{ph}">{ic("phone")}{txt}</a>'
                       f'<a class="btn btn-line btn-sm" href="https://wa.me/{wa}" target="_blank" rel="noopener">{WA_SVG}WhatsApp</a><a class="btn btn-line btn-sm" href="viber://chat?number=%2B{wa}">Viber</a></div></div></div>')
    if compact:
        return '<div class="people-lines">' + "".join(out) + "</div>"
    return f'<div class="sec-head rv"><p class="eyebrow">{e(t["eyebrow"])}</p><h2>{e(t["title"])}</h2><p>{e(t["text"])}</p></div><div class="people">' + "".join(out) + "</div>"

def lang_note(T, cls="lang-note"):
    n = T["ui"].get("lang_note")
    return f'<p class="{cls}">{ic("users")}{e(n)}</p>' if n else ""

def quote_form(T, preselect=None, compact=False):
    f = T["ui"]["form"]; S = T["svc"]
    opts = "".join(f'<option value="{e(S[s[0]]["name"])}"' + (" selected" if s[0] == preselect else "") + f'>{e(S[s[0]]["name"])}</option>' for s in SERVICES)
    areas = "".join(f'<option>{e(a)}</option>' for a in f["areas"])
    ptypes = "".join(f'<option>{e(a)}</option>' for a in f["ptypes"])
    contact = "".join(f'<option>{e(a)}</option>' for a in f["contact_opts"])
    return f'''<form class="quote" id="quote" data-endpoint="" data-whatsapp="{WA}" data-subject="{e(f["subject"])}" data-sending="{e(f["sending"])}" data-sent="{e(f["sent"])}" data-error="{e(f["error"])}" data-wa-note="{e(f["wa_note"])}" novalidate>
<h3>{e(f["title"])}</h3><p style="font-size:.95rem">{e(f["intro"])}</p>{lang_note(T, "lang-note light")}
<div class="fgrid">
<label class="f">{e(f["name"])}<input name="{e(f["name"])}" autocomplete="name" required></label>
<label class="f">{e(f["phone"])}<input name="{e(f["phone"])}" type="tel" autocomplete="tel" required></label>
<label class="f">{e(f["service"])}<select name="{e(f["service"])}">{opts}<option value="{e(f["other"])}">{e(f["other"])}</option></select></label>
<label class="f">{e(f["area"])}<select name="{e(f["area"])}">{areas}</select></label>
<label class="f">{e(f["ptype"])}<select name="{e(f["ptype"])}">{ptypes}</select></label>
<label class="f">{e(f["contact"])}<select name="{e(f["contact"])}">{contact}</select></label>
<label class="f full">{e(f["email"])}<input name="Email" type="email" autocomplete="email"></label>
<label class="f full">{e(f["msg"])}<textarea name="{e(f["msg"])}" placeholder="{e(f["msg_ph"])}" required></textarea></label>
</div>
<label class="consent"><input type="checkbox" name="Consent" required> <span>{e(f["consent"])}</span></label>
<button class="btn btn-primary" type="submit">{WA_SVG}{e(f["submit"])}</button>
<p class="form-status" role="status" aria-live="polite"></p>
<p class="form-alt">{e(f["alt"])} <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="tel:{PHONE1}">{PHONE1_TXT}</a></p>
</form>'''

def cta_band(T, preselect=None):
    u = T["ui"]
    return f'''<section class="cta-band" id="contact-block"><div class="wrap">
<div class="rv"><p class="eyebrow">{e(u["cta_eyebrow"])}</p><h2>{e(u["cta_title"])}</h2><p class="lead">{e(u["cta_text"])}</p>
{team(T, compact=True)}<div class="contact-lines"><a href="mailto:{EMAIL}">{ic("mail")}{EMAIL}</a><span>{ic("pin")}{e(u["base"])}</span><span>{ic("clock")}{e(u["hours"])}</span></div></div>
<div class="rv">{quote_form(T, preselect)}</div>
</div></section>'''

def steps(T, dark=False):
    lis = "".join(f'<li class="rv"><h3>{e(h)}</h3><p>{e(p)}</p></li>' for h, p in T["ui"]["steps"])
    return f'<ol class="steps">{lis}</ol>'

def promises(T):
    icons = ["doc", "shield", "award", "broom"]
    return '<div class="promises rv">' + "".join(f'<div class="promise">{ic(icons[i])}<h3>{e(h)}</h3><p>{e(p)}</p></div>' for i, (h, p) in enumerate(T["ui"]["promises"])) + "</div>"

def svc_card(T, slug, up, tag=True):
    s = SVC[slug]; d = T["svc"][slug]
    t = f'<span class="tag">{e(T["groups"][s[1]]["name"])}</span>' if tag else ""
    return f'<a class="card rv" href="{up}{slug}/"><div class="ic">{ic(s[2])}</div>{t}<h3>{e(d["name"])}</h3><p>{e(d["short"])}</p><span class="more">{e(T["ui"]["more"])} {ic("arrow")}</span></a>'

def faq_block(items):
    return '<div class="faq">' + "".join(f'<details class="rv"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in items) + "</div>"

def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def crumbs_ld(T, trail):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(trail)]}

def page_hero(T, crumbs, h1, lead, media=None, buttons=True):
    u = T["ui"]
    cr = " / ".join(f'<a href="{h}">{e(n)}</a>' for n, h in crumbs[:-1]) + f' / <span aria-current="page">{e(crumbs[-1][0])}</span>'
    btns = (f'<div class="btns"><a class="btn btn-primary" href="#quote">{e(u["cta_quote"])}</a>'
            f'<a class="btn btn-ghost" href="https://wa.me/{WA}" target="_blank" rel="noopener">{WA_SVG}WhatsApp</a></div>') if buttons else ""
    body = f'<div><nav class="crumbs" aria-label="Breadcrumb">{cr}</nav><h1>{e(h1)}</h1><p class="lead">{e(lead)}</p>{lang_note(T)}{btns}</div>'
    if media:
        return f'<section class="page-hero has-media"><div class="wrap">{body}<div class="media">{media}</div></div></section>'
    return f'<section class="page-hero"><div class="wrap">{body}</div></section>'

BLUEPRINT = '''<div class="blueprint"><svg viewBox="0 0 800 560" aria-hidden="true">
<path class="draw" d="M40 520V120h300v400M340 120h420v400H40"/>
<path class="draw d2" d="M340 300h170v220M510 300h250M150 120v150h190M40 270h110"/>
<path class="draw a d3" d="M560 120l100-80 100 80M600 300v-70h80v70M80 360h200v120H80zM400 360h70v90h-70z"/>
<path class="draw d2" d="M560 400a40 40 0 1 0 80 0a40 40 0 1 0-80 0M200 120a60 60 0 0 1 60 60"/>
</svg></div>'''

def hero_media(up, alt):
    parts = []
    if has_video():
        sm = f' data-src-sm="{up}../assets/video/hero-sm.mp4"' if has_video("hero-sm.mp4") else ""
        poster = f' poster="{up}../assets/img/hero.webp"' if has_img("hero") else ""
        parts.append(f'<video muted loop playsinline preload="none"{poster} data-src="{up}../assets/video/hero.mp4"{sm} aria-hidden="true"></video>')
    slides = [k for k in ("hero", "kitchen", "bathroom", "outdoor") if has_img(k)]
    if slides and not has_video():
        parts += [f'<div class="slide" style="background-image:url({up}../assets/img/{k}.webp)" role="img" aria-label="{e(alt)}"></div>' for k in slides]
    if not parts:
        parts.append(BLUEPRINT)
    return '<div class="hero-media">' + "".join(parts) + "</div>"

# ---------------------------------------------------------------- pages
def page_home(T):
    u = T["ui"]; H = T["home"]; up = ""
    ld = [faq_ld(H["faqs"])]
    out = [head(T, "", H["title"], H["desc"], ld, up="../" if False else ""), header(T, "", up)]
    chips = "".join(f'<span class="chip">{ic("check")}{e(c)}</span>' for c in H["chips"])
    out.append(f'''<section class="hero">{hero_media("", H["hero_alt"])}
<div class="wrap"><p class="eyebrow">{e(H["eyebrow"])}</p><h1>{e(H["h1"])}</h1><p class="lead">{e(H["lead"])}</p>{lang_note(T)}
<div class="btns"><a class="btn btn-primary" href="contact/#quote">{e(u["cta_visit"])} {ic("arrow", "arrow")}</a><a class="btn btn-ghost" href="https://wa.me/{WA}" target="_blank" rel="noopener">{WA_SVG}{e(u["cta_wa"])}</a></div>
<div class="chips">{chips}</div></div><span class="scroll-cue" aria-hidden="true"></span></section>''')
    trades = "".join(f"<span>{e(t)}</span>" for t in H["ticker"])
    out.append(f'<div class="ticker" aria-hidden="true"><div class="track">{trades}{trades}</div></div>')
    # pillars
    pills = []
    for i, g in enumerate(GROUPS):
        G = T["groups"][g]
        key = {"maintenance": "ac", "repairs": "plumbing", "transformation": "kitchen"}[g]
        bg = f'<div class="ph" style="background-image:url(../assets/img/{key}.webp)"></div>' if has_img(key) else f'<div class="art">{ic({"maintenance": "calendar", "repairs": "hammer", "transformation": "home"}[g])}</div>'
        lis = "".join(f'<li><a href="{s[0]}/">{e(T["svc"][s[0]]["name"])}</a></li>' for s in SERVICES if s[1] == g)
        pills.append(f'<div class="pillar rv">{bg}<div class="in"><span class="num">0{i+1} / 03</span><h3>{e(G["name"])}</h3><p>{e(G["desc"])}</p><ul>{lis}</ul></div></div>')
    out.append(f'<section><div class="wrap"><div class="sec-head rv"><p class="eyebrow">{e(H["p_eyebrow"])}</p><h2>{e(H["p_title"])}</h2><p class="lead">{e(H["p_text"])}</p></div><div class="pillars">{"".join(pills)}</div></div></section>')
    # all services
    cards = "".join(svc_card(T, s[0], "") for s in SERVICES)
    out.append(f'<section class="stone"><div class="wrap"><div class="sec-head rv"><p class="eyebrow">{e(H["s_eyebrow"])}</p><h2>{e(H["s_title"])}</h2><p>{e(H["s_text"])}</p></div><div class="grid g3">{cards}</div></div></section>')
    # transformation feature
    out.append(f'''<section><div class="wrap split"><div class="media rv">{picture("kitchen", H["f_alt"], "../", icon="kitchen")}</div>
<div class="rv"><p class="eyebrow">{e(H["f_eyebrow"])}</p><h2>{e(H["f_title"])}</h2><p class="lead">{e(H["f_text"])}</p>
<ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in H["f_list"])}</ul>
<div class="btns"><a class="btn btn-dark" href="home-renovation/">{e(H["f_btn"])} {ic("arrow", "arrow")}</a></div></div></div></section>''')
    # process
    out.append(f'<section class="dark"><div class="wrap"><div class="sec-head rv"><p class="eyebrow">{e(u["process_eyebrow"])}</p><h2>{e(u["process_title"])}</h2><p class="lead">{e(u["process_text"])}</p></div>{steps(T)}<div class="btns" style="margin-top:34px"><a class="btn btn-primary" href="how-we-work/">{e(u["process_more"])}</a></div></div></section>')
    # promises + why
    why = "".join(f'<div class="card rv"><div class="ic">{ic(icn)}</div><h3>{e(h)}</h3><p>{e(p)}</p></div>' for icn, (h, p) in zip(["users", "euro", "clock", "camera", "shield", "pin"], H["why"]))
    out.append(f'<section><div class="wrap"><div class="sec-head rv"><p class="eyebrow">{e(H["w_eyebrow"])}</p><h2>{e(H["w_title"])}</h2></div>{promises(T)}<div class="grid g3" style="margin-top:22px">{why}</div></div></section>')
    # maintenance feature
    out.append(f'''<section class="stone"><div class="wrap split rev"><div class="media rv">{picture("maintenance", H["m_alt"], "../", icon="calendar")}</div>
<div class="rv"><p class="eyebrow">{e(H["m_eyebrow"])}</p><h2>{e(H["m_title"])}</h2><p class="lead">{e(H["m_text"])}</p>
<ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in H["m_list"])}</ul>
<div class="btns"><a class="btn btn-dark" href="maintenance-plans/">{e(H["m_btn"])} {ic("arrow", "arrow")}</a></div></div></div></section>''')
    # areas teaser + faq
    out.append(f'<section><div class="wrap"><div class="sec-head rv"><p class="eyebrow">{e(T["areas"]["eyebrow"])}</p><h2>{e(H["a_title"])}</h2><p>{e(H["a_text"])}</p><div class="btns"><a class="btn btn-line" href="service-areas/">{ic("pin")}{e(u["nav"]["areas"])}</a></div></div>'
               f'<div class="sec-head rv" style="margin-top:72px"><p class="eyebrow">FAQ</p><h2>{e(H["q_title"])}</h2></div>{faq_block(H["faqs"])}<div class="btns" style="margin-top:26px"><a class="btn btn-line" href="faq/">{e(u["faq_more"])}</a></div></div></section>')
    out.append(cta_band(T))
    out.append(footer(T, ""))
    return "".join(out)

def page_service(T, slug):
    u = T["ui"]; d = T["svc"][slug]; s = SVC[slug]; up = "../"
    G = T["groups"][s[1]]
    trail = [(u["nav"]["home"], url(T["lang"], "")), (u["nav"]["services"], url(T["lang"], "services")), (d["name"], url(T["lang"], slug))]
    ld = [crumbs_ld(T, trail), faq_ld(d["faqs"]),
          {"@type": "Service", "name": d["name"], "serviceType": d["name"], "description": d["desc"], "provider": {"@id": BASE + "/#business"},
           "areaServed": {"@type": "Country", "name": "Cyprus"}, "url": url(T["lang"], slug)}]
    out = [head(T, slug, d["title"], d["desc"], ld), header(T, slug, up)]
    out.append(page_hero(T, [(u["nav"]["home"], up), (u["nav"]["services"], up + "services/"), (d["name"], "")], d["h1"], d["lead"],
                         media=picture(s[3], d["name"], up + "../", eager=True, icon=s[2])))
    scope = "".join(f'<div class="card rv"><h3>{ic("check")}{e(h)}</h3><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in items)}</ul></div>' for h, items in d["scope"])
    notes = f'<div class="note rv" style="margin-top:28px"><h3>{e(u["good_to_know"])}</h3><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in d["notes"])}</ul></div>'
    aside = f'''<aside class="sticky"><div class="cta-card"><h3>{e(u["aside_title"])}</h3><p>{e(u["aside_text"])}</p>
<a class="btn btn-primary" href="#quote">{e(u["cta_quote"])}</a><a class="btn btn-ghost" href="https://wa.me/{WA}" target="_blank" rel="noopener">{WA_SVG}WhatsApp</a><a class="btn btn-ghost" href="tel:{PHONE1}">{ic("phone")}{PHONE1_TXT}</a>
<p class="small">{e(u["aside_small"])}</p></div></aside>'''
    out.append(f'<section><div class="wrap aside-grid"><div><div class="sec-head rv" style="margin-bottom:30px"><p class="eyebrow">{e(G["name"])}</p><h2>{e(u["scope_title"])}</h2><p>{e(d["intro"])}</p></div><div class="scope">{scope}</div>{notes}</div>{aside}</div></section>')
    out.append(f'<section class="dark tight"><div class="wrap"><div class="sec-head rv"><p class="eyebrow">{e(u["process_eyebrow"])}</p><h2>{e(u["process_title"])}</h2></div>{steps(T)}</div></section>')
    out.append(f'<section><div class="wrap"><div class="sec-head rv"><p class="eyebrow">FAQ</p><h2>{e(u["svc_faq_title"])}</h2></div>{faq_block(d["faqs"])}</div></section>')
    rel = [x[0] for x in SERVICES if x[1] == s[1] and x[0] != slug][:3]
    if len(rel) < 3:
        rel += [x[0] for x in SERVICES if x[0] != slug and x[0] not in rel][: 3 - len(rel)]
    out.append(f'<section class="stone tight"><div class="wrap"><div class="sec-head rv"><h2>{e(u["related"])}</h2></div><div class="grid g3">{"".join(svc_card(T, r, up) for r in rel)}</div></div></section>')
    out.append(cta_band(T, preselect=slug))
    out.append(footer(T, up))
    return "".join(out)

def page_services(T):
    u = T["ui"]; P = T["services"]; up = "../"
    trail = [(u["nav"]["home"], url(T["lang"], "")), (u["nav"]["services"], url(T["lang"], "services"))]
    ld = [crumbs_ld(T, trail), {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": T["svc"][s[0]]["name"], "url": url(T["lang"], s[0])} for i, s in enumerate(SERVICES)]}]
    out = [head(T, "services", P["title"], P["desc"], ld), header(T, "services", up)]
    out.append(page_hero(T, [(u["nav"]["home"], up), (u["nav"]["services"], "")], P["h1"], P["lead"]))
    for i, g in enumerate(GROUPS):
        G = T["groups"][g]
        cards = "".join(svc_card(T, s[0], up, tag=False) for s in SERVICES if s[1] == g)
        out.append(f'<section class="{"stone" if i % 2 else ""}" id="{g}"><div class="wrap"><div class="sec-head rv"><p class="eyebrow">0{i+1} / 03</p><h2>{e(G["name"])}</h2><p class="lead">{e(G["desc"])}</p></div><div class="grid g3">{cards}</div></div></section>')
    out.append(f'<section class="tight"><div class="wrap">{promises(T)}</div></section>')
    out.append(cta_band(T)); out.append(footer(T, up))
    return "".join(out)

def page_process(T):
    u = T["ui"]; P = T["process"]; up = "../"
    trail = [(u["nav"]["home"], url(T["lang"], "")), (P["h1"], url(T["lang"], "how-we-work"))]
    out = [head(T, "how-we-work", P["title"], P["desc"], [crumbs_ld(T, trail), faq_ld(P["faqs"])]), header(T, "how-we-work", up)]
    out.append(page_hero(T, [(u["nav"]["home"], up), (u["nav"]["process"], "")], P["h1"], P["lead"]))
    detail = ""
    for i, (h, p, items) in enumerate(P["detail"]):
        detail += f'<div class="card rv"><span class="tag">0{i+1}</span><h3>{e(h)}</h3><p>{e(p)}</p><ul class="ticks" style="margin-top:14px">{"".join(f"<li>{e(x)}</li>" for x in items)}</ul></div>'
    out.append(f'<section><div class="wrap"><div class="sec-head rv"><p class="eyebrow">{e(u["process_eyebrow"])}</p><h2>{e(P["d_title"])}</h2></div><div class="scope">{detail}</div></div></section>')
    out.append(f'<section class="stone"><div class="wrap"><div class="sec-head rv"><h2>{e(P["p_title"])}</h2><p>{e(P["p_text"])}</p></div>{promises(T)}<div class="note rv" style="margin-top:28px"><h3>{e(P["pay_title"])}</h3><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in P["pay"])}</ul></div></div></section>')
    out.append(f'<section><div class="wrap"><div class="sec-head rv"><p class="eyebrow">FAQ</p><h2>{e(u["svc_faq_title"])}</h2></div>{faq_block(P["faqs"])}</div></section>')
    out.append(cta_band(T)); out.append(footer(T, up))
    return "".join(out)

def page_areas(T):
    u = T["ui"]; P = T["areas"]; up = "../"
    trail = [(u["nav"]["home"], url(T["lang"], "")), (P["h1"], url(T["lang"], "service-areas"))]
    out = [head(T, "service-areas", P["title"], P["desc"], [crumbs_ld(T, trail)]), header(T, "service-areas", up)]
    out.append(page_hero(T, [(u["nav"]["home"], up), (u["nav"]["areas"], "")], P["h1"], P["lead"]))
    cards = "".join(f'<div class="area rv"><span class="tag">{e(t)}</span><h3>{e(n)}</h3><p>{e(p)}</p></div>' for t, n, p in P["list"])
    out.append(f'<section><div class="wrap"><div class="sec-head rv"><p class="eyebrow">{e(P["eyebrow"])}</p><h2>{e(P["l_title"])}</h2><p>{e(P["l_text"])}</p></div><div class="areas">{cards}</div>'
               f'<div class="note rv" style="margin-top:32px"><h3>{e(P["n_title"])}</h3><p style="margin:0">{e(P["n_text"])}</p></div></div></section>')
    out.append(cta_band(T)); out.append(footer(T, up))
    return "".join(out)

def page_about(T):
    u = T["ui"]; P = T["about"]; up = "../"
    trail = [(u["nav"]["home"], url(T["lang"], "")), (P["h1"], url(T["lang"], "about"))]
    out = [head(T, "about", P["title"], P["desc"], [crumbs_ld(T, trail)]), header(T, "about", up)]
    out.append(page_hero(T, [(u["nav"]["home"], up), (u["nav"]["about"], "")], P["h1"], P["lead"]))
    paras = "".join(f"<p>{e(x)}</p>" for x in P["body"])
    vals = "".join(f'<div class="card rv"><div class="ic">{ic(icn)}</div><h3>{e(h)}</h3><p>{e(p)}</p></div>' for icn, (h, p) in zip(["users", "shield", "doc", "award"], P["values"]))
    facts = "".join(f"<li><strong>{e(k)}:</strong> {e(v)}</li>" for k, v in P["facts"])
    out.append(f'<section><div class="wrap aside-grid"><div class="rv"><p class="eyebrow">{e(P["eyebrow"])}</p><h2>{e(P["b_title"])}</h2>{paras}</div>'
               f'<aside class="sticky"><div class="cta-card"><h3>{e(P["facts_title"])}</h3><ul class="ticks">{facts}</ul></div></aside></div></section>')
    out.append(f'<section class="tight"><div class="wrap">{team(T)}</div></section>')
    out.append(f'<section class="stone"><div class="wrap"><div class="sec-head rv"><h2>{e(P["v_title"])}</h2></div><div class="grid g4">{vals}</div></div></section>')
    out.append(f'<section class="tight"><div class="wrap"><div class="note rv"><h3>{e(P["partner_title"])}</h3><p style="margin:0">{e(P["partner_text"])} <a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div></section>')
    out.append(cta_band(T)); out.append(footer(T, up))
    return "".join(out)

def page_faq(T):
    u = T["ui"]; P = T["faq"]; up = "../"
    allq = [qa for _, items in P["groups"] for qa in items]
    trail = [(u["nav"]["home"], url(T["lang"], "")), (P["h1"], url(T["lang"], "faq"))]
    out = [head(T, "faq", P["title"], P["desc"], [crumbs_ld(T, trail), faq_ld(allq)]), header(T, "faq", up)]
    out.append(page_hero(T, [(u["nav"]["home"], up), (u["nav"]["faq"], "")], P["h1"], P["lead"], buttons=False))
    body = "".join(f'<h2 class="group rv">{e(g)}</h2>{faq_block(items)}' for g, items in P["groups"])
    out.append(f'<section><div class="wrap">{body}</div></section>')
    out.append(cta_band(T)); out.append(footer(T, up))
    return "".join(out)

def page_contact(T):
    u = T["ui"]; P = T["contact"]; up = "../"
    trail = [(u["nav"]["home"], url(T["lang"], "")), (P["h1"], url(T["lang"], "contact"))]
    out = [head(T, "contact", P["title"], P["desc"], [crumbs_ld(T, trail)]), header(T, "contact", up)]
    out.append(page_hero(T, [(u["nav"]["home"], up), (u["nav"]["contact"], "")], P["h1"], P["lead"], buttons=False))
    ways = [("phone", P["w_call"], f'<a href="tel:{PHONE1}">{PHONE1_TXT}</a><br><a href="tel:{PHONE2}">{PHONE2_TXT}</a>'),
            ("check", "WhatsApp · Viber", f'<a href="https://wa.me/{WA}" target="_blank" rel="noopener">{e(P["w_wa"])}</a>'),
            ("mail", "Email", f'<a href="mailto:{EMAIL}">{EMAIL}</a>'),
            ("pin", P["w_office"], f'{ADDR["street"]}, {ADDR["postal"]} {ADDR["locality"]}<br>{e(u["by_appt"])}')]
    cards = "".join(f'<div class="card rv"><div class="ic">{ic(i)}</div><h3>{e(h)}</h3><p>{b}</p></div>' for i, h, b in ways)
    out.append(f'<section class="stone"><div class="wrap">{team(T)}</div></section>')
    out.append(f'<section class="tight"><div class="wrap"><div class="grid g4">{cards}</div><div class="note rv" style="margin-top:24px"><h3>{e(P["tips_title"])}</h3><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in P["tips"])}</ul></div></div></section>')
    out.append(cta_band(T)); out.append(footer(T, up))
    return "".join(out)

def page_legal(T, key, slug):
    u = T["ui"]; P = T[key]; up = "../"
    out = [head(T, slug, P["title"], P["desc"]), header(T, slug, up)]
    out.append(page_hero(T, [(u["nav"]["home"], up), (P["h1"], "")], P["h1"], P["lead"], buttons=False))
    body = ""
    for h, paras in P["sections"]:
        body += f"<h2>{e(h)}</h2>" + "".join(f"<p>{e(p)}</p>" for p in paras)
    out.append(f'<section><div class="wrap prose">{body}<p><em>{e(u["updated"])}: {TODAY}</em></p></div></section>')
    out.append(footer(T, up))
    return "".join(out)

# ---------------------------------------------------------------- root files
def root_index():
    items = "".join(f'<li><a href="{l}/" hreflang="{l}" lang="{l}"><b>{ALL[l]["label"]}</b> {ALL[l]["name"]}<small>{e(ALL[l]["ui"]["tagline_short"])}</small></a></li>' for l in LANGS)
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{url(l, "")}">' for l in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{BASE}/">'
    T = ALL["en"]
    ld = json.dumps({"@context": "https://schema.org", "@graph": [business_ld(T), {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "Inonda LTD", "inLanguage": LANGS}]}, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="google-site-verification" content="{GSC_TOKEN}">
<title>Inonda LTD | Maintenance, Repairs &amp; Renovation Contractor in Cyprus</title>
<meta name="description" content="Inonda LTD — contractor for maintenance, repairs and home renovation in Nicosia and across Cyprus. Εργολάβος συντήρησης, επισκευών και ανακαινίσεων.">
<link rel="canonical" href="{BASE}/">{alts}
<meta property="og:title" content="Inonda LTD | Maintenance, Repairs &amp; Home Transformation in Cyprus"><meta property="og:image" content="{BASE}/assets/og-image.jpg"><meta property="og:url" content="{BASE}/">
<meta name="theme-color" content="#0B1530"><link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" href="assets/favicon.png">
<script>(function(){{var L={json.dumps(LANGS)},s=null;try{{s=localStorage.getItem("inondacy_lang");}}catch(e){{}}
function d(){{var l=navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||"en"];for(var i=0;i<l.length;i++){{var c=String(l[i]).toLowerCase().split("-")[0];if(c==="ua")c="uk";if(c==="gr")c="el";if(c==="iw")c="he";if(L.indexOf(c)>-1)return c;}}return "en";}}
location.replace((s&&L.indexOf(s)>-1?s:d())+"/"+(location.protocol==="file:"?"index.html":""));}})();</script>
<script type="application/ld+json">{ld}</script>
<style>*{{box-sizing:border-box}}body{{font-family:system-ui,sans-serif;margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#0B1530;color:#fff;padding:24px 16px;text-align:center}}main{{max-width:520px;width:100%}}img{{margin:0 auto 12px;background:#fff;border-radius:12px;padding:4px}}h1{{font-size:clamp(22px,6vw,32px);margin:0 0 20px}}ul{{list-style:none;padding:0;margin:0;display:grid;gap:10px}}a{{display:flex;gap:10px;align-items:center;padding:14px 18px;border:1px solid rgba(255,255,255,.22);border-radius:14px;color:#fff;text-decoration:none}}a:hover{{border-color:#F4A321}}b{{font-family:monospace;color:#F4A321}}small{{margin-inline-start:auto;color:#9FADC9}}</style>
</head><body><main><img src="assets/logo-68.png" alt="Inonda LTD logo" width="68" height="53"><h1>Inonda LTD — Maintenance, Repairs &amp; Home Transformation in Cyprus</h1><ul>{items}</ul></main></body></html>
'''

def page_404():
    T = ALL["en"]
    links = " · ".join(f'<a href="/{l}/">{ALL[l]["name"]}</a>' for l in LANGS)
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found | Inonda LTD</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/site.css?v={ver("site.css")}"></head>
<body class="inner"><section class="page-hero" style="min-height:100vh"><div class="wrap"><p class="eyebrow">404</p><h1>This page doesn't exist.</h1><p class="lead">Η σελίδα δεν βρέθηκε · Страница не найдена · הדף לא נמצא</p><p>{links}</p><div class="btns"><a class="btn btn-primary" href="/">inonda.org</a><a class="btn btn-ghost" href="tel:{PHONE1}">{PHONE1_TXT}</a></div></div></section></body></html>'''

def sitemap():
    rows = []
    for p in PAGES + [s[0] for s in SERVICES]:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{url(l, p)}"/>' for l in LANGS) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{url("en", p)}"/>'
        pr = "1.0" if p == "" else ("0.9" if p in SVC or p == "services" else ("0.3" if p in ("privacy-policy", "terms-of-service") else "0.7"))
        for l in LANGS:
            rows.append(f"<url><loc>{url(l, p)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority>{alts}</url>")
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n"

def llms():
    T = ALL["en"]
    lines = ["# Inonda LTD (inonda.org)", "", "> " + T["ui"]["org_desc"], "",
             f"Registered company {REG}, {ADDR['street']}, {ADDR['postal']} {ADDR['locality']}, Cyprus. Email {EMAIL}.",
             f"Irina, Director: {PHONE1_TXT} (WhatsApp, Viber), Russian, Greek, English. Constantin, Secretary / Handyman / Foreman: {PHONE2_TXT}, Romanian, Greek, English.",
             "We answer and quote in Greek, English, Russian and Romanian (website also in Ukrainian and Hebrew). Property management services: https://www.inonda.site/", "", "## Services"]
    for s in SERVICES:
        lines.append(f"- [{T['svc'][s[0]]['name']}]({url('en', s[0])}): {T['svc'][s[0]]['short']}")
    lines += ["", "## Company", f"- [How we work]({url('en', 'how-we-work')})", f"- [Service areas]({url('en', 'service-areas')})", f"- [About]({url('en', 'about')})", f"- [FAQ]({url('en', 'faq')})", f"- [Contact]({url('en', 'contact')})"]
    return "\n".join(lines) + "\n"

# ---------------------------------------------------------------- build
def write(rel, text):
    p = os.path.join(PUB, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)

ALL = {}

def main():
    prepare_images()
    only = [a for a in sys.argv[1:] if a in LANGS]
    for l in LANGS:
        if os.path.exists(os.path.join(ROOT, "build", "content", l + ".py")):
            ALL[l] = load(l)
    missing = [l for l in LANGS if l not in ALL]
    if missing:
        print("missing languages (using English):", missing)
        import copy
        for l in missing:
            T = copy.deepcopy(ALL["en"]); T["lang"] = l; T["label"] = l.upper(); T["name"] = l.upper()
            T["dir"] = "rtl" if l == "he" else "ltr"; ALL[l] = T
    n = 0
    for l in (only or LANGS):
        T = ALL[l]
        write(f"{l}/index.html", page_home(T)); n += 1
        write(f"{l}/services/index.html", page_services(T))
        write(f"{l}/how-we-work/index.html", page_process(T))
        write(f"{l}/service-areas/index.html", page_areas(T))
        write(f"{l}/about/index.html", page_about(T))
        write(f"{l}/faq/index.html", page_faq(T))
        write(f"{l}/contact/index.html", page_contact(T))
        write(f"{l}/privacy-policy/index.html", page_legal(T, "privacy", "privacy-policy"))
        write(f"{l}/terms-of-service/index.html", page_legal(T, "terms", "terms-of-service"))
        n += 8
        for s in SERVICES:
            write(f"{l}/{s[0]}/index.html", page_service(T, s[0])); n += 1
    write("index.html", root_index())
    write("404.html", page_404())
    write("sitemap.xml", sitemap())
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    write("llms.txt", llms())
    print(f"built {n} pages")

if __name__ == "__main__":
    main()
