# Video brief: how long can a one-error-correcting quantum code be?

## The question in plain words

A quantum computer stores information in fragile units. Here they are "qudits", which take q basic values (q = 3 is a "qutrit"). A quantum error-correcting code spreads k qudits of information across n physical qudits. It adds r = n − k qudits of redundancy, so that any single damaged qudit can be found and repaired. Such a code has "distance three".

The question: **with a fixed redundancy r, how many physical qudits n can such a code protect?** More qudits for the same overhead is better. We answer it exactly, for every qudit dimension q ≥ 3 and every redundancy.

## Why anyone cares

- Single-error correction is the first useful level of protection. Its codes are the building blocks of larger schemes.
- Researchers keep public tables of the best known codes (codetables.de). Our result fills in entries that were marked "unknown", and shows that some entries can never be improved.
- For ordinary qubits (q = 2) the answer was found in 2013. For qutrits and beyond, the odd-redundancy case was open.

## The smallest concrete example

Qutrits (q = 3), redundancy r = 5:

- The old "sphere-packing" count says n ≤ 30. There are 3^5 = 243 syndrome patterns. Each qudit has 8 possible single errors, so 1 + 8n ≤ 243.
- The tables listed codes up to n = 28. For n = 29 they said "maybe".
- **Answer: 28 is the maximum.** No code with 29 qutrits exists, and a 28-qutrit code exists.
- In general, for r = 5 the maximum is q^3 + 1: 28 for qutrits, 65 for ququarts (q = 4), 126 for q = 5.

## Prerequisite ideas, in order

1. **Arithmetic mod 3** (and finite fields in general): numbers 0, 1, 2 with wrap-around addition and multiplication.
2. **Vectors and planes through the origin.** In a 5-dimensional space over this arithmetic, a "line" in projective language is a 2-dimensional subspace, a flat sheet through the origin.
3. **Errors as vectors.** Each possible error on qudit i produces a "syndrome", a vector of 5 numbers. All the syndromes of qudit i fill out one 2-dimensional subspace W_i.
4. **Correcting one error means no confusion.** Two different single errors must never produce the same syndrome. That means the sheets W_i of different qudits share only the origin: they are **skew**.
5. **A partial spread** is a family of pairwise skew lines. So a distance-three code (of the "pure" kind) is a partial spread, plus one extra algebraic condition.

## Key insight in visual steps

1. **Draw the sheets.** Show the 5-dimensional space as a stylized cloud of 121 points; each "line" is a set of 4 points. Each qudit is one line; lines must not touch.
2. **Count the holes.** If you try to fit 29 skew lines, they cover 29 × 4 = 116 points, leaving 5 uncovered "holes". Every hyperplane (a 4-dimensional slice, 40 points) must contain at least 2 holes; this is a divisibility argument mod 3. But 5 holes cannot be spread so that all 121 slices get 2 each: each hole lies in only 40 slices, and 5 × 40 = 200 < 121 × 2 = 242. Contradiction. So at most 28 lines fit.
3. **What about cheating codes?** "Impure" codes allow some low-weight errors to act harmlessly. Animate: each such harmless error forces many lines into a smaller slice of space, where even fewer lines fit. So cheating never helps.
4. **Build the champion.** Arrange 27 lines L_a, one for each element a of the 27-element field GF(27): L_a = {(x, y, a·(x + y·ω))}. They never touch. Add one more line inside the "leftover" plane: 28 lines.
5. **The balancing act.** The quantum condition says that weighted "area vectors" (Plücker vectors) of the lines must add to zero. For the 27 lines with weight 1 they already cancel. Change three weights to 2, −1, 2 and the leftover line is exactly absorbed. Show the vectors as arrows summing to zero, then the three re-weighted arrows making room for the 28th.
6. **Every length in between.** Smaller codes come from balanced groups of lines: whole rows, pairs of rows, small "4-point" groups. These are stacked like building blocks, layer by layer.

## On-screen figures and formulas

- μ_q(r) = (q^r − 1)/(q^2 − 1) for even r, and (q^r − q^3)/(q^2 − 1) + 1 for odd r.
- Table: q = 3, r = 5: max 28 (Hamming bound 30); q = 4, r = 5: max 65 (Hamming bound 68).
- The hole count: 121 points, 29 lines × 4 = 116 covered, 5 holes. Each slice needs ≥ 2 holes: 5 × 40 = 200 < 242.
- The line formula L_a = {(x, y, a(x + yω))}.
- New table entries: [[65,60,3]]_4 exists; [[29,24,3]]_3 and [[66,61,3]]_4 do not.

## Proved vs computed vs open

- **Proved by hand:** the upper bound for every q and r, including impure codes; the constructions for q ≥ 7.
- **Checked by computer:** the starting cases for q = 3, 4, 5 (245 explicit configurations) and all the new table codes. These are verified by an independent program in exact arithmetic.
- **Cited:** a classical 1971 bound by Thas for the distance-four corollaries.
- **Open:** the same question for distance four with odd redundancy. For qutrits with r = 7 we know codes with 16 qudits and a bound of 29.

## Misconceptions to avoid

- This is not about qubits: for qubits the answer is different, one less, with some gaps.
- "Code length" means the number of physical qudits, not the number of errors corrected.
- The result is about stabilizer codes; exotic non-stabilizer codes are not covered.
- The sphere-packing (Hamming) bound is not the answer for odd redundancy; geometry gives a sharper limit.
