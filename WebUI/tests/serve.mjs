// serve.mjs - a small static server for the built site (.site/), as GitHub Pages serves it: the test runner starts it.
//   node serve.mjs [folder] [port]          (defaults: .site 8811)
// Node only (no Python), so it also runs in the Playwright container.  Paths outside the folder are refused.
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { extname, join, normalize, resolve, sep } from "node:path";

const root = resolve(process.argv[2] || ".site");
const port = Number(process.argv[3] || process.env.PORT || 8811);
const TYPES = {
  ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".mjs": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8", ".json": "application/json", ".svg": "image/svg+xml", ".ico": "image/x-icon",
  ".png": "image/png", ".wasm": "application/wasm", ".zip": "application/zip", ".whl": "application/zip",
  ".woff2": "font/woff2", ".txt": "text/plain; charset=utf-8", ".md": "text/markdown; charset=utf-8", ".py": "text/plain; charset=utf-8",
  ".kicad_pcb": "text/plain; charset=utf-8",
};

createServer(async (req, res) => {
  try {
    let path = normalize(decodeURIComponent(new URL(req.url, "http://x").pathname));
    let file = join(root, path);
    if (file !== root && !file.startsWith(root + sep)) { res.writeHead(403).end(); return; }
    if ((await stat(file)).isDirectory()) {
      if (!path.endsWith("/")) { res.writeHead(301, { Location: path + "/" }).end(); return; }
      file = join(file, "index.html");
    }
    const body = await readFile(file);
    res.writeHead(200, { "Content-Type": TYPES[extname(file).toLowerCase()] || "application/octet-stream", "Content-Length": body.length, "Cache-Control": "no-cache" });
    res.end(req.method === "HEAD" ? undefined : body);
  } catch (e) {
    res.writeHead(404, { "Content-Type": "text/plain" }).end("not found");
  }
}).listen(port, "127.0.0.1", () => console.log(`serving ${root} on http://127.0.0.1:${port}/`));
