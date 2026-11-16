"""Release checks for the six-language detailed Aluminium Works page."""
import re
from pathlib import Path
import aluminium_details as details

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("el", "en", "ru", "uk", "he", "ro")
PROHIBITED = re.compile(
    r"more than one day of work|only jobs of more than one day|"
    r"λίγων λεπτών ή ωρών|άνω της μίας ημέρας|"
    r"более одного дня|понад один день|"
    r"יותר מיום אחד|mai mult de o zi|"
    r"maintenance-contract customers only|"
    r"only for customers with a maintenance contract",
    re.I,
)

for lang in LANGS:
    source = details.DATA[lang]["sections"]
    assert len(source) == 14, (lang, "source category count")
    assert all(h and d for h, d in source), (lang, "empty translated text")
    html = (ROOT / "public" / lang / "aluminium-works" / "index.html").read_text(encoding="utf-8")
    cards = re.findall(r'<details class="rv" id="aluminium-detail-([0-9]+)"', html)
    assert cards == [str(i) for i in range(1, 15)], (lang, "missing/reordered categories", cards)
    assert html.count('id="aluminium-detailed-services"') == 1, (lang, "missing detail section")
    assert html.count('href="#quote"') >= 2, (lang, "inspection / quotation CTA")
    assert not PROHIBITED.search(html), (lang, "obsolete visitor-facing eligibility rule")
    assert "aluminium-works" in html and "application/ld+json" in html, (lang, "SEO metadata")
    assert ('dir="rtl"' in html) == (lang == "he"), (lang, "text direction")
print("PASS: 14 accessible Aluminium Works categories in each of six languages, CTAs and metadata.")
