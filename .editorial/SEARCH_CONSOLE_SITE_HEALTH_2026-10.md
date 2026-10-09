# Search Console and website health: October 2026

This is a technical maintenance checklist, not an editorial publishing queue. Preserve the EKO editorial workflow in `.editorial/EKO_EDITORIAL_WORKFLOW_v2.3.md` and do not publish or rewrite articles as part of site-health work.

## Observed Search Console baseline

Screenshots dated 9 October 2026 show 17 indexed URLs and 17 excluded URLs: 15 **Discovered - currently not indexed**, 2 **Crawled - currently not indexed**. Many of the 15 excluded URLs end in `/index.html`, while corresponding trailing-slash URLs appear among indexed pages. This does **not** prove an indexing defect; verify the selected canonical on representative URLs.

## Current source configuration

- Quarto website with `website.site-url: https://kwameofori123.com` and `format.html.canonical-url: true` in `_quarto.yml`.
- `robots.txt` allows crawling and references `https://kwameofori123.com/sitemap.xml`.
- Google verification file `google63dfd647cad8477d.html` is explicitly preserved as a project resource. Do not remove it.
- The sitemap may be generated at build time; absence of a tracked root `sitemap.xml` is not proof it is missing from deployment.

## Checks before any production SEO change

1. Build Quarto from current `main` and inspect generated `_site/sitemap.xml`, `_site/robots.txt`, and `_site/index.html`. Confirm sitemap exists, contains only published pages, and has correct absolute URLs.
2. Inspect generated `<link rel="canonical">` on homepage, About, blog index, one post and one project. Compare trailing-slash and `/index.html` versions and Google's selected canonical in URL Inspection.
3. Identify the **two crawled-but-not-indexed URLs** from Search Console. Do not assume they are duplicates.
4. Verify `/about.html` and the current `/how-i-got-here/` URL with URL Inspection; request indexing only for important canonical pages after any necessary corrections.
5. Confirm all article and project links use the chosen public URL form; avoid unnecessary slug changes or mass redirects.
6. Run link and image checks. Check that images load on mobile, alt text is accurate, and Open Graph previews match the current lead image.
7. Render the site at narrow phone and desktop widths. Check navigation, category controls, page overflow, headings, cards and footer.
8. Review Search Console Performance (queries and pages) monthly. Six impressions and one click in the earlier three-month screenshot are too few to infer ranking trends.

## Change policy

- Make technical fixes only when a check demonstrates a problem. Do not add `noindex` to legitimate pages merely to reduce the excluded count.
- Keep article URLs stable; image replacements and copy revisions do not require new URLs.
- Do not modify the editorial workflow, unpublished drafts, or published prose without approval.
- Keep changes on a short-lived branch, test build and responsive output, then review before merge.
