# Approved architectural redesign — 30 October 2026

The owner reiterated that all three designs were already approved and explicitly instructed implementation without another approval request. This release replaces the earlier modest blue refresh with a visibly different architectural interface.

- inonda.site: a light blueprint editorial layout, split property viewport and interactive model/layers/plan schematic.
- inonda.org: a dark material studio, angular project framing and a working maintenance/repairs/renovation service viewer using existing company images.
- inonda.homes: a midnight planning hero, architectural schematic, workflow dock, bright instrument panels and a dark live budget card.

The schematic is explicitly labelled an architectural illustration; it is not a scanned customer property or live property monitoring. No fabricated figures, reviews, availability or project outcomes were added. All original written content, official logos, media files, contact links, social profiles, search metadata and calculator source remain preserved.

New files: tools/inonda_future.py, tools/future-design.css and tools/future-ui.js. Their public copies are generated into public/assets or dist. The shared network generator calls enhance_future, preserving the design during future rebuilds, including the inonda.org build. Shared release and design asset URLs use version 20261030-2. Both estimator host copies add only the two read-only design asset routes; existing access and security headers remain unchanged.

Validation:
- All 18 homepage language variants inspected at a 390px iframe width (375px content); each scrollWidth equalled clientWidth.
- Hebrew retained RTL and translated model controls.
- Mobile menu opened and closed.
- Model controls changed the visible architectural layers.
- Renovation tabs changed the original image and corresponding service destination.
- Estimator example remained €345–€525; changing reserve to 10% produced €380–€575, then controls were restored.
- The release guard compares every changed HTML file to main after stripping only design inclusion tags and version parameters. It rejects unexpected content, metadata, logo or calculator-source changes.
- Original media in local previews loaded from their published company domains when unchanged media files were not present locally.

Production deployment and final domain checks are recorded in the PR after merging. Browser caching may retain previous HTML on static hosts; release asset versions and the actual live DOM are the verification signals.
