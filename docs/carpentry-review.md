# INONDA LTD — Carpentry & Custom Woodwork review notes

Status: **DRAFT PR #4. NOT MERGED. NOT PUBLISHED.**

- Review: https://github.com/constapo/inonda-cy-website/pull/4
- Reference estimator catalog: `constapo/inonda-service-estimator/dist/carpentry.mjs`.
- Site: `https://www.inonda.org`; only its repository is changed.
- Source files: `build/carpentry_catalog.json` (exact categories, six-language labels/materials), `build/carpentry_details.json` (localized service guidance), `build/carpentry_pages.py` (generator), `build/carpentry.css` (presentation), `build/gen.py` (integration), `build/check_carpentry.py` and browser tests.
- **No public hosting attribution** and no changes to domain/DNS or site hosting.
- Existing `/{lang}/doors-windows-carpentry/` pages are preserved; each gains a link to the new Carpentry section.

## Page map

Each row has six localized URLs: `https://www.inonda.org/{el|en|ru|uk|he|ro}/<route>/`.

| Page or estimator ID | Route |
| --- | --- |
| Main catalog | `carpentry/` |
| `doorsFrames` | `carpentry/doors-frames/` |
| `timberWindows` | `carpentry/timber-windows-shutters/` |
| `kitchenCabinets` | `carpentry/kitchen-utility-cabinets/` |
| `wardrobes` | `carpentry/wardrobes-storage/` |
| `fittedFurniture` | `carpentry/shelving-fitted-furniture/` |
| `panelling` | `carpentry/wall-panelling-trim/` |
| `stairs` | `carpentry/stairs-balustrades/` |
| `outdoorCarpentry` | `carpentry/outdoor-carpentry/` |
| `carpentryRepairs` | `carpentry/repairs-alterations/` |
| `otherCustom` | `carpentry/custom-projects/` |

## Customer and pricing safeguards

Every subsection details what is included, materials and hardware, required measurements, typical defects, installation and aftercare, safety qualifications, four FAQs and related services. All ten categories are visible on the Carpentry landing page; pages link to the existing estimator `?lang={lang}#bp-carpentry-section`. Do not invent per-category estimator preselection.

Custom work: **Price on Request — Custom Quotation**, not an automatic estimate or fixed price. Existing contract-only restrictions for small/urgent repairs remain. No internal cost components or separate travel charges are advertised. The selected carpentry subsection is passed as a labeled field into the existing customer-controlled WhatsApp enquiry, without sending messages automatically. Company contacts, branding, language selector, original services and existing calculator remain unchanged.

## Source-driven build and verification

The generated `public/` pages are **not hand-maintained**. After owner approval, a push to `main` invokes the existing deployment workflow, now running:

```sh
python3 build/check_content.py
python3 build/gen.py
python3 build/check_carpentry.py
```

The draft PR also runs browser smoke tests using an isolated local HTTP preview and uploads the generated site package and screenshots as downloadable GitHub Actions artifacts, with no public deployment. Checks cover all 66 routes, all six languages and Hebrew RTL, language links, unique canonical titles, indexability, reciprocal hreflang, sitemap, service and breadcrumb JSON-LD, four FAQs per category, WhatsApp enquiry links, estimator links, mobile overflow, and required company attribution.

**Review the current successful workflow at the pull request**, including desktop/mobile screenshots and the exact changed files. The preview files are temporary review artifacts, not a public website.

## Limitations and release approval

A successful build checks the generated files, not every possible real-world customer interaction. Before approving publication, review text quality and official company claims, sample the screenshots, verify both WhatsApp and estimator links, and verify mobile navigation with real devices when practical.

**Explicit approval is required to merge/deploy** this draft PR. A merge to `main` triggers the repository's publishing workflow. After an approved release, verify the `/el/`, `/en/`, `/ru/`, `/uk/`, `/he/`, and `/ro/` Carpentry routes and their ten subpages, site language menu, enquiry form and sitemap. Confirm the two sister sites are unchanged.

Rollback: revert the single merged feature PR on `main` and verify the restored deployment. The pre-feature base commit in PR #4 is `f63499fcde227b7cba616fab06cb4899259a1f56`; do not force-push or rewrite history. Do not remove unrelated site updates.
