(function () {
  "use strict";
  const C = window.RubiksCube;

  const COLOR_HEX = {
    U: "#f5f5f5",
    D: "#f7d117",
    L: "#ff8c00",
    R: "#c41e3a",
    F: "#009e60",
    B: "#0051ba",
  };

  let state = C.solvedState();
  let lastSeq = [];
  let lastInv = [];

  const els = {
    sequence: document.getElementById("sequence"),
    status: document.getElementById("status"),
    tokens: document.getElementById("tokens"),
    net: document.getElementById("net"),
    ringsSvg: document.getElementById("rings-svg"),
    ringsText: document.getElementById("rings-text"),
    error: document.getElementById("error"),
  };

  function setError(msg) {
    els.error.textContent = msg || "";
    els.error.hidden = !msg;
  }

  function renderFace(face, stickers) {
    const cells = stickers
      .map(
        (c) =>
          `<span class="cell" style="background:${COLOR_HEX[c]}" title="${c}"></span>`
      )
      .join("");
    return `<div class="face" data-face="${face}"><div class="face-label">${face}</div><div class="grid">${cells}</div></div>`;
  }

  function renderNet() {
    const order = [
      [null, "U", null, null],
      ["L", "F", "R", "B"],
      [null, "D", null, null],
    ];
    els.net.innerHTML = order
      .map(
        (row) =>
          `<div class="net-row">${row
            .map((f) =>
              f
                ? renderFace(f, C.faceStickers(state, f))
                : '<div class="face face-empty"></div>'
            )
            .join("")}</div>`
      )
      .join("");
  }

  function updateRingsSvg() {
    const rings = [
      { key: "U", cx: 160, cy: 120, r: 78, stroke: "#7aa2ff" },
      { key: "R", cx: 220, cy: 180, r: 78, stroke: "#ff7a9a" },
      { key: "F", cx: 120, cy: 200, r: 78, stroke: "#5fd4a0" },
    ];
    const parts = [
      '<svg viewBox="0 0 340 320" width="340" height="320" role="img" aria-label="Three interlocking rings">',
    ];
    for (const ring of rings) {
      parts.push(
        `<circle cx="${ring.cx}" cy="${ring.cy}" r="${ring.r}" fill="none" stroke="${ring.stroke}" stroke-width="10" opacity="0.85"/>`
      );
      const colors = C.ringColors(state, ring.key);
      colors.forEach((c, i) => {
        const ang = -Math.PI / 2 + (i * Math.PI) / 2;
        const x = ring.cx + ring.r * Math.cos(ang);
        const y = ring.cy + ring.r * Math.sin(ang);
        parts.push(
          `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="14" fill="${COLOR_HEX[c]}" stroke="#111" stroke-width="1.5"/>`
        );
        parts.push(
          `<text x="${x.toFixed(1)}" y="${(y + 4).toFixed(1)}" text-anchor="middle" font-size="11" font-family="ui-monospace,monospace" fill="#111">${c}</text>`
        );
      });
      parts.push(
        `<text x="${ring.cx}" y="${ring.cy + 4}" text-anchor="middle" font-size="13" font-weight="600" fill="${ring.stroke}" font-family="system-ui,sans-serif">${ring.key}</text>`
      );
    }
    parts.push("</svg>");
    els.ringsSvg.innerHTML = parts.join("");

    const lines = ["Three interlocking rings (edge 4-cycles from U / R / F):"];
    for (const key of ["U", "R", "F"]) {
      const cols = C.ringColors(state, key).join(" → ");
      lines.push(`  ${key}-ring: (${cols} → …)`);
    }
    lines.push("  (shared stickers at face meetings = interlocking)");
    els.ringsText.textContent = lines.join("\n");
  }

  function updateStatus(extra) {
    const solved = C.isSolved(state);
    const off = C.movedStickerCount(state);
    els.status.innerHTML =
      `<span class="pill ${solved ? "ok" : "no"}">solved=${solved}</span>` +
      ` <span class="pill">stickers_off_home=${off}</span>` +
      (extra ? ` <span class="muted">${extra}</span>` : "");
  }

  function refresh(extra) {
    renderNet();
    updateRingsSvg();
    updateStatus(extra);
  }

  function readSeq() {
    return C.parseSequence(els.sequence.value || "");
  }

  document.getElementById("btn-reset").addEventListener("click", () => {
    setError("");
    state = C.solvedState();
    lastSeq = [];
    lastInv = [];
    els.tokens.textContent = "";
    refresh("reset to identity");
  });

  document.getElementById("btn-scramble").addEventListener("click", () => {
    try {
      setError("");
      const seq = readSeq();
      lastSeq = seq;
      lastInv = C.inverseSequence(seq);
      state = C.applySequence(C.solvedState(), seq);
      els.tokens.textContent =
        "scramble: [" +
        seq.map((t) => JSON.stringify(t)).join(", ") +
        "]  inverse: [" +
        lastInv.map((t) => JSON.stringify(t)).join(", ") +
        "]";
      refresh("after scramble");
    } catch (e) {
      setError(String(e.message || e));
    }
  });

  document.getElementById("btn-inverse").addEventListener("click", () => {
    try {
      setError("");
      let inv = lastInv;
      if (!inv.length) {
        const seq = readSeq();
        inv = C.inverseSequence(seq);
        lastSeq = seq;
        lastInv = inv;
      }
      state = C.applySequence(state, inv);
      els.tokens.textContent =
        "applied inverse: [" +
        inv.map((t) => JSON.stringify(t)).join(", ") +
        "]";
      refresh("after inverse — expect identity");
    } catch (e) {
      setError(String(e.message || e));
    }
  });

  document.getElementById("btn-apply").addEventListener("click", () => {
    try {
      setError("");
      const seq = readSeq();
      lastSeq = seq;
      lastInv = C.inverseSequence(seq);
      state = C.applySequence(state, seq);
      els.tokens.textContent =
        "applied: [" + seq.map((t) => JSON.stringify(t)).join(", ") + "]";
      refresh("moves applied to current state");
    } catch (e) {
      setError(String(e.message || e));
    }
  });

  // Face turn quick buttons
  document.querySelectorAll("[data-move]").forEach((btn) => {
    btn.addEventListener("click", () => {
      try {
        setError("");
        const m = btn.getAttribute("data-move");
        state = C.apply(state, m);
        lastSeq = [m];
        lastInv = C.inverseSequence([m]);
        els.tokens.textContent = "applied: " + m;
        refresh("single move");
      } catch (e) {
        setError(String(e.message || e));
      }
    });
  });

  refresh("start: solved (identity)");
})();
