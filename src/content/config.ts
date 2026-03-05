import { z, defineCollection } from 'astro:content';

const blogCollection = defineCollection({
  schema: z.object({
    draft: z.boolean(),
    title: z.string(),
    snippet: z.string(),
    // Compatibility mode: supports both previous {src, alt} objects and future "photo-xxx" strings
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
