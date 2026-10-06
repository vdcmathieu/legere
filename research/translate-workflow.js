export const meta = {
  name: 'translate-research-fr',
  description: 'Translate the English research summaries for 12 candidates into neutral French',
  phases: [{ title: 'Translate', detail: 'sonnet: one agent per candidate' }],
}

const ROOT = '/Users/mathieu.vandecatsije/Code/Legere/research/fr'
const CANDS = ['lepen','melenchon','philippe','attal','retailleau','zemmour','glucksmann','faure','tondelier','roussel','ruffin','lisnard']

const results = await parallel(CANDS.map(c => () => agent(
  `Translate ${ROOT}/in/${c}.json into French and write the result to ${ROOT}/out/${c}.json with the Write tool.

Rules:
- Keep exactly the same JSON structure, keys, array lengths and order; translate only the string values. Keep "id" values unchanged.
- Register: neutral, precise French as in a fact-checking or parliamentary-reporting context (Les Décodeurs, Public Sénat). No added judgement, no softening or sharpening.
- Use the official French names of laws, bodies and procedures (e.g. "Cour de cassation", "mise en examen", "projet de loi de financement de la sécurité sociale", "49.3").
- Keep proper names, party names, acronyms and outlet names as they are. Keep numbers and dates exact; write dates in French style.
- Empty strings stay empty.
Validate that the file parses as JSON (e.g. python3 -c "import json;json.load(open(...))"), then return "ok ${c}".
Keep reasoning bursts short and make tool calls steadily.`,
  { label: `translate:${c}`, phase: 'Translate', model: 'sonnet', effort: 'low' })))
return results
