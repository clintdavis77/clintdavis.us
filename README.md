# ClintDavis.us

Static personal website for Clint Davis, designed for GitHub Pages. It has no build step or runtime dependencies.

## Local preview

Open `index.html` in a browser, or serve the folder with any static-file server.

## Publish with GitHub Pages

1. Push the `main` branch to GitHub.
2. In the repository, open **Settings → Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Select `main` and the `/(root)` folder, then save.
5. In your custom domain's DNS, point `clintdavis.us` to GitHub Pages and add `clintdavis.us` as the custom domain in Pages settings.

GitHub will serve the site from the root of the repository after deployment completes.

## Content updates

- Add future case studies to `work/` and link them from `index.html`.
- Add articles to `writing/` and add a row in the Writing section of `index.html`.
- Replace or add approved screenshots in `assets/images/`.
- Replace `assets/docs/Clint-Davis-Resume.pdf` whenever the résumé changes.
