# Repository maintenance

This repository uses `main` as the single source of truth for the live EKO Perspectives site.

## Working rules

- New editorial or site changes should normally start from the current `main` branch.
- Use short-lived branches for reviewable work. Merge through a pull request when practical.
- After a pull request is merged, delete its head branch unless it intentionally contains continuing draft work.
- Keep long-lived branches only for genuinely unpublished drafts or continuing work that must remain separate from `main`.
- Do not use old preview, polish, image-test, rewrite, or migration branches as starting points for new work.
- `gh-pages` is a deployment branch and must not be repurposed as an editorial working branch.
- Before merging, confirm the branch is based on recent `main`, the site builds, links pass, and desktop/mobile rendering is sound.
- New posts remain `draft: true` until Elvis explicitly approves publication.
- The canonical editorial instructions are `.editorial/EKO_EDITORIAL_WORKFLOW_v2.3.md` and `AGENTS.md`.

## Suggested GitHub repository setting

Enable **Automatically delete head branches** in GitHub under **Settings → General → Pull Requests**. This prevents merged feature branches from accumulating. This setting does not delete `main`, `gh-pages`, or branches that have not been merged.

## Long-lived branches

Keep only branches that contain active unpublished work. As of 1 October 2026, the intentionally preserved draft branches are:

- `drafts/2026-09-23`
- `drafts/2026-09-24`

Review long-lived draft branches periodically. Once their useful work is merged, moved, or abandoned, delete them rather than letting them become alternative versions of the site.
