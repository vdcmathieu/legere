# Legere 2027

Voting-advice questionnaire for the 2027 French presidential election.
Published (private): https://claude.ai/artifact/5Mts8uDsDoKvMdV1KZXNrb

## Pipeline

    python3 research/consolidate.py research/journals/matrix.jsonl research/journals/supplement.jsonl
    python3 research/translate.py split   # then translate research/fr/in -> research/fr/out (translate-workflow.js)
    python3 research/translate.py merge
    python3 research/make_profiles.py
    python3 build.py                      # -> dist/index.html
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
2. After the PS-Place publique primary (online rounds 9-10 and 16-17 Oct 2026): drop the losing candidate(s).
3. After the Cour de cassation ruling on Le Pen: update record and profile.
4. Re-run the pipeline and republish to the same artifact URL.

5. Coding audit of 2026-10-07 (`research/audit/`): 18 confirmed cells fixed. Still open, need a neutrality call:
   int3 magnitudes for Glucksmann/Faure vs Attal (F08), ecol2 Philippe -1 vs -2 (F20), imm5 Glucksmann vs Tondelier/Roussel (F24),
   sec2 left-bloc magnitudes (F30), fin4 evidence-free guesses for Glucksmann and Zemmour (F29), soc4 Zemmour (F27), imm6 Philippe vs Attal (F23),
   soc4 negated wording (F26, would flip 12 cells), eco1 French wording ("pas seulement l'immobilier") vs Le Pen's +1 for a financial-only tax,
   Zemmour's current retirement-age position (F22). Faure stays the thinnest-coded candidate (smallest clone margin, 0.046 over Tondelier).

## Flow (2026-10-06)
10 fixed statements (`CORE_N` in build.py), then adaptive picks. The result is offered from 20 answers when one candidate wins >= 70% of bootstrap draws (`STOP_P` in src/app.html), at the latest after 35 (`MAX_STOP`). Simulated median: 23 answers, 93% correct top-1 among clear cases (re-run 2026-10-07 after the coding audit).
