# EKO Editorial Workflow v2.2

**Standing version: 24 September 2026.**

This is the repository-level canonical instruction for EKO Perspectives. If the installable `eko-editorial-workflow` skill is available in the current environment, use it and its reference files. If it is not available, follow this document directly. This file supersedes the older separate `pre2015-prose-voice` and `ai-slop-editing-pass` chain.

## Weekly editorial planning and human approval

Do not begin a new post simply because a daily slot exists. At the start of each editorial week, prepare a proposed weekly slate before drafting. The slate should normally contain up to three candidate topics for each relevant day, but fewer is preferable when the ideas are weak, repetitive, poorly sourced, or too close to recent coverage.

For each proposed topic, give Elvis enough information to make an editorial decision before prose is written: the working title or question, the strand/category, why it is worth doing now, the likely primary or high-quality evidence base, the intended angle, and any obvious duplication, sourcing, sensitivity, or image-rights issue. For scientist/researcher profiles, also identify the person, why the career is worth profiling, and whether sufficiently independent biographical and scientific sources appear to exist.

**Human topic approval is a hard gate.** Do not draft a new article until Elvis has explicitly approved that topic or theme. Approval of the weekly slate may cover several named topics at once. Silence, an earlier rotation schedule, or the existence of an empty daily slot is not approval. If Elvis rejects or changes a topic, research and drafting must follow the revised choice.

After approval, run the normal site preflight again immediately before research and drafting, because recent posts or drafts may have changed since the weekly slate was prepared. The daily rotation is an editorial menu, not a quota. Never create filler merely to satisfy it.

## Pipeline

1. **Site preflight.** Inspect recent published posts and current drafts before researching. Check whether the subject or angle has already been used, whether recent pieces share the same opening or structure, and what this piece would genuinely add.
2. **Evidence and originality.** Research before drafting. Prefer primary sources, then institutional records, then reputable reporting for context. If sources disagree, carry the disagreement into the prose rather than silently resolving it. Ask what the article contributes beyond obvious existing coverage.
3. **Route by content type.** Apply the appropriate research checks for policy/evidence, GitHub/tool, scientist profile, map/data, place/development, or personal/ideas.
4. **Choose the register and draft.** Use blog voice for most research, policy, methods, GitHub, evidence, and personal intellectual posts. Use magazine voice for profiles, narrative explainers, places, and pieces organised around reported scenes or chronology.
5. **Final mechanical edit.** Run one anti-slop pass after the draft is complete. It removes formulaic AI habits without changing the argument, evidence, structure, or chosen register.
6. **Image sourcing, if needed.** Use images that do real editorial work. Check licence or reuse basis, store files locally, write real alt text, and avoid decorative stock imagery.
7. **SEO and discovery packaging.** Only after the article exists, prepare title, slug, description, internal links, image metadata, structured data, and dates. SEO never dictates the prose.
8. **Publication gate.** Confirm site rules, factual integrity, metadata, links, categories, `draft: true`, and rendered desktop/phone quality. Publication requires explicit approval.

A profile adds a conditional substage after content routing: read several sources, seek independent evidence beyond an institutional biography, distinguish relevant biography from intrusive private detail, and never clone the architecture of one older profile.

## Site preflight

Before writing, scan recent posts and drafts. A follow-up on the same subject is allowed only when the angle is genuinely different. Note potentially useful internal links, but decide whether to insert them only after the new draft exists.

## Evidence and claim ledger

For substantive factual claims, keep a compact internal claim ledger with the source, date, and whether it is primary or secondary.

For this site's Quarto build, a sibling `_sources.md` is excluded from rendering, while a bare `sources.md` can become its own HTML page and `.llms.md` output. **Build exclusion is not privacy.** The website repository is public. Confidential material, unpublished research results, farm-level data, private interview notes, or anything else that should not be visible in GitHub must stay outside the repository entirely.

## Content-type checks

### Policy / evidence
Establish jurisdiction, current status with an as-of date, and the difference between a policy's stated objective and observed or expected effects.

### GitHub / tool
Inspect the repository itself, not only its README. Check licence, environment/version requirements, recent activity, the problem the architecture solves, limitations, and whether the approach transfers to another modelling problem.

### Scientist / researcher profile
Use independent evidence beyond the subject's own institution or public statements where possible. Current roles and titles must be checked. Do not include private-life detail unless it materially explains the public story and is responsibly sourced.

### Map / data
Identify the source dataset, spatial resolution, temporal coverage/date, scale, and what the visualisation cannot show.

### Place / development
Distinguish first-hand observation from sourced claims. When comparing places, apply comparable evidence standards to both.

### Personal / ideas
This is the lightest route, but factual claims still require evidence.

## Blog voice

The default register resembles strong pre-2015 research and policy blogging without imitating any single writer.

- Start where the interesting thought starts, not with a formal introduction.
- First person is natural.
- Allow explicit uncertainty and useful digressions.
- The paragraph is the unit of thought.
- Use headings only when the subject genuinely turns.
- Link evidence inline at the point it enters the discussion.
- Do not impose numbered takeaways when the material does not naturally have them.
- Stop when the thought is finished. Do not manufacture a summary conclusion.

## Magazine voice

Use for profiles and narrative explainers.

- Open on a real, documented scene, person, moment, document, dataset, or figure.
- Never invent a scene, quote, person, or incident.
- Follow with a restrained nut graf when useful.
- Develop by chronology, theme, people, place, and evidence rather than mechanical headings.
- Quote when the speaker's wording adds something a paraphrase would lose.
- A governing angle is good, but material counterevidence and genuine disagreement must be represented fairly.
- Do not clone one specific older article's paragraph structure or wording. Study shared craft across several examples instead.

## Final editing pass

Run once, after drafting. Check for:

- "In today's fast-paced..." and similar canned openings.
- "It's not just X, it's Y" constructions.
- "Moreover," "Furthermore," and "Additionally," used mechanically as paragraph openers.
- "Let's dive in," "Let's explore," "At the end of the day," "A testament to," and routine "It's worth noting" phrasing.
- Redundant tricolons and stacked hedges.
- Rhetorical-question openings used as a crutch.
- Equal-sized paragraphs or identical section shapes.
- Closing paragraphs that merely restate the opening.
- Headings or bullets imposed on prose that should flow.
- Routine "Further reading" endings.
- Em dashes, which are prohibited on this site.
- Mechanical semicolons, excessive scare quotes, manufactured excitement, false modesty, vague inspirational endings, and evasive over-hedging.

Do not solve uniformity by manufacturing irregularity. Do not force fragments, alternating sentence lengths, or artificial hedges merely to look human.

## Images

Prefer screenshots, charts, documents, maps, or photos that are genuinely part of the subject. Check licence, permission, or another clear reuse basis. A public webpage does not make every screenshot automatically reusable.

Host images locally. Compress efficiently, but do not enforce a rigid 200 KB ceiling when that would visibly damage a representative high-resolution image. Treat roughly 200 KB as a review heuristic, not a failure threshold.

Use descriptive alt text. Add captions where context or attribution requires them.

## SEO and discovery

SEO is a packaging layer, never the writing brief.

### Freshness
Platform-specific guidance ages quickly. Re-check current primary documentation when a platform rule materially affects publication, or when stored guidance is more than roughly six months old.

### Titles and slugs
Derive them from the finished article. The H1 and page title should make substantially the same promise. Avoid keyword strings and boilerplate.

### Meta descriptions
Google has no fixed character limit; displayed snippets vary with rendered width, device, and query. Roughly 150 to 160 characters can be a useful editorial approximation when a complete natural description fits, but it is not a ranking rule or a target to pad or cut prose around.

### Internal links
Add only genuinely helpful links to earlier EKO posts. Use descriptive anchor text, not "click here" or "read more."

### Structured data
Use accurate `Article` or `BlogPosting` data that matches the visible page, including headline, image where appropriate, publication/modification dates, and author identity. Use specialist SEO tooling when available, but discover the current capability rather than hard-coding one plugin name.

### Dates
Show publication date. Change `dateModified` only for meaningful factual or substantive updates, not cosmetic changes.

### AI-search and GEO rituals
Do not artificially chunk prose, add generic FAQ blocks for visibility, rewrite sentences for AI parsing, or add redundant structured data for AI systems.

The site already generates `llms.txt` and per-page `.llms.md`. Current Google guidance says these do not improve Google Search or Google's generative-AI features. Keep them because they are generated automatically at no editorial cost, but do not treat them as a Google SEO lever and do not claim a named third-party product uses them without current primary-source evidence.

Preferred Sources is a site-level item to revisit during maintenance rather than a per-post writing task.

## Publication gate

Before a draft is considered ready for review:

- `draft: true` remains set.
- Do not alter already-published posts unless explicitly requested.
- No em dashes.
- Use only the six established categories: Policy; Land & Agriculture; Economics & Evidence; Science & Technology; Places & Development; Personal & Ideas.
- Sources are linked inline where they enter the prose.
- No routine Further Reading section.
- No confidential, unpublished, or farm-level material.
- Check names, figures, dates, quotations, links, repository versions, policy status, and other time-sensitive claims.
- Check title, description, slug, image metadata, dates, and relevant structured data.
- Render the page and inspect both desktop and phone layouts, including title wrapping, hero crop, tables, code, captions, links, overflow, navigation, and reading width.
- Keep the result private for owner review. Publication requires explicit approval.

## Site-health audit

Run periodically or after template/style changes, not for every article.

Use specialist technical-SEO tooling when available, but discover capabilities rather than depending on hard-coded tool names. Check technical crawlability, broken links, internal linking, schema, canonicals, sitemap, robots directives, mobile rendering, page weight, and discovery metadata. Do not use keyword-clustering or content-brief systems to decide what EKO Perspectives should publish.

The editorial model is originality-first: choose what is worth saying, then make it discoverable.
