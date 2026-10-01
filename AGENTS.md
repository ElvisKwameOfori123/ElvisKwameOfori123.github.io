# Repository instructions

## EKO Perspectives design principle

Warm paper, black type, one restrained blue accent, strong editorial imagery, generous whitespace, few reader-facing labels, minimal decorative UI, and hierarchy created principally through typography, scale, spacing and rules. Preserve publication clarity over generic Quarto or dashboard styling. The aim is coherence, not resemblance to another publication.

## EKO Perspectives editorial work

For any task that plans, researches, drafts, revises, reviews, profiles, SEO-packages, or prepares a post for `kwameofori123.com` / EKO Perspectives, **read `.editorial/EKO_EDITORIAL_WORKFLOW_v2.3.md` first and follow its stage routing**. Also use `.editorial/story-engine-library.md` when choosing how a piece should be built, and consult `.editorial/EKO_PERSPECTIVES_EDITORIAL_PLAN.md` for the standing topic bank, site priorities and longer-horizon editorial direction.

The repository copy of **EKO Editorial Workflow v2.3** is the standing editorial workflow. It supersedes v2.2 and the older separate `pre2015-prose-voice` + `ai-slop-editing-pass` chain. Do not run those systems in parallel. The workflow is canonical if a planning-reference file contains an older or more rigid instruction.

### Editorial planning and approval

- Plan candidate topics/themes before drafting rather than posting whatever happens to be available.
- Consult `.editorial/EKO_PERSPECTIVES_EDITORIAL_PLAN.md` when building a slate, but treat its topic list and sample schedule as a bank of candidates rather than an automatic queue.
- Re-check current evidence, policy status, publication status, site coverage and topical relevance before selecting an older candidate.
- Do not start a full draft of a new topic until Elvis Kwame Ofori has approved the topic or theme, unless he explicitly asks for that specific draft in the current request.
- A quiet period is not a reason to publish a burst of weak or structurally similar pieces.

### Story structure

- There is no single E360 framework and no single pre-2015 research-blog framework.
- Choose the story engine **after** the evidence is understood. Possible engines include scene/place, contradiction/foil, claim testing, policy audit, debate diagnosis, behind-the-paper/model, one-number comparison, public-record pattern assembly, mechanism, timeline/policy reversal, and people/places behind the science.
- The engine library is a menu, not a rotation rule. Do not force variety, and do not force the same house structure onto every post.
- Where an argument is contested, read the strongest credible rebuttal or competing interpretation. Do not build the piece around a weak straw man.
- Look for the institutional or measurement problem under the visible dispute: ownership/tenure, accounting boundaries, baselines, incentives, spatial scale, implementation, displacement, leakage, or another mechanism supported by evidence.
- Public records can provide named, attributable voices, but never imply an interview, visit or first-hand scene that did not happen.
- First person must earn its place. Use `I` for something Elvis actually did, observed, modelled, read, decided, experienced or believes, not as a repeated decorative opener.
- Clear conclusions are allowed. Represent material counterevidence fairly, qualify once where needed, then state what the evidence supports. Do not make caution or another narrowing question the automatic ending.

### Non-negotiable publication safeguards

- New posts remain `draft: true` until Elvis Kwame Ofori explicitly approves publication.
- Do not publish, merge a draft into production, or alter an already-published post without explicit approval.
- No em dashes.
- Use only the site's six established categories: Policy; Land & Agriculture; Economics & Evidence; Science & Technology; Places & Development; Personal & Ideas.
- Link sources inline where they enter the prose. Do not append a routine "Further reading" section.
- Do not publish unpublished research results, confidential material, farm-level data, or private research notes.
- Evidence verification happens before drafting. The final mechanical editing pass happens after drafting. SEO/discovery packaging happens after the prose is finished and must not override the chosen voice.
- Never invent scenes, quotations, biographical facts, observations, interviews or field visits.
- Every published post must have at least one relevant lead image stored locally with descriptive alt text; use a second supporting image only when it adds real explanatory, documentary or historical value.
- Prefer original explanatory visuals, author-owned photography, maps, charts, documents and clearly reusable documentary or historical imagery over decorative stock.
- Prefer a real or documentary lead image when a strong, truthful and clearly reusable one exists. Use an original schematic as the lead when the subject is abstract or when available photography would be generic or misleading; otherwise keep schematics as supporting explanatory visuals.
- Render and check the finished draft on both desktop and phone before it is considered ready for review.

### Repository hygiene

- `main` is the single source of truth for the live site.
- Start new branches from current `main`; do not branch from old preview, rewrite, polish, image-test, or migration branches.
- Keep branches short-lived and delete them after merge unless they contain active unpublished draft work.
- Keep `gh-pages` only for deployment.
- See `.editorial/REPOSITORY_MAINTENANCE.md` for the branch-maintenance rule and GitHub setting to enable.

For a whole-site SEO or technical-health task that does not involve drafting a post, follow the site-health section in `.editorial/EKO_EDITORIAL_WORKFLOW_v2.3.md`.

For unrelated code-only work, the editorial pipeline does not need to run unless the change affects post rendering, metadata, discovery, accessibility, or publication behavior.

## Search Console verification

Do not delete, rename or edit `google63dfd647cad8477d.html` in the repository root, and do not remove it from `resources` in `_quarto.yml`. Google Search Console uses it to keep `kwameofori123.com` verified.
