# Deka Works Handoff

Date: 2026-07-04
Branch: main
Latest handoff update: includes all work through commit `12060f9` plus workflow hardening staged after that commit.

## 1) Current State

- Site is deployed and passing after Pages workflow fixes.
- Core CI checks are in place for deploy safety and content integrity.
- Performance guardrails are enabled via Lighthouse CI.
- Homepage now links comparison content to a dedicated page for cleaner UX.

## 2) Major Changes Completed

### Deploy and CI stability
- Added GitHub Pages deployment workflow.
- Added pre-deploy validations:
  - service-page shared head sync check
  - internal link checks
  - robots/sitemap checks
- Moved inline validation logic into a script to avoid heredoc/indentation failures.
- Upgraded Actions versions to avoid Node 20 deprecation warnings.

Primary files:
- .github/workflows/deploy-pages.yml
- tools/validate_site.py
- tools/sync_service_head.py

### Performance + lean-loading work
- Added Lighthouse budget workflow and config.
- Reduced font weights and deferred local JS loading.
- Added critical CSS + non-blocking stylesheet load strategy on homepage and service pages.

Primary files:
- .github/workflows/lighthouse-budget.yml
- .lighthouserc.json
- index.html
- app-development.html
- web-development.html
- ai-solutions.html
- consulting.html

### UX/content cleanup
- Removed duplicate Bildva card.
- Stabilized comparison table layout in CSS.
- Moved full comparison content to dedicated page and converted homepage section to a preview CTA.

Primary files:
- index.html
- comparison.html
- styles.css
- sitemap.xml

## 3) Newer Commit Timeline (newest first)

- 12060f9 feat: move full comparison to dedicated page
- 9573991 ci: upgrade actions versions and node runtime
- 0694160 ci: move site validation to dedicated python script
- 05e6176 fix: correct indentation in deploy validation script
- c8ae8c0 fix: remove duplicate Bildva card and stabilize comparison table layout
- 7dc0653 docs: add detailed project handoff
- b5b3eea chore: enforce shared service head block sync
- d928352 perf: add critical css and async stylesheet loading to service pages
- a82adc2 perf: inline homepage critical css and async stylesheet load
- e7af312 perf: lean loading defaults and lighthouse budgets

## 4) Active Workflow Behavior

### Deploy workflow
- File: `.github/workflows/deploy-pages.yml`
- Trigger: push to `main` and manual dispatch.
- Purpose: validate + deploy Pages artifact.
- Validation steps:
  - `python tools/sync_service_head.py --check`
  - `python tools/validate_site.py`

### Lighthouse workflow
- File: `.github/workflows/lighthouse-budget.yml`
- Trigger: push/PR for site-related files.
- Purpose: budget regressions in performance/accessibility/best-practices/SEO.

## 5) Operational Commands

### Check repo state
```powershell
git status -sb
```

### Run local validation gate
```powershell
python tools/sync_service_head.py --check
python tools/validate_site.py
```

### Re-sync service shared head block
```powershell
python tools/sync_service_head.py --write
```

### Force redeploy if needed
```powershell
git commit --allow-empty -m "chore: force pages redeploy"
git push origin main
```

## 6) Notes + Tradeoffs

- Critical CSS is intentionally minimal; full style fidelity still comes from `styles.css` after async swap.
- Service-page shared head block source of truth is still `app-development.html`.
- If comparison content changes, update both `comparison.html` and homepage preview CTA copy.

## 7) Fast Failure Triage

If deploy fails:
1. Open latest Actions run for `main` (ignore older failed runs if newer commit passed).
2. Reproduce locally:
   - `python tools/sync_service_head.py --check`
   - `python tools/validate_site.py`
3. Fix reported file/link/sitemap issue.
4. Push a small targeted commit.
