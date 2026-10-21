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
- `tags` — optional list
- `youtube` — optional video ID; renders an embed under the title
- `image` — optional social-card override (1200x630), otherwise `/images/og-default.png`
- `kicker` — optional label above the title, defaults to "Writing"

## How the site is organised

```
content/_index.md              home page copy (hero, stats, blurb, about)
content/work/                  case studies, one folder per study
content/blog/                  posts, one markdown file each
layouts/index.html             home page
layouts/work/list.html         portfolio index
layouts/work/single.html       case study template
layouts/blog/list.html         blog index
layouts/blog/single.html       post template
layouts/shortcodes/            case-section, case-figure, pullquote
assets/css/site.css            original design system
assets/css/site-extras.css     components added for the blog and portfolio index
static/images/                 screenshots and photos
static/fonts/                  self-hosted woff2 files
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

## Deployment

`.github/workflows/deploy.yml` builds with Hugo 0.168.0 (extended) and deploys `public/`
to GitHub Pages on every push to `main`.

One-time setting: **Settings → Pages → Build and deployment → Source: GitHub Actions.**
If that is left on "Deploy from a branch", the workflow runs but the site never updates.

Old case-study URLs (`/work/foo.html`) redirect to the new pretty URLs through Hugo
`aliases` in each case study's frontmatter.
