import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import autoprefixer from 'autoprefixer'
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(),
    tailwindcss()],
    proxy:{
    '/api':{
      target:'http://127.0.0.1/:8000',
      changeOrigin:true,
      rewrite: (path)=>path.replace(/^\/api/,'')
    }
  },  
    resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
})
