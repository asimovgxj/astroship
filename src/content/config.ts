// src/content/config.ts
import { z, defineCollection } from 'astro:content';

const blogCollection = defineCollection({
  schema: z.object({
    draft: z.boolean(),
    title: z.string(),
    snippet: z.string(),
    // 升级：这里我们统一接收字符串。
    // 如果是 ID（如 photo-xxx），代码会自动拼。
    // 如果是完整 URL，代码会自动识别。
    image: z.string().default(''), 
    publishDate: z.string().transform(str => new Date(str)),
    author: z.string().default('AutoChina'),
    category: z.string(),
    tags: z.array(z.string()),
  }),
});

// ... teamCollection 保持你原来的样子即可

export const collections = {
  'blog': blogCollection,
  'team': teamCollection,
};
