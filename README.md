# Rubik’s Cube facelet demo (static site)

54-sticker (facelet) model of the 3×3 cube in the browser: face turns are permutations, sequences multiply, inverse restores the solved state (**identity**).

Live:

- Site: **https://weiwan-gmail.github.io/rubiks-cube-demo/**
- Teaching page (Chinese): **https://weiwan-gmail.github.io/rubiks-cube-demo/teach.html**

Companion to the local Python derivation under `python/` (ported from the box demo). [TheMathFlow](https://x.com/TheMathFlow/status/2101154346583154801) video is inspiration only — this site does **not** invent on-screen formulas and is **not** a CFOP solver. Three interlocking rings motif (U/R/F edge 4-cycles), not six. `themathflow.mp4` is a **local reference only** (not uploaded here).

## Try it

1. Default scramble `R U R' U'` → **Apply scramble** → `solved=false`.
2. **Apply inverse** → `solved=true`.

The same loop is `python/demo.py` (see [sample-output.txt](sample-output.txt)). Chinese lesson with 【事实】 / 【视频观察】 / 【假设】 tags: [teach.html](teach.html) ([teach.md](teach.md) source). Shorter math notes: [docs/math.md](docs/math.md).

## Run locally

No build step. From the repo root:

```bash
python3 -m http.server 8080
# open http://127.0.0.1:8080/
# teach page: http://127.0.0.1:8080/teach.html
```

Or open `index.html` directly in a browser.

### 如何运行 Python demo

网页上的 Apply scramble / inverse 与下面命令镜像。在仓库根目录：

```bash
python3 python/demo.py
python3 python/demo.py "F R U R' U' F'"
```

Stdlib only (Python 3.10+). Equivalent: `cd python && python3 demo.py`. Reuse `.venv` if you have one (`./.venv/bin/python python/demo.py`). Captured default-scramble transcript: [sample-output.txt](sample-output.txt).

## Layout

| Path | Role |
|------|------|
| `index.html` / `css/` / `js/` | Interactive facelet demo (site entry) |
| `teach.html` / `teach.md` | Chinese teaching page (KaTeX; fact / hypothesis tags) |
| `sample-output.txt` | Captured run of `python/demo.py` (default scramble) |
| `js/cube.js` | Port of generators / apply / inverse / rings |
| `docs/math.md` | Shorter math writeup (Chinese; 事实 / 视频观察 / 假设) |
| `python/` | Original `cube.py` + `demo.py` (do not treat as a solver) |
| `.github/workflows/deploy.yml` | GitHub Pages (`build_type=workflow`, static repo root) |

Relative links (`css/style.css`, `teach.html`, `docs/math.md`) resolve under the Pages base path `/rubiks-cube-demo/`.

## Model ↔ math

1. Stickers `0..53` = faces **U D L R F B** × 9.
2. Generators as length-54 maps; also `X'`, `X2`.
3. `apply` / scramble / inverse → identity = solved.
4. See `docs/math.md` §7 interface notes and `teach.html` sections F–N.

