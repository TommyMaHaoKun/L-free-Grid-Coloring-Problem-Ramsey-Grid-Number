# A position-weighted proof that the three-color grid number is at most 284

Every three-coloring of the 284 by 284 square contains a monochromatic directed L. Combined with the published 20 by 20 construction, this gives $21\le R_3\le 284$. The proof uses finite triangle coloring counts and integer arithmetic. Its local catalogs cover $T_{11}$ through 5 rainbows (2,742 orbits), $T_{12}$ through 8 rainbows (1,838 orbits), $T_{13}$ through 9 rainbows (0 orbits), up to simultaneous renaming of colors and permutations of the three geometric coordinates.

## Local scores

Give each cell of $T_m$ its nonnegative coordinates $(x-y-1,y,m-x-1)$, of sum $m-2$. An L of leg $j$ has vertices obtained by adding $j$ in each of the three coordinate directions to a fixed vector $(a,b,c)$ of sum $m-j-2$. Its symmetry class is $(j,\mathrm{sort}(a,b,c))$.

For each source order $m$ and dilation $d$, the certificate assigns a nonnegative integer weight to each such class. Let $b_m$ be the archived rainbow cutoff for that order. A coloring with more than $b_m$ rainbows has weight at least $(b_m+1)\min w$. For every coloring at or below the cutoff, sum the weights of its actual rainbow Ls. The minimum of those finite scores and the preceding lower bound is a valid lower bound $s_{m,d}$ for every proper coloring. The exhaustive [boundary-deletion recurrence](LOCAL_RAINBOW_MINIMA.md) supplies every archived coloring, including the empty catalogs.

## Copies and the boundary of the host

The host is $T_N$ with $N=284$. Dilation by $d$ followed by adding any nonnegative triple with sum $N-2-d(m-2)$ gives exactly $\binom{N-d(m-2)}2$ copies. A proper coloring of the host therefore has total weighted rainbow count across copies at least
\[
  J=\sum_{m,d} s_{m,d}\binom{N-d(m-2)}2 .
\]

Fix one host L of step $h$ and base coordinates $(A,B,C)$, with $A+B+C=N-h-2$. A given source L of step $j$ at $(a,b,c)$ maps to it exactly when $h=dj$ and $A\ge da,\ B\ge db,\ C\ge dc$. These conditions uniquely determine the translation. Add the applicable weights and take the maximum $K$ over all host corners. For independent exact counting, at fixed $h,A$ the admissible $B$ form the integer interval $[db,N-h-2-A-dc]$. The verifier adds each weight to that interval using its two endpoints and scans every possible $B$.

The manuscript's line identity gives $\mathcal R_N\le U_N=\binom N2-(N-1)+\lfloor(N-1)/3\rfloor$ for the total number of rainbows in a proper coloring. Hence $J\le K\mathcal R_N\le KU_N$. The published integers give **$J-KU_N=242,473,938,095,219>0$**. This contradiction rules out a proper $T_N$ and thus a proper square of side $N$. [Three-color line identity and embedding argument](../../manuscript/main.tex)

## Reproduction

The portable C and Python checkers use their standard libraries. The first Python command checks the catalog colorings, their weighted scores, and the exact host incidences. The final command also regenerates every low-rainbow catalog from the full search and compares its colorings individually.

~~~sh
cc -O3 -std=c99 verify_rainbow_neighborhood.c -o rain_search
cc -O3 -std=c99 verify_triangle_extensions.c -o triangle_extend
python verify_triangle_grid.py
python verify_triangle_grid.py --rebuild ./rain_search ./triangle_extend --jobs 4
~~~
