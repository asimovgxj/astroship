import { getCollection, type CollectionEntry } from "astro:content";

export type BlogEntry = CollectionEntry<"blog">;
export type CategoryName = BlogEntry["data"]["category"];

// Minimum number of published posts before a category is shown in the navbar.
export const MIN_POSTS_FOR_NAV = 2;

export const slugify = (value: string) =>
  value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

export interface TaxonomyTerm {
  name: string;
  slug: string;
  title: string;
  description: string;
  intro: string;
}

// Keep names in sync with the zod enum in src/content/config.ts
export const CATEGORIES: (TaxonomyTerm & { name: CategoryName })[] = [
  {
    name: "Market",
    slug: "market",
    title: "China EV Market Intelligence",
    description:
      "Sales data, export volumes, and competitive analysis tracking China's electric vehicle market and the brands fighting for share at home and abroad.",
    intro:
      "China is the largest car market in the world and the place where the electric vehicle transition is moving fastest. This section collects our market coverage: monthly delivery and sales figures, export volumes, price wars, and market-share shifts between domestic champions and foreign incumbents. We focus on what the numbers actually say rather than what press releases claim, and we try to separate one-off spikes from durable trends. Expect close readings of registration and wholesale data, comparisons between headline brands such as BYD, Tesla, and Xiaomi, and analysis of how overseas demand is changing the business model of Chinese automakers. Each article explains its sources and states where the data is incomplete or contested, so readers can judge the evidence for themselves.",
  },
  {
    name: "Policy",
    slug: "policy",
    title: "China Auto Policy, Regulation & Legal Risk",
    description:
      "How regulation, trade measures, tariffs, and litigation shape the strategies of Chinese automakers in domestic and overseas markets.",
    intro:
      "Policy decides who wins in the automotive industry as often as engineering does. This section covers the rules around China's car makers: industrial policy and subsidies at home, tariffs and trade measures abroad, and the legal fights that increasingly define brand reputation. We look at how import duties and scrapping taxes change export profitability, how regulators and state media respond differently to domestic and foreign brands, and how defamation and trademark lawsuits affect public debate about Chinese EVs. The goal is practical: to explain what a measure or court case means for pricing, market access, and risk, not just to report that it happened. Where the legal or regulatory picture is still developing, we say so clearly and point to the primary documents available.",
  },
  {
    name: "Supply Chain",
    slug: "supply-chain",
    title: "China EV Supply Chain Analysis",
    description:
      "Batteries, raw materials, semiconductors, and manufacturing capacity behind China's electric vehicle industry and its global expansion.",
    intro:
      "China's lead in electric vehicles rests on a supply chain that stretches from lithium refining and battery cells to motors, power electronics, and software. This section examines that foundation: who controls critical materials, how battery makers price and allocate capacity, where chip and component bottlenecks remain, and how automakers are localising production overseas to manage tariffs and political risk. We pay particular attention to vertical integration, because the ability to build key parts in-house is one of the main reasons Chinese brands can undercut rivals on price. We also track the weak points, from overcapacity and supplier payment terms to dependence on imported equipment.",
  },
  {
    name: "Brands",
    slug: "brands",
    title: "Chinese EV Brands: Reviews & Comparisons",
    description:
      "Product reviews and head-to-head comparisons of Chinese electric vehicles against global benchmarks such as the Tesla Model 3 and Model Y.",
    intro:
      "Sales charts explain which cars are winning, but not why. This section looks at the products themselves: how Chinese electric vehicles compare with the global benchmarks on range, charging, driving dynamics, software, build quality, and price. We compare new models from brands such as Xiaomi, NIO, Zeekr, and BYD with established references like the Tesla Model 3, and we try to identify where Chinese makers have genuinely moved ahead and where they are still catching up. Reviews draw on published test data, specifications, and independent evaluations, and we note when a claim comes from the manufacturer rather than from measured results.",
  },
  {
    name: "Opinion",
    slug: "opinion",
    title: "Opinion & Perspectives on China's Auto Industry",
    description:
      "Argued essays on innovation, industrial strategy, and the long-term trajectory of China's automotive and technology sectors.",
    intro:
      "Not every question about China's auto industry can be settled with a data table. This section publishes argued essays on the bigger debates: whether Chinese carmakers are innovators or fast followers, what the difference between iteration and invention means for long-term competitiveness, and how industrial strategy shapes technology leadership. These pieces take a clear position and explain the reasoning behind it, drawing on market evidence, history, and comparisons with other industries. They are meant to provoke discussion rather than close it, and they are clearly labelled as opinion so readers can distinguish them from our market and policy reporting.",
  },
];

export const BRANDS: (TaxonomyTerm & { match: RegExp })[] = [
  {
    name: "BYD",
    slug: "byd",
    match: /\bbyd\b/i,
    title: "BYD News, Sales Data & Analysis",
    description:
      "Independent coverage of BYD: monthly sales, export strategy, pricing, and how China's largest EV maker competes globally.",
    intro:
      "BYD has grown from a battery supplier into the world's largest seller of new energy vehicles, and its results now set the tone for the whole Chinese car industry. This page gathers our coverage of the company: monthly sales and delivery data, the balance between domestic and export volumes, the price cuts that have pressured competitors, and the way BYD manages public perception compared with foreign rivals. We pay close attention to turning points, such as periods of slowing domestic sales or rapid growth in overseas shipments, because they reveal how durable BYD's lead really is. Its vertical integration in batteries and components is a recurring theme, as is its expansion into Europe, Latin America, and Southeast Asia.",
  },
  {
    name: "Tesla",
    slug: "tesla",
    match: /\btesla\b/i,
    title: "Tesla in China: Sales, Competition & Analysis",
    description:
      "How Tesla performs in China: Model 3 and Model Y sales, competition with BYD and Xiaomi, and the media environment it faces.",
    intro:
      "Tesla remains the benchmark every Chinese electric vehicle maker measures itself against, and China is one of its most important markets and production bases. This page collects our coverage of Tesla in that context: how the Model 3 and Model Y hold up in sales against a growing field of domestic competitors, how Chinese brands position their products directly against Tesla, and how the company's treatment by regulators and media compares with that of local champions. We also look at the broader debate over innovation, asking whether Chinese rivals are redefining the category Tesla created or refining it. Coverage relies on delivery and registration data where available and clearly separates confirmed figures from social media claims.",
  },
  {
    name: "Xiaomi",
    slug: "xiaomi",
    match: /\bxiaomi\b/i,
    title: "Xiaomi Auto: SU7 Sales, Reviews & Legal Disputes",
    description:
      "Coverage of Xiaomi's car business: SU7 deliveries, comparisons with Tesla, and the lawsuits and trademark disputes shaping its image.",
    intro:
      "Xiaomi's move from smartphones into cars is one of the most closely watched entries in the history of the electric vehicle industry. This page brings together our reporting on Xiaomi Auto: delivery numbers for the SU7 and how they compare with Tesla in China, product comparisons against established benchmarks, and the legal side of the business, including defamation suits against critics and trademark disputes that have drawn public criticism. We are interested in how a consumer electronics company with a huge fan base translates brand loyalty into car sales, and what risks come with an aggressive approach to reputation management. Coverage separates audited figures from online claims and notes where information is still disputed.",
  },
  {
    name: "NIO",
    slug: "nio",
    match: /\bnio\b/i,
    title: "NIO: Battery Swapping, Models & Competitive Position",
    description:
      "Analysis of NIO's premium electric vehicles, battery-swap network, and how models such as the ET5 compare with Tesla and other Chinese rivals.",
    intro:
      "NIO has built its identity around premium electric vehicles, a user-community model, and a large network of battery swap stations that lets drivers exchange a depleted pack in minutes. This page follows the company's competitive position: how models such as the ET5 compare with the Tesla Model 3 and newer rivals from Xiaomi and Zeekr, whether battery swapping gives NIO a lasting advantage over fast charging, and what its strategy means in an increasingly crowded and price-sensitive market. We look at product quality and service as well as the economics behind them, because NIO's model depends on customers valuing an ownership experience beyond the car itself.",
  },
];

export const getCategoryByName = (name: string) =>
  CATEGORIES.find((c) => c.name === name);

export const categoryUrl = (name: string) => `/category/${slugify(name)}`;
export const brandUrl = (slug: string) => `/brand/${slug}`;

export const matchesBrand = (entry: BlogEntry, brand: (typeof BRANDS)[number]) =>
  entry.data.tags.some((tag) => brand.match.test(String(tag)));

export const getBrandsForEntry = (entry: BlogEntry) =>
  BRANDS.filter((b) => matchesBrand(entry, b));

/** Published (non-draft) posts, newest first. */
export async function getPublishedPosts(): Promise<BlogEntry[]> {
  const posts = await getCollection("blog", ({ data }) => !data.draft);
  return posts.sort(
    (a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf()
  );
}

export const countByCategory = (posts: BlogEntry[]) => {
  const counts = new Map<string, number>();
  for (const p of posts) {
    counts.set(p.data.category, (counts.get(p.data.category) ?? 0) + 1);
  }
  return counts;
};

/** Most recent posts sharing the category or at least one tag, excluding the current one. */
export function getRelatedPosts(entry: BlogEntry, posts: BlogEntry[], limit = 3) {
  const tags = new Set(entry.data.tags.map((t) => String(t).toLowerCase()));
  return posts
    .filter((p) => p.slug !== entry.slug)
    .filter(
      (p) =>
        p.data.category === entry.data.category ||
        p.data.tags.some((t) => tags.has(String(t).toLowerCase()))
    )
    .sort((a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf())
    .slice(0, limit);
}

/** Resolves both {src, alt} objects and bare Unsplash "photo-xxx" IDs. */
export const resolveImg = (
  imgData: BlogEntry["data"]["image"],
  width = 800
): string => {
  if (!imgData) return "";
  const rawUrl = typeof imgData === "object" ? imgData.src : imgData;
  if (!rawUrl) return "";
  if (rawUrl.startsWith("http")) return rawUrl;
  return `https://images.unsplash.com/${rawUrl}?auto=format&fit=crop&w=${width}&q=80`;
};
