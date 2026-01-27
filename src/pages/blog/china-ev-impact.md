---
// 这是一个独立的 Astro 页面，不依赖任何复杂的 Layout
const title = "中国电动车：重塑全球交通";
const description = "2026年新能源汽车产业深度观察";
---

<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <title>{title}</title>
    <style>
      body { font-family: sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 2rem; background: #f4f7f6; }
      .hero { background: #000; color: #fff; padding: 3rem; border-radius: 1rem; margin-bottom: 2rem; text-align: center; }
      .card { background: #fff; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 1.5rem; }
      h1 { color: #fff; margin: 0; }
      h2 { color: #0070f3; border-bottom: 2px solid #0070f3; padding-bottom: 0.5rem; }
      .tag { background: #0070f3; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem; }
    </style>
  </head>
  <body>
    <div class="hero">
      <span class="tag">2026 行业趋势</span>
      <h1>{title}</h1>
      <p>{description}</p>
    </div>

    <div class="card">
      <h2>1. 技术引领</h2>
      <p>中国电动车产业在2026年已实现电池续航与自动驾驶技术的全面领跑。从固态电池到超充网络，中国方案正成为世界标准。</p>
    </div>

    <div class="card">
      <h2>2. 全球改变</h2>
      <p>这不仅是交通工具的更替，更是全球民用能源结构的重构。中国电动车的大规模出口，加速了全球交通脱离化石燃料的进程。</p>
    </div>

    <footer style="text-align: center; margin-top: 3rem; font-size: 0.8rem; color: #666;">
      © 2026 AutoChina 观察站 - 基于 Cloudflare Pages 构建
    </footer>
  </body>
</html>
