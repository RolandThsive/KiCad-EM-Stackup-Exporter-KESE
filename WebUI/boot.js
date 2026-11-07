/* boot.js - starts the page, before anything heavy loads.

   1. Computers only: a phone or tablet (a device with no mouse or trackpad; the window width does not decide it, a
      computer window can be narrow too) gets the message in index.html and never downloads Python.
   2. Reads the page's settings (webui.json) and the two import maps build_site.py wrote (importmaps.json): three.js
      from jsDelivr, or from this site's backup copy (vendor/three/).  Each map lists the SHA-384 of every three.js file,
      so the browser refuses a file that is not exactly the one the site was built with.
   3. jsDelivr is asked first (a HEAD of three.module.js).  If it has not answered within webui.json "cdnWaitSeconds"
      (15 s), or answers with an error, the backup map is used.  If a three.js file then fails to load from jsDelivr
      (blocked, changed, cut off), the page reloads once on the backup, remembered for the tab (sessionStorage).
   4. Adds the map, then WebUI.js.

   An import map must exist before the first module loads, and the page's Content-Security-Policy allows exactly
   these two maps (build_site.py puts their SHA-256 in it), so they are inserted here word for word. */
(function () {
  "use strict";
  var touchOnly = window.matchMedia("(pointer: coarse)").matches && !window.matchMedia("(any-pointer: fine)").matches;
  var root = document.documentElement;
  window.KESE_PHONE = touchOnly;
  if (touchOnly) root.classList.add("phone");
  if (window.self !== window.top) root.classList.add("embedded");
  if (touchOnly) return;

  var FLAG = "kese-three-backup";
  function backupChosen() {
    if (/[?&]threeBackup=1\b/.test(location.search)) return true;
    try { return window.sessionStorage.getItem(FLAG) === "1"; } catch (e) { return false; }
  }
  function reloadOnBackup() {
    try { window.sessionStorage.setItem(FLAG, "1"); location.reload(); return; } catch (e) { /* storage blocked */ }
    var q = new URLSearchParams(location.search);
    q.set("threeBackup", "1");
    location.replace(location.pathname + "?" + q + location.hash);
  }
  function whenReady(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn); else fn();
  }
  function fail(text) {
    whenReady(function () {
      var list = document.getElementById("checks-list"), button = document.getElementById("btn-generate");
      if (list) list.textContent = text;
      if (button) button.textContent = "The Page Did Not Start";
    });
  }
  function getJSON(url) {
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error(url + ": HTTP " + r.status);
      return r.json();
    });
  }
  // true when jsDelivr answers the HEAD with 2xx within ms; false on an error, a refusal or silence
  function cdnAnswers(url, ms) {
    var ctl = window.AbortController ? new AbortController() : null, timer;
    var silence = new Promise(function (done) { timer = setTimeout(function () { if (ctl) ctl.abort(); done(false); }, ms); });
    var ask = fetch(url, { method: "HEAD", mode: "cors", credentials: "omit", cache: "no-cache", signal: ctl ? ctl.signal : undefined })
      .then(function (r) { return r.ok; }, function () { return false; });
    return Promise.race([ask, silence]).then(function (ok) { clearTimeout(timer); return ok; });
  }
  function start(cfg, maps, source) {
    window.KESE_CONFIG = cfg;
    window.KESE_THREE = source;                    // "cdn" or "backup": the footer and Report a Problem name it
    var map = document.createElement("script");
    map.type = "importmap";
    map.textContent = maps[source];
    document.head.appendChild(map);
    whenReady(function () {
      var main = document.createElement("script");
      main.type = "module";
      main.src = "WebUI.js";
      main.onerror = function () {
        if (source === "cdn") reloadOnBackup();
        else fail("The page's scripts could not be loaded, also not from this site's own copy. Reload the page; if it stays like this, use Report a Problem on the project's GitHub page.");
      };
      document.body.appendChild(main);
    });
  }

  Promise.all([getJSON("webui.json"), getJSON("importmaps.json")]).then(function (got) {
    var cfg = got[0], maps = got[1];
    if (backupChosen()) return start(cfg, maps, "backup");
    return cdnAnswers(maps.probe, (cfg.cdnWaitSeconds || 15) * 1000).then(function (ok) {
      if (!ok) console.warn("jsDelivr did not answer: three.js comes from this site's backup copy");
      start(cfg, maps, ok ? "cdn" : "backup");
    });
  }).catch(function (e) {
    fail("The page's settings (webui.json, importmaps.json) could not be loaded: " + e.message);
  });
})();
