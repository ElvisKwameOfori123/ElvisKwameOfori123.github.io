## Purpose

This is a review-only rewrite of the existing EKO Perspectives prose, based on the supplied rewrite patch but **not applied verbatim**.

The six published posts had converged on one recurring architecture: reflective opener, sourced fact, explanatory visual, caution, then a narrower-question ending. This PR keeps the useful structural rewrite from the supplied patch while revising the parts that were too absolute and updating the editorial rules so the rewrite does not simply create a new fixed house template.

## What changes

- Reworks all six published posts so they use different structural engines and do not repeat the same opening/ending moves.
- Restructures **How I got here** into continuous prose while keeping only details already public. No new private-life facts, names, scholarship names or scenes were invented.
- Tightens **About** without automatically adding an AI-assistance disclosure.
- Adds plain-language openings to the public project pages and makes the project index more reader-first.
- Relabels the pre-PhD paper list on Research as **Earlier publications** and notes that doctoral working papers will be added as they become public.
- Tightens README wording.
- Updates `AGENTS.md`, the canonical editorial workflow and Copilot instructions so structure follows the subject rather than a fixed EKO template.
- Adds `.editorial/EKO_ENGINE_LIBRARY.md`, an adaptive menu of article engines and planning tests.
- Adds `.editorial/EKO_TOPIC_BACKLOG.md`, a non-binding twelve-topic idea bank with a possible first-three-month sequence. Every topic still requires current evidence checks and owner approval before drafting.

## Three opinion passages revised before this PR

The supplied patch contained three claims that were stronger than the evidence warranted. They have been revised here:

1. **ACRES:** now argues for beginning at the scale of the environmental process where outcomes depend on flows/connectivity, rather than saying all such problems must be contracted at landscape scale from the start.
2. **AI:** now says time/access exposure measures are limited when they omit how the tool was used; it no longer says such studies deserve categorically little weight.
3. **Wildfire:** now treats land management and emergency response as complementary parts of one risk-management system rather than setting them against each other.

## Hidden prompts and disclosure

- All hidden `EKO:` drafting prompts from the supplied patch were deleted, not left in public source.
- No AI-assistance disclosure sentence was added automatically. That remains a deliberate editorial-standards decision for the owner.

## Author review still requested

Please specifically review:

- the revised ACRES, AI and Wildfire judgment paragraphs;
- the `National Petroleum Authority -> Resources Policy` framing in **How I got here**;
- the tightened one-sentence description of the PhD question on **About**;
- the overall shortening/restructuring of **How I got here**.

## Editorial workflow update

The workflow now makes explicit that:

- first person is optional, not mandatory;
- caution is not the default ending;
- a clear position is allowed when evidence supports it proportionately;
- recent posts must be checked for repeated house phrases and structural arcs;
- magazine-style scene openings require actual reporting, archival evidence or first-hand observation;
- People behind the science research architecture is a checklist, not a visible article template;
- the article-engine library is a menu, not a mandatory sequence;
- the topic backlog is planning support only and never authorises drafting by itself.

## Safeguards

- Existing sources, article URLs, dates, images and image metadata are preserved.
- No hidden personal prompts remain.
- No production merge is requested by this PR.
- Published-content edits remain review-only until Elvis Kwame Ofori explicitly approves them.

## Review checklist

- [x] Quarto render passed on the rewrite content.
- [x] Rendered-link check passed on the rewrite content.
- [x] No accidental private drafting prompts remain.
- [x] Desktop and phone rendering checked for all six posts, How I got here, About and Research.
- [x] Article-engine library and topic backlog added and linked from repository instructions.
- [ ] Final owner approval of the revised first-person positions and personal-page framing.

Publication requires explicit approval from Elvis Kwame Ofori. This PR should remain draft until that review is complete.
