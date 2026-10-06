export const meta = {
  name: 'candidate-position-supplement',
  description: 'Code 12 candidates on 14 new or reworded VAA statements, then adversarially verify',
  phases: [
    { title: 'Collect', detail: 'sonnet: one agent per candidate x (statements A | statements B | record)' },
    { title: 'Verify', detail: 'opus: adversarial source check and correction per job' },
  ],
}

const ROOT = '/Users/mathieu.vandecatsije/Code/Legere/research'

const POS_SCHEMA = {type:'object',required:['candidate','positions'],properties:{
  candidate:{type:'string'},
  positions:{type:'array',items:{type:'object',
    required:['id','position','confidence','evidence_type','summary','sources','nuance'],
    properties:{
      id:{type:'string'},
      position:{type:['integer','null'],minimum:-2,maximum:2},
      confidence:{type:'string',enum:['high','medium','low','none']},
      evidence_type:{type:'string',enum:['programme','statement','vote','record_in_office','party_line','inferred','none']},
      summary:{type:'string'},
      sources:{type:'array',items:{type:'object',required:['url','outlet','outlet_lean','date','quote'],
        properties:{url:{type:'string'},outlet:{type:'string'},
          outlet_lean:{type:'string',enum:['far-left','left','centre-left','centre','centre-right','right','far-right','neutral-institutional','campaign-or-party','think-tank','fact-check']},
          date:{type:'string'},quote:{type:'string'}}}},
      nuance:{type:'string'}}}},
  verification_notes:{type:'array',items:{type:'string'}}}}

const REC_SCHEMA = {type:'object',required:['candidate','bio','offices','executive_experience_years','legal','reversals','delivery','traits','media_portrayal','sources_note'],properties:{
  candidate:{type:'string'}, bio:{type:'string'},
  offices:{type:'array',items:{type:'object',required:['office','from','to','kind'],properties:{office:{type:'string'},from:{type:'string'},to:{type:'string'},kind:{type:'string',enum:['national_executive','local_executive','legislative','party','european','other']}}}},
  executive_experience_years:{type:'number'},
  legal:{type:'array',items:{type:'object',required:['case','status','date','sources'],properties:{case:{type:'string'},status:{type:'string',enum:['convicted_final','convicted_appeal_pending','indicted','investigation','acquitted','dismissed','civil_or_other']},date:{type:'string'},sources:{type:'array',items:{type:'string'}}}}},
  reversals:{type:'array',items:{type:'object',required:['topic','before','after','years','sources'],properties:{topic:{type:'string'},before:{type:'string'},after:{type:'string'},years:{type:'string'},sources:{type:'array',items:{type:'string'}}}}},
  delivery:{type:'array',items:{type:'object',required:['what','assessment','sources'],properties:{what:{type:'string'},assessment:{type:'string'},sources:{type:'array',items:{type:'string'}}}}},
  traits:{type:'array',items:{type:'object',required:['trait','evidence','source_leans'],properties:{trait:{type:'string'},evidence:{type:'string'},source_leans:{type:'array',items:{type:'string'}}}}},
  media_portrayal:{type:'object',required:['left_media','right_media','neutral_media'],properties:{left_media:{type:'string'},right_media:{type:'string'},neutral_media:{type:'string'}}},
  sources_note:{type:'string'},
  verification_notes:{type:'array',items:{type:'string'}}}}

const CANDS = ['lepen','melenchon','philippe','attal','retailleau','zemmour','glucksmann','faure','tondelier','roussel','ruffin','lisnard']
const JOBS = CANDS.map(c => `${c}_C`)

const PACING = `Working rules: load WebSearch and WebFetch with ToolSearch ("select:WebSearch,WebFetch") before starting. Keep reasoning bursts short and make tool calls steadily - an agent with no completed tool call for 180 s is killed, so never think for long stretches between searches. Some sites (CNews, Le Monde paywall) may block fetching - fall back to search snippets and other outlets.`

const collect = job => agent(
  `Read the file ${ROOT}/prompts/${job}.txt and carry out the research task it describes, using WebSearch and WebFetch. Return the result through the structured output tool (leave verification_notes empty).\n\n${PACING}`,
  { label: `collect:${job}`, phase: 'Collect', model: 'sonnet', effort: 'medium', schema: job.endsWith('_R') ? REC_SCHEMA : POS_SCHEMA })

const verify = (draft, job) => {
  if (!draft) return null
  const isRec = job.endsWith('_R')
  const task = isRec
    ? `Adversarially verify this track-record profile. Re-check every legal case status and date against a primary or neutral source (court releases, AFP, franceinfo, Le Monde, Public Sénat) - status labels must be exact (presumption of innocence). Check offices and executive_experience_years arithmetic. Drop any reversal that is not a genuine documented change of position. Drop any trait not attested by sources of at least two different leanings. Check that media_portrayal is balanced and descriptive, not judgemental. Remove any URL you cannot confirm exists.`
    : `Adversarially verify this coding. For EVERY position coded +2/-2 or with evidence_type programme/vote/record_in_office, open or search the cited evidence and confirm it supports the code on the statement EXACTLY as worded (statements are in ${ROOT}/prompts/${job}.txt). Then sample at least 8 other positions the same way. Look actively for: outdated positions (changed in 2025-2026), party line mistaken for the candidate's own view, an opponent's characterisation taken as the position, off-by-one strength errors, null positions where evidence actually exists (search briefly for each null), and fabricated or dead URLs. Correct the codes, confidences and sources where needed.`
  return agent(
    `You are a skeptical, politically neutral fact-checker for a French 2027 presidential voting-advice application. Apply the same evidentiary bar to every candidate whatever their politics.\n\nThe research brief is in ${ROOT}/prompts/${job}.txt (read it first).\n\n${task}\n\nReturn the full corrected object (all entries, not just changed ones) through the structured output tool, and list every change you made, with the reason, in verification_notes (format: "<id>: <old> -> <new>: <reason>").\n\nDraft to verify:\n${JSON.stringify(draft)}\n\n${PACING}`,
    { label: `verify:${job}`, phase: 'Verify', model: 'opus', effort: 'medium', schema: isRec ? REC_SCHEMA : POS_SCHEMA })
    .then(v => ({ job, draft, verified: v }))
}

const results = await pipeline(JOBS, collect, verify)
const ok = results.filter(r => r && r.verified)
log(`${ok.length}/${JOBS.length} jobs verified; missing: ${JOBS.filter(j => !ok.find(r => r.job === j)).join(', ') || 'none'}`)
return results.filter(Boolean)
