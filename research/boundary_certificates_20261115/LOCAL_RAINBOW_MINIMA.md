# Exact rainbow minima on small directed triangles

Write $T_n=\{(x,y):0\le y<x<n\}$. A proper coloring has no monochromatic directed L, and a rainbow L uses all three colors. The minimum number of rainbow Ls among proper three-colorings is **0 on $T_9$, 1 on $T_{10}$, 3 on $T_{11}$ and 6 on $T_{12}$**.

| Triangle | Cells | Directed Ls | Minimum | Minimizers up to palette permutation |
|---|---:|---:|---:|---:|
| $T_9$ | 36 | 84 | 0 | 42 |
| $T_{10}$ | 45 | 120 | 1 | 12 |
| $T_{11}$ | 55 | 165 | 3 | 66 |
| $T_{12}$ | 66 | 220 | 6 | 204 |

The table counts different geometric placements separately. **small_triangle_rainbows.json** gives one literal example in each row. In particular the [five-rainbow proposal for the 11-triangle and seven-rainbow proposal for the 12-triangle](../../exploration/research_round4/research/DIVISOR_WEIGHTED_TRIANGLE_AVERAGING_0043.md) have explicit counterexamples.

## Enumerating prescribed rainbow positions

Every directed L in a proper coloring uses either two or three distinct colors. Prescribing the exact set of rainbow positions imposes one of those two constraints on each L. The checker enumerates sets of up to three positions. When a position is prescribed rainbow, its three cells may be fixed to colors 0, 1, 2 in their listed order. For an empty support we fix the first cell to 0 and divide the number of answers by two. Every coloring uses at least two colors, so the residual transposition acts freely.

Write each cell in barycentric coordinates $(x-y-1,y,n-x-1)$. Permutations of the three coordinates preserve the directed triples as unordered sets. The checker searches the least member of each geometric orbit of supports and weights its answer by the orbit size. A domain maintains the possible colors of each cell. A color can be deleted when no allowed assignment of the other two cells of an incident L supports it. After such deletions, branching tries each remaining color. Every accepted complete assignment is checked against every L.

For $T_{11}$, the numbers of supports at sizes 0, 1, 2, and 3 are 1, 165, 13,530, and 735,130. Their counts of palette classes are 0, 0, 0, and 66. The direct enumerator visits 415,514,610 search nodes at size three.

## Deleting a boundary line

Let $C(n,b)$ be the set of proper colorings of $T_n$ with at most $b$ rainbow Ls, up to geometric and palette symmetry. If a rainbow L touches any boundary line, delete that line. The remaining triangle belongs to $C(n-1,b-1)$. All three lines are equivalent under coordinate permutations. Conversely, a coloring in which no rainbow L touches any of the three lines has all rainbows in the inner $T_{n-3}$. Enumerating both cases and taking their union therefore gives the entire $C(n,b)$.

To extend an old triangle by its final row at $x=n$, each pair of new cells at indices $i<j$ closes exactly one L. Its old cell is $(n-(j-i),i)$. The extension routine tests every row prefix, rejects a monochromatic L immediately, and counts each new rainbow once. Every geometric orientation of the old triangle is tried before taking the least geometric and palette image of the result.

The interior-only search requires exactly two colors on every L touching the boundary, and two or three colors elsewhere. An interior L is forced rainbow when its current domains have no two-color assignment. If the forced number exceeds the remaining total bound, the branch ends. When it reaches the bound, every other L has to admit a two-color assignment. Branching still tries every possible color of the chosen cell.

As an independent enumeration, starting with the complete $T_{10}$ list through three rainbows gives 12, 1,182, and 32,168 palette classes at one, two, and three respectively. At $T_{11}$ there are 66 with three and 732 with four. None of these 798 colorings extends to a $T_{12}$ with five or fewer, and none exists in the interior-only case. Starting one order earlier enumerates the 204 six-rainbow colorings of $T_{12}$.

## Two larger reference colorings

Consider the set of rainbow positions of either of the [larger literal examples](RAINBOW_ROUTES.md). The following counts permit arbitrary changes to old rainbow positions and prescribe exactly $k$ new positions outside that set. The entries count all palette classes within that restriction, with geometric copies kept distinct.

| Reference | New positions | Total rainbow count and number of palette classes |
|---|---:|---|
| $T_{13}$ with 11 rainbows | 0 | 11 in one class |
| $T_{13}$ | 1 | 12 in three classes |
| $T_{13}$ | 2 | 12 in three classes, 13 in ten classes |
| $T_{14}$ with 17 rainbows | 0 | 17 in two classes |
| $T_{14}$ | 1 | 18 in five classes |
| $T_{14}$ | 2 | 18 in sixteen classes, 19 in seven classes |

Any improvement to either reference must introduce at least three previously absent rainbow positions. The exact-two-new-position searches cover 37,675 and 60,031 pairs, respectively.

## Reproduction

From this directory, compile both C99 programs. The Python drivers use only the standard library. The final command reports the multiplicity at six rainbows.

~~~sh
cc -O3 -std=c99 verify_rainbow_neighborhood.c -o rain_search
cc -O3 -std=c99 verify_triangle_extensions.c -o triangle_extend
python verify_local_rainbows.py ./rain_search --jobs 4
python verify_triangle_boundary.py ./rain_search ./triangle_extend --jobs 4
python verify_triangle_boundary.py ./rain_search ./triangle_extend --target 12 --budget 6 --jobs 4
~~~

## Exhaustive bounds on the 13-triangle

The minimum on $T_{13}$ is **11**. The complete run with budget ten has no coloring, and the archived literal example attains eleven. The complete order-13 run with budget nine gives the following orbit counts.

| Order | Budget | Geometric and palette orbits |
|---:|---:|---:|
| 7 | 3 | 68,209 |
| 8 | 4 | 577,522 |
| 9 | 5 | 1,469,001 |
| 10 | 6 | 1,014,625 |
| 11 | 7 | 411,914 |
| 12 | 8 | 1,838 |
| 13 | 9 | 0 |

Reproduce with **python verify_triangle_boundary.py ./rain_search ./triangle_extend --target 13 --budget 9 --jobs 4**. Increase the budget to ten to reproduce the sharp lower bound. The [position-weighted grid proof](THREE_COLOR_WEIGHTED.md) uses the resulting catalogs.

### Complete order-13 run at budget ten

| Order | Rainbow budget | Geometric and palette orbits |
|---|---:|---:|
| 6 | 3 | 9,037 |
| 7 | 4 | 209,967 |
| 8 | 5 | 2,159,586 |
| 9 | 6 | 6,471,235 |
| 10 | 7 | 4,698,032 |
| 11 | 8 | 1,644,484 |
| 12 | 9 | 16,060 |
| 13 | 10 | 0 |

At order 13, both the boundary extensions and the interior-only branch are empty. The reference eleven-rainbow coloring thus attains the minimum.

Every proper $T_{14}$ has **at least twelve** rainbow Ls. A hypothetical coloring with at most eleven and a rainbow touching a boundary would restrict to $T_{13}$ with at most ten, whose catalog is empty. The remaining interior-only case at order 14 was exhausted over the 27 assignments of cells 2, 3 and 4 in zero-based row-major order, after fixing cell 0 to color 0 and the domain of cell 1 to colors 0 and 1. All 1,420,657,038 branch nodes yielded zero colorings. The literal example at order 14 has seventeen.

The unpartitioned portable version of the interior-only search is **./rain_search 14 shell 11 0 0**. An independent full reconstruction from the base catalog is **python verify_triangle_boundary.py ./rain_search ./triangle_extend --target 14 --budget 11 --jobs 4**.

## The order-13 minimizers and the order-14 obstruction

The minimum of eleven on $T_{13}$ is attained by **21** colorings up to geometric symmetry and palette permutations, or **126** up to palette permutations alone. Every proper $T_{14}$ has **at least thirteen** rainbow Ls. A known coloring has seventeen. The [21 canonical colorings](triangle_13_minimizers.json) are stored in row-major order. All six palette-normalized geometric images of every word are distinct.

| Order | Rainbow budget | Geometric and palette orbits |
|---:|---:|---:|
| 6 | 4 | 16,330 |
| 7 | 5 | 497,369 |
| 8 | 6 | 6,625,801 |
| 9 | 7 | 24,681,208 |
| 10 | 8 | 19,798,396 |
| 11 | 9 | 5,285,641 |
| 12 | 10 | 296,559 |
| 13 | 11 | 21 |
| 14 | 12 | 0 |

Starting at order six, enumerate every proper coloring through four rainbows. At each subsequent order, start a separate exhaustive search for colorings whose rainbow Ls all avoid the three boundary lines. A coloring with a boundary rainbow has an orientation in which the last row touches a rainbow. Deleting this row leaves a proper coloring of the previous order with at least one fewer rainbow.

For a unique parent, normalize palette labels by first appearance and take the lexicographically first orientation among those whose last row touches a rainbow. Enumerate the distinct geometric orientations of each parent and append a row one cell at a time. For row entries at columns $i<j$, the third cell of their new L is the earlier cell at $(n-(j-i),i)$ when the new row is $x=n$. Check all these triples and keep the child only in its chosen eligible orientation. The unrestricted geometric minimum is its stored representative. Every parent here contains at least two colors, so normalizing the parent fixes how all three labels are used in extending it. The two sources of children are disjoint. The initial-word search divides into fixed prefixes after setting the first cell to zero and restricting the second cell to zero or one.

The following commands rebuild both top-order catalogs in one pass, check every saved coloring literally, and compare the order-13 words individually.

~~~sh
cc -O3 -std=c99 verify_rainbow_neighborhood.c -o rain_search
cc -O3 -std=c99 verify_triangle_stream.c -o triangle_stream
python verify_triangle_stream.py ./rain_search ./triangle_stream --jobs 4
~~~

## The central 13-triangle of a proper 22-triangle

The central copy of $T_{13}$ in every proper $T_{22}$ has **at least twelve** rainbow Ls. The embedding adds $(3,3,3)$ to the barycentric coordinates, or sends $(x,y)$ to $(x+6,y+3)$. Every symmetry of the central copy extends to the whole triangle because its three margins are equal. Thus a coloring with eleven central rainbows would yield an extension of one of the 21 archived words after a geometric symmetry and palette permutation.

The formula imposes one of three colors on each of the 231 cells and forbids all monochromatic directed Ls. It requires that at least one of the 21 canonical words matches the central cells. The archived RUP refutation excludes every such choice in one formula. Run **python verify_triangle_center.py /path/to/drat-trim** to reconstruct the 7,183 clauses and check the supplied proof. This gives a stronger local score for copies with sufficient space around them.

## Order 15

Every proper $T_{15}$ has at least **fourteen** rainbow Ls. A hypothetical coloring with at most thirteen and a boundary rainbow would restrict, after deleting a touched side, to $T_{14}$ with at most twelve. The latter catalog is empty. In the remaining case all rainbows avoid the boundary. The 27 prefix searches visited 5,742,796,021 branch nodes and returned zero colorings. The streaming reproduction above now continues through order 15.
