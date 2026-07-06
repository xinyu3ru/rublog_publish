// astro.config.mjs
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://xinyu3ru.github.io',
  base: '/rublog_publish/',
  output: 'static',

  markdown: {
    shikiConfig: {
      theme: 'github-dark',
    },
  },

  vite: {
    ssr: { external: ['fs', 'path'] },
  },
});

