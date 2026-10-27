# Video brief: "Nine multiplications, and not one fewer"

Audience: a bright 16-year-old who has just finished GCSE maths. Target length 6-8 minutes.

## 1. The question in plain words

When a computer multiplies two numbers built from several pieces, the expensive step is multiplying pieces together; adding them is cheap. So we ask: what is the smallest number of piece-by-piece multiplications that always gets the right answer?

Our number system is tiny. Its "numbers" are expressions a0 + a1 x + a2 x^2 + a3 x^3 where every coefficient is 0 or 1, we add with 1 + 1 = 0 (arithmetic mod 2, like XOR), and whenever x^4 appears we replace it by x^2 + 1. We prove that multiplying two such numbers needs exactly 9 multiplications of coefficients: 9 suffice and 8 never do. If instead coefficients live in arithmetic mod 3 (with the rule (x^2+1)^2 = 0), 8 suffice. A consequence: "length-6 cyclic convolution" of bit strings, a standard signal-processing operation, needs exactly 12 multiplications.

## 2. Why anyone cares

- Fast multiplication in finite number systems sits inside cryptography, error-correcting codes and computer algebra. Counting multiplications is the classic way to measure its cost.
- A 2012 paper by Hugues Randriambololona built fast multiplication from small pieces like ours and asked whether 9 was the true cost for coefficients mod 2 or mod 3. Rambaud later proved the binary value 9 when both inputs use the same linear combinations. The present binary search also allows different combinations for the two inputs; it still needs 9. Over mod 3, eight suffice.
- A 2026 table by Chengu Wang listed length-6 cyclic convolution mod 2 as "11 or 12". We show it is 12.

## 3. Smallest concrete example: Karatsuba

Multiply (a0 + a1 x)(b0 + b1 x) = a0 b0 + (a0 b1 + a1 b0) x + a1 b1 x^2.
The obvious way uses 4 multiplications. Karatsuba's trick uses 3:
- P1 = a0 b0, P2 = a1 b1, P3 = (a0 + a1)(b0 + b1);
- middle coefficient = P3 - P1 - P2.
Animate with numbers: a = 2 + 3x, b = 4 + 5x. P1 = 8, P2 = 15, P3 = 5 x 9 = 45, middle = 45 - 8 - 15 = 22. Check: (2+3x)(4+5x) = 8 + 22x + 15x^2.

Then show our number system: each number has 4 coefficients, the schoolbook method uses 4 x 4 = 16 multiplications, and a clever Karatsuba-style method uses 9.

## 4. Prerequisites to build, in order

1. Arithmetic mod 2: 1 + 1 = 0. Adding is XOR.
2. Polynomials and "reducing" with a rule: here x^4 = x^2 + 1, so x^5 = x^3 + x and x^6 = 1.
3. An "algorithm with r multiplications": each multiplication is (some sum of a's) times (some sum of b's), and every coefficient of the answer is a sum of these r products.
4. A 4 x 4 grid of 0s and 1s, and the special "rank-one" grids: the outer product of a column of 0/1 and a row of 0/1 (pick some rows and some columns; the grid is 1 exactly where a picked row meets a picked column). There are 15 x 15 = 225 of them.
5. Combining grids by adding mod 2 (XOR), and the "span" of a set of grids: all grids you can make by XOR-ing some of them.

## 5. Key insight in visual steps

1. **The multiplication table as four grids.** For each output coefficient x^k, draw the 4 x 4 grid whose (i, j) entry says whether x^i times x^j contributes to x^k. With the rule x^4 = x^2 + 1 they are:
   - x^0: rows 1000 / 0001 / 0010 / 0101
   - x^1: rows 0100 / 1000 / 0001 / 0010
   - x^2: rows 0010 / 0101 / 1010 / 0100
   - x^3: rows 0001 / 0010 / 0101 / 1010
2. **One multiplication = one rank-one grid.** The product (a0 + a2)(b1 + b3) is the grid with 1s where rows {0, 2} meet columns {1, 3}. An algorithm with r products works exactly when every one of the four target grids is an XOR of some of the r rank-one grids. (Show Karatsuba this way first, on 2 x 2 grids.)
3. **Rooms instead of lists.** Instead of choosing 8 grids, picture the "room" they span. An 8-product algorithm exists exactly when there is an 8-dimensional room that contains the four target grids and is built from rank-one grids. Since the four targets already fill 4 dimensions, only 4 extra rank-one grids have to be chosen: about 100 million choices.
4. **Symmetry shrinks the search.** Multiplying both inputs by fixed invertible numbers of the system shuffles the rank-one grids but keeps the targets inside their room. Every rank-one grid can be moved to one of just 3 standard ones, so the first choice is fixed. Sorting the last choice into "buckets" leaves 74,377 cases.
5. **Every case fails.** In no case is the room built from rank-one grids. So 8 is impossible and 9 is the answer. Five separate programs, written different ways, agree; they also correctly find 8 for a similar system where 8 is known to work, and correctly fail for one where 9 is known to be needed.
6. **Mod 3 is different.** The same search over arithmetic mod 3 finds an 8-product algorithm almost immediately. Show its eight products as a table (paper, Table 1), each of the form (combination of f's) times (the same combination of g's).
7. **The convolution corollary.** Length-6 cyclic convolution mod 2 splits into two independent pieces: one 2-coefficient piece costing 3 and our 4-coefficient piece costing 9. A 1986 theorem of Ja'Ja' and Takche says costs simply add when one piece is this small, so the total is 3 + 9 = 12.

## 6. Objects to show on screen

- The Karatsuba example with numbers above.
- The four 4 x 4 target grids (step 1), colour-coded by output coefficient.
- One rank-one grid lighting up as rows x columns.
- A "room" picture: four target grids inside a box, four extra rank-one grids added to complete the box.
- A counter: 103,406,616 raw choices -> 3 starting choices -> 74,377 cases -> 0 successes.
- The final table: q = 2: 9; q = 3: 8; q = 4: 8; q = 5: 8; q >= 7: 7.
- The equation x^6 - 1 = (x + 1)^2 (x^2 + x + 1)^2 (mod 2) and "3 + 9 = 12".

## 7. Proved, computed, open

- Proved by hand: the 9-product algorithm (any field), the 8-product constructions for fields with at least 4 elements, the reduction of the question to "rooms", and the symmetry reduction.
- Proved by exhaustive computation (computer-assisted proof): no 8-product algorithm exists mod 2. Checked by several independent programs; not formalized in a proof assistant.
- Checked directly: the 8-product algorithm mod 3 (16 identities).
- Proved by exact computation: the lower bound 8 for fields of size 3, 4 and 5. The two prime-field cases also have a second checker in a different basis. The q=5 run has 73,000 prefixes and 17,417,506 candidate buckets, with zero successes. Do not explain this as a consequence of an unchecked Blaser field-size claim.
- Taken from the literature: the Ja'Ja'-Takche theorem, the general lower bound of seven, the symmetric binary value, and the established subspace-search method. The q=4 value was already claimed in the survey. Broader originality remains moderately confident, not certain.
- Still open: the same questions for bigger systems, such as 6-coefficient versions (for example multiplying modulo x^6 mod 2 needs 13 or 14, and nobody knows which).

## 8. Misconceptions to avoid

- This is not about multiplying ordinary integers faster; it is about a specific small number system and counting coefficient multiplications, with additions free.
- "No algorithm found" is not the argument: the search is exhaustive, and its completeness is proved, so it rules out every possible 8-product algorithm, not just the ones we thought of.
- The answer depends on the coefficient arithmetic: 9 for mod 2, 8 for mod 3. Smaller fields have fewer "evaluation points", which is why they cost more.
- Costs of independent pieces do not always add (the general "direct sum conjecture" is false), so the convolution result needs the special theorem for small pieces.
