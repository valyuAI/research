# Video brief: networks with four negative eigenvalues have at most 30 essential dots

Audience: a bright 16-year-old who has just finished GCSE maths or physics. Target length: 6 to 8 minutes.

## 1. The question in plain words

Draw a network of dots joined by lines (a graph). Write it as a table of 0s and 1s: put a 1 in row i, column j when dots i and j are joined. This table, the adjacency matrix, has special numbers called eigenvalues. For these tables they are always real, and they may be positive, zero or negative. They add up to zero.

Copying a dot, so that the copy is joined to exactly the same dots, changes nothing about the positive and negative counts. So call a network *reduced* if it has no copies and no lonely dots. Torgašev proved in 1985 that only finitely many reduced networks have exactly four negative eigenvalues.

Two questions follow: **how many dots can such a reduced network have, and how many positive eigenvalues?** We prove the answers are **30 dots** and **11 positive eigenvalues**. The value 30 settles a 2022 guess of Mohammadian (the bound 2⁵ − 2). The value 11 was implicitly known from a 2013 computer search; what is new for it is a proof that exactly two networks achieve it.

## 2. Why anyone cares

- Eigenvalues connect a graph to linear algebra. In this note their signs constrain the size and structure of the graph; no physical experiment or performance improvement is claimed.
- The balance between positive and negative eigenvalues (the inertia) controls things like how many dots can be chosen with no two joined: the independence number is at most n minus the number of positive eigenvalues, and also at most n minus the number of negative ones.
- The question has a history. Torgašev knew the answers 1, 3, 6 (positive eigenvalues) and 2, 6, 14 (dots) for one, two and three negative eigenvalues by 1989. Mohammadian guessed in 2022 that the dot counts follow 2, 6, 14, 30, ..., that is 2^(k+1) − 2. In 2025 others guessed that the positive counts follow the triangle numbers 1, 3, 6, 10; in 2026 a network with 11 refuted that. A 2013 paper on a related question had in fact already implied that 11 is the maximum, and the newer inertia identity makes that implication explicit. We confirm the dot bound 30 and show that only two networks achieve 11.

## 3. The smallest concrete examples (show these on screen)

| Network | Table (adjacency matrix) | Eigenvalues | Positive / negative |
|---|---|---|---|
| One edge (2 dots) | [[0,1],[1,0]] | +1, −1 | 1 / 1 |
| Triangle | all 1s off the diagonal | 2, −1, −1 | 1 / 2 |
| Pentagon (5-cycle) | each dot joined to its two neighbours | 2, 0.618, 0.618, −1.618, −1.618 | 3 / 2 |

The pentagon is the record holder for two negative eigenvalues: no network with two negative eigenvalues has more than three positive ones. Show 0.618 and −1.618 as (√5 − 1)/2 and −(√5 + 1)/2 (golden-ratio numbers).

Check by hand for the single edge: the vector (1,1) is sent to (1,1), stretched by +1. The vector (1,−1) is sent to (−1,1), flipped, so stretched by −1.

Table of records to animate as a growing bar chart:
- 1 negative → at most 1 positive
- 2 negative → at most 3 positive
- 3 negative → at most 6 positive
- 4 negative → at most **11** positive (implied by 2013 work; uniqueness of the two extremal networks is new)
- reduced networks: at most 2, 6, 14 dots for 1, 2, 3 negatives, and at most **30** for 4 (new)

## 4. Prerequisite ideas, in order

1. A graph as dots and lines; its 0/1 table (symmetric, zeros on the diagonal).
2. Matrix times vector (rows times column). An eigenvector is a direction the table only stretches, and the stretch factor is the eigenvalue. Use the single-edge example.
3. Symmetric tables have only real eigenvalues, and there are exactly as many as dots, counted with repeats. They sum to zero because the diagonal is all zeros.
4. Counting signs: the numbers of positive, zero and negative eigenvalues. This is the inertia.
5. Copying a dot, or adding a lonely dot, changes nothing in the positive and negative counts. So we only look at "reduced" networks, with no copies and no lonely dots.
6. Determinant zero or nonzero: "nonsingular" means no zero eigenvalue.

## 5. The key insight in six visual steps

1. **Shrink to the essential core.** Any network contains a core network, possibly the entire graph, with the same numbers of positive and negative eigenvalues and no zero eigenvalues. Animate dots fading out until only the core remains. So we only need to search cores.
2. **Cores grow one or two dots at a time.** Any core can be built from a smaller core by adding one dot, or sometimes two new dots, which need not be joined to each other. This is the key lemma, and it comes from Jacobi's rule about determinants of pieces of a matrix and of its inverse. Animate a growing tree of networks: level 2, level 3, level 4, and so on.
3. **A single sign test decides each new dot.** When a dot is added with a chosen set of connections, one number computed with whole-number arithmetic decides everything. If it is positive, we gain a negative eigenvalue. If it is negative, we gain a positive one. If it is zero, the result is not a core. Show the formula sign(det H) × sign(bᵀ·adj(H)·b), which is the sign of bᵀH^(-1)b with b as a column of 0s and 1s.
4. **Climb the levels until they run dry.** Keep only networks with at most four negative eigenvalues. Show the counts per level as a rising and falling bar chart: 1, 17, 295, 3648, 10384, 14422, 10810, 4473, 993, 110, 2, then 0 and 0. Two empty levels in a row mean nothing bigger can ever appear.
5. **The top of the mountain has exactly two networks**, each with 15 dots: 11 positive and 4 negative eigenvalues. Reveal both (section 6).
6. **Adding back zero eigenvalues.** Every reduced network is a core plus extra dots whose connection patterns are "invisible" (zero) in the core's geometry and compatible with each other. A clique search over these patterns shows that the biggest reduced network has 30 dots, and that exactly four networks reach 30. These four were already known (Akbari, Cameron and Khosrovshahi, 2004) as the largest reduced networks of "rank 8"; what is new is that no network with four negative eigenvalues and a different rank gets that far. All four are built from a single edge by three "doubling" steps. Doubling: copy every dot (the copy is joined to the same dots and to their copies), then add a new dot x joined to all the copies, and a dot y joined to x. That is the 1996 Kotlov–Lovász step (Construction A of Akbari, Cameron and Khosrovshahi). In their Construction B, y is also joined to all the original dots. Animate it: K₂ (2 dots), then 6, 14, 30. Using variant steps first and ordinary steps after gives the four 30-dot networks (VVV, VVO, VOO, OOO), with 225, 211, 187 and 155 lines.

## 6. Exact figures and objects to show

- **W₅ (Charles–Farber–Johnson–Kennedy-Shaffer 2013; Chen–Li 2026).** Five "point" dots joined to each other (a pentagram inside a pentagon, i.e. K₅). Ten "pair" dots, one for each pair of points, joined when their pairs share no point. These form the Petersen graph (outer pentagon plus inner star). Each pair dot is joined to its two points. 45 lines.
  Characteristic polynomial: (x − 1)⁵ (x² − 7x + 4) (x² + 3x − 1)⁴.
- **X (the second 2013 network, described via the affine plane).** A 3×3 grid of dots, joined when they share a row or a column (the rook's graph: a rook could move between them). Draw the two diagonal directions of a 3×3 tic-tac-toe board that wraps around. Each direction has 3 wrap-around diagonals, giving 6 new "line" dots. Each line dot is joined to the 3 grid dots on its diagonal. Line dots of the same direction are joined to each other, giving two triangles. 42 lines, 72 symmetries.
  Characteristic polynomial: (x − 2)(x − 1)⁴ (x² − 6x + 2) (x² + 3x − 1)⁴.
- Both have the same four negative eigenvalues: −(3 + √13)/2 ≈ −3.30, repeated four times.
- The census bar chart from section 5, and the record table from section 3.

## 7. What is proved, what is computed, what is open

- **Proved by hand (in the paper):** shrinking to a core keeps the counts; cores grow by one or two dots; the termination rule.
- **Computed exactly, and checked twice by independent programs:** the full list of 45,242 core networks with at most four negative eigenvalues. Every sign is decided with whole numbers, never with rounded decimals. A third, brute-force check covers every network with at most 10 dots. The same programs reproduce the old answers 1, 3, 6 and Torgašev's list of 32 maximal networks for three negatives.
- **Also computed (the headline new result):** a reduced network with four negative eigenvalues has at most 30 dots, confirming Mohammadian's 2022 guess 2⁵ − 2 for k = 4. Exactly four reduced networks have 30 dots (the four known since 2004 as the largest of rank 8).
- **Credit:** the bound 11 follows from a 2013 computer proof that every network with 16 or more dots has at least five nonpositive eigenvalues. Our computation re-proves that independently.
- **Open:** five negative eigenvalues. The answer is at least 16, and the search would be hundreds of times larger. It is also known (2026) that the answers eventually grow faster than any square law.

## 8. Misconceptions to avoid

- "More dots means more positive eigenvalues." Copying dots adds only zero eigenvalues, which is why we only count reduced networks.
- "The pattern 1, 3, 6, 10 (triangle numbers) continues." It does not: four negatives allow 11, not 10.
- "The computer tried random networks." It did not. It built every possible core network level by level, and a proved lemma guarantees nothing was missed.
- "Eigenvalues were computed with decimals, so rounding could fool us." The theorem-producing sign decisions use exact integer or rational arithmetic. The separate brute-force cross-check uses a numerical filter with exact fallback; it is supporting evidence, not the sole proof.
- Do not say "the computer proved it alone". The proof combines two short lemmas with an exhaustive exact computation, and both parts are needed.

## Final scope lock

Research package complete at n(4)=30 plus the uniqueness of the two reduced inertia-(11,0,4) graphs. The 45,242-graph census has been freshly checked for exact inertia and distinctness, and its hash and counts match both completed enumerations. Per-rank maxima are 5,10,18,30,26,22,20,17,15,15,15 for ranks 5..15. The recovered full k<=4 doubling check finishes ALL OK. Credit ACK 2004 for the rank-8 four classes, both constructions and the compatibility-clique method; credit CFJK 2013 for W5/X and the bound underlying A4=11. Novel scope is the remaining ranks 9..15 and uniqueness, subject to bounded priority searches. Nothing is proved for k>=5; six negative one-vertex-extension searches and unsuccessful beam searches are not an exhaustive theorem. No video folders were edited in this research pass.
