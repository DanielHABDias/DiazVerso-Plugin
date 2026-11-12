---
name: find-broll
description: "Find, vet and place scenes, receipts and B-roll from the works being discussed, timed to the spoken words, with source and rights recorded. Use when a beat needs media of a film, comic, series or claim."
---

# Find B-roll

Source cutaways that illustrate what the speaker means, not merely the nearest noun. Prefer a small number of accurate, authoritative assets over broad stock search or decorative coverage.

In Diazverso, media comes into the Content Lab with confirmed rights (`media_import_files`) and the render is checked with `motion_preview`, `render_start` and real frames ([Content Lab](../diazverso-contentlab/SKILL.md)).

## Establish the contract

Inspect the real source before planning. Accept a transcript, a word-timestamp transcript, or local video/audio. If only media is supplied, transcribe once with word timestamps and preserve the raw output.

Capture only preferences that materially change sourcing:

- delivery aspect ratio and duration;
- desired coverage density and whether the hook is denser than the body;
- allowed source types and any explicit bans;
- whether clip audio is stripped or intentionally mixed;
- source-credit preference;
- existing brand tokens or Remotion project for concept graphics;
- any user-owned library, channels, or must-include assets.

User overrides apply immediately for the rest of the run. Do not infer licensing permission, brand ownership, or consent from availability.

## Plan before downloading

Read the whole transcript and state its thesis. Then create an annotated beat plan with:

1. stable beat ID;
2. exact narration and anchor word;
3. one-sentence interpretation of what the line means;
4. route: `receipt`, `entity`, `product`, `concept`, `archival`, or `cultural`;
5. proposed source type and why it is authoritative;
6. intended duration and output placement;
7. status: `planned`, `sourced`, `approved`, `placed`, or `dropped`.

Walk the full palette before dropping a meaningful beat, but never pad. A correct empty space is better than a wrong cutaway. Read [references/sourcing-and-routing.md](references/sourcing-and-routing.md) when choosing routes or search strategies.

Treat plan approval as authorization for read-only research and downloading public candidates. Ask separately before paid acquisition, publishing, signing in with new credentials, or sending anything externally.

## Source by authority

Cluster the approved beats by source so each page, channel, or film is fetched once. Search metadata first; download only likely winners.

- **Receipts:** use the authentic post, headline, study, pricing page, review, or metric.
- **People and entities:** use the official or primary source and match the moment to the claim, not just the name.
- **Products and interfaces:** prefer the user's own current recording, then the official current demonstration.
- **Concepts:** create a restrained brand-consistent graphic, or use authoritative real footage when one exists.
- **Archival material:** prefer canonical archives with explicit provenance and usage terms.
- **Cultural or reaction clips:** use the user's curated library; do not blind-pick memes.

Inspect real search and metadata payloads before writing parsers or choosing formats. Record the canonical URL, creator, title, publication date, capture/download time, rights or usage note, and exact source interval. Reject watermarks, synthetic stock presented as real, burned-in captions that conflict with the edit, stale product interfaces, and sources whose provenance cannot be explained.

The agent may select one best candidate for an objective route when the evidence is unambiguous. Present choices for subjective or taste-sensitive routes, and preserve the user's final selection in the manifest.

## Place on meaning

Anchor a cutaway to the spoken word or phrase it illustrates, usually 0.2–0.5 seconds after the word begins. Never reveal the answer before the narration says it. Bias slightly late when timestamps are uncertain.

Keep source time and output time distinct. Strip external clip audio unless the edit explicitly calls for it. Use full-frame cover crop only when it preserves the subject; use a designed background for partial-frame or portrait material. Static receipts may remain still or use truly sub-pixel motion—never integer-stepped FFmpeg `zoompan`.

Write every approved choice to a project-local manifest before rendering. Read [references/manifest-and-timing.md](references/manifest-and-timing.md) for the fields and timing checks.

## Verify the render

Render a low-resolution candidate first (`motion_preview` in the Content Lab). Generate:

- a midpoint frame for every placed beat;
- a strip around every B-roll entrance and exit;
- a contact sheet covering the full sequence;
- a technical validation report for the final deliverable.

Inspect the actual images. Confirm the source is the intended one, the cut lands after the anchor, the subject survives the crop, no flash of talking head appears between adjacent cutaways, captions and overlays remain readable, audio continuity is intact, and every `approved` beat appears exactly once.

Deliver the master with the B-roll manifest, source list, approval state, review artifacts, validation report, and checksum. Never redistribute unused source media.

## Attribution

This workflow adapts the MIT-licensed [B-Roll Finder](https://github.com/louisedesadeleer/b-roll-finder) methodology by Louise De Sadeleer. Third-party media retains its own rights and terms.
