#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = process.cwd();
const upstream = 'zeromicro/go-zero';
const token = process.env.GH_TOKEN || process.env.GITHUB_TOKEN || '';
const requestedTag = process.env.RELEASE_TAG || process.argv[2] || '';
const model = process.env.AI_MODEL || 'gpt-4o-mini';
const endpoint = process.env.AI_ENDPOINT || 'https://models.inference.ai.azure.com/chat/completions';

const output = {};

function setOutput(name, value) {
  output[name] = String(value);
  if (process.env.GITHUB_OUTPUT) {
    fs.appendFileSync(process.env.GITHUB_OUTPUT, `${name}=${String(value).replace(/\n/g, '%0A')}\n`);
  }
}

function readFile(file) {
  return fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : '';
}

function writeFileIfChanged(file, content) {
  const current = readFile(file);
  if (current === content) return false;
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content);
  return true;
}

async function github(pathname) {
  const headers = {
    Accept: 'application/vnd.github+json',
    'User-Agent': 'zeromicro-autodoc-sync',
  };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`https://api.github.com${pathname}`, { headers });
  if (!res.ok) {
    throw new Error(`GitHub API ${pathname} failed: ${res.status} ${await res.text()}`);
  }
  return res.json();
}

async function getRelease() {
  if (requestedTag) {
    return github(`/repos/${upstream}/releases/tags/${encodeURIComponent(requestedTag)}`);
  }
  return github(`/repos/${upstream}/releases/latest`);
}

function extractCompareTags(body) {
  const match = body.match(/github\.com\/zeromicro\/go-zero\/compare\/([^.\s]+)\.\.\.([^\s)]+)/);
  return match ? { base: match[1], head: match[2] } : null;
}

async function findPreviousTag(release) {
  const fromBody = extractCompareTags(release.body || '');
  if (fromBody?.base) return fromBody.base;

  const releases = await github(`/repos/${upstream}/releases?per_page=30`);
  const currentIndex = releases.findIndex((item) => item.tag_name === release.tag_name);
  if (currentIndex >= 0 && releases[currentIndex + 1]) {
    return releases[currentIndex + 1].tag_name;
  }
  return '';
}

async function getCompare(base, head) {
  if (!base || !head) return null;
  try {
    return await github(`/repos/${upstream}/compare/${encodeURIComponent(base)}...${encodeURIComponent(head)}`);
  } catch (error) {
    console.warn(`Could not fetch compare ${base}...${head}: ${error.message}`);
    return null;
  }
}

function ymd(date) {
  return new Date(date).toISOString().slice(0, 10);
}

function slugTag(tag) {
  return tag.toLowerCase().replace(/^v/, 'v').replace(/[^a-z0-9.-]/g, '-');
}

function escapeYaml(value) {
  return String(value).replace(/"/g, '\\"');
}

function trimMarkdown(value) {
  return String(value || '').trim().replace(/\n{3,}/g, '\n\n');
}

export function validateRelease(release) {
  const tag = String(release?.tag_name || '').trim();
  if (!/^v\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$/.test(tag)) {
    throw new Error(`GitHub returned an invalid release tag: ${JSON.stringify(release?.tag_name)}`);
  }
  if (!release?.html_url || !(release.published_at || release.created_at)) {
    throw new Error(`GitHub release ${tag} is missing its URL or publication date`);
  }
  return release;
}

function fallbackDoc(release, previousTag, compare) {
  const body = trimMarkdown(release.body || 'No release notes were provided upstream.');
  const changedFiles = compare?.files?.slice(0, 25).map((file) => `- \`${file.filename}\``).join('\n') || '- Not available.';
  const compareLine = previousTag
    ? `\n\n**Full Changelog**: https://github.com/${upstream}/compare/${previousTag}...${release.tag_name}`
    : '';

  return {
    en: `Released on **${ymd(release.published_at || release.created_at)}** - [GitHub Release](${release.html_url})\n\n## Highlights\n\n${body}${compareLine}`,
    zh: `发布于 **${ymd(release.published_at || release.created_at)}** - [GitHub Release](${release.html_url})\n\n## 亮点\n\n${body}${compareLine}`,
    ko: `릴리스 날짜: **${ymd(release.published_at || release.created_at)}** - [GitHub Release](${release.html_url})\n\n## Highlights\n\n${body}${compareLine}`,
    impact: `## Documentation Impact\n\nReview these changed upstream files and update related guides, components, reference pages, and FAQs when needed.\n\n${changedFiles}\n`,
  };
}

function extractJson(text) {
  const fenced = text.match(/```json\s*([\s\S]*?)```/);
  const raw = fenced ? fenced[1] : text;
  const start = raw.indexOf('{');
  const end = raw.lastIndexOf('}');
  if (start < 0 || end < start) throw new Error('model response did not contain a JSON object');
  return JSON.parse(raw.slice(start, end + 1));
}

async function generateWithModel(release, previousTag, compare) {
  if (!token || process.env.DISABLE_AI === 'true') return null;

  const changedFiles = (compare?.files || [])
    .slice(0, 120)
    .map((file) => `${file.status}\t${file.filename}`)
    .join('\n');

  const prompt = `You maintain the go-zero documentation site.

Create release documentation for ${release.tag_name}.

Return only a JSON object with these string fields:
- en: English Markdown body for src/content/docs/reference/releases/${release.tag_name}.md. Do not include frontmatter.
- zh: Simplified Chinese Markdown body for zh-cn.
- ko: Korean Markdown body for ko.
- impact: English Markdown report listing which documentation pages or topics should be reviewed beyond release notes.

Rules:
- Use factual information from the upstream release notes and changed file list only.
- Preserve GitHub PR links when present.
- Keep release docs concise and useful.
- Mention potential breaking changes or migration work only if supported by the notes.
- The first line of each localized release doc should include the release date and GitHub release link.

Release date: ${ymd(release.published_at || release.created_at)}
GitHub release: ${release.html_url}
Previous tag: ${previousTag || 'unknown'}
Compare: ${previousTag ? `https://github.com/${upstream}/compare/${previousTag}...${release.tag_name}` : 'unknown'}

Upstream release notes:
${release.body || '(empty)'}

Changed files:
${changedFiles || '(not available)'}`;

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model,
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.2,
      max_tokens: 5000,
    }),
  });

  if (!res.ok) {
    console.warn(`AI generation failed: ${res.status} ${await res.text()}`);
    return null;
  }

  const data = await res.json();
  const text = data?.choices?.[0]?.message?.content || '';
  try {
    const parsed = extractJson(text);
    if (parsed.en && parsed.zh && parsed.ko && parsed.impact) return parsed;
  } catch (error) {
    console.warn(`AI response could not be parsed: ${error.message}`);
  }
  return null;
}

function frontmatter(tag, locale, date) {
  const prefix = locale === 'root' ? '' : `${locale}/`;
  const description =
    locale === 'zh-cn'
      ? `go-zero ${tag} 发布说明 - ${date}。`
      : locale === 'ko'
        ? `go-zero ${tag} 릴리스 노트 - ${date}.`
        : `go-zero ${tag} release notes - ${date}.`;

  return `---\nslug: ${prefix}reference/releases/${tag}\ntitle: ${tag}\ndescription: "${escapeYaml(description)}"\nsidebar:\n  order: 1\n---\n\n`;
}

function updateReleaseIndex(locale, tag, date) {
  const base = locale === 'root' ? 'src/content/docs' : `src/content/docs/${locale}`;
  const file = path.join(repoRoot, base, 'reference/releases/index.md');
  let content = readFile(file);
  if (!content || content.includes(`[${tag}](${tag}/)`)) return false;

  const minor = tag.match(/^v(\d+)\.(\d+)\./);
  const heading = minor ? `## v${minor[1]}.${minor[2]}.x` : '## Other';
  const line = `- [${tag}](${tag}/) — ${date}`;

  if (content.includes(heading)) {
    content = content.replace(`${heading}\n\n`, `${heading}\n\n${line}\n`);
  } else {
    const firstVersionHeading = content.search(/\n## v\d+\.\d+\.x/);
    if (firstVersionHeading >= 0) {
      content = `${content.slice(0, firstVersionHeading)}\n${heading}\n\n${line}\n${content.slice(firstVersionHeading)}`;
    } else {
      content = `${content.trim()}\n\n${heading}\n\n${line}\n`;
    }
  }
  return writeFileIfChanged(file, content);
}

function updateChangelog(locale, tag, date) {
  const base = locale === 'root' ? 'src/content/docs' : `src/content/docs/${locale}`;
  const file = path.join(repoRoot, base, 'reference/changelog.md');
  let content = readFile(file);
  if (!content) return false;

  const localized = {
    root: {
      section: `## ${tag} – ${date}\n\nFor complete details, see the [${tag} release notes](../releases/${tag}/).\n\n`,
      latest: 'Latest Releases',
      highlight: 'See release notes',
    },
    'zh-cn': {
      section: `## ${tag} – ${date}\n\n完整变更请查看 [${tag} 发布说明](../releases/${tag}/)。\n\n`,
      latest: '最新版本',
      highlight: '查看发布说明',
    },
    ko: {
      section: `## ${tag} – ${date}\n\n전체 변경 사항은 [${tag} 릴리스 노트](../releases/${tag}/)에서 확인하세요.\n\n`,
      latest: '최신 릴리스',
      highlight: '릴리스 노트 보기',
    },
  }[locale];

  if (!new RegExp(`^## ${tag.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[ –-]`, 'm').test(content)) {
    const match = content.match(/^---\n[\s\S]*?\n---\n/);
    if (!match) throw new Error(`${file} has invalid frontmatter`);
    content = content.replace(match[0], `${match[0]}\n${localized.section}`);
  }

  const escapedTag = tag.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  if (!new RegExp(`^\\| \\[${escapedTag}\\]\\(\\.\\./releases/${escapedTag}\\)`, 'm').test(content)) {
    const tableStart = new RegExp(`(## ${localized.latest}\\n\\n\\|[^\\n]+\\n\\|[^\\n]+\\n)`);
    if (!tableStart.test(content)) throw new Error(`${file} is missing its latest-release table`);
    const row = `| [${tag}](../releases/${tag}) | ${date} | ${localized.highlight} |\n`;
    content = content.replace(tableStart, `$1${row}`);
  }

  const releaseCount = fs.readdirSync(path.join(repoRoot, base, 'reference/releases'))
    .filter((name) => /^v.*\.md$/.test(name)).length;
  content = content
    .replace(/\[all \d+ releases →\]/, `[all ${releaseCount} releases →]`)
    .replace(/\[全部 \d+ 个版本 →\]/, `[全部 ${releaseCount} 个版本 →]`)
    .replace(/\[모든 \d+(?:개)? 릴리스(?: 보기)? →\]/, `[모든 ${releaseCount}개 릴리스 보기 →]`);

  return writeFileIfChanged(file, content);
}

function sourcePacket(release, previousTag, compare, impact) {
  const date = ymd(new Date().toISOString());
  const releaseDate = ymd(release.published_at || release.created_at);
  const files = (compare?.files || []).map((file) => `- ${file.status}: \`${file.filename}\``).join('\n') || '- Not available.';

  return `---\ntitle: go-zero ${release.tag_name} release\nsource_type: release\nsource_url: ${release.html_url}\ncaptured_at: ${date}\nrelated_docs:\n  - src/content/docs/reference/releases/${release.tag_name}.md\n  - src/content/docs/zh-cn/reference/releases/${release.tag_name}.md\n  - src/content/docs/ko/reference/releases/${release.tag_name}.md\nstatus: ingested\n---\n\n## Key Facts\n\n- Release: ${release.tag_name}\n- Published: ${releaseDate}\n- Previous tag: ${previousTag || 'unknown'}\n- Compare: ${previousTag ? `https://github.com/${upstream}/compare/${previousTag}...${release.tag_name}` : 'unknown'}\n\n## Upstream Release Notes\n\n${trimMarkdown(release.body || 'No upstream release notes were provided.')}\n\n## Changed Files\n\n${files}\n\n${trimMarkdown(impact)}\n`;
}

function updateMemoryIndex(tag) {
  const file = path.join(repoRoot, 'docs-memory/index.md');
  let content = readFile(file);
  const line = `- [go-zero ${tag} release](sources/go-zero-${slugTag(tag)}.md) - release source packet and documentation impact report.`;

  if (!content || content.includes(`go-zero ${tag} release`)) return false;
  if (content.includes('No source packets have been ingested yet.')) {
    content = content.replace('No source packets have been ingested yet.', line);
  } else {
    content = content.replace('## Known Maintenance Themes', `${line}\n\n## Known Maintenance Themes`);
  }
  return writeFileIfChanged(file, content);
}

function updateMemoryLog(tag) {
  const file = path.join(repoRoot, 'docs-memory/log.md');
  let content = readFile(file);
  const today = ymd(new Date().toISOString());
  const heading = `## [${today}] ingest | go-zero ${tag} release`;
  if (content.includes(heading)) return false;

  const entry = `${heading}\n\n- Captured upstream release notes and changed files for ${tag}.\n- Generated English, Simplified Chinese, and Korean release pages.\n- Added a source packet for future cross-page documentation maintenance.\n\n`;
  content = content.replace('\n## ', `\n${entry}## `);
  return writeFileIfChanged(file, content);
}

async function main() {
  const release = validateRelease(await getRelease());
  const tag = release.tag_name;
  const date = ymd(release.published_at || release.created_at);
  const releaseFiles = [
    path.join(repoRoot, 'src/content/docs/reference/releases', `${tag}.md`),
    path.join(repoRoot, 'src/content/docs/zh-cn/reference/releases', `${tag}.md`),
    path.join(repoRoot, 'src/content/docs/ko/reference/releases', `${tag}.md`),
  ];

  const localizedBases = ['src/content/docs', 'src/content/docs/zh-cn', 'src/content/docs/ko'];
  const allOutputsExist = releaseFiles.every((file) => fs.existsSync(file))
    && localizedBases.every((base) => readFile(path.join(repoRoot, base, 'reference/releases/index.md')).includes(`[${tag}](${tag}/)`))
    && localizedBases.every((base) => {
      const changelog = readFile(path.join(repoRoot, base, 'reference/changelog.md'));
      const escapedTag = tag.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      return changelog.includes(`## ${tag}`)
        && new RegExp(`^\\| \\[${escapedTag}\\]\\(\\.\\./releases/${escapedTag}\\)`, 'm').test(changelog);
    })
    && fs.existsSync(path.join(repoRoot, 'docs-memory/sources', `go-zero-${slugTag(tag)}.md`));

  if (process.env.FORCE_SYNC !== 'true' && allOutputsExist) {
    setOutput('has_changes', 'false');
    setOutput('tag', tag);
    setOutput('release_url', release.html_url);
    console.log(JSON.stringify({ tag, changed: false, reason: 'release docs already exist' }, null, 2));
    return;
  }

  const previousTag = await findPreviousTag(release);
  const compare = await getCompare(previousTag, tag);
  const generated = (await generateWithModel(release, previousTag, compare)) || fallbackDoc(release, previousTag, compare);

  let changed = false;
  const files = [
    ['root', 'en', generated.en],
    ['zh-cn', 'zh', generated.zh],
    ['ko', 'ko', generated.ko],
  ];

  for (const [locale, key, body] of files) {
    const base = locale === 'root' ? 'src/content/docs' : `src/content/docs/${locale}`;
    const file = path.join(repoRoot, base, 'reference/releases', `${tag}.md`);
    changed = writeFileIfChanged(file, `${frontmatter(tag, locale, date)}${trimMarkdown(body)}\n`) || changed;
    changed = updateReleaseIndex(locale, tag, date) || changed;
    changed = updateChangelog(locale, tag, date) || changed;
  }

  const packetFile = path.join(repoRoot, 'docs-memory/sources', `go-zero-${slugTag(tag)}.md`);
  changed = writeFileIfChanged(packetFile, sourcePacket(release, previousTag, compare, generated.impact)) || changed;
  changed = updateMemoryIndex(tag) || changed;
  changed = updateMemoryLog(tag) || changed;

  setOutput('has_changes', changed ? 'true' : 'false');
  setOutput('tag', tag);
  setOutput('release_url', release.html_url);

  console.log(JSON.stringify({ tag, previousTag, changed, output }, null, 2));
}

if (path.resolve(process.argv[1] || '') === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    console.error(error);
    process.exit(1);
  });
}
