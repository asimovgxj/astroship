import { z, defineCollection } from 'astro:content';

// 1. 定义 Blog 集合
const blogCollection = defineCollection({
  schema: z.object({
    draft: z.boolean(),
    title: z.string(),
    snippet: z.string(),
    // 升级为字符串模式：支持完整 URL 或 Unsplash ID
    image: z.string().default(''), 
    publishDate: z.string().transform(str => new Date(str)),
    author: z.string().default('AutoChina'),
    category: z.string(),
    tags: z.array(z.string()),
  }),
});

// 2. 定义 Team 集合 (报错就是因为之前漏了这一段)
const teamCollection = defineCollection({
  schema: z.object({
    draft: z.boolean(),
    name: z.string(),
    title: z.string(),
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

// 3. 统一导出
export const collections = {
  'blog': blogCollection,
  'team': teamCollection,
};
