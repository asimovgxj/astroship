import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import icon from "astro-icon";

const repo = "astroship";
const target = process.env.DEPLOY_TARGET;
const isGithubPages = target === "GITHUB_PAGES";

export default defineConfig({
site: isGithubPages ? `https://asimovgxj.github.io/${repo}` : 'http://localhost:4321',
 
  base: isGithubPages ? `/${repo}` : "/",
  outDir: "dist",
  integrations: [mdx(), sitemap(), icon()],
  vite: {
    plugins: [tailwindcss()],
  },
});
