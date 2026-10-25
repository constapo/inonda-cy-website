# INONDA LTD website instructions

- The owner explicitly authorized coordinated public updates and referrals between inonda.site, inonda.org and inonda.homes. Do not change DNS or repository visibility.
- Preserve existing page content, language URLs, search metadata, forms and the official company logo. No fabricated reviews or customer claims. Use company media only.
- inonda.site explains property management; inonda.org explains maintenance, repairs and renovation; inonda.homes provides editable planning estimates, not fixed quotations.
- Shared navigation and website cards come from tools/inonda_network.py and tools/network-copy.json. Keep those source files synchronized with the other two INONDA repositories. Run python tools/inonda_network.py org after shared-copy updates.
- All six languages (el, en, ru, uk, he, ro) must link to both other INONDA websites in the selected language. Hebrew retains RTL.
- Carry only allowlisted service IDs and named areas to the estimator, with no personal data, notes or saved plans. Specialist trade work is not covered by the estimator’s general handyman allowance.
- Preserve 19% VAT-inclusive estimates on inonda.homes and its commercial pricing. Do not display the commercial adjustment percentage in public copy.
- Company: HE490415; all-Cyprus coverage. Contact Irina +35794091616, Constantin +35794091613, inonda2026@outlook.com. Call, inspection, then written offer. Do not send messages during testing.
- Read README.md. The main branch deploys automatically on Wasmer. Inspect current remote main and preserve concurrent edits; use expected_sha leases. Verify the live domain after deployment.
- inonda.org pages are generated: keep changes in build/gen.py or the shared tools and ensure future builds preserve the network component.

- The owner explicitly requested original WhatsApp and Viber brand icons. Local original files are whatsapp-official.svg and viber-official.svg; provenance is in BRAND-ASSETS.md. This is an explicit exception to the company-only media rule for communication-channel icons. Do not replace brand symbols with letters or recolour them.
- The same six-language guided chatbot runs on all three websites from tools/inonda_chat.js, tools/inonda_chat.css, tools/chat-copy.json and tools/chat-ui.json. It is an automated local service guide, not a generative AI or a human. Requests open WhatsApp/email drafts only on a visitor’s explicit click; no automatic sending, booking or quote confirmation.

- Footer social profiles use tools/social-links.json. Preserve the owner-supplied Facebook and Instagram company URLs. TikTok is the confirmed company profile https://www.tiktok.com/@inonda26; YouTube is https://www.youtube.com/@InondaLTD. Do not substitute guessed or generic profiles. LinkedIn remains excluded.

- The owner explicitly requested social-media brand icons in every footer. Preserve the self-hosted facebook-brand.svg, instagram-brand.svg, tiktok-brand.svg and youtube-brand.svg assets and their attribution comments. The company-only photography rule does not exclude these requested platform brand symbols.

- Increment the shared VERSION before changing cached shared assets, and regenerate all affected pages. Keep HTML revalidation and versioned static-asset caching so remote updates appear on refresh.
