# Sourcing and routing

## Route from the claim

| Narration pattern | Preferred route | What earns the cut |
|---|---|---|
| “People are saying,” current controversy, complaint | Receipt | Current primary post, headline, review, or search result |
| Number, price, usage, growth, decline | Receipt | The actual pricing page, dashboard, report, chart, or metric |
| Named person | Entity | The person doing or saying the thing in context, or their work |
| Company or product | Product | Current official interface, demonstration, launch, or milestone |
| Research or direct quotation | Receipt | Original paper, author, interview, or authentic publication |
| Place, era, physical event | Archival/entity | Recognizable canonical footage with provenance |
| Process, mental model, invisible system | Concept | On-brand diagram or motion graphic |
| Reaction or punchline | Cultural | A user-curated clip chosen for taste |

Ask “what is this line actually claiming?” before searching. “X from Company made the account popular” is about X's work and the account, not the company logo. “Research shows” calls for the research, not generic laboratory footage.

## Authority order

Prefer:

1. user-owned recordings and assets;
2. original posts, papers, records, and product pages;
3. official entity channels and reputable archives;
4. reputable reporting that directly documents the claim;
5. clearly licensed stock when literal or evocative footage is appropriate.

Flag open-web results outside those lanes. Availability is not permission to republish. Record the license, terms, attribution expectation, or fair-use rationale as a note for the human editor; never manufacture a legal conclusion.

## Efficient search

- Search or inspect metadata before downloading media.
- Scope video search to official channels when possible.
- Search people by `person + claim/action/event`, not bare name.
- Prefer recent sources for current products and claims.
- Capture a source once and derive multiple crops or intervals locally.
- Batch metadata requests, downloads, and page captures by source.
- Cache approved raw assets inside the project, outside the skill repository.
- Stop after one method fails and try a materially different route. After a second failure, drop or flag the beat rather than looping.

## Tool routing and fallbacks

Adapted from the MIT-licensed [Agent Reach](https://github.com/Panniantong/Agent-Reach) routing model:

- **Check the tools first.** Before searching, confirm which tools answer in this session (web search, page reader, browser, `yt-dlp`, Content Lab MCP). Report a missing tool once, by name, with the next step; do not discover it beat by beat.
- **Route by source, not by habit.** Pick the tool from the link or the source type: official site or press page → page reader; YouTube trailer or clip → `yt-dlp` metadata and subtitles; forum or social reaction → search, then the page itself.
- **Ordered fallbacks.** Each route has a preferred tool and one or two alternatives, for example page reader → browser → web search snippet. Move to the next tool only when one fails, and record which one produced the asset.
- **Find the moment by subtitles.** For a trailer or official clip, read the subtitles or transcript with timestamps first and cut only the interval where the line or action happens. Download only that clip, never the whole video when an interval is enough.
- **Read-only, no borrowed logins.** Research reads and downloads; it never posts, comments, likes, or messages. Use only public pages or sessions the user already opened in their own browser. Never ask for a password, never copy cookies from the main account, and treat login-gated platforms as optional.
- **Report failures as source, cause, next step.** Example: "YouTube: video unavailable in the region — try the studio's official site."

Useful authorized tools include browser automation for public pages, `yt-dlp` for permitted metadata/downloads, FFprobe for the real media payload, and the adjacent video workbench for contact sheets and stills.

## Candidate score

Score 1–5:

- source authority;
- exact relevance to the interpreted claim;
- recency fit;
- immediate recognizability;
- format fitness: legible, silent-able, crop-safe, sufficient resolution;
- rights clarity.

Reject a candidate with weak authority or relevance even if the aggregate score is high. Motion wins ties only when reading the original artifact is not the point.

## Cadence

Use genre and intent to set density:

- interview or webinar: light punctuation around references and claims;
- opinion or explainer: selective receipt and concept bursts;
- story or list: moderate people, product, place, and archival coverage;
- evidence-heavy critique: receipt-dominant, while leaving enough face time for trust.

Let a single strong asset breathe. Avoid sub-second shots except inside one deliberate montage. Adjacent cutaways should connect directly when a one-frame or split-second talking-head flash would read as an error.
