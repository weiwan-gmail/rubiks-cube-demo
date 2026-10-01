# Rubik’s Cube facelet demo (static site)

54-sticker (facelet) model of the 3×3 cube in the browser: face turns are permutations, sequences multiply, inverse restores the solved state (**identity**).

Live: **https://weiwan-gmail.github.io/rubiks-cube-demo/**

Companion to the local Python derivation under `python/` (ported from the box demo). [TheMathFlow](https://x.com/TheMathFlow/status/2101154346583154801) video is inspiration only — this site does **not** invent on-screen formulas and is **not** a CFOP solver. Three interlocking rings motif (U/R/F edge 4-cycles), not six.

## Try it

1. Default scramble `R U R' U'` → **Apply scramble** → `solved=false`.
2. **Apply inverse** → `solved=true`.

## Run locally

No build step. From the repo root:

```bash
python3 -m http.server 8080
# open http://127.0.0.1:8080/
```

Or open `index.html` directly in a browser.

Python reference (stdlib):

```bash
python3 python/demo.py
python3 python/demo.py "F R U R' U' F'"
```

## Layout

| Path | Role |
|------|------|
| `index.html` / `css/` / `js/` | Static UI + facelet engine |
| `js/cube.js` | Port of generators / apply / inverse / rings |
| `docs/math.md` | Math writeup (Chinese; fact / video / hypothesis) |
| `python/` | Original `cube.py` + `demo.py` |
| `.github/workflows/deploy.yml` | GitHub Pages (`build_type=workflow`) |

## Model ↔ math

1. Stickers `0..53` = faces **U D L R F B** × 9.
2. Generators as length-54 maps; also `X'`, `X2`.
3. `apply` / scramble / inverse → identity = solved.
4. See `docs/math.md` §7 interface notes.
