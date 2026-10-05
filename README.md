# Elvis Kwame Ofori

Personal research website and **EKO Perspectives**, built with [Quarto](https://quarto.org/) and published with GitHub Pages.

**Live site:** https://kwameofori123.com

## About this repository

This repository contains the source for my personal website: research, public writing, project pages and professional information. The aim is to keep the site readable, lightweight and useful on both desktop and mobile.

The site includes:

- **EKO Perspectives** — essays on policy, land and agriculture, economics and evidence, science and technology, places and development, and personal ideas
- **Research** — current work, publications and public project links
- **About** — background and editorial standards
- **Contact** — institutional and professional contact details

## Built with

- [Quarto](https://quarto.org/)
- GitHub Pages
- GitHub Actions for rendering, publishing and link checks
- custom CSS for the shared light and dark editorial design

## Repository structure

```text
.
├── blog/                 # EKO Perspectives index and posts
├── projects/             # public research/project pages
├── includes/             # reusable Quarto fragments
├── assets/               # shared site assets
├── .editorial/           # internal editorial guidance and maintenance notes
├── .github/workflows/    # publishing and quality-control workflows
├── _quarto.yml           # site configuration
├── styles-common.css     # shared layout and typography
├── styles-light.scss     # light theme
└── styles-dark.scss      # dark theme
```

Individual posts keep their own images and source notes alongside the article where practical. Draft posts remain in the repository but are excluded from the public site until they are ready.

## Preview locally

Install [Quarto](https://quarto.org/docs/get-started/) and then run:

```bash
quarto preview
```

To render the site without starting a preview server:

```bash
quarto render
```

Generated output is written to `_site/` and is not committed to the source branch.

## Publishing

The editable source lives on `main`. A GitHub Actions workflow renders the Quarto site and publishes the generated site to `gh-pages`.

A separate automated link check renders the site and tests internal and external links so broken references can be caught without committing generated files.

## Design principles

The site deliberately keeps the interface simple: readable typography, restrained colour, accessible contrast, responsive layouts and minimal decoration. Content and evidence should remain more prominent than the interface around them.

## Reuse

The repository is public so the implementation can be inspected and learned from. Articles, photographs and other third-party material may have their own copyright or licence terms; check the relevant page and attribution before reusing content.
