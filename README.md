# AutoChina.org

AutoChina is a content site focused on China's electric vehicle industry, strategy, policy, supply chain, and export trends. The project combines editorial coverage with structured market analysis and SEO-friendly page generation.

## Technology stack

- Astro 5
- Tailwind CSS
- MDX + content collections
- Cloudflare Pages deployment
- Canonical domain: https://autochina.org

## Deployment

The active production deployment is on Cloudflare Pages and is connected to the GitHub repository. The canonical site is configured in [astro.config.mjs](astro.config.mjs), and the Node engine is pinned to 22.19.0 in [package.json](package.json).

## Local development

```bash
pnpm install
pnpm dev
pnpm build
```

## Useful project notes

- SEO metadata is centralized in [src/layouts/Layout.astro](src/layouts/Layout.astro)
- Homepage metadata is defined in [src/pages/index.astro](src/pages/index.astro)
- Blog content uses the collection schema under [src/content](src/content)
- Static redirects and site domain settings live in [astro.config.mjs](astro.config.mjs)

## Production and maintenance

- Keep the site domain aligned with the Cloudflare Pages project
- Prefer Cloudflare as the single deployment source of truth
- Validate builds after content or routing changes before publishing

## License

This project is for the AutoChina editorial and intelligence site and is maintained as a custom implementation built on the Astro platform.
