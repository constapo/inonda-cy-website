# INONDA design and SEO verification — 29 October 2026

## Preserved
Original visible content, company logo and media files, JavaScript, calculation rates and formulas, contact links and language routes are unchanged. No paid service or new external dependency was added.

## Verified in GitHub source
- Both static websites: all six language homepages have titles, descriptions, indexable robots metadata, self-referencing canonicals, seven language alternates including x-default, Open Graph metadata and parseable structured data.
- Property-management sitemap: 120 unique URLs, each mapped to an existing repository page.
- Renovation sitemap: 186 unique URLs, each mapped to an existing repository page.
- All three robots.txt files allow crawling and identify their sitemap.
- Estimator: company and free WebApplication structured data, search ownership tags, canonical and six language alternates are retained.
- Estimator SEO update adds Open Graph and Twitter preview metadata using the existing title, description and original logo; allows large search image previews; adds reciprocal language alternates to all six sitemap entries.
- CSS structural checks passed for all three stylesheets. Checked contrast pairs: white/ocean-blue 4.87:1, white/dark-navy 10.20:1, muted text/white 5.31:1, light-cyan/deep-navy 10.96:1.

## Verification boundaries
These are source checks, not live indexing or ranking results. Individual interior-page metadata has not been exhaustively audited. Chrome visual QA, live response headers, rendered language pages, Google structured-data validation and Wasmer deployment verification remain pending.
The estimator changes language and canonical metadata in JavaScript; its server returns the same initial English HTML for language query URLs. Search-engine rendering and localized indexing need live verification. Social preview crawlers receive the existing default English metadata.
No Search Console/Bing submission or performance measurement was performed. Existing ownership tags do not prove current account access or indexing.
No ranking, traffic or AI citation improvement is guaranteed.

## Release checks
1. Review desktop/mobile layouts in Chrome, including Greek and Hebrew RTL, forms, menu and estimator controls.
2. Confirm content, logos and calculation code remain unchanged against main.
3. Verify existing Wasmer account and free-plan deployment settings before release; deploy only through Wasmer.
4. Verify public pages and assets after deployment, including sitemap responses and canonical/hreflang behavior.
5. Use the authorized Google Search Console and Bing Webmaster Tools accounts to check sitemap ingestion, indexed pages and search performance.

## Release follow-up — 30 October 2026

GitHub PR #1 was inspected against its recorded base/head. The blue design refresh preserves the original logo/media and application/calculation sources. Asset URLs now use release version 20261030-1, and the shared generator VERSION is synchronized across the three repositories. Only version parameters change in existing static page HTML.

Desktop previews were inspected for all three sites at 1363px. Mobile homepage checks used a 390px iframe (375px content width); all six languages on each website reported scrollWidth equal to clientWidth. Hebrew retained RTL. The management mobile menu opened successfully. The management header breakpoint/quote layout and renovation hero-label contrast were corrected during QA. Estimator hero and inset company images loaded. Local preview copies did not include every unchanged repository media file.

The estimator passed 36 JavaScript tests and 17 Python tests. The host robots check now validates index/follow semantics while accepting the added search-preview directives. The GitHub safeguard permits asset-version changes while comparing existing static HTML and estimator body content, and rejects unexpected changes to application logic or logo files.

Wasmer deployment and live-domain verification are pending at this commit. No new service, paid subscription, DNS change or repository-visibility change is part of the release. Historical verification boundaries above remain applicable to indexing/rankings and interior-page visual coverage.
