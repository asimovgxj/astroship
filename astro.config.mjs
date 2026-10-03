import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import icon from "astro-icon";

export default defineConfig({
  // 核心：必须是 https 协议
  site: 'https://autochina.org',
  base: "/",
  outDir: "dist",
  redirects: {
    // Sitemap 修正
    '/sitemap-main.xml': '/sitemap-index.xml',

    // Category page redirect (old market page -> new category page)
    '/market': '/category/market',

    // 博客文章修正 (旧地址 -> 新地址)
    '/blog/chinese-ev-review-2025': '/blog/tesla-vs-china-bev-2025',
    '/blog/asymmetric-narrative-china-ev': '/blog/tesla-vs-byd-narrative-control',
    '/blog/russia-windfall': '/blog/contentrussia-car-scrapping-tax-ice-profit',

    // Removed template pages -> redirect to home
    '/pricing': '/',

    // 已删除的旧页面 -> 全部导向首页
    '/seagull-detail.html': '/',
    '/t03-detail.html': '/',
    '/dolphin-detail.html': '/',
    '/sedan.html': '/',
    '/suv.html': '/',
    '/mini.html': '/',
    '/mpv.html': '/',
    '/M93.html': '/',
    '/miniev-detail.html': '/',
    '/ant-detail.html': '/',
    '/detail.html': '/',
    '/M9.html': '/'
  },
  integrations: [
    mdx(),
    sitemap({
      serialize(item) {
        // Add lastmod to blog article pages based on build date;
        // the actual publishDate will be injected via the page's <lastmod> if available.
        // For article pages, set lastmod to today (build date) as a baseline.
        if (item.url.includes('/blog/')) {
          item.lastmod = new Date().toISOString();
        }
        return item;
      },
    }),
    icon(),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});