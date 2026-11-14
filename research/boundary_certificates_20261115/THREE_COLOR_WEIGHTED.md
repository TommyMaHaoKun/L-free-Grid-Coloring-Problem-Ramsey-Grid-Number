# A position-weighted proof that the three-color grid number is at most 188

Every three-coloring of the 188 by 188 square contains a monochromatic directed L. Combined with the published 20 by 20 construction, this gives $21\le R_3\le 188$. The proof uses finite triangle coloring counts and integer arithmetic. Its local catalogs cover $T_{11}$ through 5 rainbows (2,742 orbits), $T_{12}$ through 8 rainbows (1,838 orbits), $T_{13}$ through 10 rainbows (0 orbits), up to simultaneous renaming of colors and permutations of the three geometric coordinates.

## Local scores

Give each cell of $T_m$ its nonnegative coordinates $(x-y-1,y,m-x-1)$, of sum $m-2$. An L of leg $j$ has vertices obtained by adding $j$ in each of the three coordinate directions to a fixed vector $(a,b,c)$ of sum $m-j-2$. Its symmetry class is $(j,\mathrm{sort}(a,b,c))$.

For each source order $m$ and dilation $d$, the certificate assigns a nonnegative integer weight to each such class. Let $b_m$ be the archived rainbow cutoff for that order. A coloring with more than $b_m$ rainbows has weight at least $(b_m+1)\min w$. For every coloring at or below the cutoff, sum the weights of its actual rainbow Ls. The minimum of those finite scores and the preceding lower bound is a valid lower bound $s_{m,d}$ for every proper coloring. The exhaustive [boundary-deletion recurrence](LOCAL_RAINBOW_MINIMA.md) supplies every archived coloring, including the empty catalogs.

## Copies and the boundary of the host

The host is $T_N$ with $N=188$. At a dilation $d$ the translation triple $(\alpha,\beta,\gamma)$ has sum $Q=N-2-d(m-2)$. A rule may select only copies with $\ell\le\min(\alpha,\beta,\gamma)<u$. The number of such copies is $H_Q(\ell)-H_Q(u)$, where $H_Q(t)=\binom{Q-3t+2}{2}$ for $Q\ge3t$ and zero otherwise. Subtract $t$ from all three coordinates to obtain this formula. Summing the guaranteed local score times this copy count over the rules gives the lower bound $J$ for the total weighted rainbow count.

Other rules select $\ell\le\max(\alpha,\beta,\gamma)<u$. For any threshold $t$, the indicator that all three coordinates are less than $t$ equals the product of the three factors $1-\mathbf 1_{\alpha_i\ge t}$. Expanding it gives eight signed restrictions on coordinatewise lower bounds. Subtract the expansion for $t=\ell$ from that for $t=u$. A term with lower bounds $(r,s,t)$ contributes $\binom{Q-r-s-t+2}{2}$ translations when $r+s+t\le Q$ and zero otherwise. Each selected copy contributes one regardless of its translation region. Summing over overlapping rules is legitimate because each rule contributes its own specified weights.

Fix a host L of step $h$ and base coordinates $(A,B,C)$, with $A+B+C=N-h-2$. A source L at $(a,b,c)$ of step $j$ maps to it exactly when $h=dj$ and
\[
 \ell\le\min(A-da,B-db,C-dc)<u.
\]
For a maximum-coordinate rule, require all three gaps nonnegative and apply the same band to their maximum. The translation is then unique. Add the applicable weights to get the incidence $I(e)$ of each host corner $e$. For an independent integer count, the code handles the lower threshold $t=\ell$ by adding its weight and handles $t=u$ by subtracting it. At fixed $h,A$ the admissible $B$ for threshold $t$ form the interval $[db+t,N-h-2-A-dc-t]$ when $A\ge da+t$. For a general signed term with shifts $(r,s,t)$, use the interval $[db+s,N-h-2-A-dc-t]$ when $A\ge da+r$. Integer interval additions followed by a scan cover every host position.

The manuscript's line identity bounds the host's total number of rainbows by $U_N=\binom N2-(N-1)+\lfloor(N-1)/3\rfloor$. For this certificate $V$ is the sum of the $U_N$ largest values of $I(e)$. Every set of at most $U_N$ host rainbows has total incidence at most that sum. Therefore the weighted rainbow count is at most $V$. The certificate gives **$J-V=73,587,459,120,415>0$**. This contradiction rules out a proper $T_N$ and hence a proper square of side $N$. [Three-color line identity and embedding argument](../../manuscript/main.tex)

## Reproduction

The portable C and Python checkers use their standard libraries. The first Python command checks the catalog colorings, their weighted scores, and the exact host incidences. The final command also regenerates every low-rainbow catalog from the full search and compares its colorings individually.

~~~sh
cc -O3 -std=c99 verify_rainbow_neighborhood.c -o rain_search
cc -O3 -std=c99 verify_triangle_extensions.c -o triangle_extend
python verify_triangle_grid.py
python verify_triangle_grid.py --rebuild ./rain_search ./triangle_extend --jobs 4
~~~
