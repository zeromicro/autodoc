// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';

/** Remark plugin: convert ```mermaid fences to <pre class="mermaid"> so Mermaid.js renders them */
function remarkMermaid() {
	return (tree) => {
		function walk(node) {
			if (node.children) {
				for (let i = 0; i < node.children.length; i++) {
					const child = node.children[i];
					if (child.type === 'code' && child.lang === 'mermaid') {
						node.children[i] = {
							type: 'html',
							value: `<pre class="mermaid">\n${child.value}\n</pre>`,
						};
					} else {
						walk(child);
					}
				}
			}
		}
		walk(tree);
	};
}

// https://astro.build/config
export default defineConfig({
	site: 'https://go-zero.dev',
	integrations: [
		starlight({
			title: 'go-zero',
			description: 'A cloud-native Go microservices framework with built-in resilience and code generation',
			locales: {
				root: { label: 'English', lang: 'en' },
				'zh-cn': { label: '简体中文', lang: 'zh-CN' },
				ko: { label: '한국어', lang: 'ko' },
			},
			defaultLocale: 'root',
			logo: {
				src: './src/assets/logo.png',
				replacesTitle: false,
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/zeromicro/go-zero' },
			],
			editLink: {
					baseUrl: 'https://github.com/zeromicro/autodoc/edit/main/',
			},
			customCss: [
				'./src/styles/custom.css',
			],
			head: [
				{
					tag: 'script',
					attrs: { type: 'module' },
					content: `import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
mermaid.initialize({ startOnLoad: true, theme: 'neutral', securityLevel: 'loose' });`,
				},
				{
					tag: 'script',
					content: `
						(function() {
							// Skip if user has manually selected a language
							if (localStorage.getItem('starlight-lang-choice')) return;

							// Only redirect on first visit to root pages
							const path = window.location.pathname;
							const isRootLocale = !path.startsWith('/zh-cn') && !path.startsWith('/ko');

							if (isRootLocale) {
								const lang = (navigator.language || navigator.userLanguage || '').toLowerCase();
								if (lang.startsWith('zh')) {
									// Redirect to Chinese version
									const newPath = '/zh-cn' + (path === '/' ? '/' : path);
									window.location.replace(newPath);
								} else if (lang.startsWith('ko')) {
									// Redirect to Korean version
									const newPath = '/ko' + (path === '/' ? '/' : path);
									window.location.replace(newPath);
								}
							}

							// Mark that auto-detection has run
							localStorage.setItem('starlight-lang-choice', 'auto');
						})();
					`,
				},
			],
			sidebar: [
				// ── 1. Concepts ──────────────────────────────────────────
				{
					label: 'Concepts',
					translations: { 'zh-CN': '核心概念', ko: '개념' },
					collapsed: true,
					items: [
						{ slug: 'concepts' },
						{ slug: 'concepts/architecture' },
						{ slug: 'concepts/design-principles' },
						{ slug: 'concepts/project-structure' },
						{ slug: 'concepts/glossary' },
					],
				},
				// ── 2. Getting Started ───────────────────────────────────
				{
					label: 'Getting Started',
					translations: { 'zh-CN': '快速开始', ko: '시작하기' },
					collapsed: true,
					autogenerate: { directory: 'getting-started' },
				},
				// ── 3. Guides (was Tutorials) ────────────────────────────
				{
					label: 'Guides',
					translations: { 'zh-CN': '指南', ko: '가이드' },
					collapsed: true,
					items: [
						{ slug: 'guides' },
						{
							label: 'Quick Start',
							translations: { 'zh-CN': '快速入门', ko: '빠른 시작' },
							collapsed: true,
							autogenerate: { directory: 'guides/quickstart' },
						},
						{
							label: 'HTTP Service',
							translations: { 'zh-CN': 'HTTP 服务', ko: 'HTTP 서비스' },
							collapsed: true,
							autogenerate: { directory: 'guides/http' },
						},
						{
							label: 'gRPC Service',
							translations: { 'zh-CN': 'gRPC 服务', ko: 'gRPC 서비스' },
							collapsed: true,
							autogenerate: { directory: 'guides/grpc' },
						},
						{
							label: 'Database',
							translations: { 'zh-CN': '数据库', ko: '데이터베이스' },
							collapsed: true,
							autogenerate: { directory: 'guides/database' },
						},
						{
							label: 'Microservice',
							translations: { 'zh-CN': '微服务', ko: '마이크로서비스' },
							collapsed: true,
							autogenerate: { directory: 'guides/microservice' },
						},
						{
							label: 'Message Queue',
							translations: { 'zh-CN': '消息队列', ko: '메시지 큐' },
							collapsed: true,
							autogenerate: { directory: 'guides/queue' },
						},
						{
							label: 'API Gateway',
							translations: { 'zh-CN': 'API 网关', ko: 'API 게이트웨이' },
							collapsed: true,
							autogenerate: { directory: 'guides/gateway' },
						},
						{
							label: 'Deployment',
							translations: { 'zh-CN': '部署运维', ko: '배포' },
							collapsed: true,
							autogenerate: { directory: 'guides/deployment' },
						},
						{
							label: 'Cron Job',
							translations: { 'zh-CN': '定时任务', ko: 'Cron 작업' },
							collapsed: true,
							autogenerate: { directory: 'guides/cron-job' },
						},
						{
							label: 'MCP Integration',
							translations: { 'zh-CN': 'MCP 集成', ko: 'MCP 통합' },
							collapsed: true,
							autogenerate: { directory: 'guides/mcp' },
						},
					],
				},
				// ── 4. Components ────────────────────────────────────────
				{
					label: 'Components',
					translations: { 'zh-CN': '组件', ko: '컴포넌트' },
					collapsed: true,
					items: [
						{ slug: 'components' },
						{
							label: 'Cache',
							translations: { 'zh-CN': '缓存', ko: '캐시' },
							collapsed: true,
							autogenerate: { directory: 'components/cache' },
						},
						{
							label: 'Resilience',
							translations: { 'zh-CN': '服务韧性', ko: '탄력성' },
							collapsed: true,
							autogenerate: { directory: 'components/resilience' },
						},
						{
							label: 'Concurrency',
							translations: { 'zh-CN': '并发工具', ko: '동시성 도구' },
							collapsed: true,
							autogenerate: { directory: 'components/concurrency' },
						},
						{
							label: 'Log',
							translations: { 'zh-CN': '日志', ko: '로그' },
							collapsed: true,
							autogenerate: { directory: 'components/log' },
						},
						{
							label: 'Observability',
							translations: { 'zh-CN': '可观测性', ko: '관측 가능성' },
							collapsed: true,
							autogenerate: { directory: 'components/observability' },
						},
						{
							label: 'Queue',
							translations: { 'zh-CN': '队列', ko: '큐' },
							collapsed: true,
							autogenerate: { directory: 'components/queue' },
						},
					],
				},
				// ── 5. Reference ─────────────────────────────────────────
				{
					label: 'Reference',
					translations: { 'zh-CN': '参考文档', ko: '참조 문서' },
					collapsed: true,
					items: [
						{ slug: 'reference' },
						{
							label: 'API DSL',
							translations: { 'zh-CN': 'API DSL', ko: 'API DSL' },
							collapsed: true,
							autogenerate: { directory: 'reference/api-dsl' },
						},
						{
							label: 'Proto DSL',
							translations: { 'zh-CN': 'Proto DSL', ko: 'Proto DSL' },
							collapsed: true,
							autogenerate: { directory: 'reference/proto-dsl' },
						},
						{
							label: 'goctl CLI',
							translations: { 'zh-CN': 'goctl 命令', ko: 'goctl 명령어' },
							collapsed: true,
							autogenerate: { directory: 'reference/cli-guide' },
						},
						{
							label: 'Configuration',
							translations: { 'zh-CN': '配置', ko: '설정' },
							collapsed: true,
							autogenerate: { directory: 'reference/configuration' },
						},
						{
							label: 'Customization',
							translations: { 'zh-CN': '模板定制', ko: '템플릿 커스터마이징' },
							collapsed: true,
							autogenerate: { directory: 'reference/customization' },
						},
						{ slug: 'reference/goctl-plugins' },
						{ slug: 'reference/changelog' },
						{
							label: 'Releases',
							translations: { 'zh-CN': '版本记录', ko: '릴리스 노트' },
							collapsed: true,
							autogenerate: { directory: 'reference/releases' },
						},
					],
				},
				// ── 6. Community (FAQ + Contributing + Examples) ─────────
				{
					label: 'Community',
					translations: { 'zh-CN': '社区', ko: '커뮤니티' },
					collapsed: true,
					items: [
						{ slug: 'community' },
						{ slug: 'community/about' },
						{ slug: 'community/code-style' },
						{ slug: 'community/pull-request' },
						{ slug: 'community/documentation' },
						{ slug: 'community/contributors' },
						{
							label: 'FAQ',
							translations: { 'zh-CN': '常见问题', ko: '자주 묻는 질문' },
							collapsed: true,
							autogenerate: { directory: 'community/faq' },
						},
						{
							label: 'Examples',
							translations: { 'zh-CN': '示例', ko: '예제' },
							collapsed: true,
							autogenerate: { directory: 'examples' },
						},
					],
				},
			],
		}),
		sitemap(),
	],
	markdown: {
		remarkPlugins: [remarkMermaid],
	},
});
