import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, resolve, sep } from 'node:path';
import { POST, GET } from './api/work-submission.mjs';

const root = resolve('public');
const types = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.webp': 'image/webp', '.woff': 'font/woff', '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
};

createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  if (url.pathname === '/api/work-submission') {
    const chunks = [];
    for await (const chunk of req) chunks.push(chunk);
    const request = new Request(url, { method: req.method, headers: req.headers,
      ...(req.method === 'POST' ? { body: Buffer.concat(chunks) } : {}) });
    const response = req.method === 'POST' ? await POST(request) : GET();
    res.writeHead(response.status, Object.fromEntries(response.headers));
    res.end(Buffer.from(await response.arrayBuffer()));
    return;
  }

  const route = decodeURIComponent(url.pathname);
  const relative = route === '/' ? '/index.html' : extname(route) ? route : `${route}.html`;
  const file = resolve(join(root, relative.slice(1)));
  if (file !== root && !file.startsWith(root + sep)) {
    res.writeHead(403).end(); return;
  }
  try {
    const data = await readFile(file);
    res.writeHead(200, { 'Content-Type': types[extname(file)] || 'application/octet-stream' });
    res.end(data);
  } catch {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not found');
  }
}).listen(3000, '127.0.0.1', () => console.log('CW3 preview: http://127.0.0.1:3000'));
