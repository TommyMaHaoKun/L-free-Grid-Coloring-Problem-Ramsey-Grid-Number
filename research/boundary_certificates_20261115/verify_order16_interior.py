"""Verify the zero-boundary case for the fifteen-rainbow lower bound on T16."""
import argparse
import lzma
from itertools import combinations, permutations
from pathlib import Path
from tempfile import TemporaryDirectory

from pysat.card import CardEnc, EncType
from verify_rectangle_lines import check

HERE = Path(__file__).resolve().parent


def formula():
    n = 16
    cells = [(x,y) for x in range(1,n) for y in range(x)]
    index = {point: i for i,point in enumerate(cells)}
    rows = []
    for v in range(len(cells)):
        colors = [1+3*v+c for c in range(3)]
        rows.append(colors)
        rows.extend([[-i,-j] for i,j in combinations(colors,2)])
    interior = []
    for x,y in cells:
        for d in range(1,n-x):
            points = ((x,y),(x+d,y),(x+d,y+d))
            corners = [index[p] for p in points]
            rows.extend([[-1-3*v-c for v in corners] for c in range(3)])
            boundary = any(b==0 or b==a-1 or a==n-1 for a,b in points)
            if boundary:
                rows.extend([[-1-3*v-c for v,c in zip(corners,p)] for p in permutations(range(3))])
            else:
                interior.append(((x-y-1,y,n-1-x-d),corners))
    rows.extend([[1], [1+3*index[(15,0)]], [2+3*index[(15,14)]]])
    high = 3*len(cells)
    selectors = []
    for position,corners in interior:
        high += 1
        selectors.append((position,high))
        rows.extend([[-1-3*v-c for v,c in zip(corners,p)]+[high] for p in permutations(range(3))])
    assert len(selectors)==286

    def at_most(flags,limit):
        nonlocal high
        if len(flags)<=limit:
            return
        encoding = EncType.pairwise if limit==1 else EncType.seqcounter
        block = CardEnc.atmost(flags,limit,high,encoding=encoding)
        rows.extend(block.clauses)
        high = max(high,block.nv)

    seen = set()
    for m,minimum in ((15,14),(14,13),(13,11),(12,6),(11,3)):
        for a in range(n-m+1):
            for b in range(n-m-a+1):
                c = n-m-a-b
                outside = tuple(flag for (i,j,k),flag in selectors if i<a or j<b or k<c)
                limit = 14-minimum
                if (outside,limit) not in seen:
                    at_most(outside,limit)
                    seen.add((outside,limit))
    at_most([v for _,v in selectors],14)
    return (f"p cnf {high} {len(rows)}\n" +
            "".join(" ".join(map(str,row))+" 0\n" for row in rows)).encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checker",type=Path,help="path to drat-trim")
    args = parser.parse_args()
    with TemporaryDirectory() as tmp:
        cnf,proof = Path(tmp)/"triangle.cnf",Path(tmp)/"triangle.rup"
        cnf.write_bytes(formula())
        proof.write_bytes(lzma.decompress((HERE/"order16_interior.rup.xz").read_bytes()))
        check(args.checker.resolve(),cnf,proof)
    print("Every proper order-16 triangle with no boundary rainbow has at least fifteen interior rainbows.")


if __name__=="__main__":
    main()
