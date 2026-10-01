# EKO Editorial Workflow v2.2

**Standing version: 1 October 2026.**

This is the repository-level canonical instruction for EKO Perspectives. If the installable `eko-editorial-workflow` skill is available in the current environment, use it and its reference files. If it is not available, follow this document directly. This file supersedes the older separate `pre2015-prose-voice` and `ai-slop-editing-pass` chain.

This workflow is a working editorial system, not a fixed prose template. If a rule repeatedly produces sameness, evasive caution, or artificial writing, revise the rule rather than forcing new work back into the old pattern. The safeguards around evidence, sourcing, privacy, images and publication remain firm; the prose architecture should remain responsive to the subject.

## Pipeline

1. **Site preflight.** Inspect recent published posts and current drafts before researching. Check whether the subject or angle has already been used, whether recent pieces share the same opening, structural engine, transition phrases or ending, and what this piece would genuinely add.
2. **Evidence and originality.** Research before drafting. Prefer primary sources, then institutional records, then reputable reporting for context. If sources disagree, carry the disagreement into the prose rather than silently resolving it. Ask what the article contributes beyond obvious existing coverage.
3. **Route by content type.** Apply the appropriate research checks for policy/evidence, GitHub/tool, scientist profile, map/data, place/development, or personal/ideas.
4. **Choose the register and the article engine.** Use blog voice for most research, policy, methods, GitHub, evidence and personal intellectual posts. Use magazine voice for profiles, narrative explainers, places and pieces organised around reported scenes or chronology. Before drafting, decide what actually drives this particular piece: an argument, mechanism, disagreement, number, document, modelling episode, observation, place, person or other genuine centre of gravity.
5. **Draft to the subject.** Do not import the opening, paragraph architecture or closing move from the previous EKO post. First person is available but not mandatory. A piece may take a clear position when the evidence supports one, but the strength of the claim must match the evidence.
6. **Final mechanical edit.** Run one anti-slop pass after the draft is complete. It removes formulaic habits without changing the argument, evidence, structure or chosen register.
7. **Image sourcing, if needed.** Use images that do real editorial work. Check licence or reuse basis, store files locally, write real alt text, and avoid decorative stock imagery.
8. **SEO and discovery packaging.** Only after the article exists, prepare title, slug, description, internal links, image metadata, structured data and dates. SEO never dictates the prose.
9. **Publication gate.** Confirm site rules, factual integrity, metadata, links, categories, `draft: true`, and rendered desktop/phone quality. Publication requires explicit approval.

A profile adds a conditional substage after content routing: read several sources, seek independent evidence beyond an institutional biography, distinguish relevant biography from intrusive private detail, and never clone the architecture of one older profile.

## Site preflight

Before writing, scan recent posts and drafts. A follow-up on the same subject is allowed only when the angle is genuinely different. Note potentially useful internal links, but decide whether to insert them only after the new draft exists.

Also scan for repeated house habits. Look for reused openings such as reflective first-person throat-clearing, recurring pivots such as "the more interesting question" or "there is another reason for caution," and endings that repeatedly narrow the argument into a question. Repetition across a body of work matters even when each sentence is individually competent.

## Evidence and claim ledger

For substantive factual claims, keep a compact internal claim ledger with the source, date and whether it is primary or secondary.

For this site's Quarto build, a sibling `_sources.md` is excluded from rendering, while a bare `sources.md` can become its own HTML page and `.llms.md` output. **Build exclusion is not privacy.** The website repository is public. Confidential material, unpublished research results, farm-level data, private interview notes, personal prompts, or anything else that should not be visible in GitHub must stay outside the repository entirely.

## Content-type checks

### Policy / evidence
Establish jurisdiction, current status with an as-of date, and the difference between a policy's stated objective and observed or expected effects. A policy piece may reach a judgment, but avoid converting a contingent result into a universal rule.

### GitHub / tool
Inspect the repository itself, not only its README. Check licence, environment/version requirements, recent activity, the problem the architecture solves, limitations, and whether the approach transfers to another modelling problem.

### Scientist / researcher profile
Use independent evidence beyond the subject's own institution or public statements where possible. Current roles and titles must be checked. Do not include private-life detail unless it materially explains the public story and is responsibly sourced.

### Map / data
Identify the source dataset, spatial resolution, temporal coverage/date, scale, and what the visualisation cannot show.

### Place / development
Distinguish first-hand observation from sourced claims. When comparing places, apply comparable evidence standards to both.

### Personal / ideas
This is the lightest route, but factual claims still require evidence. Do not invent biographical detail to make the prose more vivid.

## Blog voice

The default register resembles strong pre-2015 research and policy blogging without imitating any single writer.

- Start where the interesting thought starts, not with a formal introduction.
- First person is optional. Use it when the writer's experience, judgment, method, uncertainty or observation contributes something real. Do not add "I" merely to make sourced analysis sound personal.
- Let the subject determine the engine of the piece. One post may be built around a number, another around a disagreement, another around a mechanism, a document, a modelling problem or a position that needs defending.
- Allow explicit uncertainty and useful digressions when they belong to the thought. Do not make caution the default rhetorical destination.
- When evidence supports a position, state it proportionately and show the assumptions or limits that matter. Do not retreat automatically into "the answer is complicated" or a narrower question.
- The paragraph is the unit of thought. Vary paragraph length because the ideas require it, not to simulate human irregularity.
- Use headings only when the subject genuinely turns.
- Link evidence inline at the point it enters the discussion.
- Do not impose numbered takeaways when the material does not naturally have them.
- End where the thought actually lands. That may be a conclusion, implication, unresolved problem, return to an object or place, or simply the end of the argument. Do not manufacture a summary conclusion, a cautionary ending or a rhetorical question because earlier EKO posts used one.

## Magazine voice

Use for profiles and narrative explainers when the material genuinely supports narrative treatment.

- Open on a real, documented scene, person, moment, document, dataset, object or figure.
- Use a reported scene only when there is reporting, archival evidence or first-hand observation to support it. Do not manufacture scene-setting for analytical or opinion pieces.
- Never invent a scene, quote, person or incident.
- Follow with a restrained nut graf when useful.
- Develop by chronology, theme, people, place and evidence rather than mechanical headings.
- Quote when the speaker's wording adds something a paraphrase would lose.
- A governing angle is good, but material counterevidence and genuine disagreement must be represented fairly.
- Do not clone one specific older article's paragraph structure or wording. Study shared craft across several examples instead.
- For People behind the science, treat any behind-the-scenes architecture as a research checklist, not a visible template. Person, question, place, collaborators, mechanism and consequences matter only in the proportions the specific story earns.

## Final editing pass

Run once, after drafting. Check for:

- "In today's fast-paced..." and similar canned openings.
- "It's not just X, it's Y" constructions.
- "Moreover," "Furthermore," and "Additionally," used mechanically as paragraph openers.
- "Let's dive in," "Let's explore," "At the end of the day," "A testament to," and routine "It's worth noting" phrasing.
- Redundant tricolons and stacked hedges.
- Rhetorical-question openings used as a crutch.
- Equal-sized paragraphs or identical section shapes.
- Repeated EKO house phrases across recent posts, including habitual uses of "interesting," "obvious," "familiar problem," "another reason for caution," or "the more useful question," when they are doing structural rather than substantive work.
- Repeated article arcs across recent posts, especially reflective opener -> evidence -> caution -> narrower question.
- First-person framing that never supplies a genuine observation, experience, method, judgment or reason the writer belongs in the sentence.
- Closing paragraphs that merely restate the opening.
- Endings that turn every argument into another question instead of saying what the evidence supports.
- Headings or bullets imposed on prose that should flow.
- Routine "Further reading" endings.
- Em dashes, which are prohibited on this site.
- Mechanical semicolons, excessive scare quotes, manufactured excitement, false modesty, vague inspirational endings and evasive over-hedging.

Do not solve uniformity by manufacturing irregularity. Do not force fragments, alternating sentence lengths, artificial hedges or performative certainty merely to look human. The goal is not randomness. It is prose whose form follows what is being said.

## Images

Every published post must have at least one relevant lead image. A second supporting image is recommended when it materially improves understanding, but never add decorative filler just to reach a count.

Prefer a real or documentary lead image when a strong, truthful and clearly reusable image exists, especially for stories about people, places, landscapes, institutions or events. Use an original explanatory visual as the lead when the subject is abstract or when available photography would be generic or misleading. Schematics often work best as supporting visuals inside the article rather than replacing documentary imagery at the top. Avoid generic stock imagery standing in for the topic.

Check licence, permission, or another clear reuse basis. A public webpage does not make every screenshot automatically reusable. Host every image locally in the post folder. Never hotlink.

Compress efficiently, but do not enforce a rigid 200 KB ceiling when that would visibly damage a representative high-resolution image. Treat roughly 200 KB as a review heuristic, not a failure threshold.

Every image needs descriptive alt text. Add a caption where context is useful, and always add full attribution and licence information when reuse terms require it. The lead image should also be represented in post metadata so the Writing archive and social/discovery surfaces can use it consistently.

## SEO and discovery

SEO is a packaging layer, never the writing brief.

### Freshness
Platform-specific guidance ages quickly. Re-check current primary documentation when a platform rule materially affects publication, or when stored guidance is more than roughly six months old.

### Titles and slugs
Derive them from the finished article. The H1 and page title should make substantially the same promise. Avoid keyword strings and boilerplate.

### Meta descriptions
Google has no fixed character limit; displayed snippets vary with rendered width, device and query. Roughly 150 to 160 characters can be a useful editorial approximation when a complete natural description fits, but it is not a ranking rule or a target to pad or cut prose around.

### Internal links
Add only genuinely helpful links to earlier EKO posts. Use descriptive anchor text, not "click here" or "read more."

### Structured data
Use accurate `Article` or `BlogPosting` data that matches the visible page, including headline, image where appropriate, publication/modification dates and author identity. Use specialist SEO tooling when available, but discover the current capability rather than hard-coding one plugin name.

### Dates
Show publication date. Change `dateModified` only for meaningful factual or substantive updates, not cosmetic changes.

### AI-search and GEO rituals
Do not artificially chunk prose, add generic FAQ blocks for visibility, rewrite sentences for AI parsing, or add redundant structured data for AI systems.

The site already generates `llms.txt` and per-page `.llms.md`. Current Google guidance says these do not improve Google Search or Google's generative-AI features. Keep them because they are generated automatically at no editorial cost, but do not treat them as a Google SEO lever and do not claim a named third-party product uses them without current primary-source evidence.

Preferred Sources is a site-level item to revisit during maintenance rather than a per-post writing task.

## Publication gate

Before a draft is considered ready for review:

- `draft: true` remains set for new posts.
- Do not alter already-published posts unless explicitly requested.
- No em dashes in original site prose. Preserve exact punctuation when quoting or reproducing an official title where changing it would make the citation inaccurate.
- Use only the six established categories: Policy; Land & Agriculture; Economics & Evidence; Science & Technology; Places & Development; Personal & Ideas.
- Sources are linked inline where they enter the prose.
- No routine Further Reading section.
- No confidential, unpublished or farm-level material.
- No hidden personal prompts or private drafting notes are left in public repository source.
- Check names, figures, dates, quotations, links, repository versions, policy status and other time-sensitive claims.
- Confirm that stated opinions are genuinely approved as the author's position and are no stronger than the evidence can support.
- Confirm the post has at least one relevant lead image, stored locally, with descriptive alt text and any required caption, credit and licence.
- Check title, description, slug, image metadata, dates and relevant structured data.
- Render the page and inspect both desktop and phone layouts, including title wrapping, hero crop, tables, code, captions, links, overflow, navigation and reading width.
- Keep the result private for owner review. Publication requires explicit approval.

## Site-health audit

Run periodically or after template/style changes, not for every article.

Use specialist technical-SEO tooling when available, but discover capabilities rather than depending on hard-coded tool names. Check technical crawlability, broken links, internal linking, schema, canonicals, sitemap, robots directives, mobile rendering, page weight and discovery metadata. Do not use keyword-clustering or content-brief systems to decide what EKO Perspectives should publish.

The editorial model is originality-first: choose what is worth saying, then make it discoverable.
