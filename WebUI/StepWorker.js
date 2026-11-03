/* StepWorker.js - reads a STEP file KESE wrote into triangles, in a background thread (StepReader.js does the
   reading).  The page sends {buffer} (the file's bytes) and gets {type: "progress", fraction} while it reads, then
   {type: "done", solids: [{name, color, positions}]} or {type: "error", error}. */
import { readKeseStep } from "./StepReader.js";

onmessage = (ev) => {
  try {
    const text = new TextDecoder().decode(ev.data.buffer);
    let last = 0;
    const solids = readKeseStep(text, (f) => {
      if (f - last >= 0.02) { last = f; postMessage({ type: "progress", fraction: f }); }
    });
    postMessage({ type: "done", solids }, solids.map((s) => s.positions.buffer));
  } catch (e) {
    postMessage({ type: "error", error: String(e && e.message || e) });
  }
};
