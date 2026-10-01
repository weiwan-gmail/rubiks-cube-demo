#!/usr/bin/env python3
"""
Rubik's Cube derivation demo: 54 stickers, face-turn permutations.

Starts solved → short scramble → show state → inverse → solved again.
Stdlib only. See README.md and docs/math.md.
"""

from __future__ import annotations

import sys

from cube import (
    GENERATORS,
    N_STICKERS,
    apply_sequence,
    assert_reachable_invariants,
    inverse_sequence,
    is_solved,
    moved_sticker_count,
    net_str,
    parse_sequence,
    rings_str,
    solved_state,
    sticker_list_str,
)


SCRAMBLE = "R U R' U'"  # sexy move: short, well-known, order 6


def banner(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def show(state, *, rings: bool = True) -> None:
    print(net_str(state))
    print(f"solved={is_solved(state)}  stickers_off_home={moved_sticker_count(state)}")
    if rings:
        print(rings_str(state))


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    scramble_str = SCRAMBLE
    if argv:
        scramble_str = " ".join(argv)

    banner("1. Model: 54 stickers, six face-turn generators")
    print(f"N_STICKERS = {N_STICKERS}")
    print("Faces: U D L R F B  (each 9 facelets, ids face*9 + 0..8)")
    for face, perm in GENERATORS.items():
        moved = sum(1 for i, j in enumerate(perm) if i != j)
        # show one 4-cycle fragment from the perm
        print(f"  {face}: perm sends {moved} stickers (center fixed); e.g. 0→{perm[0]}")

    banner("2. Start: solved (identity)")
    state = solved_state()
    show(state)

    banner(f"3. Scramble: {scramble_str}")
    seq = parse_sequence(scramble_str)
    print("tokens:", seq)
    state = apply_sequence(state, seq)
    try:
        assert_reachable_invariants(state)
        print("invariants: corner/edge parity match, corner twist sum ≡ 0 (mod 3)")
    except AssertionError as e:
        print("invariant check failed:", e)
    show(state)
    print("--- sticker list (index:color) ---")
    print(sticker_list_str(state))

    banner("4. Inverse sequence → expect solved")
    inv = inverse_sequence(seq)
    print("inverse tokens:", inv)
    state = apply_sequence(state, inv)
    show(state)

    ok = is_solved(state)
    banner("5. Result")
    print(f"scramble then inverse returns to solved: {ok}")
    if not ok:
        print("FAILED", file=sys.stderr)
        return 1
    print("OK — face turns permute stickers; inverse restores identity.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
