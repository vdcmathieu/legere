# Legere 2027

Voting-advice questionnaire for the 2027 French presidential election.
Published (private): https://claude.ai/artifact/5Mts8uDsDoKvMdV1KZXNrb

## Pipeline

    python3 research/consolidate.py research/journals/matrix.jsonl research/journals/supplement.jsonl
    python3 research/translate.py split   # then translate research/fr/in -> research/fr/out (translate-workflow.js)
    python3 research/translate.py merge
    python3 research/make_profiles.py
    python3 build.py                      # -> dist/legere.html
    python3 analysis/power.py 800         # -> analysis/power_real.json (accuracy by number of answers)
    python3 analysis/stop_rules.py analysis/stop_rules.json   # when the checkpoint fires
    python3 analysis/e2e.py <url> <outdir> [mobile] [dark] [persona=<cid>]

## Data
- `data/statements.json` v0.2 (80 statements, 14 areas, 3 axes), `data/questionnaire.json` v0.2
- `data/positions.json` (12 candidates x 80, verified codings + records), `data/profiles.json`
- `data/audit.json` + `data/context_update.json` (neutral "En savoir plus" explainers)
- `data/method.html`, `data/power_section.html`, `data/meta.json` (polls)

## Next
1. Gap-fill pass with Codex (own web search): 227 uncoded cells (Zemmour, Faure, Ruffin, Glucksmann, Attal, Lisnard worst), 109 unsourced cells, cross-lean corroboration (partisan press of both sides), and the 9 context facts the explainer agent could not confirm.
2. After the PS-Place publique primary (17-18 Oct 2026): drop the losing candidate(s).
3. After the Cour de cassation ruling on Le Pen: update record and profile.
4. Re-run the pipeline and republish to the same artifact URL.

## Flow (2026-10-06)
10 fixed statements (`CORE_N` in build.py), then adaptive picks. The result is offered from 20 answers when one candidate wins >= 70% of bootstrap draws (`STOP_P` in src/app.html), at the latest after 35 (`MAX_STOP`). Simulated median: 22 answers, 93% correct top-1 among clear cases.
