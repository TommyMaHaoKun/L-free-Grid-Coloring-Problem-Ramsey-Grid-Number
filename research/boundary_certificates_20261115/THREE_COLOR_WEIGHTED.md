# A position-weighted proof that the three-color grid number is at most 152

Every three-coloring of the 152 by 152 square contains a monochromatic directed L. Combined with the published 20 by 20 construction, this gives $21\le R_3\le 152$. The proof uses finite triangle coloring counts and integer arithmetic. Its local catalogs cover $T_{11}$ through 6 rainbows (59,401 orbits), $T_{12}$ through 9 rainbows (16,060 orbits), $T_{13}$ through 11 rainbows (21 orbits), $T_{14}$ through 12 rainbows (0 orbits), $T_{15}$ through 13 rainbows (0 orbits), $T_{16}$ through 14 rainbows (0 orbits), up to simultaneous renaming of colors and permutations of the three geometric coordinates.

## Local scores

Give each cell of $T_m$ its nonnegative coordinates $(x-y-1,y,m-x-1)$, of sum $m-2$. An L of leg $j$ has vertices obtained by adding $j$ in each of the three coordinate directions to a fixed vector $(a,b,c)$ of sum $m-j-2$. Its symmetry class is $(j,\mathrm{sort}(a,b,c))$.

For each source order $m$ and dilation $d$, the certificate assigns a nonnegative integer weight to each such class. Let $b_m$ be the archived rainbow cutoff for that order. A coloring with more than $b_m$ rainbows has weight at least $(b_m+1)\min w$. For every coloring at or below the cutoff, sum the weights of its actual rainbow Ls. The minimum of those finite scores and the preceding lower bound is a valid lower bound $s_{m,d}$ for every proper coloring. The exhaustive [boundary-deletion recurrence](LOCAL_RAINBOW_MINIMA.md) supplies the archived colorings through order 15. The [order-16 interior proof](LOCAL_RAINBOW_MINIMA.md#fifteen-rainbows-at-order-16-sixteen-at-order-17-and-seventeen-at-order-18) and the boundary checks supply the empty higher-order catalogs.

## Using the surrounding square

Assume that the whole $N$ by $N$ square is properly colored. The triangle supplies the upper bound on rainbows. Its surrounding square supplies additional lower bounds. A source triangle of order $m$ with translation $(a,b,c)$ and dilation $d$ has an axis-aligned bounding square of side $m-1$ in its own lattice. Its lower-left lattice point in host coordinates is $(1+a+b,b)$.

The [square extension checks](SQUARE_PATCHES.md) increase the guaranteed count on specific placements. Test every certified offset and its antidiagonal reflection. If an enclosing square of side $s$ and step $d$ fits inside the host and forces at least $r$ rainbows, omit catalog profiles containing fewer than $r$ rainbows. The new floor is the minimum over the remaining profiles and the unseen-coloring floor $\max(b_m+1,r)\min w$. The side-152 certificate uses the unit-spacing square checks and the even-dilation order-13 obstruction. For each rule the checker counts every eligible translation once, including when several enclosing squares fit. Placements outside the certified positions use the original floor. Summing these contributions gives $J$.

## Copies and the boundary of the host

The host is $T_N$ with $N=152$. At a dilation $d$ the translation triple $(\alpha,\beta,\gamma)$ has sum $Q=N-2-d(m-2)$. A rule may select only copies with $\ell\le\min(\alpha,\beta,\gamma)<u$. The number of such copies is $H_Q(\ell)-H_Q(u)$, where $H_Q(t)=\binom{Q-3t+2}{2}$ for $Q\ge3t$ and zero otherwise. Subtract $t$ from all three coordinates to obtain this formula. These counts give the base contribution to $J$ before the placement-specific increases.

Other rules select $\ell\le\max(\alpha,\beta,\gamma)<u$. For any threshold $t$, the indicator that all three coordinates are less than $t$ equals the product of the three factors $1-\mathbf 1_{\alpha_i\ge t}$. Expanding it gives eight signed restrictions on coordinatewise lower bounds. Subtract the expansion for $t=\ell$ from that for $t=u$. A term with lower bounds $(r,s,t)$ contributes $\binom{Q-r-s-t+2}{2}$ translations when $r+s+t\le Q$ and zero otherwise. Each selected copy contributes one regardless of its translation region. Summing over overlapping rules is legitimate because each rule contributes its own specified weights.

Fix a host L of step $h$ and base coordinates $(A,B,C)$, with $A+B+C=N-h-2$. A source L at $(a,b,c)$ of step $j$ maps to it exactly when $h=dj$ and
\[
 \ell\le\min(A-da,B-db,C-dc)<u.
\]
For a maximum-coordinate rule, require all three gaps nonnegative and apply the same band to their maximum. The translation is then unique. Add the applicable weights to get the incidence $I(e)$ of each host corner $e$. For an independent integer count, the code handles the lower threshold $t=\ell$ by adding its weight and handles $t=u$ by subtracting it. At fixed $h,A$ the admissible $B$ for threshold $t$ form the interval $[db+t,N-h-2-A-dc-t]$ when $A\ge da+t$. For a general signed term with shifts $(r,s,t)$, use the interval $[db+s,N-h-2-A-dc-t]$ when $A\ge da+r$. Integer interval additions followed by a scan cover every host position.

The manuscript's line identity bounds the host's total number of rainbows by $U_N=\binom N2-(N-1)+\lfloor(N-1)/3\rfloor$. The same bound applies separately inside every translated copy of $T_m$ in the host. The certificate assigns a nonnegative integer coefficient $c_H$ to selected such copies $H$. A sorted translation $(i,j,k)$ stands for each distinct permutation of those coordinates, with $m=N-i-j-k$. Its total contribution to the ceiling is $c_H U_m$ per copy. A host corner of step $h$ and base $(A,B,C)$ belongs to that copy exactly when $A\ge i$, $B\ge j$, and $C\ge k$ for the chosen ordering. These inequalities already imply $h\le m-2$.

Subtract the weights of all covering copies from each host incidence to form $I'(e)=I(e)-\sum_{H\ni e}c_H$. The maximum possible rainbow score is bounded by
\[
 V=\sum_H c_H U_{|H|} + \text{sum of the } U_N \text{ largest values of } \max(0,I'(e)),
\]
where $|H|$ denotes the triangle's order. Indeed the original score is the sum of the residuals on the rainbow set plus $\sum_H c_H r(H)$, where $r(H)$ counts the rainbows in $H$. Each local count satisfies its own line bound, and the whole set has at most $U_N$ elements. For side 152 the translated copies contribute 493,277,836,612,026 and the ranked residual contributes 11,297,007,130,543,636. Together they give $V=11,790,284,967,155,662$. The lower score is $J=11,828,798,917,652,112$, hence **$J-V=38,513,950,496,450>0$**. A proper square of side $N$ would force its triangular subregion to satisfy both counts. Their strict inequality proves the bound. [Three-color line identity and embedding argument](../../manuscript/main.tex)

## Reproduction

The first command checks the scores and the exact integer contradiction. The next two rebuild the small-square and triangle searches. The square checker uses python-sat and drat-trim. The triangle checker uses two C99 programs and Python's standard library.

~~~sh
python verify_triangle_grid.py
python verify_square_patches.py /path/to/drat-trim --cache /path/to/proofs
python verify_order16_interior.py /path/to/drat-trim
python verify_rainbow_boundary_layers.py /path/to/drat-trim
cc -O3 -std=c99 verify_rainbow_neighborhood.c -o rain_search
cc -O3 -std=c99 verify_triangle_stream.c -o triangle_stream
python verify_triangle_stream.py ./rain_search ./triangle_stream --jobs 4
~~~

For individual reconstruction of every weighted source catalog use **python verify_triangle_grid.py --rebuild ./rain_search ./triangle_extend --jobs 4 --rup-checker /path/to/drat-trim** after compiling **verify_triangle_extensions.c**. The [streaming proof](LOCAL_RAINBOW_MINIMA.md#the-order-13-minimizers-and-the-order-14-obstruction) reconstructs the largest three orders with less memory.
