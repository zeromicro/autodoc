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
				// ── Getting Started ──────────────────────────────────────
				{
					label: 'Getting Started',
					translations: { 'zh-CN': '快速开始' },
					autogenerate: { directory: 'getting-started' },
				},
				// ── Tutorials ────────────────────────────────────────────
				// Explicit items so legacy duplicate dirs (mysql/, redis/,
				// mongo/, ops/, log/, service-governance/) are hidden.
				{
					label: 'Tutorials',
					translations: { 'zh-CN': '教程' },
					items: [
						{ slug: 'tutorials' },
						{
							label: 'HTTP Service',
							translations: { 'zh-CN': 'HTTP 服务' },
							autogenerate: { directory: 'tutorials/http' },
						},
						{
							label: 'API DSL',
							translations: { 'zh-CN': 'API DSL' },
							autogenerate: { directory: 'tutorials/api' },
						},
						{
							label: 'gRPC Service',
							translations: { 'zh-CN': 'gRPC 服务' },
							autogenerate: { directory: 'tutorials/grpc' },
						},
						{
							label: 'Proto DSL',
							translations: { 'zh-CN': 'Proto DSL' },
							autogenerate: { directory: 'tutorials/proto' },
						},
						{
							label: 'Database',
							translations: { 'zh-CN': '数据库' },
							autogenerate: { directory: 'tutorials/database' },
						},
						{
							label: 'Microservice',
							translations: { 'zh-CN': '微服务' },
							autogenerate: { directory: 'tutorials/microservice' },
						},
						{
							label: 'Message Queue',
							translations: { 'zh-CN': '消息队列' },
							autogenerate: { directory: 'tutorials/queue' },
						},
						{
							label: 'API Gateway',
							translations: { 'zh-CN': 'API 网关' },
							autogenerate: { directory: 'tutorials/gateway' },
						},
						{
							label: 'Deployment',
							translations: { 'zh-CN': '部署运维' },
							autogenerate: { directory: 'tutorials/deployment' },
						},
						{
							label: 'goctl CLI',
							translations: { 'zh-CN': 'goctl 命令' },
							autogenerate: { directory: 'tutorials/cli' },
						},
						{
							label: 'Configuration',
							translations: { 'zh-CN': '配置管理' },
							autogenerate: { directory: 'tutorials/configuration' },
						},
						{
							label: 'Cron Job',
							translations: { 'zh-CN': '定时任务' },
							autogenerate: { directory: 'tutorials/cron-job' },
						},
						{
							label: 'Customization',
							translations: { 'zh-CN': '模板定制' },
							autogenerate: { directory: 'tutorials/customization' },
						},
						{
							label: 'MCP Integration',
							translations: { 'zh-CN': 'MCP 集成' },
							autogenerate: { directory: 'tutorials/mcp' },
						},
					],
				},
				// ── Components ───────────────────────────────────────────
				{
					label: 'Components',
					translations: { 'zh-CN': '组件' },
					autogenerate: { directory: 'components' },
				},
				// ── Concepts ─────────────────────────────────────────────
				// Explicit to hide duplicate layout.md, keywords.md,
				// components.md, architecture-evolution.md.
				{
					label: 'Concepts',
					translations: { 'zh-CN': '核心概念' },
					items: [
						{ slug: 'concepts' },
						{ slug: 'concepts/architecture' },
						{ slug: 'concepts/design-principles' },
						{ slug: 'concepts/project-structure' },
						{ slug: 'concepts/glossary' },
					],
				},
				// ── Reference ────────────────────────────────────────────
				// Explicit to hide examples.md, proto.md, about-us.md.
				{
					label: 'Reference',
					translations: { 'zh-CN': '参考文档' },
					items: [
						{ slug: 'reference' },
						{
							label: 'goctl',
							autogenerate: { directory: 'reference/goctl' },
						},
						{
							label: 'Configuration',
							translations: { 'zh-CN': '配置参考' },
							autogenerate: { directory: 'reference/configuration' },
						},
						{ slug: 'reference/goctl-plugins' },
						{ slug: 'reference/changelog' },
						{
							label: 'Releases',
							translations: { 'zh-CN': '版本记录' },
							autogenerate: { directory: 'reference/releases' },
						},
					],
				},
				// ── Examples ─────────────────────────────────────────────
				{
					label: 'Examples',
					translations: { 'zh-CN': '示例' },
					autogenerate: { directory: 'examples' },
				},
				// ── FAQ ──────────────────────────────────────────────────
				{
					label: 'FAQ',
					translations: { 'zh-CN': '常见问题' },
					autogenerate: { directory: 'faq' },
				},
				// ── Contributing ─────────────────────────────────────────
				{
					label: 'Contributing',
					translations: { 'zh-CN': '贡献指南' },
					autogenerate: { directory: 'contributing' },
				},
			],
		}),
		sitemap(),
	],
	markdown: {
		remarkPlugins: [remarkMermaid],
	},
});
