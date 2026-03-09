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

    // 博客文章修正 (旧地址 -> 新地址)
    '/blog/chinese-ev-review-2025/': '/blog/tesla-vs-china-bev-2025',
    '/blog/chinese-ev-review-2025': '/blog/tesla-vs-china-bev-2025',
    '/blog/asymmetric-narrative-china-ev/': '/blog/tesla-vs-byd-narrative-control',
    '/blog/russia-windfall/': '/blog/contentrussia-car-scrapping-tax-ice-profit',

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
  integrations: [mdx(), sitemap(), icon()],
  vite: {
    plugins: [tailwindcss()],
  },
});