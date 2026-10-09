# Search Console and website health: October 2026

This is a technical maintenance record, not an editorial publishing queue. Preserve the EKO editorial workflow in `.editorial/EKO_EDITORIAL_WORKFLOW_v2.3.md` and do not publish or rewrite articles as part of site-health work.

## Observed Search Console baseline

Screenshots dated 9 October 2026 show 17 indexed URLs and 17 excluded URLs: 15 **Discovered - currently not indexed**, 2 **Crawled - currently not indexed**. Fourteen of the 15 discovered exclusions supplied in the screenshots were explicit directory `/index.html` variants; `/about.html` was the exception. Several clean trailing-slash counterparts were already indexed.

## Verified rendered-site findings

A GitHub Actions render of the site established the following:

- Quarto generates a sitemap at build time.
- Before correction, that sitemap contained 29 public URLs, including **24 explicit `/index.html` URLs**.
- The rendered public pages themselves already declared clean canonical URLs, and **0 pages canonicalized to `/index.html`**.
- The sitemap therefore disagreed with the pages' own `rel=canonical` form. This provides a concrete technical explanation for why Google discovered many `/index.html` variants even though their clean counterparts were canonical.
- Draft pages render only as empty HTML stubs and are not included in the sitemap.
- `robots.txt` allows crawling and advertises `https://kwameofori123.com/sitemap.xml`.
- The Google Search Console verification file remains present.
- The two **Crawled - currently not indexed** URLs are still unidentified from the screenshots and must not be guessed.

## Implemented correction

The Quarto build now runs a post-render normalization step that changes only sitemap `<loc>` values ending in `/index.html` to the matching clean trailing-slash URL. Standalone pages such as `/about.html`, `/contact.html` and `/privacy.html` remain unchanged.

An automated site-health check now verifies on every pull request that:

- the sitemap exists and uses the canonical domain;
- no sitemap URL ends in `/index.html`;
- every sitemap URL has a matching rendered page;
- every sitemap page has `rel=canonical`;
- sitemap and canonical URLs agree;
- no sitemap page is `noindex`;
- private `_sources.md` claim ledgers do not render publicly;
- published blog posts carry valid `BlogPosting` JSON-LD.

The first clean verification after the sitemap correction reported **29 sitemap URLs, 0 canonical errors, 0 noindex pages, 0 missing canonicals and 0 `/index.html` canonicals**. The rendered link checker also completed with 0 errors after fixing or correctly handling the few automated-check edge cases.

## Remaining Search Console follow-up

1. Identify the two **Crawled - currently not indexed** URLs from Search Console.
2. Use URL Inspection on `/about.html` and representative clean article/project URLs to compare Google's selected canonical with the declared canonical.
3. After the corrected sitemap is deployed, resubmit or refresh the sitemap in Search Console and allow Google time to recrawl it.
4. Do not request indexing for duplicate `/index.html` variants; request indexing only for important canonical pages when useful.
5. Review Search Console Performance monthly. The earlier sample of six impressions and one click is too small for ranking conclusions.

## Change policy

- Keep article URLs stable; image replacements and copy revisions do not require new URLs.
- Do not add `noindex` to legitimate pages merely to make the exclusion count smaller.
- Do not modify unpublished drafts or published prose during technical site-health work unless a source link or metadata defect is specifically verified.
- Keep technical changes on a short-lived branch, require a clean render/link/site-health check, and review before production merge.
