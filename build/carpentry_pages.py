"""Source-driven rendering of INONDA LTD's six-language, ten-category carpentry pages.

The six-language content is in build/carpentry_details.json; category labels,
material options and immutable category IDs mirror the existing estimator.
The source generator in build/gen.py is authoritative, not public/*.html.
"""
import json
from pathlib import Path
from urllib.parse import quote

BASE_DIR=Path(__file__).resolve().parent
CATALOG=json.loads((BASE_DIR/'carpentry_catalog.json').read_text(encoding='utf-8'))
DETAILS=json.loads((BASE_DIR/'carpentry_details.json').read_text(encoding='utf-8'))['languages']
SLUGS=CATALOG['slugs']
CATEGORIES=CATALOG['categories']
CATS={cat['id']:cat for cat in CATEGORIES}
LANGUAGES=['el','en','ru','uk','he','ro']
RELATED=['doors-windows-carpentry','kitchen-renovation','home-renovation','outdoor-works','decorative-panels','flooring-tiling']

def routes():
    return ['carpentry']+['carpentry/'+SLUGS[c['id']] for c in CATEGORIES]

def validate():
    assert len(CATEGORIES)==10 and len(CATS)==10, 'The estimator has exactly ten categories'
    assert len(SLUGS)==10 and len(set(SLUGS.values()))==10, 'Every category needs a unique slug'
    for lang in LANGUAGES:
        assert lang in DETAILS, 'Missing locale: '+lang
        loc=DETAILS[lang]
        assert len(loc['ui']['steps'])==8 and len(loc['ui']['questions'])==4
        assert len(loc['entries'])==10
        for c in CATEGORIES:
            assert len(c['label'][lang])>2 and len(c['description'][lang])>10
            assert c['id'] in loc['entries'], (lang,c['id'])
            d=loc['entries'][c['id']]
            assert len(d['scope'])>=5,(lang,c['id'],'scope')
            assert all(len(d[k])>=30 for k in ('material','measure','issues','install','care','safety','quote')),(lang,c['id'],'technical copy')
            assert all(material in CATALOG['materials'] for material in c['materials'])
    return True

def title(lang,category=None):
    if category is None:return DETAILS[lang]['ui']['title']
    return CATS[category]['label'][lang]

def url(lang,category=None):
    slug='carpentry'+('/'+SLUGS[category] if category else '')
    return 'https://www.inonda.org/'+lang+'/'+slug+'/'

def estimator_url(lang):
    return 'https://www.inonda.homes/?lang='+lang+'#bp-carpentry-section'

def link(g,href,caption,css='btn btn-line',extra=''):
    return '<a class="'+g.e(css)+'" href="'+g.e(href)+'"'+extra+'>'+g.e(caption)+'</a>'

def quote_url(lang,category=None):
    ui=DETAILS[lang]['ui']
    subject=title(lang,category)
    text=ui['quoteButton']+': '+subject+'\n'+ui['requestDetails']
    return 'https://wa.me/35794091616?text='+quote(text,safe='')

def card(g,lang,cat,up):
    ui=DETAILS[lang]['ui'];name=cat['label'][lang]
    href=up+'carpentry/'+SLUGS[cat['id']]+'/'
    return ('<article class="card rv inonda-wood-card"><div class="ic">'+g.ic('door')+'</div>'
            '<h3><a href="'+g.e(href)+'">'+g.e(name)+'</a></h3>'
            '<p>'+g.e(cat['description'][lang])+'</p>'
            '<p class="small">'+g.e(ui['workTypes'])+'</p>'
            +link(g,href,ui['more'],'btn btn-line')+'</article>')

def promo(g,T,up):
    l=T['lang'];ui=DETAILS[l]['ui']
    return ('<section class="stone tight" id="carpentry-services-promo"><div class="wrap">'
            '<div class="note rv"><h2>'+g.e(ui['short'])+'</h2><p>'+g.e(ui['intro'])+'</p>'
            '<div class="btns">'+link(g,up+'carpentry/',ui['source'],'btn btn-primary')
            +link(g,estimator_url(l),ui['estimator'],'btn btn-ghost',' target="_blank" rel="noopener"')
            +'</div></div></div></section>')

def common_actions(g,T,category=None):
    lang=T['lang'];ui=DETAILS[lang]['ui']
    return ('<div class="btns inonda-wood-actions">'
            +link(g,quote_url(lang,category),ui['quoteButton'],'btn btn-primary',' target="_blank" rel="noopener"')
            +link(g,estimator_url(lang),ui['estimator'],'btn btn-ghost',' target="_blank" rel="noopener"')
            +link(g,'#quote',ui['contact'],'btn btn-line')+'</div>'
            '<p class="small">'+g.e(ui['estimatorNote'])+'</p>')

def material_options(g,lang,cat):
    ui=DETAILS[lang]['ui']
    return ('<div class="inonda-wood-chips" aria-label="'+g.e(ui['materialLabel'])+'">'
            +''.join('<span class="chip">'+g.e(CATALOG['materials'][code][lang])+'</span>' for code in cat['materials'])
            +'</div>')

def page(T,g,category=None):
    lang=T['lang'];ui=DETAILS[lang]['ui']
    root=category is None;up='../' if root else '../../'
    page_slug='carpentry' if root else 'carpentry/'+SLUGS[category]
    heading=ui['title'] if root else title(lang,category)
    lead=ui['intro'] if root else CATS[category]['description'][lang]
    desc=lead[:210] # Unique localized description, no unverified marketing claims.
    title_tag=(heading+' | INONDA LTD, Cyprus') if not root else (heading+' | INONDA LTD')
    breadcrumb=[(T['ui']['nav']['home'],g.url(lang,'')),(T['ui']['nav']['services'],g.url(lang,'services'))]
    breadcrumb += [(ui['short'],url(lang,None))]
    if not root:breadcrumb.append((heading,url(lang,category)))
    ld=[g.crumbs_ld(T,breadcrumb)]
    if root:
        ld.append({'@type':'ItemList','name':ui['short'],'itemListElement':[
            {'@type':'ListItem','position':i+1,'name':cat['label'][lang],'url':url(lang,cat['id'])}
            for i,cat in enumerate(CATEGORIES)]})
    else:
        d=DETAILS[lang]['entries'][category]
        faq=[(q,a) for q,a in zip(ui['questions'], [
            ' '.join(d['scope'][:4]),
            d['material']+' '+d['care'],
            d['measure']+' '+d['quote'],
            d['issues']+' '+d['safety']])]
        ld.append({'@type':'Service','name':heading,'serviceType':ui['short'],
                   'description':lead,'provider':{'@id':g.BASE+'/#business'},
                   'areaServed':{'@type':'Country','name':'Cyprus'},'url':url(lang,category)})
        ld.append(g.faq_ld(faq))
    head=g.head(T,page_slug,title_tag,desc,ld,up=up)
    css='<link rel="stylesheet" href="/assets/carpentry.css?v=20261116-carpentry-1">'
    head=head.replace('</head>',css+'</head>',1)
    crumbs=[(T['ui']['nav']['home'],up),
            (T['ui']['nav']['services'],up+'services/')]
    if root:crumbs.append((heading,''))
    else:crumbs.extend([(ui['short'],up+'carpentry/'),(heading,'')])
    out=[head,g.header(T,page_slug,up),g.page_hero(T,crumbs,heading,lead,buttons=False)]
    if root:
        out.append('<section class="inonda-wood-section" id="woodwork-categories"><div class="wrap">'
                   '<div class="sec-head rv"><h2>'+g.e(ui['browse'])+'</h2><p>'+g.e(ui['workTypes'])+'</p></div>'
                   '<div class="grid g3 inonda-wood-grid">'
                   +''.join(card(g,lang,cat,up) for cat in CATEGORIES)+'</div></div></section>')
        out.append('<section class="stone inonda-wood-section"><div class="wrap prose">'
                   '<h2>'+g.e(ui['materialsTitle'])+'</h2><p>'+g.e(ui['materialsIntro'])+'</p>'
                   '<h2>'+g.e(ui['process'])+'</h2><ol class="inonda-wood-process">'
                   +''.join('<li>'+g.e(s)+'</li>' for s in ui['steps'])+'</ol>'
                   '<h2>'+g.e(ui['quote'])+'</h2><p>'+g.e(ui['quoteNote'])+'</p>'
                   '<p>'+g.e(ui['repairRule'])+'</p><p>'+g.e(ui['compliance'])+'</p>'
                   +common_actions(g,T)+'</div></section>')
    else:
        cat=CATS[category];d=DETAILS[lang]['entries'][category]
        out.append('<section class="inonda-wood-section"><div class="wrap aside-grid"><div>'
                   '<h2>'+g.e(ui['scope'])+'</h2><p>'+g.e(ui['workTypes'])+'</p>'
                   '<ul class="ticks inonda-wood-list">'+''.join('<li>'+g.e(item)+'</li>' for item in d['scope'])+'</ul>'
                   '<h2>'+g.e(ui['materials'])+'</h2><p>'+g.e(d['material'])+'</p>'
                   +material_options(g,lang,cat)
                   +'<h2>'+g.e(ui['measurement'])+'</h2><p>'+g.e(d['measure'])+'</p>'
                   '<h2>'+g.e(ui['issues'])+'</h2><p>'+g.e(d['issues'])+'</p>'
                   '<h2>'+g.e(ui['installation'])+'</h2><p>'+g.e(d['install'])+'</p>'
                   '<h2>'+g.e(ui['care'])+'</h2><p>'+g.e(d['care'])+'</p>'
                   '<h2>'+g.e(ui['safety'])+'</h2><p>'+g.e(d['safety'])+'</p>'
                   '<p class="small">'+g.e(ui['compliance'])+'</p>'
                   '</div><aside class="sticky"><div class="cta-card">'
                   '<h3>'+g.e(ui['quote'])+'</h3><p>'+g.e(ui['quoteNote'])+'</p>'
                   '<p>'+g.e(d['quote'])+'</p><p class="small">'+g.e(ui['scopeFoot'])+'</p>'
                   +common_actions(g,T,category)+'</div></aside></div></section>')
        out.append('<section class="stone inonda-wood-section"><div class="wrap prose">'
                   '<h2>'+g.e(ui['process'])+'</h2><ol class="inonda-wood-process">'
                   +''.join('<li>'+g.e(s)+'</li>' for s in ui['steps'])+'</ol>'
                   '<h2>'+g.e(ui['faq'])+'</h2>'+g.faq_block(faq)
                   +(('<p class="note">'+g.e(ui['repairRule'])+'</p>') if category=='carpentryRepairs' else '')
                   +'</div></section>')
        out.append('<section class="inonda-wood-section"><div class="wrap">'
                   '<h2>'+g.e(ui['related'])+'</h2>'
                   '<div class="grid g3 inonda-wood-grid">'
                   +''.join(card(g,lang,c,up) for c in [x for x in CATEGORIES if x['id']!=category][:3])
                   +'</div>'
                   +link(g,up+'carpentry/',ui['return'],'btn btn-line')
                   +'</div></section>')
    out.append('<section class="inonda-wood-section"><div class="wrap">'
               '<h2>'+g.e(ui['related'])+'</h2><div class="btns">'
               +''.join(link(g,up+slug+'/',T['svc'][slug]['name'],'btn btn-line') for slug in RELATED)
               +'</div></div></section>')
    # Preserve the existing required-description enquiry form while including the
    # selected Carpentry category in the customer's editable WhatsApp draft.
    # This is a static hidden field, not an automatically sent enquiry.
    inquiry=g.cta_band(T,preselect='doors-windows-carpentry')
    marker=' novalidate>'
    assert marker in inquiry, 'Existing quote form markup changed'
    inquiry=inquiry.replace(marker,
        marker+'<input type="hidden" name="Carpentry category" value="'+g.e(heading)+'">',1)
    out.append(inquiry)
    out.append(g.footer(T,up))
    return ''.join(out)

def stylesheet():
    return (BASE_DIR/'carpentry.css').read_text(encoding='utf-8')
