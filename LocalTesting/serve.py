"""Test server for the web tool: builds the site as GitHub Pages gets it (WebUI/build_site.py, into
LocalTesting/_site) and serves it with caching turned off, on the first free port from 8000.

Every load of the page builds the site again (about a second), so a change to WebUI/ or to Generator/ shows on
the next reload; there is nothing to restart.  The backup copy of Pyodide and three.js (WebUI/vendor.json) is
downloaded once into LocalTesting/_vendor and reused while it matches vendor.json."""
import functools, http.server, os, socket, sys, threading, webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SITE = os.path.join(HERE, "_site")
VENDOR = os.path.join(HERE, "_vendor")                              # the backup copy, downloaded once
sys.path.insert(0, os.path.join(REPO, "WebUI"))
import build_site                                                    # noqa: E402  (WebUI/build_site.py)

class Gate:
    """Files are served side by side; a build waits until none is being sent, and nothing is sent during a build.
    (One lock round every request would hang the page: the browser reads Pyodide's .wasm only once its .mjs
    has arrived, so the .mjs must not wait behind the .wasm.)"""
    def __init__(self):
        self.cv, self.sending, self.building = threading.Condition(), 0, False

    def build(self):
        with self.cv:
            self.cv.wait_for(lambda: not self.building and not self.sending)
            self.building = True
        try:
            return build_site.build(SITE, vendor_cache=VENDOR)
        finally:
            with self.cv:
                self.building = False
                self.cv.notify_all()

    def send(self, serve):
        with self.cv:
            self.cv.wait_for(lambda: not self.building)
            self.sending += 1
        try:
            serve()
        finally:
            with self.cv:
                self.sending -= 1
                self.cv.notify_all()


GATE = Gate()


def build():
    v = GATE.build()
    print(f"built: KESE {v.get('kese')}, generator.zip {v['bytes'] / 1024:.0f} KB")


class NoCache(http.server.SimpleHTTPRequestHandler):
    # module scripts and WebAssembly need their exact types (older Pythons do not know .mjs)
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      ".mjs": "text/javascript", ".js": "text/javascript", ".wasm": "application/wasm",
                      ".json": "application/json", ".whl": "application/zip", ".woff2": "font/woff2"}

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/WebUI/", "/WebUI/index.html"):            # the page itself: rebuild first
            try:
                build()
            except Exception as e:                                   # noqa: BLE001  (shown in the browser)
                self.send_error(500, f"build_site.py failed: {e}")
                return
        GATE.send(super().do_GET)

    def end_headers(self):
        # the browser must always load the files of this folder, never an older copy it kept
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def log_message(self, *args):
        pass


def free_port(start=8000):
    for port in range(start, start + 50):
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    sys.exit("No free port between 8000 and 8049")


build()
port = free_port()
url = f"http://localhost:{port}/WebUI/"
server = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(NoCache, directory=SITE))
print(f"Serving {SITE}")
print(f"Open {url}   (close this window or press Ctrl+C to stop)")
webbrowser.open(url)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
