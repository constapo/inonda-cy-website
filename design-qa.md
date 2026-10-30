# Living Blueprint release QA — 31 October 2026

final result: passed

## Visual target and evidence

Source visual truth: the third displayed concept selected by the owner, `exec-cde95957-66fe-4a58-a690-20e803fff573.png` (1122 × 1402 pixels). The approved reference remains in the conversation and its generated-image record.

Implementation: Chrome-rendered `/el/`, `/el/bathroom-renovation/`, `/el/contact/#quote` and six-language responsive checks. A combined comparison capture in Chrome tab 10 at `http://terminal.local:4173/__qa_compare.html` placed the source and working implementation together in one screenshot. Source displayed at 650px wide; working iframe was 1440 × 1800 CSS px scaled to 650px wide. Browser viewport 1363 × 936 CSS px, default density. The browser returned inline screenshots rather than a filesystem screenshot path. The full-page mock and above-fold browser captures were compared with their scale/crop differences explicitly accounted for.

Focused comparisons: header/logo, Greek headline, cutaway house crop, CTAs, service tabs, original brand icons. Additional mobile comparison capture showed Greek, Hebrew and Russian at 390px frame widths; all six languages were checked at 320, 390, 768 and 1363px frames. Scrollbar-adjusted content widths were 305, 375, 753 and 1348px. Hebrew retained RTL.

## Findings and fixes

- P1, first iteration: shared navigation stylesheet overrode body padding and covered the hero. Fixed by placing the versioned presentation assets after the shared styles. Post-fix hero top equals header bottom: desktop 144px, mobile 124px.
- P2, first mobile iteration: logo/language/menu row clipped the menu. Fixed compact brand sizing, language-selector width and fixed button sizing. Post-fix menu stays inside the viewport at 320px and 390px; no horizontal overflow across all 24 viewport/language combinations.
- P2, first comparison: hero hierarchy was smaller than the selected mock. Increased desktop headline and hero height, widened the editorial column and added service-category icons. Final combined capture preserves the selected white header, architectural blue hero, cutaway-house focal point, service navigation, white service columns and original social colours.
- P2, interaction check: the transparent hero layout could intercept room hotspots. Set the layout to pass pointer events through while its copy and selector retain interaction. Re-loaded browser navigation from the bathroom hotspot reached the correct service page.
- P2, live check: the floating chat toggle could overlap the service-panel link. Moved it beside the fixed phone controls at the lower edge, including mirrored RTL positioning; presentation release 2 refreshes cached styles.

## Required fidelity surfaces

- Typography: existing free Commissioner/Manrope families retained; Greek and Hebrew fallbacks checked, hierarchy/line wrapping reviewed. Headline remains real accessible HTML.
- Spacing: desktop hero and responsive stacking reviewed; no persistent controls clip. Original longer service detail remains below the concept's shorter illustrative layout.
- Colours: navy, Ocean Blue, white and restrained cyan; readable focus indicators. Full-colour Facebook/Instagram/TikTok/YouTube and WhatsApp/Viber assets preserved without filters.
- Images: one generated cutaway-house illustration matches the selected direction and is explicitly labelled as conceptual. Responsive WebP exports are 389,560 and 135,448 bytes, with intrinsic dimensions, preload and high fetch priority. Original company logo and other company media unchanged.
- Copy: original content modules and all language routes preserved. The original hero description moves into an intro strip; original presentation video remains farther down the page. New brief labels are localized in all six languages.

## Interactions and technical checks

- Click and arrow/Home/End keyboard service selection; correct panel visibility and destination links.
- Room hotspot navigation, inspection CTA, contact page and empty form validation. Four invalid required fields prevent submission; no messages sent.
- Mobile menu opens; Escape closes it and returns focus.
- Browser console review: no first-party site JavaScript errors observed. Unrelated Chrome-extension metadata errors were excluded.
- Content consistency build passed. Release checker passed on all 186 pages: one H1, titles/descriptions, canonical/hreflang targets, valid JSON-LD, unique IDs, existing local links/assets/anchors, social profiles, RTL and sitemap coverage.
- JavaScript syntax check passed. Reduced-motion styling disables animation and smooth scroll. No new runtime library or paid service.

## Intentional differences and limits

The full original website content remains; the short concept is not a replacement for detailed service pages. The conceptual 360° glyph is not shipped as a fake control: production uses real service tabs and room links rather than claiming a rotatable 3D model. Original PNG logo proportions are preserved rather than recreating the generated lockup. Existing five-step process remains complete. Browser checks cover representative interactions and all homepage languages, not every possible device or assistive technology.

## Follow-up polish

P3 only: exact wireframe geometry and room arrangement differ slightly from the concept because the production illustration is a separate asset. Field Core Web Vitals and search ranking changes require post-release measurement.
