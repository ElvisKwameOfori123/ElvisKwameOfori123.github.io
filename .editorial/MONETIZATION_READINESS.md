# Monetization readiness plan

Updated: 9 October 2026.

This is a technical and policy-readiness plan for EKO Perspectives. It does not enable advertising and does not change editorial topic selection.

## Current position

EKO Perspectives is primarily a personal research and editorial website hosted with GitHub Pages. It currently has no advertising, behavioural analytics, newsletter tracking, user accounts or comments. The privacy notice reflects that state.

GitHub Pages permits some monetization, but GitHub says Pages is primarily intended for static pages that showcase personal or organizational projects and is not intended to run an online business, e-commerce site or commercial SaaS. If advertising ever becomes the site's primary commercial purpose, reassess hosting rather than stretching Pages beyond its intended use.

## AdSense readiness gate

Do not add AdSense code merely to test it. Apply only when all of the following are true:

- the important canonical pages are consistently indexed;
- Search Console shows a meaningful trend in impressions and organic clicks rather than a handful of observations;
- navigation, mobile rendering, sitemap, canonicals and link checks are healthy;
- published posts remain original, evidence-based and useful to readers;
- About, Contact, Privacy, Copyright/reuse and Editorial standards remain easy to find;
- the site has a stable pattern of publication rather than a burst of thin search-targeted pages;
- an actual AdSense publisher ID is available for verification and ads.txt;
- consent requirements for EEA/UK/Switzerland traffic are implemented before personalized advertising is served.

Google's own AdSense guidance emphasizes unique content, clear navigation and a good user experience. EKO should preserve those qualities rather than redesign around ad inventory.

## Implementation when approved

1. Create or connect the AdSense account and submit the canonical domain.
2. Add the exact AdSense verification/ad code only after the publisher ID is known.
3. Add a root `ads.txt` using Google's exact publisher record. Never use a placeholder publisher ID.
4. Configure a Google-certified CMP appropriate for EEA/UK/Switzerland traffic before serving personalized ads there.
5. Update `privacy.qmd` to describe advertising, cookies/local storage, consent controls and relevant third parties before advertising goes live.
6. Start with restrained placements that do not interrupt article reading, obscure navigation or create layout shift.
7. Test phone and desktop rendering, Core Web Vitals, consent behavior and ad layout before production.
8. Monitor policy messages and earnings separately from editorial decisions.

## Audience before ads

Near-term growth should come from:

- strong original posts chosen through the editorial planning process;
- accurate titles and descriptions after the prose is finished;
- useful internal links between related writing and research pages;
- RSS, professional sharing and relevant academic/public-policy communities;
- Search Console query/page data;
- durable project pages that connect public research outputs to explanatory writing.

Do not use keyword clusters or high-volume search terms as an automatic publishing queue.

## Hosting decision rule

Remain on GitHub Pages while the site is principally a research/publication website and monetization is secondary. Reassess hosting if any of these become true:

- advertising or commercial activity becomes the primary purpose;
- bandwidth/build limits become constraining;
- a server-side newsletter, memberships, paywall, user accounts or payments are needed;
- consent/analytics requirements become difficult to manage cleanly on a static deployment.

A future migration should preserve the custom domain and canonical URLs so search equity is not discarded.
