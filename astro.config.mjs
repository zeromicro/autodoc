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
	site: 'https://doc.go-zero.dev',
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
				{
					label: 'Getting Started',
					translations: { 'zh-CN': '快速开始' },
					autogenerate: { directory: 'getting-started' },
				},
				{
					label: 'Tutorials',
					translations: { 'zh-CN': '教程' },
					autogenerate: { directory: 'tutorials' },
				},
				{
					label: 'Concepts',
					translations: { 'zh-CN': '核心概念' },
					autogenerate: { directory: 'concepts' },
				},
				{
					label: 'Reference',
					translations: { 'zh-CN': '参考文档' },
					autogenerate: { directory: 'reference' },
				},
				{
					label: 'Examples',
					translations: { 'zh-CN': '示例' },
					autogenerate: { directory: 'examples' },
				},
			],
		}),
		sitemap(),
	],
	markdown: {
		remarkPlugins: [remarkMermaid],
	},
});
