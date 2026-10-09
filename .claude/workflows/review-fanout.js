export const meta = {
  name: 'review-fanout',
  description: 'Review every changed file with cheap haiku finders, then have the framework reviewer try to refute each finding',
  whenToUse: 'A branch touches many files and one review pass would skim. For a handful of files, /review-code is simpler.',
  phases: [
    { title: 'Scope', detail: 'list files changed against the base branch', model: 'haiku' },
    { title: 'Find', detail: 'one haiku finder per file', model: 'haiku' },
    { title: 'Verify', detail: 'framework-code-reviewer tries to refute each finding' },
  ],
}

// One file per finder keeps each haiku prompt far below its 100K price threshold.
// Verification runs as framework-code-reviewer, so it keeps that agent's own tier.

const FILES = {
  type: 'object',
  required: ['files'],
  properties: { files: { type: 'array', items: { type: 'string' } } },
}
const FINDINGS = {
  type: 'object',
  required: ['findings'],
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['line', 'summary'],
        properties: { line: { type: 'integer' }, summary: { type: 'string' } },
      },
    },
  },
}
const VERDICT = {
  type: 'object',
  required: ['refuted', 'reason'],
  properties: { refuted: { type: 'boolean' }, reason: { type: 'string' } },
}

const base = (args && args.base) || 'main'

// A model transcribing `git diff` output once returned the repo root as the only
// "file", so one finder reviewed everything. Prefer a list passed in args, and
// keep only repo-relative file paths from the scope agent.
const isFile = p => typeof p === 'string' && !p.startsWith('/') && !p.startsWith('archive/')
  && /\.[A-Za-z0-9]+$/.test(p)

phase('Scope')
let candidates = args && Array.isArray(args.files) ? args.files : null
if (!candidates) {
  const scope = await agent(
    `Run \`git diff --name-only ${base}...HEAD\` and return its output lines exactly, one entry ` +
    `per line, as repo-relative paths. Do not summarize, group, or return directories.`,
    { model: 'haiku', effort: 'low', schema: FILES },
  )
  candidates = scope ? scope.files : []
}
const files = candidates.filter(isFile)
if (files.length < candidates.length) {
  log(`Dropped ${candidates.length - files.length} entries that are not repo-relative files`)
}
if (files.length === 0) {
  log(`No files to review against ${base}`)
  return []
}
log(`${files.length} files to review against ${base}`)

const perFile = await pipeline(
  files,
  file => agent(
    `Review ${file} for correctness defects: wrong logic, broken references, contract violations. ` +
    `Report only concrete defects with a line number. Return an empty list if there are none.`,
    { label: `find:${file}`, phase: 'Find', model: 'haiku', effort: 'low', schema: FINDINGS },
  ),
  (found, file) => parallel((found ? found.findings : []).map(f => () =>
    agent(
      `Try to refute this finding in ${file} at line ${f.line}: "${f.summary}". ` +
      `Read the code. Default to refuted=true unless you can show the defect is real.`,
      { label: `verify:${file}:${f.line}`, phase: 'Verify', agentType: 'framework-code-reviewer', schema: VERDICT },
    ).then(v => (v && !v.refuted ? { file, line: f.line, summary: f.summary, why: v.reason } : null)),
  )).then(vs => vs.filter(Boolean)),
)

return perFile.filter(Boolean).flat()
