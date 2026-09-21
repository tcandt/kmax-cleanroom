import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 3112,
    host: '0.0.0.0',
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8111',
        changeOrigin: true,
      },
      '/devices': {
        target: 'http://127.0.0.1:8111',
        changeOrigin: true,
      },
      '/upload': {
        target: 'http://127.0.0.1:8111',
        changeOrigin: true,
      },
      '/downloads': {
        target: 'http://127.0.0.1:8111',
        changeOrigin: true,
      },
      '/snapshots': {
        target: 'http://127.0.0.1:8111',
        changeOrigin: true,
      },
      '/_test': {
        target: 'http://127.0.0.1:8111',
        changeOrigin: true,
      },
      '/register_device': {
        target: 'ws://127.0.0.1:8111',
        ws: true,
      },
      '/register_agent': {
        target: 'ws://127.0.0.1:8111',
        ws: true,
      },
      '/connect_client': {
        target: 'ws://127.0.0.1:8111',
        ws: true,
      },
      '/ws': {
        target: 'ws://127.0.0.1:8111',
        ws: true,
      },
    },
  },
  build: {
    outDir: 'dist-src',
    emptyOutDir: true,
    rollupOptions: {
      input: path.resolve(__dirname, 'index.src.html'),
    },
  },
});
