# INONDA search and business-listing setup

The owner authorized free promotion of all three company websites. No paid ads, subscriptions, accreditation or review purchases. One company with three complementary websites; do not create duplicate company listings for each domain.

Primary website: https://www.inonda.site/ (property management). Service detail: https://www.inonda.org/. Editable VAT-inclusive budget ranges: https://www.inonda.homes/. INONDA LTD, HE490415; main contact Irina +35794091616; Constantin +35794091613; inonda2026@outlook.com. All-Cyprus service, including owners based abroad with properties in Cyprus. No claim of physical operations abroad.

The owner confirmed on 25 October 2026 that the company visits clients at their properties. Use a service-area listing; hide the registered street address where permitted. Do not invent customer-facing opening hours, storefront, ratings, reviews, accreditation or recommendations. The imported Google Business Profile is the existing company listing and must not be duplicated.

Public search ownership tags and IndexNow ownership files are intentionally public protocol proofs; they are not account passwords or private API credentials. Keep private account credentials out of all files.

`tools/inonda_seo.py` supplies a single company identity across the three sites, both contact points, all four company social profiles, public verification tags and crawlable language controls. `tools/inonda_network.py` applies it, including to root language choosers. Keep tools/search-config.json and these shared tools synchronized. The inonda.org generator calls the same enhancement on every HTML build.

After a meaningful deployment, wait until the public domain serves the latest version, then run `python tools/submit_indexnow.py site`, `org` or `homes` once for the updated host. It validates the deployed public ownership file before submitting the host's canonical sitemap URLs. HTTP 200 means received; HTTP 202 means key validation pending. Neither guarantees crawling, indexing or ranking. Do not repeatedly resubmit unchanged pages. Google uses Search Console and sitemaps, not IndexNow.

Search Console and Bing Webmaster Tools require the owner's authenticated accounts. Do not grant third-party account access merely to avoid adding a public verification tag. Verification tokens must remain after success. Apple Business requires organization verification and, where eligible, separate location/brand setup; account creation alone is not an active Maps listing.

Cyprus eligibility checked against primary platform documentation on 25 October 2026. Apple Business supports Cyprus brand/location management; Google Business Profile supports Cyprus. Nextdoor's 11-country platform list excludes Cyprus. BBB serves the US/Canada and paid accreditation is outside this free-only task. Yelp country eligibility needs confirmation in its country selector before submitting a Cyprus listing.
