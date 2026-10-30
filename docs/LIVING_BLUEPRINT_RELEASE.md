# INONDA.org Living Blueprint

Approved by the owner: third displayed homepage concept. Authorized for publication with technical SEO checks on 31 October 2026 (Cyprus time).

## Scope

New white company header, blue cutaway-house hero, localized service selector and clickable room/service links. Existing content, six languages, original logo, forms, contact destinations, social profiles, original platform colours and website referrals remain. Only inonda.org receives this redesign.

Presentation source: `tools/inonda_living.py`, `public/assets/living-blueprint.css` and `public/assets/living-blueprint.js`, applied by `build/gen.py`. Bump the presentation VERSION after changing cached presentation assets, then rebuild. Shared network assets remain unchanged.

Hero is an AI-generated conceptual architectural illustration approved as part of this design, not a photograph of completed work. Production exports are self-hosted responsive WebP; the generated master remains in the design conversation's image record. No third-party rendering service or runtime dependency is required.

## SEO

Preserves existing service/location titles, descriptions, canonical URLs, crawlable localized links, six-language alternates, Google/Bing ownership tags, company identity, service/FAQ/breadcrumb schema, social preview metadata, robots and IndexNow proof files. Adds localized WebPage schema and a 14-service homepage ItemList. Refreshes all 186 sitemap entries with the Cyprus date of the meaningful design release. Images have descriptive alt text, explicit sizes, lazy loading below the hero, responsive WebP and prioritized hero loading.

These checks establish technical readiness, not search ranking, rich-result eligibility or traffic gains. Google submission requires Search Console; IndexNow submission can run once after the public release is verified using the existing `tools/submit_indexnow.py org`.

## Validation

```
python -m pip install -r requirements-dev.txt
python build/check_content.py
python build/gen.py
python build/check_release.py
node --check public/assets/living-blueprint.js
```

See `design-qa.md` for visual and interaction evidence. Browser checks include 24 language/viewport combinations. `python tools/preview_server.py --host 0.0.0.0 --port 4173` starts the dependency-free local preview. The local preview package manifest is deliberately excluded from production so Wasmer continues using the original Staticfile host.

## Rollback

Pre-redesign main: `34dc284292a13068fca471a70409eef104629438`. Restore that tree in a new commit to keep history recoverable. Use an expected-SHA lease and verify the live domain after deployment. Never force-reset main or change DNS for this release.
