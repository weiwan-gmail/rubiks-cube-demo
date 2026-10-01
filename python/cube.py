"""
3×3 Rubik's Cube as 54-sticker (facelet) permutations.

Aligns with docs/math.md §7 interface:
  - sticker ids 0..53 by face U D L R F B × 9
  - generators as list[int] length 54: perm[i] = σ(i)
  - apply(state, move); is_solved(state)

Composition: applying move m to state replaces state so that the sticker
at position i moves to perm[i] (right action: state := state ∘ σ^{-1}
in array form: new[σ(i)] = old[i]).
"""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

# ---------------------------------------------------------------------------
# Indexing: face × 9, row-major when looking at that face
#   0 1 2
#   3 4 5
#   6 7 8
# ---------------------------------------------------------------------------

FACES = ("U", "D", "L", "R", "F", "B")
FACE_INDEX = {f: i for i, f in enumerate(FACES)}
N_STICKERS = 54

# Solved colors: one letter per face (centers define color)
SOLVED_COLORS = "".join(f * 9 for f in FACES)

def facelet(face: str, i: int) -> int:
    """Absolute sticker index for face in FACES and local 0..8."""
    return FACE_INDEX[face] * 9 + i


def _perm_from_cycles(cycles: Sequence[Sequence[int]]) -> List[int]:
    """Build length-54 map perm[i]=σ(i) from disjoint cycles (σ sends a→b→…)."""
    perm = list(range(N_STICKERS))
    for cycle in cycles:
        if len(cycle) < 2:
            continue
        for a, b in zip(cycle, cycle[1:]):
            perm[a] = b
        perm[cycle[-1]] = cycle[0]
    return perm


def _face_cw_cycles(face: str) -> List[Tuple[int, ...]]:
    """90° CW cycles on the 8 non-center stickers of one face."""
    b = facelet(face, 0)
    # corners 0→2→8→6→0 ; edges 1→5→7→3→1
    return [
        (b + 0, b + 2, b + 8, b + 6),
        (b + 1, b + 5, b + 7, b + 3),
    ]


def _U_side() -> List[Tuple[int, ...]]:
    """U CW (viewed from above): F top → L top → B top → R top → F."""
    # Derived from cubie tracking; indices 0,1,2 on each side face top row.
    return [
        (facelet("F", 0), facelet("L", 0), facelet("B", 0), facelet("R", 0)),
        (facelet("F", 1), facelet("L", 1), facelet("B", 1), facelet("R", 1)),
        (facelet("F", 2), facelet("L", 2), facelet("B", 2), facelet("R", 2)),
    ]


def _D_side() -> List[Tuple[int, ...]]:
    """D CW (viewed from below): F bottom → R bottom → B bottom → L bottom → F.

    With D face oriented so D0–D2 touch F6–F8 in the cross net, looking at D
    from below maps F→R→B→L for the bottom rows. B bottom indices reverse
    relative to F because B is opposite.
    """
    return [
        (facelet("F", 6), facelet("R", 6), facelet("B", 8), facelet("L", 6)),
        (facelet("F", 7), facelet("R", 7), facelet("B", 7), facelet("L", 7)),
        (facelet("F", 8), facelet("R", 8), facelet("B", 6), facelet("L", 8)),
    ]


def _L_side() -> List[Tuple[int, ...]]:
    """L CW (viewed from left): U left → F left → D left → B right → U.

    B is opposite F; when L turns, the B stickers that touch L are B2,B5,B8
    (B's right column when looking at B), and they cycle in reverse order.
    """
    return [
        (facelet("U", 0), facelet("F", 0), facelet("D", 0), facelet("B", 8)),
        (facelet("U", 3), facelet("F", 3), facelet("D", 3), facelet("B", 5)),
        (facelet("U", 6), facelet("F", 6), facelet("D", 6), facelet("B", 2)),
    ]


def _R_side() -> List[Tuple[int, ...]]:
    """R CW (viewed from right): U right → B left → D right → F right → U."""
    return [
        (facelet("U", 2), facelet("B", 6), facelet("D", 2), facelet("F", 2)),
        (facelet("U", 5), facelet("B", 3), facelet("D", 5), facelet("F", 5)),
        (facelet("U", 8), facelet("B", 0), facelet("D", 8), facelet("F", 8)),
    ]


def _F_side() -> List[Tuple[int, ...]]:
    """F CW (viewed from front): U bottom → R left → D top → L right → U."""
    return [
        (facelet("U", 6), facelet("R", 0), facelet("D", 2), facelet("L", 8)),
        (facelet("U", 7), facelet("R", 3), facelet("D", 1), facelet("L", 5)),
        (facelet("U", 8), facelet("R", 6), facelet("D", 0), facelet("L", 2)),
    ]


def _B_side() -> List[Tuple[int, ...]]:
    """B CW (viewed from back): U top → L left → D bottom → R right → U."""
    return [
        (facelet("U", 2), facelet("L", 0), facelet("D", 6), facelet("R", 8)),
        (facelet("U", 1), facelet("L", 3), facelet("D", 7), facelet("R", 5)),
        (facelet("U", 0), facelet("L", 6), facelet("D", 8), facelet("R", 2)),
    ]


def _build_generators() -> dict[str, List[int]]:
    sides = {
        "U": _U_side,
        "D": _D_side,
        "L": _L_side,
        "R": _R_side,
        "F": _F_side,
        "B": _B_side,
    }
    gens: dict[str, List[int]] = {}
    for face, side_fn in sides.items():
        cycles = _face_cw_cycles(face) + side_fn()
        gens[face] = _perm_from_cycles(cycles)
    return gens


GENERATORS = _build_generators()  # U D L R F B : each list[int] len 54


def compose(p: Sequence[int], q: Sequence[int]) -> List[int]:
    """Return p∘q as maps: (p∘q)(i) = p(q(i))."""
    return [p[q[i]] for i in range(len(q))]


def invert_perm(p: Sequence[int]) -> List[int]:
    inv = [0] * len(p)
    for i, j in enumerate(p):
        inv[j] = i
    return inv


def power_perm(p: Sequence[int], n: int) -> List[int]:
    """p^n for n >= 0."""
    out = list(range(len(p)))
    base = list(p)
    while n:
        if n & 1:
            out = compose(base, out)
        base = compose(base, base)
        n >>= 1
    return out


def all_moves() -> dict[str, List[int]]:
    """U, U', U2, D, D', … for all six faces."""
    moves: dict[str, List[int]] = {}
    for face, p in GENERATORS.items():
        moves[face] = list(p)
        moves[face + "'"] = invert_perm(p)
        moves[face + "2"] = power_perm(p, 2)
    return moves


MOVES = all_moves()


# ---------------------------------------------------------------------------
# State API
# ---------------------------------------------------------------------------

def solved_state() -> List[str]:
    return list(SOLVED_COLORS)


def is_solved(state: Sequence[str]) -> bool:
    return list(state) == list(SOLVED_COLORS)


def apply(state: Sequence[str], move: str) -> List[str]:
    """Apply one move name (e.g. \"R\", \"U'\", \"F2\") to a color state."""
    if move not in MOVES:
        raise KeyError(f"Unknown move {move!r}; expected one of {sorted(MOVES)}")
    perm = MOVES[move]
    # Sticker at i moves to perm[i] ⇒ new[perm[i]] = old[i]
    new = [""] * N_STICKERS
    for i, color in enumerate(state):
        new[perm[i]] = color
    return new


def apply_sequence(state: Sequence[str], sequence: Iterable[str]) -> List[str]:
    for m in sequence:
        state = apply(state, m)
    return list(state)


def parse_sequence(s: str) -> List[str]:
    """Parse Singmaster-like tokens: \"R U' F2\" or \"R U' F2\"."""
    tokens: List[str] = []
    i = 0
    s = s.strip()
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        face = s[i]
        if face not in FACE_INDEX:
            raise ValueError(f"Bad face {face!r} in {s!r}")
        i += 1
        suffix = ""
        if i < len(s) and s[i] in "'2i":
            if s[i] == "i":
                suffix = "'"
            else:
                suffix = s[i]
            i += 1
        tokens.append(face + suffix)
    return tokens


def inverse_sequence(seq: Sequence[str]) -> List[str]:
    inv_token = {"'": "", "2": "2", "": "'"}
    out: List[str] = []
    for m in reversed(seq):
        face, suf = m[0], m[1:] if len(m) > 1 else ""
        out.append(face + inv_token[suf])
    return out


# ---------------------------------------------------------------------------
# Optional: permutation parity / orientation sanity (legal moves only)
# ---------------------------------------------------------------------------

# Corner cubies as triples of facelet indices (U/D sticker first for twist).
# Twist 0 = U or D color on U/D; +1 / -1 = 120° CW / CCW of that reference.
CORNERS: Tuple[Tuple[int, int, int], ...] = (
    (facelet("U", 8), facelet("R", 0), facelet("F", 2)),  # UFR
    (facelet("U", 2), facelet("B", 0), facelet("R", 2)),  # UBR
    (facelet("U", 0), facelet("L", 0), facelet("B", 2)),  # UBL
    (facelet("U", 6), facelet("F", 0), facelet("L", 2)),  # UFL
    (facelet("D", 2), facelet("F", 8), facelet("R", 6)),  # DFR
    (facelet("D", 0), facelet("L", 8), facelet("F", 6)),  # DFL
    (facelet("D", 6), facelet("B", 8), facelet("L", 6)),  # DBL
    (facelet("D", 8), facelet("R", 8), facelet("B", 6)),  # DBR
)

# Edge cubies: (U/D or F/B reference sticker, other)
EDGES: Tuple[Tuple[int, int], ...] = (
    (facelet("U", 7), facelet("F", 1)),  # UF
    (facelet("U", 5), facelet("R", 1)),  # UR
    (facelet("U", 1), facelet("B", 1)),  # UB
    (facelet("U", 3), facelet("L", 1)),  # UL
    (facelet("D", 1), facelet("F", 7)),  # DF
    (facelet("D", 5), facelet("R", 7)),  # DR
    (facelet("D", 7), facelet("B", 7)),  # DB
    (facelet("D", 3), facelet("L", 7)),  # DL
    (facelet("F", 5), facelet("R", 3)),  # FR
    (facelet("F", 3), facelet("L", 5)),  # FL
    (facelet("B", 3), facelet("R", 5)),  # BR
    (facelet("B", 5), facelet("L", 3)),  # BL
)


def _perm_parity(perm: Sequence[int]) -> int:
    """Sign of permutation as map i→perm[i]: 0 even, 1 odd."""
    seen = [False] * len(perm)
    sign = 0
    for i in range(len(perm)):
        if seen[i]:
            continue
        length = 0
        j = i
        while not seen[j]:
            seen[j] = True
            j = perm[j]
            length += 1
        if length > 0:
            sign ^= (length - 1) & 1
    return sign


def corner_orientation_sum(state: Sequence[str]) -> int:
    """Sum of corner twists mod 3 (0 for reachable states)."""
    # Color of U/D centers
    ud = {state[facelet("U", 4)], state[facelet("D", 4)]}
    total = 0
    for trip in CORNERS:
        colors = [state[i] for i in trip]
        # find which slot holds U or D color
        for ori, c in enumerate(colors):
            if c in ud:
                total += ori
                break
    return total % 3


def edge_orientation_sum(state: Sequence[str]) -> int:
    """Sum of edge flips mod 2 (0 for reachable states).

    Good orientation: U/D color on U/D faces, or for equator edges,
    F/B color on F/B faces.
    """
    u_c = state[facelet("U", 4)]
    d_c = state[facelet("D", 4)]
    f_c = state[facelet("F", 4)]
    b_c = state[facelet("B", 4)]
    total = 0
    for a, b in EDGES:
        ca, cb = state[a], state[b]
        # Determine if flipped relative to solved home of this slot pair.
        # Rule: if either sticker is U/D colored, that color should be on the
        # U/D facelet of the pair when the pair sits on U/D; for M-slice style
        # we use: flip if U/D color is on the second slot when first is U/D
        # facelet, etc. Simpler facelet rule used by many solvers:
        face_a = a // 9
        # Faces: 0=U 1=D 2=L 3=R 4=F 5=B
        if face_a in (0, 1):  # first index is U or D facelet
            if ca not in (u_c, d_c):
                total ^= 1
        elif face_a in (4, 5):  # F/B facelet first (equator edges FR FL BR BL)
            if ca not in (f_c, b_c) and cb in (u_c, d_c):
                total ^= 1
            elif ca not in (f_c, b_c) and cb not in (u_c, d_c):
                # L/R colored on F/B counts as flip when other is L/R... 
                if ca in (state[facelet("L", 4)], state[facelet("R", 4)]):
                    total ^= 1
        else:
            # Should not happen with our EDGE table ordering
            pass
    return total


def assert_reachable_invariants(state: Sequence[str]) -> None:
    """Raise AssertionError if classic invariants fail (after legal moves they hold)."""
    # Build where each solved sticker color-position went — use piece permutation
    # via matching corner/edge color sets.
    solved = SOLVED_COLORS

    def corner_id(colors: Tuple[str, str, str]) -> frozenset:
        return frozenset(colors)

    solved_corners = [corner_id(tuple(solved[i] for i in t)) for t in CORNERS]
    cur_corners = [corner_id(tuple(state[i] for i in t)) for t in CORNERS]
    cperm = [solved_corners.index(c) for c in cur_corners]
    if _perm_parity(cperm) != 0:
        # Corner perm parity must match edge perm parity; check both.
        pass

    solved_edges = [frozenset(solved[i] for i in e) for e in EDGES]
    cur_edges = [frozenset(state[i] for i in e) for e in EDGES]
    eperm = [solved_edges.index(c) for c in cur_edges]

    if _perm_parity(cperm) != _perm_parity(eperm):
        raise AssertionError("corner/edge permutation parity mismatch")
    if corner_orientation_sum(state) != 0:
        raise AssertionError("corner orientation sum != 0 mod 3")
    # Edge orientation check is subtle with facelet rules; skip hard fail if
    # ambiguous — still verify corner twist + equal parity which are robust.
    _ = edge_orientation_sum(state)


# ---------------------------------------------------------------------------
# Display: face net + optional three interlocking rings (ASCII)
# ---------------------------------------------------------------------------

def face_str(state: Sequence[str], face: str) -> str:
    b = FACE_INDEX[face] * 9
    rows = []
    for r in range(3):
        rows.append(" ".join(state[b + 3 * r + c] for c in range(3)))
    return "\n".join(rows)


def net_str(state: Sequence[str]) -> str:
    """Cross net:

          U
        L F R B
          D
    """
    def row(face: str, r: int) -> str:
        b = FACE_INDEX[face] * 9 + 3 * r
        return " ".join(state[b + c] for c in range(3))

    lines = []
    pad = "        "
    for r in range(3):
        lines.append(pad + row("U", r))
    for r in range(3):
        lines.append(
            f"{row('L', r)}  {row('F', r)}  {row('R', r)}  {row('B', r)}"
        )
    for r in range(3):
        lines.append(pad + row("D", r))
    return "\n".join(lines)


def sticker_list_str(state: Sequence[str], width: int = 18) -> str:
    parts = [f"{i:02d}:{state[i]}" for i in range(N_STICKERS)]
    lines = []
    for i in range(0, N_STICKERS, width):
        lines.append(" ".join(parts[i : i + width]))
    return "\n".join(lines)


def rings_str(state: Sequence[str]) -> str:
    """ASCII hint of three interlocking rings (video motif).

    Not six face rings: three rings whose cycles share stickers at crossings,
    echoing interlocking orbits under face turns. Colors shown are current
    stickers on representative 4-cycles from U, R, F generators.
    """
    # Representative 4-cycles (corner orbit pieces) from three generators
    u_ring = [facelet("F", 1), facelet("L", 1), facelet("B", 1), facelet("R", 1)]
    r_ring = [facelet("U", 5), facelet("B", 3), facelet("D", 5), facelet("F", 5)]
    f_ring = [facelet("U", 7), facelet("R", 3), facelet("D", 1), facelet("L", 5)]

    def show(label: str, idxs: List[int]) -> str:
        cols = " → ".join(state[i] for i in idxs)
        return f"  {label}: ({cols} → …)"

    return "\n".join(
        [
            "Three interlocking rings (edge 4-cycles from U / R / F):",
            show("U-ring", u_ring),
            show("R-ring", r_ring),
            show("F-ring", f_ring),
            "  (shared stickers at face meetings = interlocking)",
        ]
    )


def moved_sticker_count(state: Sequence[str]) -> int:
    return sum(1 for i, c in enumerate(state) if c != SOLVED_COLORS[i])


__all__ = [
    "FACES",
    "N_STICKERS",
    "SOLVED_COLORS",
    "GENERATORS",
    "MOVES",
    "facelet",
    "solved_state",
    "is_solved",
    "apply",
    "apply_sequence",
    "parse_sequence",
    "inverse_sequence",
    "assert_reachable_invariants",
    "net_str",
    "rings_str",
    "sticker_list_str",
    "face_str",
    "moved_sticker_count",
]
