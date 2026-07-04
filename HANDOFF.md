# Deka Works Handoff

Date: 2026-07-04
Branch: main
Latest commit at handoff: b5b3eea

## 1) What was fixed

### GitHub Pages deploy failure
- Root cause was deploy configuration mismatch for a static site repo.
- Added a proper Pages workflow to deploy repository root as static artifact.

File:
- .github/workflows/deploy-pages.yml

### Added deploy-time validation gates
- Added validation checks before deploy:
  - Internal local link checks from all HTML files.
  - robots.txt existence + Sitemap line presence.
  - sitemap.xml existence + parse checks + URL entry checks.
- Deploy job now requires validation job success.

File:
- .github/workflows/deploy-pages.yml

### Added validation allowlist support
- Link checker now supports intentional exceptions:
  - ignored_refs (exact paths)
  - ignored_prefixes (path prefix matches)

File:
- .github/workflows/deploy-pages.yml

## 2) Performance and lean-loading updates

### Lighthouse CI budget workflow
- Added Lighthouse workflow running on push/main and pull requests.
- Added `.lighthouserc.json` with score thresholds and key URLs.

Files:
- .github/workflows/lighthouse-budget.yml
- .lighthouserc.json

### HTML loading improvements
- Deferred local `script.js` includes on non-home pages where present.
- Reduced Google Font weights from `400;500;600;700;800` to `400;600;700`.
- Homepage (`index.html`):
  - Added small critical CSS block for above-the-fold content.
  - Converted stylesheet to non-blocking load pattern:
    - preload stylesheet
    - `media="print"` + `onload` swap to `all`
    - `noscript` fallback
- Service pages (`app-development.html`, `web-development.html`, `ai-solutions.html`, `consulting.html`):
  - Added service-page critical CSS block.
  - Same non-blocking stylesheet load pattern.

Files touched:
- index.html
- app-development.html
- web-development.html
- ai-solutions.html
- consulting.html
- 404.html
- thank-you.html
- privacy-policy.html
- terms-and-conditions.html
- case-study-template.html

## 3) Maintainability improvements

### Shared head-block sync for service pages
- Added explicit markers around shared service head block:
  - `<!-- shared-service-head:start -->`
  - `<!-- shared-service-head:end -->`
- Added sync/check tool to enforce consistency across service pages.
- CI now runs this check in deploy workflow.

Files:
- tools/sync_service_head.py
- .github/workflows/deploy-pages.yml
- app-development.html
- web-development.html
- ai-solutions.html
- consulting.html

## 4) Commit timeline (newest first)

- b5b3eea chore: enforce shared service head block sync
- d928352 perf: add critical css and async stylesheet loading to service pages
- a82adc2 perf: inline homepage critical css and async stylesheet load
- e7af312 perf: lean loading defaults and lighthouse budgets
- aeb12bb ci: add allowlist support for link validation
- 9dd0d0a ci: add pages validation checks and workflow badge
- b863b2f ci: add github pages deployment workflow
- 4e36c72 chore: force pages redeploy

## 5) Operational commands for later

### Verify clean git state
```powershell
git status -sb
```

### Run service head sync check locally
```powershell
python tools/sync_service_head.py --check
```

### Auto-sync service head block from source page
Source of truth currently: `app-development.html`
```powershell
python tools/sync_service_head.py --write
```

### Trigger a redeploy manually
```powershell
git commit --allow-empty -m "chore: force pages redeploy"
git push origin main
```

## 6) CI/CD expectations

### Deploy workflow
- Workflow: `Deploy static site to Pages`
- Trigger: push to `main` and manual dispatch.
- Steps:
  - checkout
  - shared head sync check
  - internal links/robots/sitemap validation
  - pages artifact upload
  - pages deploy

### Performance workflow
- Workflow: `Lighthouse Budget`
- Trigger: pull_request and push to `main`.
- Runs Lighthouse against key pages and enforces configured thresholds.

## 7) Known tradeoffs / notes

- Critical CSS is intentionally minimal and focused on above-the-fold stability and faster first paint.
- Full styling still comes from `styles.css` after async stylesheet swap.
- If service-page hero/header design changes, update one source page block and run `--write`.

## 8) Suggested next improvements (optional)

1. Add image optimization pass when image-heavy sections are introduced (AVIF/WebP + responsive sizes).
2. Add HTML minification in build/deploy step if repo grows significantly.
3. Expand Lighthouse URLs to include legal and thank-you pages for broader guardrails.
4. Add a tiny CHANGELOG.md for non-technical stakeholders.

## 9) Fast recovery checklist

If deploy fails later:
1. Open failed workflow run details in Actions.
2. Check sync gate first (`tools/sync_service_head.py --check`).
3. Check broken local links reported by validation step.
4. Confirm robots/sitemap still valid after content edits.
5. If urgent and no content changes needed, force redeploy commit.
