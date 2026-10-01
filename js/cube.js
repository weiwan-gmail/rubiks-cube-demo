/**
 * 3×3 Rubik's Cube as 54-sticker (facelet) permutations.
 * Port of python/cube.py — same cycles, apply, inverse, net display helpers.
 */
(function (global) {
  "use strict";

  const FACES = ["U", "D", "L", "R", "F", "B"];
  const FACE_INDEX = Object.fromEntries(FACES.map((f, i) => [f, i]));
  const N_STICKERS = 54;
  const SOLVED_COLORS = FACES.map((f) => f.repeat(9)).join("");

  function facelet(face, i) {
    return FACE_INDEX[face] * 9 + i;
  }

  function permFromCycles(cycles) {
    const perm = Array.from({ length: N_STICKERS }, (_, i) => i);
    for (const cycle of cycles) {
      if (cycle.length < 2) continue;
      for (let k = 0; k < cycle.length - 1; k++) {
        perm[cycle[k]] = cycle[k + 1];
      }
      perm[cycle[cycle.length - 1]] = cycle[0];
    }
    return perm;
  }

  function faceCwCycles(face) {
    const b = facelet(face, 0);
    return [
      [b + 0, b + 2, b + 8, b + 6],
      [b + 1, b + 5, b + 7, b + 3],
    ];
  }

  function USide() {
    return [
      [facelet("F", 0), facelet("L", 0), facelet("B", 0), facelet("R", 0)],
      [facelet("F", 1), facelet("L", 1), facelet("B", 1), facelet("R", 1)],
      [facelet("F", 2), facelet("L", 2), facelet("B", 2), facelet("R", 2)],
    ];
  }

  function DSide() {
    return [
      [facelet("F", 6), facelet("R", 6), facelet("B", 8), facelet("L", 6)],
      [facelet("F", 7), facelet("R", 7), facelet("B", 7), facelet("L", 7)],
      [facelet("F", 8), facelet("R", 8), facelet("B", 6), facelet("L", 8)],
    ];
  }

  function LSide() {
    return [
      [facelet("U", 0), facelet("F", 0), facelet("D", 0), facelet("B", 8)],
      [facelet("U", 3), facelet("F", 3), facelet("D", 3), facelet("B", 5)],
      [facelet("U", 6), facelet("F", 6), facelet("D", 6), facelet("B", 2)],
    ];
  }

  function RSide() {
    return [
      [facelet("U", 2), facelet("B", 6), facelet("D", 2), facelet("F", 2)],
      [facelet("U", 5), facelet("B", 3), facelet("D", 5), facelet("F", 5)],
      [facelet("U", 8), facelet("B", 0), facelet("D", 8), facelet("F", 8)],
    ];
  }

  function FSide() {
    return [
      [facelet("U", 6), facelet("R", 0), facelet("D", 2), facelet("L", 8)],
      [facelet("U", 7), facelet("R", 3), facelet("D", 1), facelet("L", 5)],
      [facelet("U", 8), facelet("R", 6), facelet("D", 0), facelet("L", 2)],
    ];
  }

  function BSide() {
    return [
      [facelet("U", 2), facelet("L", 0), facelet("D", 6), facelet("R", 8)],
      [facelet("U", 1), facelet("L", 3), facelet("D", 7), facelet("R", 5)],
      [facelet("U", 0), facelet("L", 6), facelet("D", 8), facelet("R", 2)],
    ];
  }

  function buildGenerators() {
    const sides = { U: USide, D: DSide, L: LSide, R: RSide, F: FSide, B: BSide };
    const gens = {};
    for (const [face, sideFn] of Object.entries(sides)) {
      const cycles = faceCwCycles(face).concat(sideFn());
      gens[face] = permFromCycles(cycles);
    }
    return gens;
  }

  const GENERATORS = buildGenerators();

  function compose(p, q) {
    return q.map((_, i) => p[q[i]]);
  }

  function invertPerm(p) {
    const inv = new Array(p.length);
    for (let i = 0; i < p.length; i++) inv[p[i]] = i;
    return inv;
  }

  function powerPerm(p, n) {
    let out = Array.from({ length: p.length }, (_, i) => i);
    let base = p.slice();
    while (n > 0) {
      if (n & 1) out = compose(base, out);
      base = compose(base, base);
      n >>= 1;
    }
    return out;
  }

  function allMoves() {
    const moves = {};
    for (const [face, p] of Object.entries(GENERATORS)) {
      moves[face] = p.slice();
      moves[face + "'"] = invertPerm(p);
      moves[face + "2"] = powerPerm(p, 2);
    }
    return moves;
  }

  const MOVES = allMoves();

  function solvedState() {
    return SOLVED_COLORS.split("");
  }

  function isSolved(state) {
    return state.join("") === SOLVED_COLORS;
  }

  function apply(state, move) {
    const perm = MOVES[move];
    if (!perm) throw new Error("Unknown move: " + move);
    const next = new Array(N_STICKERS);
    for (let i = 0; i < N_STICKERS; i++) next[perm[i]] = state[i];
    return next;
  }

  function applySequence(state, sequence) {
    let s = state.slice();
    for (const m of sequence) s = apply(s, m);
    return s;
  }

  function parseSequence(str) {
    const tokens = [];
    let i = 0;
    const s = str.trim();
    while (i < s.length) {
      if (/\s/.test(s[i])) {
        i++;
        continue;
      }
      const face = s[i];
      if (!(face in FACE_INDEX)) throw new Error("Bad face '" + face + "' in " + JSON.stringify(s));
      i++;
      let suffix = "";
      if (i < s.length && "'2i".includes(s[i])) {
        suffix = s[i] === "i" ? "'" : s[i];
        i++;
      }
      tokens.push(face + suffix);
    }
    return tokens;
  }

  function inverseSequence(seq) {
    const invToken = { "'": "", "2": "2", "": "'" };
    const out = [];
    for (let k = seq.length - 1; k >= 0; k--) {
      const m = seq[k];
      const face = m[0];
      const suf = m.length > 1 ? m.slice(1) : "";
      out.push(face + invToken[suf]);
    }
    return out;
  }

  function movedStickerCount(state) {
    let n = 0;
    for (let i = 0; i < N_STICKERS; i++) if (state[i] !== SOLVED_COLORS[i]) n++;
    return n;
  }

  /** Edge 4-cycles from U / R / F — three interlocking rings motif. */
  const RING_INDICES = {
    U: [facelet("F", 1), facelet("L", 1), facelet("B", 1), facelet("R", 1)],
    R: [facelet("U", 5), facelet("B", 3), facelet("D", 5), facelet("F", 5)],
    F: [facelet("U", 7), facelet("R", 3), facelet("D", 1), facelet("L", 5)],
  };

  function ringColors(state, key) {
    return RING_INDICES[key].map((i) => state[i]);
  }

  function faceStickers(state, face) {
    const b = FACE_INDEX[face] * 9;
    return state.slice(b, b + 9);
  }

  global.RubiksCube = {
    FACES,
    FACE_INDEX,
    N_STICKERS,
    SOLVED_COLORS,
    GENERATORS,
    MOVES,
    facelet,
    solvedState,
    isSolved,
    apply,
    applySequence,
    parseSequence,
    inverseSequence,
    movedStickerCount,
    RING_INDICES,
    ringColors,
    faceStickers,
  };
})(typeof window !== "undefined" ? window : globalThis);
