# EKO Editorial Workflow v2.3

**Standing version: 1 October 2026.**

This is the repository-level canonical instruction for EKO Perspectives. If the installable `eko-editorial-workflow` skill is available, use it and its reference files. If it is not available, follow this document plus `.editorial/story-engine-library.md` directly. For topic planning, also consult `.editorial/EKO_PERSPECTIVES_EDITORIAL_PLAN.md` as the standing topic bank and longer-horizon planning reference.

This version supersedes v2.2 and the former separate `pre2015-prose-voice` + `ai-slop-editing-pass` chain. If a planning-reference file contains an older or more rigid instruction, this workflow is authoritative.

The central change in v2.3 is simple: **editorial consistency must not become structural sameness**. Older E360 features, research blogs, academic op-eds, trade press, journal articles and classic essays are craft references, not moulds. There is no single E360 framework and no single pre-2015 blog framework.

## Pipeline

0. **Editorial planning and owner approval.** Build a short weekly slate or evaluate the explicitly proposed topic. Consult `.editorial/EKO_PERSPECTIVES_EDITORIAL_PLAN.md` for standing ideas and site priorities, but do not treat it as an automatic queue. Do not draft a newly proposed topic until Elvis approves the topic/theme, unless the current request already explicitly asks for that draft.
1. **Site preflight.** Inspect recent published posts and drafts. Check topic overlap, geographic/category gaps, repeated openings, repeated diagrams, repeated caution moves, and repeated endings.
2. **Evidence and originality.** Research before drafting. Prefer primary sources. Keep a claim ledger. Identify the strongest credible counterargument or rebuttal when the claim is contested.
3. **Route by content type.** Apply policy/evidence, GitHub/tool, scientist profile, map/data, place/development, personal/ideas, behind-the-paper/model, or policy-audit checks.
4. **Choose the story engine.** Choose only after the evidence is understood. Use `.editorial/story-engine-library.md`. The library is a menu, not a rotation rule.
5. **Choose the register and draft.** Use research/blog voice for most analytical pieces. Use magazine/reported-feature voice only when the evidence genuinely supports narrative, chronology, place, people or documented scenes.
6. **Final mechanical edit.** Run one anti-slop pass after the draft is structurally finished.
7. **Images.** Source images that do real editorial work, check reuse basis, store locally, write real alt text and avoid decorative filler.
8. **SEO and discovery packaging.** Only after the prose exists, prepare title, slug, description, internal links, image metadata, structured data and dates.
9. **Publication gate.** Confirm evidence, distinctiveness, site rules, metadata, links, categories, `draft: true`, and rendered desktop/phone quality. Publication requires explicit approval.

## Stage 0: editorial planning and approval

Plan topics rather than filling a posting quota. For each candidate, give only enough to decide: the subject/question, why it matters now, what EKO Perspectives can add beyond obvious coverage, likely route, provisional engine, and whether it needs first-hand reporting, personal modelling experience, public records or desk research.

Before proposing a slate, consult `.editorial/EKO_PERSPECTIVES_EDITORIAL_PLAN.md` for existing candidate topics, geographic gaps, site fixes and longer-horizon sequencing. Re-check current evidence, policy status, paper-publication status and recent site coverage before reusing any candidate. The plan is a source of possibilities, not a commitment to publish them in order.

Two to four candidates are enough for a normal weekly slate. Variety in geography, category and engine is useful, but do not manufacture variety for its own sake.

A quiet period is not a reason to publish several similar pieces at once. Consistency matters more than volume.

## Stage 1: site preflight

Before research deepens, scan recent posts and drafts.

Check:

- Has the same subject or argument already been used?
- What does this piece add beyond existing coverage?
- Have recent posts used the same opener, source base, diagram, caution paragraph or narrowing-question ending?
- Is first person necessary because Elvis actually did, observed, modelled, read, decided, experienced or believes something relevant?
- Has coverage become too narrow relative to the site's stated scope, including Ghana/Africa, the United States, Places & Development, or research-behind-the-paper work?

Watch for emerging house tics rather than only generic AI tics. Repeated scaffolding such as "I keep coming back to...", "I was reading...", "There is a familiar...", "There is another reason for caution...", habitual uses of "interesting" or "obvious", and conclusions that repeatedly turn into "the more useful question is..." should trigger review. These are not banned phrases; the problem is repetition doing structural work.

## Stage 2: evidence, rebuttal and claim ledger

### Source hierarchy

Prefer:

1. Primary sources: paper, repository, dataset, government document, transcript, original interview.
2. Institutional records: official statistics, agency reports, parliamentary records, court judgments, public consultations, official biographies.
3. Reputable reporting for context, timeline and colour when primary records do not settle the point.

If two sources disagree, carry the disagreement into the prose rather than silently choosing the cleaner number.

### Read against the claim

For a substantive argument, identify the strongest credible foil: a competing paper, rebuttal, agency interpretation, trade-body response, court finding, parliamentary objection or another source a knowledgeable critic would actually use.

Do not create a vague or weak opponent merely to make the piece look balanced. A strong claim should survive the strongest reasonable objection available.

### Find the deeper mechanism

Ask whether the visible controversy is actually driven by property/tenure, accounting boundaries, baselines, incentives, measurement, spatial scale, displacement, leakage, implementation capacity or another mechanism. Name it only when the evidence supports it.

### Public-record voices

Named voices can come from Dáil or parliamentary debates, court judgments, consultation submissions, agency records and other public documents. Attribute them accurately. Never imply that Elvis interviewed or personally observed someone when he did not.

### Claim ledger

Keep a compact private audit trail with the substantive claim, source, date and whether the source is primary or secondary. A sibling `_sources.md` can be excluded from Quarto rendering, but build exclusion is not privacy. Confidential material, farm-level data, unpublished research and private notes must stay outside the public repository entirely.

## Stage 3: content routes

### Policy / evidence

Establish jurisdiction, current status with an as-of date, stated objective, relevant outcome measure, and observed/expected effects. Distinguish a target from delivery.

### GitHub / tool

Inspect the repository itself, not only the README. Check licence, versions, recent activity, architecture, limitations and what transfers to another modelling problem.

### Scientist / researcher profile

Read several sources and seek independent evidence beyond an institutional biography. Distinguish relevant biography from intrusive private detail. Current roles and titles must be checked.

### Map / data

Identify the dataset, spatial resolution, temporal coverage/date, scale and what the visual cannot show.

### Place / development

Distinguish first-hand observation from sourced claims. Apply comparable evidence standards across places.

### Personal / ideas

This is the lightest route, but factual claims still require evidence.

### Behind the paper / behind the model

Identify the research decision, modelling difficulty, failed assumption, methodological trade-off or surprise that gives the post a reason to exist. Separate public results from unpublished work. Use first person for real research experience, not ornament.

### Policy audit / target-versus-delivery

State what was promised, targeted or claimed, establish the appropriate comparison period, test rather than assume success/failure, identify implementation constraints, and conclude with the degree to which the evidence supports the claim.

## Stage 4: story engine

Read `.editorial/story-engine-library.md`.

A story engine is the organising force of a piece, not a visible template. Possible families include:

- scene or place led;
- contradiction or foil led;
- claim testing or policy audit;
- debate diagnosis;
- behind the paper or behind the model;
- one number or one comparison;
- pattern assembly from public records;
- mechanism led;
- timeline or policy reversal;
- people or places behind the science.

Choose the engine from the evidence. A piece can combine engines if the combination is natural. Do not create a rule such as "never use the same engine twice in a row". Instead, notice repetition and decide whether the material earns it.

When studying older pieces, outline what the writer does, identify the evidence carrying the argument, and read a strong rebuttal where one exists. Study architecture across multiple pieces without copying distinctive wording or imitating one writer's voice.

## Stage 5: register and drafting

### Research/blog voice

Use for most research, policy, methods, data commentary, reactions to papers/documents and behind-the-paper pieces.

- Start where the real thought, result, disagreement, number, document or modelling problem begins.
- Do not force a reflective first-person opening.
- First person is welcome when it carries actual experience or judgment.
- Let paragraphs develop ideas rather than making every sentence a standalone aphorism.
- Use headings only when the subject genuinely turns.
- Link evidence inline where it enters the discussion.
- Explicit uncertainty is fine, but do not make caution the default ending.
- Clear conclusions are allowed. Represent counterevidence fairly, qualify where needed, then state what the evidence supports.
- Stop when the thought is finished. The ending may be a verdict, implication, unresolved tension, return to a number, or simply the end.

### Magazine / reported-feature voice

Use for profiles, narrative explainers, place pieces, historical stories and pieces genuinely organised around people, chronology or documented scenes.

A scene must be real: first-hand, directly reported, or responsibly reconstructed from documents. Never invent weather, dialogue, expressions, room details or sensory description to make desk research resemble field reporting. If no real scene exists, choose another engine.

There is no single E360 structure. Some strong features begin with place, some with contradiction, some with a debate, some with a figure or document, and some with a person confronting a problem.

For people/places behind the science, use the richer unit: person + question + place + people + method + consequence. Laboratories, field stations, institutions, funders, technicians, collaborators and predecessors can be part of the causal story. Avoid prize-first biography and the lone-genius narrative. Explain the central mechanism.

The ending does not have to return to the opening. Do not manufacture symmetry.

## Stage 6: final mechanical edit

Run once, after drafting. Check for generic AI phrasing and EKO-specific house tics.

Generic checks include canned openings, "It's not just X, it's Y", mechanical "Moreover/Furthermore/Additionally", rhetorical-question openers used as a crutch, equal-sized paragraphs, identical section shapes, summary conclusions, imposed bullets/headings, routine Further Reading endings, em dashes, mechanical semicolons, scare quotes, manufactured excitement, false modesty and over-hedging.

EKO-specific checks include repeated reflective openers, "There is a familiar...", "There is another reason for caution...", "interesting" and "obvious" doing argumentative work, and conclusions that repeatedly turn a verdict into another question.

Do not fix uniformity by manufacturing irregularity. Vary form because the thought demands it.

## Stage 7: images

Every published post must have at least one relevant lead image.

Prefer a truthful documentary lead image for people, places, landscapes, institutions and events when a clearly reusable one exists. Use an original explanatory visual as the lead for abstract subjects or when available photography would be generic or misleading. Schematics often work best inside the article as supporting explanation.

Use author-owned images, original visuals, maps/charts/documents, or clearly reusable documentary/historical imagery before generic stock. Host locally, never hotlink. Add descriptive alt text and required caption, credit and licence. A second image is used only when it materially improves understanding.

## Stage 8: SEO and discovery

SEO is packaging, never the writing brief.

- Derive title and slug from the finished piece.
- H1 and page title should make substantially the same promise.
- Write a natural meta description; do not optimise prose around a fixed character myth.
- Add internal links only when genuinely useful.
- Use accurate Article/BlogPosting structured data matching the visible page.
- Show publication date and change modification date only for meaningful substantive updates.
- Do not add generic FAQ blocks, artificial chunks, or redundant schema for AI visibility.
- Keep generated `llms.txt` / `.llms.md` if automatic, but do not treat them as a Google ranking lever without current primary evidence.

## Stage 9: publication gate

Before a draft is ready for owner review:

- `draft: true` remains set.
- No published post is altered without explicit approval.
- No em dashes.
- Use only: Policy; Land & Agriculture; Economics & Evidence; Science & Technology; Places & Development; Personal & Ideas.
- Sources are linked inline.
- No routine Further Reading section.
- No confidential, unpublished or farm-level material.
- Check names, figures, dates, quotations, policy status and links.
- Confirm at least one relevant lead image stored locally with alt text and required credit/licence.
- Check title, description, slug, dates, image metadata and structured data.
- Render and inspect desktop and phone layouts, including title wrapping, hero crop, tables, code, captions, links, overflow, navigation and reading width.

### Editorial distinctiveness check

Compare the finished piece with the last several posts. If the same engine, opener, caution move, schematic placement or ending appears again, confirm that the material genuinely requires it.

If the draft takes a clear position in Elvis's voice, Elvis must review that position rather than silently inheriting an editor's or AI draft's opinion.

If a scene is used, confirm whether it is first-hand, directly reported or reconstructed from documents, and ensure the prose does not imply more access than actually occurred.

Publication or merge into production requires explicit owner approval.

## Site-health audit

Run periodically or after template/style changes, not for every article. Check crawlability, broken links, internal linking, schema, canonicals, sitemap, robots directives, mobile rendering, page weight and discovery metadata. Do not use keyword-clustering or content-brief systems to decide what EKO Perspectives should publish.

The editorial model is originality-first: choose what is worth saying, choose the engine the evidence deserves, then make the finished piece discoverable.
