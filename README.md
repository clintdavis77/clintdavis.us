# ClintDavis.us

Personal site for Clint Davis, built with [Hugo](https://gohugo.io) and deployed to
GitHub Pages by GitHub Actions. Writing lives in markdown; the design lives in
`assets/css` and `layouts/`.

## Local preview

```bash
hugo server --buildDrafts
```

Then open http://localhost:1313. Drafts (`draft: true`) only appear in this mode.

Plain build, exactly what CI runs:

```bash
hugo --gc --minify
```

## Publishing a post

```bash
hugo new content blog/my-post-slug.md
```

That creates `content/blog/my-post-slug.md` from `archetypes/blog.md`. Fill in the
frontmatter, write the post, then set `draft: false` when it is ready.

Frontmatter fields that matter:

- `title` — post title, used in the browser tab, social cards, and the list
- `description` — one or two sentences; this is the teaser text and the meta description
- `date` — publish date, `YYYY-MM-DD`
- `draft` — `true` keeps the post out of production builds
- `tags` — optional list; each tag gets a page at `/tags/<tag>/` (they are real, indexable pages)
- `youtube` — optional video ID; renders an embed under the title
- `image` — optional social-card override (1200x630). Leave it out and the build uses
  `static/images/og/<slug>.png` when that file exists, otherwise `/images/og-default.png`
- `kicker` — optional label above the title, defaults to "Writing"

## How the site is organised

```
content/_index.md              home page copy (hero, stats, blurb, about)
content/work/                  case studies, one folder per study
content/blog/                  posts, one markdown file each
content/search.md              the /search/ page (frontmatter only)
content/tags/_index.md         intro copy for the /tags/ index
layouts/index.html             home page
layouts/work/list.html         portfolio index
layouts/work/single.html       case study template
layouts/blog/list.html         blog index
layouts/blog/single.html       post template
layouts/taxonomy.html          /tags/ index
layouts/term.html              one tag's page
layouts/_default/search.html   /search/ page
layouts/index.json             search index generated at build time
layouts/partials/              head, header, footer, image, toc, post-tags
layouts/shortcodes/            case-section, case-figure, pullquote
assets/css/site.css            original design system
assets/css/site-extras.css     components added for the blog, portfolio index, search, tags
assets/images/                 screenshots and photos (processed into WebP at build time)
assets/js/                     site.js, search.js, fuse.min.js
static/images/og-default.png   fallback social card
static/images/og/              per-page social cards, one PNG per page
static/fonts/                  self-hosted woff2 files
scripts/make-og-cards.py       renders the per-page social cards
```

Case studies use two shortcodes so the layout stays in the template, not the content:

```markdown
{{</* case-figure src="/images/foo.jpg" width="1200" height="800" alt="..." caption="..." */>}}

{{</* case-section eyebrow="The problem" */>}}
## A markdown heading

Body text, lists, whatever the section needs.

{{</* pullquote */>}}One line you want pulled out.{{</* /pullquote */>}}
{{</* /case-section */>}}
```

## Search, tags, and tables of contents

Search is client-side, no service: `layouts/index.json` writes every case study and post
into `/index.json` at build time, `assets/js/search.js` loads it with Fuse.js. The library
ships with the site (no CDN), and it is only loaded on `/search/`. Press `/` on that page
to jump into the box.

Tags are real pages. Add `tags: [...]` to a post or case study and the build creates
`/tags/`, `/tags/<tag>/`, the chips under the title, and the "Browse by topic" block on
the blog index. A tag that spans a case study and a post is the point: it links them.

A post with two or more `##` headings gets an automatic table of contents under the
intro. Headings inside the `case-section` shortcode are **not** picked up, so case
studies do not get one.

## Images

Screenshots and photos live in `assets/images/`, not `static/images/`. The
`layouts/partials/image.html` partial resizes each one into WebP plus an original-format
fallback and emits a `<picture>` with `srcset` and `sizes`, so a phone downloads a phone-sized
file instead of a 1600px screenshot. Reference an image in content as usual
(`/images/foo.jpg`) and the shortcodes, gallery, and card layouts do the rest.

Width/height attributes are intrinsic sizes; the stylesheet sets `height: auto` on figures
and the gallery so tall phone shots keep their aspect ratio instead of stretching.

## Social cards

Each case study and post gets its own 1200x630 card, rendered from the site's own fonts:

```bash
python3 scripts/make-og-cards.py           # every page
python3 scripts/make-og-cards.py --check   # list what would be rendered
python3 scripts/make-og-cards.py my-post   # one page
```

Output lands in `static/images/og/<slug>.png` and `head.html` picks it up automatically.
The script needs Chrome, Chromium, or Edge installed (it drives it headless).

## Deployment

`.github/workflows/deploy.yml` builds with Hugo 0.168.0 (extended) and deploys `public/`
to GitHub Pages on every push to `main`.

One-time setting: **Settings → Pages → Build and deployment → Source: GitHub Actions.**
If that is left on "Deploy from a branch", the workflow runs but the site never updates.

Old case-study URLs (`/work/foo.html`) redirect to the new pretty URLs through Hugo
`aliases` in each case study's frontmatter.
