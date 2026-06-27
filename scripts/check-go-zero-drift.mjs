#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const repoRoot = process.cwd();
const upstream = 'zeromicro/go-zero';
const token = process.env.GH_TOKEN || process.env.GITHUB_TOKEN || '';
const baseRefInput = process.env.BASE_REF || '';
const headRefInput = process.env.HEAD_REF || '';
const maxFiles = Number(process.env.MAX_FILES || 300);

const RULES = [
  {
    name: 'goctl and code generation',
    patterns: [/^tools\/goctl\//, /^tools\/goctl-/, /^tools\/goctl_/, /^tools\/goctl\.go$/],
    docs: [
      'src/content/docs/reference/cli-guide/',
      'src/content/docs/reference/api-dsl/',
      'src/content/docs/reference/proto-dsl/',
      'src/content/docs/getting-started/',
      'src/content/docs/guides/quickstart/',
    ],
  },
  {
    name: 'HTTP server and client',
    patterns: [/^rest\//, /^core\/handler\//],
    docs: [
      'src/content/docs/guides/http/',
      'src/content/docs/reference/configuration/api-config.md',
      'src/content/docs/community/faq/http/',
    ],
  },
  {
    name: 'gRPC and zRPC',
    patterns: [/^zrpc\//, /^rpc\//],
    docs: [
      'src/content/docs/guides/grpc/',
      'src/content/docs/reference/configuration/rpc-config.md',
      'src/content/docs/reference/proto-dsl/',
    ],
  },
  {
    name: 'Gateway',
    patterns: [/^gateway\//],
    docs: ['src/content/docs/guides/gateway/'],
  },
  {
    name: 'Configuration loading',
    patterns: [/^core\/conf\//, /^core\/mapping\//, /^core\/configcenter\//],
    docs: [
      'src/content/docs/reference/configuration/',
      'src/content/docs/guides/microservice/config-center.md',
    ],
  },
  {
    name: 'Service configuration',
    patterns: [/^core\/service\//],
    docs: [
      'src/content/docs/reference/configuration/service-config.md',
      'src/content/docs/guides/microservice/',
    ],
  },
  {
    name: 'Redis, cache, and storage',
    patterns: [/^core\/stores\/redis\//, /^core\/stores\/cache\//, /^core\/stores\/sql/, /^core\/stores\/mon/],
    docs: [
      'src/content/docs/components/cache/',
      'src/content/docs/guides/database/',
      'src/content/docs/reference/cli-guide/model.md',
    ],
  },
  {
    name: 'Resilience and traffic protection',
    patterns: [/^core\/breaker\//, /^core\/limit\//, /^core\/load\//, /^core\/stat\//],
    docs: [
      'src/content/docs/components/resilience/',
      'src/content/docs/guides/microservice/load-balancing.md',
    ],
  },
  {
    name: 'Concurrency utilities',
    patterns: [/^core\/fx\//, /^core\/mr\//, /^core\/syncx\//, /^core\/threading\//],
    docs: ['src/content/docs/components/concurrency/'],
  },
  {
    name: 'Logging',
    patterns: [/^core\/logx\//, /^core\/logc\//],
    docs: [
      'src/content/docs/components/log/',
      'src/content/docs/reference/configuration/log.md',
      'src/content/docs/community/faq/log/',
    ],
  },
  {
    name: 'Observability',
    patterns: [/^core\/trace\//, /^core\/metric\//, /^core\/prometheus\//, /^core\/prof\//],
    docs: [
      'src/content/docs/components/observability/',
      'src/content/docs/guides/microservice/distributed-tracing.md',
    ],
  },
  {
    name: 'Message queues',
    patterns: [/^core\/queue\//, /^core\/stores\/kafka\//],
    docs: [
      'src/content/docs/components/queue/',
      'src/content/docs/guides/queue/',
    ],
  },
  {
    name: 'MCP',
    patterns: [/^mcp\//, /^core\/mcp\//],
    docs: ['src/content/docs/guides/mcp/'],
  },
  {
    name: 'Examples and demos',
    patterns: [/^example\//, /^examples\//, /^demo\//],
    docs: ['src/content/docs/examples/'],
  },
];

function setOutput(name, value) {
  if (process.env.GITHUB_OUTPUT) {
    fs.appendFileSync(process.env.GITHUB_OUTPUT, `${name}=${String(value).replace(/\n/g, '%0A')}\n`);
  }
}

function ymd(date = new Date()) {
  return new Date(date).toISOString().slice(0, 10);
}

function slug(value) {
  return String(value).toLowerCase().replace(/[^a-z0-9._-]+/g, '-').replace(/^-|-$/g, '');
}

async function github(pathname) {
  const headers = {
    Accept: 'application/vnd.github+json',
    'User-Agent': 'zeromicro-autodoc-drift',
  };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`https://api.github.com${pathname}`, { headers });
  if (!res.ok) {
    throw new Error(`GitHub API ${pathname} failed: ${res.status} ${await res.text()}`);
  }
  return res.json();
}

async function defaultBranch() {
  const repo = await github(`/repos/${upstream}`);
  return repo.default_branch || 'master';
}

async function latestReleaseTag() {
  const release = await github(`/repos/${upstream}/releases/latest`);
  return release.tag_name;
}

async function resolveRefs() {
  const head = headRefInput || (await defaultBranch());
  const base = baseRefInput || (await latestReleaseTag());
  return { base, head };
}

async function compareRefs(base, head) {
  return github(`/repos/${upstream}/compare/${encodeURIComponent(base)}...${encodeURIComponent(head)}`);
}

function matchRules(filename) {
  return RULES.filter((rule) => rule.patterns.some((pattern) => pattern.test(filename)));
}

function uniq(values) {
  return [...new Set(values)];
}

function relatedLocalizedDocs(docs) {
  const localized = [];
  for (const doc of docs) {
    localized.push(doc);
    if (doc.startsWith('src/content/docs/')) {
      const suffix = doc.slice('src/content/docs/'.length);
      localized.push(`src/content/docs/zh-cn/${suffix}`);
      localized.push(`src/content/docs/ko/${suffix}`);
    }
  }
  return uniq(localized);
}

function classify(files) {
  const topics = new Map();
  const unmatched = [];

  for (const file of files) {
    const matches = matchRules(file.filename);
    if (!matches.length) {
      unmatched.push(file);
      continue;
    }

    for (const rule of matches) {
      if (!topics.has(rule.name)) {
        topics.set(rule.name, {
          name: rule.name,
          docs: new Set(rule.docs),
          files: [],
        });
      }
      topics.get(rule.name).files.push(file);
    }
  }

  return { topics: [...topics.values()], unmatched };
}

function tableRows(files) {
  if (!files.length) return '| Status | File |\n| --- | --- |\n| - | No files |\n';
  return [
    '| Status | File |',
    '| --- | --- |',
    ...files.map((file) => `| ${file.status} | \`${file.filename}\` |`),
  ].join('\n');
}

function renderReport({ base, head, compare, topics, unmatched }) {
  const today = ymd();
  const compareUrl = `https://github.com/${upstream}/compare/${base}...${head}`;
  const changedFiles = compare.files || [];
  const truncated = changedFiles.length >= maxFiles ? `\n\n:::caution\nThe report considered the first ${maxFiles} files returned by GitHub. Re-run with a narrower compare range if needed.\n:::\n` : '';

  const sections = topics.map((topic) => {
    const docs = relatedLocalizedDocs([...topic.docs]).map((doc) => `- \`${doc}\``).join('\n');
    return `## ${topic.name}\n\n### Changed Upstream Files\n\n${tableRows(topic.files)}\n\n### Documentation To Review\n\n${docs}\n`;
  }).join('\n');

  const unmatchedSection = unmatched.length
    ? `## Unmatched Changes\n\nThese files did not match a documentation ownership rule. Review whether a new rule or docs update is needed.\n\n${tableRows(unmatched)}\n`
    : '## Unmatched Changes\n\nNo unmatched upstream changes.\n';

  return `# go-zero Upstream Drift Report\n\n- Captured: ${today}\n- Upstream: \`${upstream}\`\n- Base: \`${base}\`\n- Head: \`${head}\`\n- Compare: ${compareUrl}\n- Commits ahead: ${compare.ahead_by ?? 'unknown'}\n- Changed files reviewed: ${changedFiles.length}\n${truncated}\n## Summary\n\n${topics.length ? topics.map((topic) => `- **${topic.name}**: ${topic.files.length} changed file(s), review ${topic.docs.size} doc area(s).`).join('\n') : '- No owned documentation areas matched upstream changes.'}\n\n${sections || '## Matched Documentation Areas\n\nNo matched documentation areas.\n'}\n${unmatchedSection}\n## Suggested Review Workflow\n\n1. Read the changed upstream files for each matched area.\n2. Check the listed English docs first, then mirror necessary updates into \`zh-cn\` and \`ko\`.\n3. Update \`docs-memory/index.md\` if this reveals a new durable maintenance theme.\n4. Run \`npm run validate\` and \`npm run build\`.\n`;
}

function writeIfChanged(file, content) {
  const current = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : '';
  if (current === content) return false;
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content);
  return true;
}

function updateMemoryIndex(reportRelPath) {
  const file = path.join(repoRoot, 'docs-memory/index.md');
  if (!fs.existsSync(file)) return false;
  let content = fs.readFileSync(file, 'utf8');
  const line = `- [Latest upstream drift report](${reportRelPath.replace(/^docs-memory\//, '')}) - mapped go-zero source changes to documentation areas.`;

  if (content.includes('Latest upstream drift report')) {
    content = content.replace(/- \[Latest upstream drift report\]\([^)]+\) - mapped go-zero source changes to documentation areas\./, line);
  } else {
    content = content.replace('## Known Maintenance Themes', `${line}\n\n## Known Maintenance Themes`);
  }
  return writeIfChanged(file, content);
}

function updateMemoryLog(base, head, reportRelPath, topics) {
  const file = path.join(repoRoot, 'docs-memory/log.md');
  if (!fs.existsSync(file)) return false;
  let content = fs.readFileSync(file, 'utf8');
  const today = ymd();
  const heading = `## [${today}] lint | go-zero upstream drift ${base}...${head}`;
  if (content.includes(heading)) return false;

  const entry = `${heading}\n\n- Generated \`${reportRelPath}\`.\n- Matched ${topics.length} documentation ownership area(s).\n- Review the report before editing public docs.\n\n`;
  content = content.replace('\n## ', `\n${entry}## `);
  return writeIfChanged(file, content);
}

async function main() {
  const { base, head } = await resolveRefs();
  const compare = await compareRefs(base, head);
  const files = (compare.files || []).slice(0, maxFiles);
  const { topics, unmatched } = classify(files);
  const hasChanges = files.length > 0 && topics.length > 0;

  const reportName = `${slug(base)}...${slug(head)}.md`;
  const reportRelPath = `docs-memory/reports/${reportName}`;
  const reportPath = path.join(repoRoot, reportRelPath);
  const report = renderReport({ base, head, compare: { ...compare, files }, topics, unmatched });

  let changed = false;
  if (hasChanges || process.env.WRITE_EMPTY_REPORT === 'true') {
    changed = writeIfChanged(reportPath, report) || changed;
    changed = updateMemoryIndex(reportRelPath) || changed;
    changed = updateMemoryLog(base, head, reportRelPath, topics) || changed;
  }

  setOutput('has_changes', changed ? 'true' : 'false');
  setOutput('base_ref', base);
  setOutput('head_ref', head);
  setOutput('report_path', reportRelPath);
  setOutput('topic_count', topics.length);
  setOutput('file_count', files.length);

  console.log(JSON.stringify({
    base,
    head,
    fileCount: files.length,
    topicCount: topics.length,
    reportPath: reportRelPath,
    changed,
  }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
