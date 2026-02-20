import { z, defineCollection } from 'astro:content';

const blogCollection = defineCollection({
  schema: z.object({
    draft: z.boolean(),
    title: z.string(),
    snippet: z.string(),
    // 💡 兼容模式：既支持你以前的 {src, alt} 对象，也支持未来的 "photo-xxx" 字符串
    image: z.union([
      z.string(), 
      z.object({
        src: z.string(),
        alt: z.string().default('AutoChina Intelligence'),
      }),
    ]).default(''), 
    publishDate: z.string().transform(str => new Date(str)),
    author: z.string().default('AutoChina'),
    category: z.string(),
    tags: z.array(z.string()),
  }),
});

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

export const collections = {
  'blog': blogCollection,
  'team': teamCollection,
};
