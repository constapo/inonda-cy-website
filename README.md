# inonda.org

Website of Inonda LTD: maintenance, repairs and home transformation in Nicosia and across Cyprus.
6 languages (el, en, ru, uk, he, ro). Replies and quotes are in Greek, English, Russian and Romanian;
the Ukrainian and Hebrew pages present the company and say so.

## How it is built

The pages in `public/` are generated. Do not edit them by hand: edit the content and rebuild.

| Path | What it is |
|------|------------|
| `build/content/<lang>.py` | All text for one language |
| `build/gen.py` | Page templates, phone numbers, team, services list |
| `build/check_content.py` | Checks every language has the same structure as English |
| `build/source-images/` | Drop photos here (see below) |
| `public/` | The finished website that is published |
| `public/assets/site.css`, `site.js` | Design and behaviour |
| `settings/config.toml`, `Staticfile` | Web server settings for Wasmer |

Rebuild after any change:

```bash
python3 build/check_content.py && python3 build/gen.py
```

## Photos and video

- Photos: save a JPG or PNG in `build/source-images/` named after its slot, then rebuild.
  Slots: `hero`, `kitchen`, `bathroom`, `plumbing`, `electrical`, `roof`, `painting`, `outdoor`, `ac`,
  `tiling`, `carpentry`, `handyman`, `emergency`, `maintenance`, `renovation`. They are converted to WebP automatically,
  and `hero` also becomes the social-share image. Until a photo exists the slot shows a drawn icon.
- Hero video: put `hero.mp4` (1080p, 8–15 s, muted, ideally under 6 MB) and optionally `hero-sm.mp4`
  (720p, for phones) in `public/assets/video/`, then rebuild. Until then the hero shows the animated blueprint,
  or a photo slideshow once photos exist.

## Publishing

Push to `main`; Wasmer deploys automatically.


## Connected INONDA websites

All public language pages now include shared navigation and a three-website chooser.

- https://www.inonda.site: property management and owner support.
- https://www.inonda.org: maintenance, repairs and renovation scope.
- https://www.inonda.homes: configurable planning estimates, including 19% VAT.

The visitor’s language is preserved. Relevant service pages link to selected calculator services; regional pages can preselect their named area. No personal details, visitor notes or saved estimates are synchronized between domains. Specialist work still requires an assessment.

To update shared wording, edit tools/network-copy.json in all three repositories, keep tools/inonda_network.py synchronized, then run:

```bash
python tools/inonda_network.py org
```

Commit the tools, versioned CSS/JS and changed HTML pages together. The inonda.org build generator also applies the component automatically. Keep each site’s canonical URLs and existing content.

## Shared chatbot and contact icons

The same automated INONDA service and request guide is installed on all three websites. Source: tools/inonda_chat.js, tools/inonda_chat.css, tools/chat-copy.json and tools/chat-ui.json. Keep these copies synchronized alongside the network generator. It supports six languages, service combinations, referrals and a guided request draft. On inonda.homes it can explain the actual current budget. Visitor messages stay in page memory; no AI service or shared conversation database is configured.

Visitors review a request before opening a WhatsApp or email draft. Viber buttons open the selected person’s chat; the visitor can copy their visible request. No message is sent automatically. Original communication icons are self-hosted; see BRAND-ASSETS.md.

Company footer social profiles are in tools/social-links.json. Facebook and Instagram use the owner’s previously supplied company URLs. TikTok uses the confirmed company profile @inonda26; YouTube uses @InondaLTD. Preserve these exact company channels. Keep the configuration synchronized across all three repositories. LinkedIn is excluded by the owner.

Shared asset changes require incrementing VERSION in tools/inonda_network.py before regenerating. HTML now revalidates on refresh; versioned assets remain cached for performance.
