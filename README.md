# Legere

A voting-advice questionnaire for the April 2027 French presidential election.
Answer short statements one at a time, and Legere shows which candidates' positions are closest to yours.

Live: https://legere.vandecatsije.com

## How it works

- 80 statements across 14 policy areas, each coded for 12 candidates from public, sourced positions.
- 10 fixed statements first, then adaptive picks; results are offered once one candidate clearly leads (median around 22 answers).
- Candidates are never named before the results, and every candidate is held to the same evidentiary bar.
- No backend, no cookies: answers stay in your browser.

## Build and run

```sh
python3 build.py   # injects data/*.json into src/app.html -> dist/index.html
open dist/index.html
```

## Layout

- `src/app.html` - the whole app (HTML, CSS, JS), French UI.
- `data/` - statements, questionnaire, candidate positions and profiles, explainers, method page.
- `research/` - the pipeline that produced the candidate codings.
- `analysis/` - Monte-Carlo power analysis behind the stop rule, and the browser E2E script.
- `docs/` - UX research, plain-language audit, legal notes.

See `RESUME.md` for the full pipeline and open follow-ups.
