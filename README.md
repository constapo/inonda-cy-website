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
  `tiling`, `carpentry`, `handyman`, `emergency`, `maintenance`. They are converted to WebP automatically,
  and `hero` also becomes the social-share image. Until a photo exists the slot shows a drawn icon.
- Hero video: put `hero.mp4` (1080p, 8–15 s, muted, ideally under 6 MB) and optionally `hero-sm.mp4`
  (720p, for phones) in `public/assets/video/`, then rebuild. Until then the hero shows the animated blueprint,
  or a photo slideshow once photos exist.

## Publishing

Push to `main`; Wasmer deploys automatically.
