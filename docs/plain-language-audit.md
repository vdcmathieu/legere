# Plain-language audit

Branch `plain-language`, audited 6 October 2026.
Scope: 31 statements rewritten (28 for plain language, 3 reordered for layout) in everyday French (`fr`), a one-sentence `plain_fr` status quo added to all 80 statements, the `GLOSS` definitions fact-checked, and `data/method.html` updated.
The English `en` field is the meaning anchor the candidate codings were made against; it was not edited.
Every rewrite was checked against `en` by the author, then audited independently by gpt-6-astra (Codex CLI, read-only, with its own web search).

## Rewritten statements

| id | old fr | new fr | en | audit verdict |
|---|---|---|---|---|
| eco1 | Rétablir un impôt sur la fortune incluant le patrimoine financier (type ISF). | Rétablir un impôt annuel sur les grandes fortunes qui taxe aussi les placements financiers, et pas seulement l'immobilier (type ISF). | Reinstate a wealth tax that includes financial assets (ISF-style). | OK (Codex OK). |
| eco3 | Baisser les impôts de production et les cotisations sociales payées par les entreprises. | Baisser les impôts de production, que les entreprises paient quel que soit leur bénéfice, et les cotisations sociales qu'elles versent sur les salaires. | Cut production taxes and employer social contributions to boost business competitiveness. | OK. Codex MINOR: en carries the purpose clause "to boost competitiveness"; rejected, the earlier wording audit removed purpose clauses from all statements on purpose (persuasive). Reworded once more so the glossary term is not preceded by a bracket. |
| eco7 | Augmenter la TVA pour financer une baisse des cotisations sociales sur les salaires (« TVA sociale »). | Augmenter la TVA pour financer une baisse des cotisations sociales sur les salaires, ce qu'on appelle la TVA sociale. | Raise VAT to fund lower social contributions on wages ('social VAT'). | Reworded after the Codex audit only to keep the glossary term out of brackets (layout); same words, same meaning. Self-checked against en. |
| fin4 | Inscrire dans la Constitution une règle limitant le déficit public (« règle d'or »). | Inscrire dans la Constitution une règle d'or, c'est-à-dire une règle limitant le déficit public. | Write a deficit-limiting 'golden rule' into the Constitution. | Same: reordered so « règle d'or » is in running text. Self-checked against en. |
| trav1 | Donner au SMIC un « coup de pouce » nettement supérieur à sa revalorisation automatique sur l'inflation. | Augmenter le SMIC nettement plus que l'inflation, au-delà de sa hausse automatique (un « coup de pouce »). | Raise the minimum wage significantly faster than inflation. | OK. Codex MINOR ("above the automatic rise" is extra); rejected: the automatic rise is the inflation indexation, so the two clauses say the same thing, as in the old fr. |
| imm3 | Remplacer l'aide médicale d'État (AME) par une aide limitée aux soins urgents. | Limiter aux soins urgents la prise en charge gratuite des soins des étrangers en situation irrégulière (remplacer l'aide médicale d'État, AME). | Replace state medical aid for undocumented migrants (AME) with urgent-care-only aid. | OK (Codex OK). |
| imm4 | Régulariser les travailleurs sans papiers dans les métiers en tension. | Donner un titre de séjour aux travailleurs sans papiers employés dans les métiers en tension, ceux qui manquent de main-d'œuvre. | Regularise undocumented workers in labour-shortage occupations. | OK (Codex OK). Reordered after the audit so the glossary term is in running text (layout only; same words). |
| sec1 | Instaurer des peines minimales obligatoires pour les récidivistes (peines planchers). | Fixer dans la loi des peines planchers, c'est-à-dire une peine minimale que le juge doit prononcer contre les récidivistes. | Introduce mandatory minimum sentences for repeat offenders. | OK (Codex OK). Reordered after the audit so the glossary term is in running text (layout only; same words). |
| sec3 | Confier les enquêtes sur les fautes des policiers et gendarmes à un organisme indépendant, à la place de l'IGPN et de l'IGGN. | Confier les enquêtes sur les fautes des policiers et gendarmes à un organisme indépendant de la police, à la place de ses services internes (IGPN, IGGN). | Give oversight of the police to a body independent of the police. | OK vs old fr. Codex PROBLEM: both old and new fr narrow "oversight" to misconduct investigations and name IGPN/IGGN. Pre-existing scope, unchanged by the rewrite; flagged for the coding owner rather than changed here. |
| sec4 | Légaliser et encadrer le cannabis récréatif. | Rendre légal et encadrer le cannabis consommé par loisir, hors usage médical (cannabis récréatif). | Legalise and regulate recreational cannabis. | OK (Codex OK). |
| sec6 | Remettre un récépissé lors de chaque contrôle d'identité pour lutter contre les contrôles au faciès. | Remettre à la personne contrôlée un document écrit (récépissé) lors de chaque contrôle d'identité, pour lutter contre les contrôles au faciès. | Issue a receipt at every identity check to curb ethnic profiling. | Fixed after audit: back to "lors de chaque contrôle d'identité" and no longer "la police" (gendarmes also check identities). |
| int3 | Quitter le commandement intégré de l'OTAN. | Retirer la France du commandement militaire intégré de l'OTAN, c'est-à-dire des structures où les armées alliées planifient et commandent ensemble. | Leave NATO's integrated military command. | OK (Codex OK). |
| int4 | Suspendre l'accord d'association entre l'UE et Israël en raison de la guerre menée à Gaza. | Suspendre l'accord d'association entre l'Union européenne et Israël, qui organise leur commerce et leur coopération, en raison de la manière dont la guerre est menée à Gaza. | Suspend the EU-Israel association agreement over the conduct of the Gaza war. | Fixed after audit: "en raison de la manière dont la guerre est menée à Gaza" to match en "over the conduct of the Gaza war" (old fr had the same gap). Reordered after the audit so the glossary term is in running text (layout only; same words). |
| ecol1 | Supprimer les zones à faibles émissions (ZFE) dans les villes. | Supprimer les zones à faibles émissions (ZFE), qui limitent la circulation des véhicules les plus polluants dans les grandes villes. | Abolish low-emission zones (ZFE) in cities. | OK (Codex OK). |
| ecol3 | Maintenir l'objectif européen de 100 % de voitures neuves sans émissions en 2035 (fin des ventes de thermiques neuves), plutôt que l'assouplir. | Maintenir la fin de la vente des voitures neuves à moteur thermique (essence, diesel, hybrides), prévue en 2035 par l'Union européenne, plutôt que l'assouplir. | Keep the 2035 end of sales of new combustion-engine cars. | Fixed after audit: "moteur thermique (essence, diesel, hybrides)" instead of "essence ou diesel" (combustion engines in general). |
| ecol6 | Garantir aux agriculteurs des prix minimaux (prix planchers) pour leurs produits. | Garantir aux agriculteurs des prix planchers, c'est-à-dire des prix minimaux pour leurs produits. | Guarantee farmers minimum floor prices for their produce. | Same: reordered so « prix planchers » is in running text. Self-checked against en. |
| ene1 | Construire de nouveaux réacteurs nucléaires au-delà des six EPR2 déjà engagés, par exemple les huit réacteurs supplémentaires à l'étude. | Construire de nouveaux réacteurs nucléaires en plus des six déjà prévus (EPR2), par exemple les huit supplémentaires à l'étude. | Build new nuclear reactors beyond the six EPR2 already planned. | Fixed after audit: "déjà prévus" instead of "déjà engagés" (en: planned; EDF's final investment decision is still pending). |
| ene3 | Décréter un moratoire sur l'installation de nouvelles éoliennes, terrestres et en mer. | Suspendre l'installation de toute nouvelle éolienne, sur terre comme en mer (moratoire). | Halt the development of new wind turbines. | OK. Codex MINOR (moratorium is temporary, en says halt); unchanged from old fr and "moratoire" is the term used in the programmes. |
| ins1 | Changer de constitution pour passer à une VIe République plus parlementaire. | Adopter une nouvelle Constitution donnant plus de pouvoir au Parlement, pour remplacer la Ve République actuelle par une VIe République. | Adopt a new constitution for a more parliamentary Sixth Republic. | OK (Codex OK). |
| ins2 | Élire les députés à la proportionnelle. | Élire les députés à la proportionnelle, c'est-à-dire répartir les sièges entre les partis selon leur part des voix. | Elect MPs by proportional representation. | Fixed after audit: dropped "au lieu d'un seul élu par circonscription" so mixed systems are not excluded. |
| ins3 | Créer un référendum d'initiative citoyenne (RIC). | Permettre aux citoyens de déclencher eux-mêmes un référendum en réunissant assez de signatures (référendum d'initiative citoyenne, RIC). | Create a citizens' initiative referendum (RIC). | OK (Codex OK). |
| ins4 | Supprimer ou restreindre fortement l'usage de l'article 49.3. | Supprimer ou limiter fortement l'article 49.3, qui permet au gouvernement de faire adopter une loi sans vote des députés. | Abolish or strongly restrict use of Article 49.3. | OK (Codex OK). |
| soc1 | Maintenir la loi de 2026 qui ouvre, sous conditions strictes, un droit à l'aide à mourir. | Maintenir la loi de 2026 qui autorise l'aide à mourir sous conditions strictes. | Allow assisted dying under strict conditions. | Partly fixed: removed the eligibility description (now in plain_fr); kept "Maintenir la loi de 2026", a deliberate re-stem from the earlier audit because the law has passed (en still reads "Allow assisted dying", same direction). |
| soc3 | Interdire les signes religieux ostensibles aux parents qui accompagnent les sorties scolaires. | Interdire aux parents qui accompagnent les sorties scolaires de porter des signes religieux bien visibles (« ostensibles »). | Ban conspicuous religious symbols for parents accompanying school trips. | OK (Codex OK). |
| soc5 | Autoriser la gestation pour autrui (GPA) non commerciale, dans un cadre strict. | Autoriser, dans un cadre strict et sans rémunération, qu'une femme porte un enfant pour un couple ou une personne qui en deviendra parent (gestation pour autrui, GPA). | Allow regulated, non-commercial surrogacy. | Fixed after audit: "un couple ou une personne" restored so single intended parents are covered. |
| soc6 | Interdire les signes religieux ostensibles à l'université. | Interdire le port de signes religieux bien visibles (« ostensibles ») à l'université. | Ban conspicuous religious symbols at university. | OK (Codex OK). |
| edu3 | Rendre obligatoires au collège les groupes de niveau (« groupes de besoins ») en français et en mathématiques. | Rendre obligatoires au collège les groupes de besoins, c'est-à-dire le regroupement des élèves par niveau en français et en mathématiques. | Group lower-secondary pupils by ability level in some subjects. | OK vs old fr. Codex PROBLEM: "rendre obligatoire" and French/maths are not in en ("some subjects"). Pre-existing re-stem decided by the earlier audit because the groups became optional in 2026; unchanged here, flagged for the coding owner. Reordered after the audit so the glossary term is in running text (layout only; same words). |
| edu4 | Réduire le financement public des écoles privées sous contrat qui ne respectent pas des objectifs de mixité sociale. | Réduire l'argent public versé aux écoles privées sous contrat avec l'État qui n'atteignent pas des objectifs de mixité sociale (accueil d'élèves de tous milieux). | Cut public funding for state-contracted private schools that miss social-mix targets. | OK (Codex OK). |
| san2 | Augmenter la part des soins laissée à la charge des patients (franchises et forfaits). | Augmenter la part du coût des soins que les patients paient eux-mêmes, via les franchises et forfaits (par exemple sur les médicaments et les consultations). | Increase patient co-payments to control health spending. | Fixed after audit: back to "la part du coût des soins que les patients paient eux-mêmes", with medicines and consultations only as examples (franchises also apply to other acts and transport). Purpose clause "to control spending" rejected, as for eco3. Reordered after the audit so the glossary term is in running text (layout only; same words). |
| san3 | Encadrer les loyers dans toutes les zones où le logement est rare. | Encadrer les loyers, c'est-à-dire imposer un loyer maximum aux propriétaires, dans toutes les zones où les logements manquent. | Cap rents in all areas with housing shortages. | OK (Codex OK). Reordered after the audit so the glossary term is in running text (layout only; same words). |
| san5 | Assouplir les normes de construction et l'objectif « zéro artificialisation nette » (ZAN) pour construire davantage de logements. | Assouplir les règles de construction et l'objectif « zéro artificialisation nette » (ZAN), qui limite la construction sur des terres naturelles ou agricoles, pour bâtir plus de logements. | Loosen building rules and the zero-net-land-take target to build more housing. | OK (Codex OK). |

## GLOSS corrections (`src/app.html`)

Every factual claim in the 37 definitions was checked against a dated source as of October 2026.
Entries not listed below were found correct (ISF threshold 1.3 M€ and 2018 replacement by the IFI; AME three-month residence and means condition; peines planchers 2007-2014; NATO 32 members, 1966 exit and 2009 return; EU-Israel agreement in force since 2000; acétamipride banned in France since 2018 and still authorised in the EU; six EPR2 at Penly, Gravelines and Bugey; franchise 1 € per box and 2 € per consultation; ZAN target 2050 from the 2021 Climat law; RSA about 650 €; rent control in Paris, Lyon, Lille).

| entry | change | source |
|---|---|---|
| SMIC | "environ 1 800 € brut" -> "1 867 € brut par mois depuis juin 2026, soit un peu moins de 1 500 € net" (the June 2026 revaluation of 2.41 % took it past 1 800 €) | [info.gouv.fr, Le SMIC revalorisé le 1er juin 2026](https://www.info.gouv.fr/actualite/le-smic-revalorise-le-1er-juin-2026); [Urssaf, Montant du Smic](https://www.urssaf.fr/accueil/outils-documentation/taux-baremes/montant-smic.html) |
| RSA | kept "environ 650 €", added the exact figure "651,69 € depuis avril 2026" (+0.8 % on 1 April 2026) | [legisocial.fr, RSA 2026](https://www.legisocial.fr/reperes-sociaux/calcul-rsa-revenu-de-solidarite-active-2026.html); [aide-sociale.fr, hausse au 1er avril 2026](https://www.aide-sociale.fr/rsa-augmentation/) |
| groupes de besoins | "mise en place à partir de 2024 en 6e et 5e" -> "Obligatoires en 6e et 5e de 2024 à 2026, ils sont facultatifs depuis la rentrée 2026" (decree of 12 March 2026) | [cnews.fr, 13 March 2026](https://www.cnews.fr/france/2026-03-13/college-les-groupes-de-besoin-deviendront-facultatifs-des-la-rentree-2026-1830648); [apel.fr](https://www.apel.fr/actualites/les-groupes-de-besoin-au-college-deviennent-facultatifs) |
| ZAN | "sols bétonnés ou bâtis" -> "terres naturelles ou agricoles transformées en zones bâties ou aménagées" (wording closer to the legal definition of artificialisation, and "bétonnés" read as loaded) | Loi Climat et résilience 2021, art. 192 (définition de l'artificialisation) |
| key `3 % du PIB` | renamed `sous 3 % du PIB`: the old key also matched int5 ("Porter le budget de la défense à plus de 3 % du PIB") and showed the deficit-rule definition on a defence statement | code check (`termify` regex run over all 80 `fr`) |
| key `Encadrer les loyers` | renamed `encadrement des loyers` to match the rewritten san3 | code check |
| key `répartition` | kept, but edu3 was reworded ("regroupement des élèves" instead of "répartition des élèves") so the pension-system definition no longer fires on a school statement | code check |
| new entry `ostensibles` | definition of "signes religieux ostensibles" (term of the 2004 law, with the examples given by its application circular), used by the rewritten soc3 and soc6 | Loi n° 2004-228 du 15 mars 2004 and circulaire du 18 mai 2004 |

No entry was removed: after the rewrites every key still matches exactly one statement (`ostensibles` matches soc3 and soc6 by design).

Facts corrected in `plain_fr` relative to the longer `today_fr` source texts in `data/audit.json`:

| statement | correction | source |
|---|---|---|
| fin1 | 2025 deficit was 5.1 % of GDP (INSEE, 27 March 2026), not "environ 5,4 %" | [INSEE Informations rapides n° 78](https://www.insee.fr/fr/statistiques/8956575) |
| fin3 | debt 115.6 % of GDP at end 2025 ("environ 116 %" kept); dropped the unverified comparison with Spain | same INSEE release |
| san5 | the 2026 loosening of the 2031 ZAN milestone was censured by the Conseil constitutionnel (decision 2026-903 DC, 21 May 2026) rather than "débattu à l'Assemblée" | [maire-info.com](https://www.maire-info.com/lois/zfe-et-zan-le-conseil-constitutionnel-sauve-deux-dispositifs-controverses-article-30811); [batiactu.com](https://www.batiactu.com/edito/conseil-constitutionnel-censure-assouplissement-zan-74522.php) |
| sec5 | the extension of algorithmic video surveillance to 2030 (loi RIPOST, CMP of 21 July 2026) is stated instead of the vaguer "prolongé et élargi en 2025-2026" | [publicsenat.fr](https://www.publicsenat.fr/actualites/parlementaire/loi-ripost-le-senat-prolonge-et-etend-le-recours-a-la-video-surveillance-algorithmique) |
| san3 | about 70 communes under rent control; expiry 23 November 2026; the extension bill reaches the Sénat on 21 October 2026 | [actu-juridique.fr](https://www.actu-juridique.fr/fiscalite/fiscal-finances/pas-de-clap-de-fin-pour-lencadrement-des-loyers/) |
| soc1 | promulgation date 18 August 2026 kept; the Conseil constitutionnel decision date (13 August per most reports, 14 in the source text) is omitted | [franceinfo](https://www.franceinfo.fr/societe/euthanasie/la-loi-sur-l-aide-a-mourir-a-ete-promulguee-par-emmanuel-macron-macron-et-publiee-au-journal-officiel_8153051.html) |

Facts verified and kept: pension age frozen at 62 ans 9 mois until January 2028 (LFSS 2026); three uses of 49.3 for the 2026 budget in January 2026; ZFE abolition struck down on 21 May 2026 as a legislative rider; franchises cap raised to 140 € on 1 October 2026 (décret 2026-858); PPE3 decree of 12 February 2026 with 6 EPR2 and 8 more as an option; first Ukraine accession clusters opened 15 June and 14 July 2026; no unanimity on suspending the EU-Israel agreement on 21 April 2026; 21st Russia sanctions package 23 July 2026; civic exam mandatory for naturalisation since 1 January 2026; SNU ended 1 January 2026 and the ten-month voluntary military service takes its first 3 000 volunteers in autumn 2026; Commission proposal of 16 December 2025 to lower the 2035 car target to 90 %.

## Independent audit by gpt-6-astra (Codex CLI)

Run: `codex exec -s read-only -c model_reasoning_effort=high`, with the 28 old/new/en triples, all 80 `plain_fr` and the full GLOSS in the prompt; the model made about 100 web searches.
It found no loaded wording and no candidate or party named.
Its findings and what was done with them:

### Meaning (28 rewrites)

- Applied (8): sec6, int4, ecol3, ene1, ins2, soc1 (partly), soc5, san2. See the table above.
- Rejected (4): eco3, ret2, trav2 and san2 "restore the purpose clause present in `en`" ("to boost competitiveness", "to balance the system", "to encourage return to work", "to control health spending").
  The earlier wording audit (`data/audit.json`) removed these clauses deliberately because a justification inside the item pushes toward agreement; the measure itself is what the candidates were coded on.
  trav1 (automatic rise = inflation indexation, so nothing is added) and ene3 (moratoire, unchanged from the old fr).
- Pre-existing, not changed, flagged for the coding owner (5): sec3 and edu3 (old and new fr both narrower or more specific than `en`), and outside the 28, imm2 (fr asks for a constitutional revision, en for a referendum), trav3 (fr says "maintain the 15-20 h obligation", en "make RSA conditional"), soc4 (fr drops "state neutrality").
  These are re-stems made by the earlier audit when the status quo changed; aligning `en` or the codings is a separate decision.

### Neutrality (80 statements)

- Applied: removed "déjà" from the eco3 and trav2 `plain_fr` ("déjà allégées", "déjà durcies" read as "enough already").
- Rejected: the same purpose-clause point as above.

### Facts (80 `plain_fr`, 38 GLOSS)

Applied, after checking the source Codex gave or my own:

- ret3 and GLOSS capitalisation: funded pensions also exist in a compulsory form (RAFP for civil servants); "n'existe qu'à titre volontaire" was false.
- fin2: about 5.9 million public employees (DGAFP, end 2024), not 5.7.
- fin3: debt 3 595.5 bn, 119.0 % of GDP at end Q2 2026 (INSEE Informations rapides n° 239), replacing the end-2025 snapshot.
- imm1: about 380 000 first residence permits in 2025 (ministry of the Interior, 27 January 2026: 377 000 provisional, 384 230 in the later release), not 330 000.
- imm6: birthright citizenship requires residence at 18 and five years' residence since age 11.
- imm3 and GLOSS AME: the three-month condition does not apply to minors.
- imm5: the RSA condition is five years holding a residence permit allowing work.
- trav3: the contract provides at least 15 hours in principle, with adjustments, and a breach "can" lead to suspension.
- trav4: full-time employees report close to 39 usual weekly hours (INSEE 2025), not 37.
- sec1: the judge chooses within the statutory frame, without a mandatory minimum (other constraints exist).
- sec2: the judge can already set aside the minority excuse case by case for 16-18-year-olds; what was censured in 2025 was making that the rule.
- sec6: "aucun récépissé" instead of "aucune trace écrite"; the unverified 2016 vote replaced by the 2023 Conseil d'État decision from the source text.
- eu1: EU law primacy over statutes, with the Constitution remaining supreme domestically, instead of "the only exception is constitutional identity".
- eu2: 750 bn and 150 bn are envelopes ("jusqu'à").
- eu4 and GLOSS unanimité: unanimity "en principe"; abstention does not block.
- eu8: "aucune date n'est fixée" instead of the forecast "prendra des années".
- int1, int2: no general ceasefire "début octobre 2026"; the claim restricted to the reassurance force.
- int5: 57 bn is the defence mission excluding pensions.
- int6: the suspension of conscription was decided in 1997.
- ecol4: kerosene on commercial flights is untaxed; the "international agreements" justification dropped (domestic taxation is legally possible).
- ecol6: "pas de prix minimum légal garanti" (EU intervention prices exist).
- ene1 and GLOSS EPR2: "prévus" rather than "engagés".
- ene3: wind targets cut relative to the previous draft programme.
- ene4 and GLOSS marché européen: interconnected national markets with hourly prices, no single continent-wide price; regulated tariffs do not track spot prices directly.
- ins1: a constituent assembly is not a procedure the current Constitution provides.
- ins2: proportional representation used once "sous la Ve République".
- ins4: "sauf adoption d'une motion de censure".
- ins5, imm2: Article 11 exclusions stated less categorically.
- san1: "médecins libéraux", "proposition de loi".
- san2: two separate 70 € annual ceilings (franchises and participations forfaitaires), not one 140 € ceiling (décret 2026-858).
- soc2: full-face veil ban in force since April 2011 (law of October 2010); school ban concerns "ostensible" symbols.
- edu4: three quarters of costs covered by public money overall (State and local authorities), not by the State alone.
- GLOSS ISF (net taxable wealth above 1.3 M€), règle d'or (a rule the proposal wants in the Constitution, not one that is there), RSA (maximum amount before deductions), regroupement familial (spouse and minor children, under conditions), peines planchers (the "décision motivée" exception attributed to the 2007-2014 regime), acétamipride (approved at EU level), audiovisuel public (INA is an archive body), franchises (not reimbursed by the Assurance maladie), ZAN (net balance made explicit), encadrement des loyers (per zone and dwelling type), ostensibles (manifesting "ostensiblement"; discreet symbols allowed).

Rejected or left as is:

- GLOSS proportionnelle "au lieu du scrutin actuel où un seul candidat gagne": describes the current system, kept.
- eu3 net contribution "d'une dizaine de milliards": Codex "not verified"; the order of magnitude is the Commission's own figure for 2023 and the phrasing is already approximate.
- fin3 comparison with Germany: Codex "not verified"; the OAT-Bund spread has been positive throughout, kept.
- ins6 "aucune privatisation n'est engagée": Codex "not verified"; confirmed by the earlier explainer audit, kept.
- eco6 (donation allowance renews every 15 years), eco5 wording, eco1 (IFI scale starts at 800 k€ once liable): detail beyond a one-sentence box, not added.
- sec4 "le plus souvent" for the fixed fine: kept; the amende forfaitaire délictuelle is the standard response to simple use.

Everything else in the Codex fact table was marked OK.

## Follow-ups outside this branch's scope

- `termify()` renders glossary terms as `<button>` elements, which are inline-block and therefore wrap as a unit: a multi-word term after an opening bracket leaves the bracket orphaned at the end of a line, and the closing bracket can fall on the next line (seen on eco3 and san3 at 360 px). All statements were reworded so that multi-word glossary terms sit in running text (eco3, sec1, imm4, int4, edu3, san2, san3, and the pre-existing eco7, fin4, ecol6); single-word terms such as "(type ISF)" or "(EPR2)" can still break at other widths. Suggested fix in `src/app.html` (not touched here, outside the GLOSS object): emit a `<span class="term" role="button" tabindex="0">` with a keydown handler, or split the button per word.
- The results screen still says « Sans vos "compte beaucoup" » in the robustness table (`src/app.html`, `specs` in `screens.results`); the chip is now "Important pour moi".
- en/fr alignment for sec3, edu3, imm2, trav3, soc4 (see above).

