"""Test server for the web tool: builds the site as GitHub Pages gets it (WebUI/build_site.py, into
LocalTesting/_site) and serves it with caching turned off, on the first free port from 8000.

Every load of the page builds the site again (about a second), so a change to WebUI/ or to Generator/ shows on
the next reload; there is nothing to restart."""
import functools, http.server, os, socket, sys, threading, webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SITE = os.path.join(HERE, "_site")
sys.path.insert(0, os.path.join(REPO, "WebUI"))
import build_site                                                    # noqa: E402  (WebUI/build_site.py)

LOCK = threading.Lock()


def build():
    with LOCK:
        v = build_site.build(SITE)
    print(f"built: KESE {v.get('kese')}, generator.zip {v['bytes'] / 1024:.0f} KB")


class NoCache(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/WebUI/", "/WebUI/index.html"):            # the page itself: rebuild first
            try:
                build()
            except Exception as e:                                   # noqa: BLE001  (shown in the browser)
                self.send_error(500, f"build_site.py failed: {e}")
                return
        with LOCK:
            super().do_GET()

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
