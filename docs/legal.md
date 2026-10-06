# Legal checklist for publishing Legere

Research date: 2026-10-06.
Scope: Legere as a free, non-commercial, politically neutral voting-advice site for the April 2027 French presidential election, published by a private individual living in Switzerland, static hosting, no backend, no cookies, no analytics, answers kept in the visitor's `localStorage`.
The French page body is `data/legal.html` ("Mentions légales et confidentialité"); this file is the English working checklist behind it.

This is research, not legal advice.
Items marked **LAWYER** are where a short consultation with a French media or election lawyer (one hour is enough) is worth more than this document.

Decisions taken on 2026-10-06, after this research:
- The poll table was removed from the site, so the poll-law items (loi 77-808 caption, range presentation, poll freeze) no longer apply as long as no poll is shown again.
- Host: Vercel Inc. at https://legere.vandecatsije.com; the host block in `data/legal.html` is filled in except Vercel's phone number.
- Publisher: Mathieu is named, without a postal address; the contact email is still a placeholder.
- Done in the UI: self-hosted fonts with OFL files, source links and a presumption-of-innocence line on judicial cases, "Condamnations pénales" label with its rule, `removeItem` on reset, `noopener noreferrer` on external links, photo credits noting the crop and black-and-white edit.

Status legend: **DONE** = in the repo now; **TO DO** = must happen before a public launch; **DECIDE** = Mathieu's call; **N/A** = researched and does not apply.

## 0. Does living in Switzerland change anything?

Mostly no: French law applies because the site is in French, about a French election, and aimed at French voters.
- French criminal courts accept jurisdiction over online content aimed at a French audience, so defamation (loi 1881), the poll law (loi 77-808) and the Code électoral reach Mathieu regardless of where he lives.
- The poll law covers polls "publiés, diffusés ou rendus publics sur le territoire national" (loi 77-808, art. 1); a site aimed at France is published in France.
- The GDPR applies through art. 3(2)(a): a controller outside the EU offering a service, even free, to people in the EU.
  Switzerland has an EU adequacy decision, so data flowing to Mathieu is not a problematic transfer.
- The Swiss Federal Act on Data Protection (nFADP/nLPD) also applies to him as a Swiss-resident controller; the same privacy notice satisfies its information duty (art. 19 nFADP).
- Swiss telecom law (LTC art. 45c) allows storage on the user's device if the user is informed of it and its purpose and told they can refuse it; the privacy section covers this.

Where his residence does matter:
- **GDPR art. 27 representative.** A non-EU controller under art. 3(2) must appoint an EU representative unless processing is occasional, does not involve large-scale special-category data and is unlikely to create risk (art. 27(2)(a)).
  Legere never receives the answers and only the host sees access logs, so the exemption very likely applies.
  Status: **DECIDE / LAWYER** (low risk; note the reasoning in the processing record).
- **Campaign-finance exposure.** Only natural persons who are French nationals or resident in France may give to a candidate (Code électoral L.52-8, as amended by loi 2017-1339).
  If a judge ever treated Legere as partisan help for one candidate, its cost would be an in-kind donation from someone who may not be allowed to give at all.
  Strict, demonstrable neutrality (section 4) is the protection.
- **EU political-advertising rules.** Regulation (EU) 2024/900 (TTPA), in force since 10 October 2025, bars third-country sponsors (Swiss residents included) from buying political ads in the three months before an election (art. 5(2)).
  See item 1.7.
- **Domain.** If he wants a `.fr` domain, AFNIC accepts holders resident in Switzerland, and individuals' WHOIS data is not published by default (verify on afnic.fr at registration).

## 1. Must do before publishing

### 1.1 Complete the poll notice (loi 77-808, art. 2, 9, 11, 12) - TO DO

Legere shows the Toluna Harris Interactive poll for M6/RTL (fieldwork 8-10 September 2026).
Its notice was filed with the Commission des sondages as notice 10263, "Pres IV TOLUNA HARRIS INTERACTIVE RTL 14 septembre" ([notice PDF](https://www.commission-des-sondages.fr/notices/medias/fichiers/add/2276), [list](https://www.commission-des-sondages.fr/notices/)).
Art. 2 lists eight indications that must accompany a published poll ([text of the law](https://www.commission-des-sondages.fr/pdf/Loi77.pdf)).
Strictly, art. 2 binds the "première publication", but art. 9 lets the Commission order any later publisher to add missing indications or publish a correction, and art. 12 punishes publishing a poll "en violation de la présente loi" with a fine of up to EUR 75,000.
The pollster's own notice says every re-use must repeat the margin-of-error statement and name "Toluna Harris Interactive pour M6 et RTL".

Check of the current `data/meta.json` `polls.source` string against art. 2:

| # | Art. 2 indication | In meta.json? |
|---|---|---|
| 1 | Name of the polling organisation | Yes ("Toluna Harris Interactive") |
| 2 | Name and capacity of the client/buyer | Yes ("pour M6/RTL"); use "pour M6 et RTL" as the pollster asks |
| 3 | Number of people interviewed | Partly: "2 052 inscrits"; the notice says 2 052 registered voters drawn from a sample of 2 358 people representative of the French population aged 18+ |
| 4 | Fieldwork dates | Yes ("du 8 au 10 septembre 2026") |
| 5 | Full text of the question(s) | **Missing** (may sit on the publisher's own site with its address given; now in `data/legal.html`) |
| 6 | Statement that every poll has margins of error | **Missing** ("Un sondage n'est pas une prévision" in `src/app.html` is not this statement) |
| 7 | The margins of error of the published results | **Missing** (notice: between +/-1.4 and +/-3.1 points depending on the score; may sit on the publisher's site; now in `data/legal.html`) |
| 8 | Right of anyone to consult the notice at the Commission des sondages | **Missing** |
| - | Date of first publication and the medium (needed to keep the table online during the eve-of-vote ban, art. 11) | **Missing** (notice dated 14 September 2026; confirm the actual publication date) |

Suggested `polls.source` text (another agent owns `data/meta.json` and `src/app.html`):

> Sondage Toluna Harris Interactive pour M6 et RTL, publié le [date], réalisé en ligne du 8 au 10 septembre 2026 auprès de 2 052 personnes inscrites sur les listes électorales (échantillon de 2 358 personnes représentatif des Français de 18 ans et plus). Tout sondage est affecté de marges d'erreur (ici de 1,4 à 3,1 points). Question posée et marges d'erreur : voir les mentions légales. Notice consultable auprès de la Commission des sondages (commission-des-sondages.fr).

The UI must also link from the poll table to the legal page, because art. 2 allows items 5 and 7 off the page only if the publisher points to where they are.

**Range presentation - DECIDE / LAWYER.**
Legere shows each candidate's lowest and highest score across five line-up hypotheses.
That number is not a result the pollster published, and art. 9 lets the Commission order a correction for publication "en altérant la portée des résultats obtenus".
Art. 1 also treats "opérations de simulation de vote réalisées à partir de sondages" as polls in their own right.
The Commission's 2022 report shows how hard it pushed pollsters away from multi-hypothesis "fourchettes" to one reference column ([rapport annuel 2022](https://www.commission-des-sondages.fr/hist/pdf/rapport-annuel-2022.pdf)).
Safest option: show one named hypothesis with its exact figures, or every hypothesis in full.
If he keeps the range, the caption must say it is a min-max across hypotheses (`data/legal.html` already does).
Also re-check every figure against the notice tables before launch, since the result tables in the PDF are images.

**Never call Legere or any of its outputs a "sondage".**
Art. 12 1° fines using the word "sondage" for an election-related survey that is not a representative-sample poll.
Legere must not publish aggregate user statistics ("X % des utilisateurs...").
The current code collects nothing, so this holds as long as no analytics or results counter is added.

### 1.2 Eve-of-vote and voting-day freeze (loi 77-808 art. 11; Code électoral L.49, L.48-1) - TO DO

- For the presidential election, the poll ban runs from **Saturday 00:00 before each round** until the last polling station in metropolitan France closes (20:00 Sunday), and later for overseas territories whose polls close later (art. 11, art. 14).
- During that window nothing new about polls may be published or commented "par quelque moyen que ce soit".
  Polls published earlier may stay online only if the date of first publication, the medium and the pollster are shown (art. 11, last paragraph).
- Code électoral L.49: from midnight on the eve of the vote, no message "ayant le caractère de propagande électorale" may be disseminated electronically; L.48-1 extends all propaganda rules to online communication.
  A neutral VAA is not propaganda, but the conservative practice is to change nothing during that window.
- Recommended rule for Legere: deploy nothing from Friday 23:59 to Sunday 20:00 (Paris time) before each round, post nothing about Legere on social media in that window, and either hide the poll table for those days or make sure item 1.1 is complete.
- The dates are not official yet.
  `data/meta.json` says 18 April and 2 May 2027; press reports say 11 and 25 April or 18 April are both possible ([LCP](https://lcp.fr/actualites/pourquoi-la-presidentielle-2027-se-jouera-entre-le-11-avril-et-le-2-mai-434190)).
  The convocation decree will fix them; update `meta.json` then.
- Status: **TO DO** (calendar reminder, and a build flag to hide polls if he wants one).

### 1.3 Mentions légales: publisher and host identification (LCEN art. 1-1, created by loi SREN art. 48) - TO DO

The SREN law (loi n° 2024-449 du 21 mai 2024, [art. 48](https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000049563632)) moved publisher identification from old LCEN art. 6 III into new art. 1-1, with penalties in art. 1-2 (one year and EUR 75,000).
- A professional publisher who is an individual must show name, first names, home address and phone number, plus the director of publication and the host's name, address and phone number.
- A **non-professional** publisher may stay anonymous and show only the host's name and address, provided he has given his identity to the host (art. 1-1, II).
  Mathieu publishing a free side project qualifies as non-professional.
- `data/method.html` ("Qui a fait Legere") already names him, and `data/legal.html` names him as publisher and director of publication without address or phone, which the law allows.
  **DECIDE:** keep his name (recommended: a named author makes the neutrality claim credible and the right of reply workable), or go anonymous, in which case remove his name from both pages and make sure the host account holds his real identity.
- Fill the host block from the chosen host's own legal page (company name, legal form, postal address, phone number).
- Status: **TO DO** (placeholders below); the footer link to the page on every screen is being added by another agent.

### 1.4 Contact for corrections and right of reply (LCEN art. 1-1, III; décret n° 2007-1527) - TO DO

- Anyone named or designated on the site has a right of reply for three months after the content went online.
  The publisher must insert the reply within three days of receiving it, on pain of a EUR 3,750 fine.
  If the publisher is anonymous, the request goes to the host, which forwards it.
- The site needs a working, monitored email address; `data/legal.html` uses it for both corrections and right of reply.
- Use an address that does not reveal more than he wants (a dedicated alias is fine).
- Practical rule: answer every candidate or campaign request within 72 hours and log what was changed.

### 1.5 Privacy notice (GDPR art. 13; nFADP art. 19; loi Informatique et Libertés art. 82; LTC art. 45c) - DONE in draft, placeholders TO DO

What is actually processed:
- **Answers in `localStorage`.** Political opinions are special-category data (GDPR art. 9), but the answers never leave the visitor's device and Mathieu never has access to them.
  Saving them is still "writing to the terminal" under art. 82 loi I&L (French transposition of the ePrivacy directive).
  Consent is not needed because the storage is strictly necessary for a service the user explicitly asked for (resuming the questionnaire), the same logic as the CNIL's exempt examples of a shopping basket or an interface choice ([CNIL, cookies et traceurs](https://www.cnil.fr/cookies-traceurs-que-dit-la-loi); [lignes directrices, délibération n° 2020-091](https://www.cnil.fr/sites/cnil/files/atoms/files/lignes_directrices_de_la_cnil_sur_les_cookies_et_autres_traceurs.pdf)).
  The CNIL still expects users to be informed, so no banner, but a clear notice.
- **Host access logs** (IP address, time, URL, user agent) are personal data; Mathieu is controller and the host is his processor, or an independent controller for its own security logs, depending on the host's terms.
  Legal basis: legitimate interest (art. 6(1)(f)).
  The household exemption does not apply to a site open to the public (CJEU C-101/01 Lindqvist).
- **Fonts.** Loading Google Fonts sends every visitor's IP to Google (a German court awarded a visitor damages for this: LG München I, 3 O 17493/20, 20 January 2022).
  `src/app.html` still loads `fonts.googleapis.com` at lines 7-9; self-hosting is in progress elsewhere and must land before launch.
- **Portraits** are served from `public/candidates/`, so there is no hotlinking to Wikimedia.
- **Outbound source links** use `rel="noopener"`; add `noreferrer` too if he wants zero leakage (the answers are not in the URL, so the leak is only "came from Legere").

What `data/legal.html` already says: no server, no account, no cookies, no analytics; what is stored and under which key; that answers can reveal political opinions and are visible to anyone using the same browser; how to delete (the "Tout recommencer" button or browser settings); logs at the host with legal basis, retention and transfer; rights and the CNIL complaint route.

Other GDPR duties:
- DPO: not required (art. 37); Legere's core activity is not large-scale processing of special-category data because it never receives the answers.
- DPIA: not required; nothing on the CNIL list fits.
- Record of processing (art. 30): the under-250-employee exemption does not cover non-occasional processing, and logs are continuous.
  Keep a five-line record (purpose, data, host, retention, legal basis) in this repo or his notes.
  Status: **TO DO** (10 minutes).
- Data processing agreement with the host: all four candidate hosts offer a standard DPA in their terms; accept it when creating the account.
- US hosts: transfers rely on the EU-US Data Privacy Framework, upheld by the General Court on 3 September 2025 (Latombe, T-553/23); an appeal (C-703/25 P) is pending, so mention the DPF in the notice and check the status before launch ([WilmerHale](https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20251201-european-court-of-justice-to-review-challenge-to-eu-us-data-privacy-framework)).
  Switzerland has its own Swiss-US DPF since 15 September 2024.
- Minor improvement: "Tout recommencer" currently overwrites the key with a fresh state; calling `localStorage.removeItem("legere-2027-v1")` would be a cleaner erase.
  It is reachable only from the home screen; consider exposing it on the result screen too.

### 1.6 Candidate information: defamation, presumption of innocence, sources - TO DO (review), LAWYER for the wording

- **Defamation** (loi du 29 juillet 1881, art. 29 and 32): any allegation of a fact that harms someone's honour.
  The defences are proof of truth or good faith (legitimate aim, no personal animosity, care in wording, sufficient factual basis).
  Prosecution must start within three months of publication (art. 65), and the online director of publication is the first person liable (loi n° 82-652, art. 93-3).
  Every judicial or biographical line on a candidate page must have a source link; today the "Affaires judiciaires" card in `src/app.html` (around line 992) shows the case text, status and date but no source.
- **Presumption of innocence** (Code civil art. 9-1): presenting someone as guilty before a final conviction lets the judge order a correction or insertion, even in summary proceedings.
  The status labels ("condamnation, recours en cours", "mise en examen", "enquête") are the right approach.
  Add the sentence "Toute personne mise en cause est présumée innocente tant qu'elle n'a pas été définitivement condamnée." directly under the "Affaires judiciaires" card and under the "Condamnations" column of the profile table, as well as on the legal page (done).
  The column header "Condamnations" next to cases still under appeal is the riskiest wording on the site; consider "Condamnations (définitives ou non)" or "Procédures".
- Keep each case status current (README "Next" already plans the Le Pen Cour de cassation update); a stale "recours en cours" after a final acquittal or a stale "mise en examen" after a dismissal is where liability arises.
- "Comment la presse le présente" is attributed opinion and low risk as long as each summary is balanced and sourced.
- Same evidentiary bar for every candidate: a case listed for one candidate and an equivalent case omitted for another is both a neutrality and a good-faith problem.

### 1.7 No paid promotion during the campaign (Code électoral L.52-1; Regulation (EU) 2024/900) - TO DO (rule to follow)

- L.52-1: from the first day of the sixth month before the month of the election (so **since 1 October 2026** for an April 2027 vote) until the vote, any commercial advertising for electoral propaganda through the press or audiovisual communication is banned.
  Courts apply it to paid social-media posts; it applies to the presidential election through loi n° 62-1292 du 6 novembre 1962, art. 3.
  A neutral VAA is not propaganda, but a paid ad mentioning candidates invites the argument.
- The TTPA regulation treats a paid message "liable and designed to influence the outcome of an election" as political advertising, with labelling duties and a ban on third-country sponsors within three months of the vote.
- Meta stopped all political, electoral and social-issue ads in the EU from October 2025, and Google announced the same in November 2024, so such ads are not even available ([report](https://www.business-humanrights.org/de/neuste-meldungen/european-union-meta-to-halt-political-advertising-from-october-citing-eu-rules)).
- Rule: share Legere organically only; no boosted posts, no paid search ads.
  `data/legal.html` states the site has no paid advertising.

### 1.8 Portraits: licences and image rights - TO DO (verify per photo)

- Image rights: French case law lets the press publish images of public figures without consent when the image relates to their public role and the information of the public, subject to respect for dignity.
  An official-style portrait next to a candidate's political positions fits that; avoid unflattering or private-context pictures, and use comparable framing and quality for every candidate (neutrality).
- Copyright: each Wikimedia Commons file carries its own licence (CC BY, CC BY-SA 2.0/3.0/4.0, CC0, public domain, sometimes Licence Ouverte for official portraits).
  CC BY and CC BY-SA require attribution: author, licence name with a link, link to the source file, and a statement that the image was modified ([CC BY-SA 4.0 legal code](https://creativecommons.org/licenses/by-sa/4.0/legalcode), section 3(a)).
  Format per portrait: "Photo : [auteur], [licence avec lien], via Wikimedia Commons, recadrée."
- ShareAlike: cropping makes an adaptation, so the cropped file itself stays under CC BY-SA.
  The page that shows it does not become CC BY-SA; placing an image next to text is not an adaptation of the image.
- `build.py` reads `data/photos.json` for credits (another agent's work); check that every entry has author, licence, licence URL and source URL, and that each "Personality rights" warning template on Commons is respected.
- `data/legal.html` states that the portraits were cropped and resized; correct that sentence if the final files are not modified.

### 1.9 Fonts licence - TO DO

Spectral and IBM Plex Sans are under the SIL Open Font License 1.1, which allows self-hosting but requires the copyright notice and licence to travel with the font files.
Put `OFL.txt` next to the font files in `public/`.

## 2. Mathieu must decide

| Topic | Options | Recommendation |
|---|---|---|
| Anonymity | Named publisher (current) vs anonymous with host details only | Named; it is lawful without address or phone and supports credibility |
| Host | GitHub Pages, Cloudflare Pages, Netlify, Vercel | Any; pick one with an EU region or a DPA plus DPF certification, then fill the host placeholders |
| Poll display | Min-max range (current) vs one named hypothesis vs every hypothesis | One named hypothesis or every hypothesis (**LAWYER** if keeping the range) |
| Poll table on the weekends of the votes | Keep (legal if item 1.1 is complete) vs hide | Hide; simpler and closer to the spirit of the law |
| Candidate list | Current 12 vs all official candidates once the Conseil constitutionnel publishes the list (about four weeks before round 1) | Cover every official candidate, or publish the inclusion rule on the method page; no law forces it, but neutrality and L.52-8 both point that way |
| GDPR representative | None (art. 27(2) exemption) vs appoint one | None, with the reasoning written in the processing record (**LAWYER** if traffic becomes large) |
| Name "Legere" | Keep vs rename | Search INPI, EUIPO and Swissreg before buying a domain; non-commercial use is not "use in the course of trade", so trademark risk is low, but a domain dispute is still a nuisance |

## 3. Done or already handled by the design

- No cookies, analytics or third-party trackers: no consent banner is needed (art. 82 loi I&L exemption plus information in the privacy section).
- Answers never leave the device: no special-category processing by Mathieu, no DPO, no DPIA.
- Candidates not named before the result, no party colours, same method for all: this is the neutrality evidence for L.52-8 and good faith under the 1881 law.
- AI disclosure: the method page says the research used AI assistants and was checked source by source.
  EU AI Act art. 50(4) (labelling AI-generated text on matters of public interest, applicable since 2 August 2026) excludes content under human editorial responsibility and probably does not reach a private non-professional deployer anyway, so this disclosure is more than enough.
- The word "sondage" is used only for the real poll.

## 4. Neutrality and election rules that do not directly bind Legere

- ARCOM's equal-treatment and speaking-time recommendations for the presidential election bind radio and TV services only; ARCOM's 2027 recommendation was still expected this autumn.
  They are still a useful yardstick for equal treatment.
- L.48-2 (new polemical element too late for a reply) binds candidates, not third parties.
- L.97 (false news that diverts votes) and the L.163-2 summary procedure against "deliberate, artificial or automated and massive" false allegations in the three months before the election target disinformation campaigns, not a sourced VAA; accuracy and a fast correction process keep it that way.
- L.163-1 transparency duties apply only to platforms above 5 million unique monthly visitors in France.
- The DSA obligations for hosts and platforms do not apply to Mathieu as a publisher.

## 5. Not applicable

- Digital accessibility law (loi n° 2005-102, art. 47; European Accessibility Act transposed by loi n° 2023-171) covers public bodies, large companies and consumer e-commerce, not a free personal site.
  Following RGAA basics voluntarily is still good practice.
- Swiss "impressum" duty (UWG art. 3(1)(s)) covers e-commerce only.
- Minors: GDPR art. 8 applies only to consent-based processing, which Legere does not do; non-voters using the tool raise no legal issue.
- Consumer-law information duties: no sale, no contract.

## 6. Placeholders in `data/legal.html` that Mathieu must fill

- `[ADRESSE E-MAIL DE CONTACT]` (two occurrences plus the mailto links).
- `[NOM DE L'HÉBERGEUR]`, `[FORME JURIDIQUE DE L'HÉBERGEUR]`, `[ADRESSE POSTALE DE L'HÉBERGEUR]`, `[TÉLÉPHONE DE L'HÉBERGEUR]`.
- `[DURÉE DE CONSERVATION DES JOURNAUX PAR L'HÉBERGEUR]`, `[PAYS DE L'HÉBERGEUR]`, `[GARANTIE APPLICABLE AU TRANSFERT ...]` (from the host's privacy policy and DPA).
- `[DATE DE PREMIÈRE PUBLICATION PAR M6 ET RTL]` (the notice is dated 14 September 2026; confirm on RTL or M6).
- `[DATE DE MISE À JOUR]`.
- When the displayed poll changes, update the "Sondage affiché" panel (question, sample, margins) together with `data/meta.json`.

## 7. Changes needed in files owned by others

- `data/meta.json`: replace `polls.source` with the complete notice text in 1.1 and add the first-publication date.
- `src/app.html`: link the poll caption to the legal page; replace "Un sondage n'est pas une prévision" with, or add, "Tout sondage est affecté de marges d'erreur"; add a source link to each judicial case; add the presumption-of-innocence sentence under "Affaires judiciaires" and the "Condamnations" table; reconsider the "Condamnations" header; remove the Google Fonts links (lines 7-9) once fonts are self-hosted; optionally `removeItem` on reset and `noreferrer` on source links.
- `public/`: add `OFL.txt` with the fonts.
- `data/photos.json`: author, licence, licence URL, source URL and "recadrée" for every portrait.

## Sources

- Loi n° 2004-575 (LCEN), art. 1-1 and 1-2 as created by loi n° 2024-449 (SREN), art. 48: https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000049563632
- Loi n° 77-808 du 19 juillet 1977 (consolidated by the Commission des sondages): https://www.commission-des-sondages.fr/pdf/Loi77.pdf
- Commission des sondages, notices: https://www.commission-des-sondages.fr/notices/ ; notice of the displayed poll: https://www.commission-des-sondages.fr/notices/medias/fichiers/add/2276
- Commission des sondages, annual report 2022: https://www.commission-des-sondages.fr/hist/pdf/rapport-annuel-2022.pdf
- Code électoral (L.48-1, L.48-2, L.49, L.52-1, L.52-8, L.97, L.163-1, L.163-2): https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006070239
- Loi du 29 juillet 1881 sur la liberté de la presse: https://www.legifrance.gouv.fr/loda/id/LEGITEXT000006070722
- Code civil, art. 9-1: https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006070721
- CNIL, cookies et autres traceurs: https://www.cnil.fr/cookies-traceurs-que-dit-la-loi
- CNIL guidelines (délibération n° 2020-091 of 17 September 2020): https://www.cnil.fr/sites/cnil/files/atoms/files/lignes_directrices_de_la_cnil_sur_les_cookies_et_autres_traceurs.pdf
- GDPR (Regulation (EU) 2016/679): https://eur-lex.europa.eu/eli/reg/2016/679/oj
- Regulation (EU) 2024/900 on political advertising: https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/democracy-eu-citizenship-anti-corruption/democracy-and-electoral-rights/transparency-and-targeting-political-advertising_en
- EU AI Act (Regulation (EU) 2024/1689): https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- Swiss nFADP: https://www.fedlex.admin.ch/eli/cc/2022/491/fr ; LTC art. 45c: https://www.fedlex.admin.ch/eli/cc/1997/2187_2187_2187/fr
- CC BY-SA 4.0 legal code: https://creativecommons.org/licenses/by-sa/4.0/legalcode
- EU-US DPF appeal status: https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20251201-european-court-of-justice-to-review-challenge-to-eu-us-data-privacy-framework
- Meta ending political ads in the EU: https://www.business-humanrights.org/de/neuste-meldungen/european-union-meta-to-halt-political-advertising-from-october-citing-eu-rules
- Election dates (not yet official): https://lcp.fr/actualites/pourquoi-la-presidentielle-2027-se-jouera-entre-le-11-avril-et-le-2-mai-434190
