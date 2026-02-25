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
							const isRootLocale = !path.startsWith('/zh-cn');

							if (isRootLocale) {
								const lang = navigator.language || navigator.userLanguage;
								if (lang && lang.toLowerCase().startsWith('zh')) {
									// Redirect to Chinese version
									const newPath = '/zh-cn' + (path === '/' ? '/' : path);
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
					translations: { 'zh-CN': '核心概念' },
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
					translations: { 'zh-CN': '快速开始' },
					collapsed: true,
					autogenerate: { directory: 'getting-started' },
				},
				// ── 3. Guides (was Tutorials) ────────────────────────────
				{
					label: 'Guides',
					translations: { 'zh-CN': '指南' },
					collapsed: true,
					items: [
						{ slug: 'guides' },
						{
							label: 'Quick Start',
							translations: { 'zh-CN': '快速入门' },
							collapsed: true,
							autogenerate: { directory: 'guides/quickstart' },
						},
						{
							label: 'HTTP Service',
							translations: { 'zh-CN': 'HTTP 服务' },
							collapsed: true,
							autogenerate: { directory: 'guides/http' },
						},
						{
							label: 'gRPC Service',
							translations: { 'zh-CN': 'gRPC 服务' },
							collapsed: true,
							autogenerate: { directory: 'guides/grpc' },
						},
						{
							label: 'Database',
							translations: { 'zh-CN': '数据库' },
							collapsed: true,
							autogenerate: { directory: 'guides/database' },
						},
						{
							label: 'Microservice',
							translations: { 'zh-CN': '微服务' },
							collapsed: true,
							autogenerate: { directory: 'guides/microservice' },
						},
						{
							label: 'Message Queue',
							translations: { 'zh-CN': '消息队列' },
							collapsed: true,
							autogenerate: { directory: 'guides/queue' },
						},
						{
							label: 'API Gateway',
							translations: { 'zh-CN': 'API 网关' },
							collapsed: true,
							autogenerate: { directory: 'guides/gateway' },
						},
						{
							label: 'Deployment',
							translations: { 'zh-CN': '部署运维' },
							collapsed: true,
							autogenerate: { directory: 'guides/deployment' },
						},
						{
							label: 'Cron Job',
							translations: { 'zh-CN': '定时任务' },
							collapsed: true,
							autogenerate: { directory: 'guides/cron-job' },
						},
						{
							label: 'MCP Integration',
							translations: { 'zh-CN': 'MCP 集成' },
							collapsed: true,
							autogenerate: { directory: 'guides/mcp' },
						},
					],
				},
				// ── 4. Components ────────────────────────────────────────
				{
					label: 'Components',
					translations: { 'zh-CN': '组件' },
					collapsed: true,
					items: [
						{ slug: 'components' },
						{
							label: 'Cache',
							translations: { 'zh-CN': '缓存' },
							collapsed: true,
							autogenerate: { directory: 'components/cache' },
						},
						{
							label: 'Resilience',
							translations: { 'zh-CN': '服务韧性' },
							collapsed: true,
							autogenerate: { directory: 'components/resilience' },
						},
						{
							label: 'Concurrency',
							translations: { 'zh-CN': '并发工具' },
							collapsed: true,
							autogenerate: { directory: 'components/concurrency' },
						},
						{
							label: 'Log',
							translations: { 'zh-CN': '日志' },
							collapsed: true,
							autogenerate: { directory: 'components/log' },
						},
						{
							label: 'Observability',
							translations: { 'zh-CN': '可观测性' },
							collapsed: true,
							autogenerate: { directory: 'components/observability' },
						},
						{
							label: 'Queue',
							translations: { 'zh-CN': '队列' },
							collapsed: true,
							autogenerate: { directory: 'components/queue' },
						},
					],
				},
				// ── 5. Reference ─────────────────────────────────────────
				{
					label: 'Reference',
					translations: { 'zh-CN': '参考文档' },
					collapsed: true,
					items: [
						{ slug: 'reference' },
						{
							label: 'DSL Syntax',
							translations: { 'zh-CN': 'DSL 语法' },
							collapsed: true,
							autogenerate: { directory: 'reference/dsl' },
						},
						{
							label: 'API DSL',
							translations: { 'zh-CN': 'API DSL' },
							collapsed: true,
							autogenerate: { directory: 'reference/api-dsl' },
						},
						{
							label: 'Proto DSL',
							translations: { 'zh-CN': 'Proto DSL' },
							collapsed: true,
							autogenerate: { directory: 'reference/proto-dsl' },
						},
						{
							label: 'goctl CLI',
							translations: { 'zh-CN': 'goctl 命令' },
							collapsed: true,
							autogenerate: { directory: 'reference/cli-guide' },
						},
						{
							label: 'goctl',
							collapsed: true,
							autogenerate: { directory: 'reference/goctl' },
						},
						{
							label: 'Configuration Reference',
							translations: { 'zh-CN': '配置参考' },
							collapsed: true,
							autogenerate: { directory: 'reference/configuration' },
						},
						{
							label: 'Configuration Guide',
							translations: { 'zh-CN': '配置管理' },
							collapsed: true,
							autogenerate: { directory: 'reference/configuration-guide' },
						},
						{
							label: 'Customization',
							translations: { 'zh-CN': '模板定制' },
							collapsed: true,
							autogenerate: { directory: 'reference/customization' },
						},
						{ slug: 'reference/goctl-plugins' },
						{ slug: 'reference/changelog' },
						{
							label: 'Releases',
							translations: { 'zh-CN': '版本记录' },
							collapsed: true,
							autogenerate: { directory: 'reference/releases' },
						},
					],
				},
				// ── 6. Community (FAQ + Contributing + Examples) ─────────
				{
					label: 'Community',
					translations: { 'zh-CN': '社区' },
					collapsed: true,
					items: [
						{ slug: 'community' },
						{ slug: 'community/code-style' },
						{ slug: 'community/pull-request' },
						{ slug: 'community/documentation' },
						{ slug: 'community/contributors' },
						{
							label: 'FAQ',
							translations: { 'zh-CN': '常见问题' },
							collapsed: true,
							autogenerate: { directory: 'community/faq' },
						},
						{
							label: 'Examples',
							translations: { 'zh-CN': '示例' },
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
