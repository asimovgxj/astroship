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
    author: z.string().default('AutoChina Research'),
    // Keep in sync with CATEGORIES in src/utils/taxonomy.ts
    category: z.enum(['Market', 'Policy', 'Supply Chain', 'Brands', 'Opinion']),
    tags: z.array(z.string()),
  }),
});

export const collections = {
  'blog': blogCollection,
};
