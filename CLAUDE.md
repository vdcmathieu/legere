# Legere

Voting-advice questionnaire for the April 2027 French presidential election (formerly "Isoloir 2027").
Single-page app, French UI, no backend: answers stay in the browser (localStorage key `legere-2027-v1`).
Public site: https://legere.vandecatsije.com (Vercel project `legere`, static `dist/`): `python3 build.py && vercel deploy --prod`.
Cookieless Vercel Web Analytics loads only on the production host; any new tracking must keep answers out of URLs and be reflected in `data/legal.html`.

## Layout
- `src/app.html` - the whole app (HTML/CSS/JS); `build.py` injects `data/*.json` into it -> `dist/index.html`.
- `data/` - statement bank, questionnaire modules, candidate positions, explainers, method page.
- `research/` - pipeline that produced the candidate codings (journals, consolidation, translation).
- `analysis/power.py` - Monte-Carlo power analysis behind the stop rule; `analysis/e2e.py` - browser E2E.
- `docs/ux-research.md` - Mobbin patterns behind the one-question-per-screen redesign; `docs/screens/` - E2E screenshots.

See RESUME.md for the full pipeline and open follow-ups.

## Rules
- Political neutrality is the product: no party colours, candidates never named before results, same evidentiary bar for every candidate, plain neutral wording.
- Any change to statement wording must keep its meaning, or the candidate codings in `data/positions.json` become invalid.
- Any change to the core set or stop rule must be backed by a re-run of `analysis/power.py`.
