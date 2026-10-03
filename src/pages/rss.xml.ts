import rss from "@astrojs/rss";
import type { APIContext } from "astro";
import { getPublishedPosts } from "@/utils/taxonomy";

export async function GET(context: APIContext) {
  const posts = await getPublishedPosts();
  return rss({
    title: "AutoChina – China EV Intelligence",
    description:
      "Independent research, strategic intelligence, and real-time insights into China's electric vehicle revolution and global expansion strategy.",
    site: context.site!.toString(),
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.snippet,
      pubDate: post.data.publishDate,
      link: `/blog/${post.slug}/`,
      categories: [post.data.category, ...post.data.tags],
    })),
  });
}
