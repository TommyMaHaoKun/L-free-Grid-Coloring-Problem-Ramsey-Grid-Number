"""Check a weighted triangle certificate with exact integer arithmetic."""
import argparse
import json
import lzma
from heapq import heappush, heapreplace
from collections import Counter
from itertools import chain, product
from math import comb
from pathlib import Path

from verify_triangle_boundary import extend, listed, seed

ROOT = Path(__file__).resolve().parent


def geometry(n):
    corners = []
    for x in range(1, n):
        for y in range(x):
            for j in range(1, n-x):
                key = (j, *sorted((x-y-1, y, n-x-j-1)))
                i = x*(x-1)//2+y
                k = (x+j)*(x+j-1)//2+y
                corners.append((key, i, k, k+j))
    multiplicity = Counter(row[0] for row in corners)
    keys = sorted(multiplicity)
    ids = {k: i for i, k in enumerate(keys)}
    assert len(corners) == comb(n, 3)
    return keys, multiplicity, [(ids[key], a, b, c) for key, a, b, c in corners]


def profile(word, corners):
    out = []
    for k, a, b, c in corners:
        x, y, z = word[a], word[b], word[c]
        assert x != y or y != z
        if x != y and x != z and y != z:
            out.append(k)
    return tuple(sorted(out))


def rebuild(n, budget, search, extender, jobs):
    first = n-budget+3
    assert 6 <= first <= n
    words = seed(search, first, 3, jobs)
    for side in range(first+1, n+1):
        bound = 3+side-first
        words = extend(extender, side-1, bound, words)
        _, shell = listed([search, str(side), "shell", str(bound), "0", "0", "list"])
        words.update(shell)
    return words


def unpack(rule, N):
    n, d, weights, *band = rule
    Q = N-2-d*(n-2)
    if len(band) == 3:
        kind, lo, hi = band
    else:
        kind = "min"
        lo, hi = band if band else (0, Q//3+1)
    assert kind in ("min", "max")
    bound = Q//3+1 if kind == "min" else Q+1
    assert type(lo) is int and type(hi) is int and 0 <= lo < hi <= bound
    return n, d, weights, kind, lo, hi, Q


def translation_terms(Q, kind, lo, hi):
    """Signed lower-coordinate restrictions for the indicated translation band."""
    terms = Counter()
    if kind == "min":
        terms[lo, lo, lo] += 1
        terms[hi, hi, hi] -= 1
    else:
        for threshold, sign in [(hi, 1), (lo, -1)]:
            for bits in product((0, 1), repeat=3):
                terms[tuple(threshold*i for i in bits)] += sign*(-1)**sum(bits)
    return [(a, b, c, v) for (a, b, c), v in terms.items() if v and a+b+c <= Q]


def exact_incidence(N, rules, sources, keep=0):
    """Count placements at every host corner using independent row interval additions."""
    placements = {}
    for rule in rules:
        n, d, weights, kind, lo, hi, Q = unpack(rule, N)
        terms = translation_terms(Q, kind, lo, hi)
        _, keys, _, _ = sources[n]
        look = dict(zip(keys, weights))
        for j in range(1, n-1):
            shifts = placements.setdefault(j*d, Counter())
            for a in range(n-j-1):
                for b in range(n-j-1-a):
                    c = n-j-2-a-b
                    w = look[(j, *sorted((a, b, c)))]
                    if w:
                        for u, v, t, sign in terms:
                            shifts[d*a+u, d*b+v, d*c+t] += sign*w
    maximum = 0
    top = []
    for h, shifts in placements.items():
        L = N-h-2
        differences = [[0]*(L-A+2) for A in range(L+1)]
        for (a, b, c), w in shifts.items():
            for A in range(a, L-b-c+1):
                differences[A][b] += w
                differences[A][L-A-c+1] -= w
        for row in differences:
            running = 0
            for change in row[:-1]:
                running += change
                assert running >= 0
                maximum = max(maximum, running)
                if keep and running:
                    if len(top) < keep:
                        heappush(top, running)
                    elif running > top[0]:
                        heapreplace(top, running)
            assert running+row[-1] == 0
    return maximum, sum(top)


def verify(cert, catalogs):
    N = cert["host"]
    sources = {}
    for n, b in cert["sources"]:
        keys, multiplicity, corners = geometry(n)
        words = catalogs[f"{n}/{b}"]
        assert len(words) == len(set(words))
        assert all(len(w) == comb(n, 2) and set(w) <= set("012") for w in words)
        profiles = {profile(w, corners) for w in words}
        assert all(len(p) <= b for p in profiles)
        sources[n] = b, keys, multiplicity, profiles
    incidence = Counter()
    copy_counts = {}
    total = 0
    for rule in cert["rules"]:
        n, d, weights, kind, lo, hi, Q = unpack(rule, N)
        b, keys, multiplicity, profiles = sources[n]
        assert 1 <= d <= (N-2)//(n-2) and len(weights) == len(keys)
        assert all(type(v) is int and v >= 0 for v in weights)
        floor = min(chain([(b+1)*min(weights)], (sum(weights[i] for i in p) for p in profiles)))
        terms = translation_terms(Q, kind, lo, hi)
        copies = sum(sign*comb(Q-u-v-t+2, 2) for u, v, t, sign in terms)
        region = Q, kind, lo, hi
        if region not in copy_counts:
            select = min if kind == "min" else max
            copy_counts[region] = sum(
                lo <= select(a, b, Q-a-b) < hi
                for a in range(Q+1) for b in range(Q-a+1)
            )
        assert copies == copy_counts[region]
        total += floor*copies
        for (j, a, c, e), w in zip(keys, weights):
            incidence[j*d] += multiplicity[j, a, c, e]*w
    upper = comb(N, 2)-(N-1)+(N-1)//3
    ranked = cert.get("mode") == "ranked"
    if cert.get("mode") in ("exact", "bands", "ranked", "regions"):
        K, heaviest = exact_incidence(N, cert["rules"], sources, upper if ranked else 0)
    else:
        K, heaviest = max(incidence.values()), 0
    ceiling = heaviest if ranked else K*upper
    margin = total-ceiling
    assert margin > 0
    print(f"Side {N}, weighted lower total {total:,}, maximum incidence {K:,}, "
          f"global rainbow ceiling {upper:,}, weighted ceiling {ceiling:,}, contradiction margin {margin:,}.")
    return margin


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rebuild", nargs=2, metavar=("SEARCH", "EXTEND"),
                        help="re-enumerate every archived low-rainbow catalog")
    parser.add_argument("--jobs", type=int, default=1)
    args = parser.parse_args()
    cert = json.loads((ROOT/"triangle_grid_certificate.json").read_text())
    catalogs = json.loads(lzma.decompress((ROOT/"triangle_grid_catalogs.json.xz").read_bytes()))
    if args.rebuild:
        search, extender = (str(Path(p).resolve()) for p in args.rebuild)
        for n, b in cert["sources"]:
            words = rebuild(n, b, search, extender, args.jobs)
            assert {w.decode() for w in words} == set(catalogs[f"{n}/{b}"])
            print(f"Reproduced T{n} through {b} rainbows, {len(words):,} orbits.", flush=True)
    result = verify(cert, catalogs)
    assert result == cert["margin"]


if __name__ == "__main__":
    main()
