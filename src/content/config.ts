// 1. Import utilities from `astro:content`
import { z, defineCollection } from 'astro:content';

// 2. Define your collection(s)
const blogCollection = defineCollection({
  schema: z.object({
    draft: z.boolean(),
    title: z.string(),
    snippet: z.string(),
    // 修复：允许图片是字符串链接，或者是带 src 和 alt 的对象
    image: z.union([
      z.string(), 
      z.object({
        src: z.string(),
        alt: z.string().default('Blog Image'),
      }),
    ]),
    publishDate: z.string().transform(str => new Date(str)),
    author: z.string().default('Astroship'),
    category: z.string(),
    tags: z.array(z.string()),
  }),
});

const teamCollection = defineCollection({
  schema: z.object({
    draft: z.boolean(),
    name: z.string(),
    title: z.string(),
    // 同样修复：防止团队成员头像因为格式问题报错
    avatar: z.union([
      z.string(),
      z.object({
        src: z.string(),
        alt: z.string().default('Team Member'),
      }),
    ]),
    publishDate: z.string().transform(str => new Date(str)),
  }),
});

// 3. Export a single `collections` object to register your collection(s)
export const collections = {
  'blog': blogCollection,
  'team': teamCollection,
};
