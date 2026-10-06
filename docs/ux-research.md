# UX research note - Legere redesign (October 2026)

Goal: a questionnaire anyone can finish on a phone, with no prior knowledge of French political jargon.
Success metrics: completion rate and comprehension.
Patterns below were checked on Mobbin (iOS flows and screens), then adapted.

## Patterns adopted

### 1. One question per screen, stacked full-width answers, auto-advance
Seen in Headspace check-ins (5 options stacked, radio on the right, progress "7/7" in the top bar), Liven assessment (5 stacked pills with "Single choice 1/18"), Bloom, Flo, Finch, Cleo AI, Nutmeg.
Every one of these keeps the question short and large, the options as full-width tap targets (48-56 px tall), and a back arrow top-left.
Adopted: the Likert scale becomes five stacked buttons labelled in words, 56 px tall, ordered from "Pas du tout d'accord" to "Tout à fait d'accord".
Tapping an answer advances immediately (Flo, Bloom, Wonder/Tolan); no "Continue" button on single-choice screens.
Keyboard 1-5 and 0 on desktop.

### 2. Thin progress bar in the top bar, no promised total
Duolingo onboarding, Headspace, Liven and Bloom all use a single thin bar at the top with a back arrow at the left and a close button at the right.
Nibble uses a segmented bar for short quizzes.
Adopted: continuous bar driven by `DATA.core.length + 6` (the minimum before the stop rule can fire), plus a small answer counter.
Copy never promises a fixed number of questions, because the stop rule is adaptive.

### 3. Plain-language context under the question
Hers (consultation) and Wealthsimple put one explanatory sentence under the question and short descriptions under each option; Nutmeg adds a reassuring line ("there is no right answer").
Adopted: a visible "De quoi parle-t-on ?" line under every statement, filled from `s.plain_fr || ctx.today_fr`.
"Pour / contre" stays one tap away in a bottom sheet.

### 4. Inline glossary for jargon
Public (stocks) opens a bottom sheet with a plain definition when a metric name is tapped; Moonlitt and Box Box Club use a glossary sheet.
Adopted: acronyms and technical terms inside statements (ISF, AME, 49.3, ZFE, RIC, ZAN, EPR2, IGPN, SMIC, RSA...) get a dotted underline; tapping opens a short neutral definition in the same bottom sheet.
Statement wording is untouched; the underline is applied at render time.

### 5. Results: one honest headline, details below
Headspace results lead with one number and one sentence, then "Suggested for you"; Yazio leads with "Your results are in" and a single recommended card, then "You might also like"; Liven leads with the primary pattern then one sentence.
Adopted: the results page opens with the closest candidate(s), ties shown as ties, a plain confidence sentence, then the full ranking with its uncertainty band, then collapsible sections for the curious (robustness, map, themes, disagreements).

### 6. Optional refinement after a first result
Duolingo's "Find my level - recommended" card and Headspace's "Why this recommendation" tiles show that optional depth sits best after the reward.
Adopted: dilemmas, priorities, profile, open questions and "keep answering" are cards in an "Affiner mon résultat" section on the results page, each with an estimated time and a done state.
Scoring still uses them when answered.

### 7. Resume card
Mimo, Mindvalley, Brilliant and Skillshare show a "Continue" card with a progress bar and the count done.
Adopted: the home screen shows "Reprendre" with the number of answers and a progress bar when a session exists.

### 8. Mid-flow checkpoint
Uxcel Go and ChatGPT quizzes stop with a short card and two choices ("Keep learning / Exit", "View results / Try harder").
Adopted: when the stop rule fires, a checkpoint screen says the result is ready, with "Voir mon résultat" as primary and "Continuer à répondre" as secondary.
The optional expectation question lives there as a compact select, so candidates are named only once answers are locked.

## Patterns rejected
- Horizontal five-dot Likert rows (Lyft, Vrbo): small targets and unlabelled middle points; worse for older users.
- Gamified streaks and mascots (Duolingo, Nibble): not credible for a civic tool.
- Colour-coded correct/incorrect feedback (Quizlet, Premier League): there is no right answer, and red/green reads as left/right in a French political context.
