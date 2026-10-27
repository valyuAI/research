# Video brief: why no covering system with these moduli can ever close

Audience: a bright 16-year-old who has just finished GCSE maths. Target length: 6-8 minutes.

## 1. The question in plain words

A *covering system* is a list of rules like "n leaves remainder 1 when divided by 6" such that **every** whole number obeys at least one rule. Each divisor (the *modulus*) may be used only once.

The question: can you build such a list where every modulus is at least 6 and is a divisor of 2^a × 45, for some power of two 2^a? For example, the allowed moduli for a = 3 are 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 60, 72, 90, 120, 180 and 360. Four mathematicians asked this in May 2026 (arXiv:2605.18644, Problem 2) and guessed "no". We prove "no" for **every** a, however large.

## 2. Why anyone cares

Covering systems go back to Erdős (1950), who used them to show that some odd numbers are never a power of two plus a prime. The famous question was whether the smallest modulus can be as large as you like. Hough proved in 2015 that it cannot, and the best known bound is 616000. Mapping exactly which small cases are possible is still active work. This closes the remaining case in the source paper's classification for smallest modulus 6 with LCM 2^a 3^b 5^c under its ordering a >= b >= c >= 1. There is a twist: an **infinite** list with these moduli does exist. So the obstruction must use the fact that the list is finite.

## 3. Smallest concrete example (warm-up)

Show the classic covering with moduli 2, 3, 4, 6, 12:

* n ≡ 0 (mod 2), n ≡ 0 (mod 3), n ≡ 1 (mod 4), n ≡ 5 (mod 6), n ≡ 7 (mod 12).

Animate the numbers 0-11 on a clock face. Colour each number by the first rule that hits it: 0, 2, 4, 6, 8, 10 (mod 2); 3, 9 (mod 3); 1, 5 (mod 4); 11 (mod 6); 7 (mod 12). Every number gets a colour, so the whole clock is covered, and because 12 is a multiple of every modulus the pattern repeats forever.

## 4. Prerequisites to build, in order

1. Remainders and "clock arithmetic" mod n.
2. Two remainders at once: knowing n mod 4 and n mod 45 tells you n mod 180 (Chinese remainder theorem; show the 4 × 45 grid).
3. The binary tree of remainders mod 2, 4, 8, 16, ...: each class mod 2^k splits into two classes mod 2^(k+1).
4. A 9 × 5 board for n mod 45 (column u = n mod 9, row v = n mod 5). The six divisors of 45 give six piece shapes:
   * mod 1: the whole board (45 cells);
   * mod 3: a "block" of 3 columns, all rows (15 cells);
   * mod 5: one full row (9 cells);
   * mod 9: one column (5 cells);
   * mod 15: a block within one row (3 cells);
   * mod 45: one cell.

## 5. The key insight in 5 visual steps

1. **Columns.** Lay out numbers mod 2^k × 45 as 2^k boards side by side, one per branch of the binary tree. A rule with modulus 2^i × d stamps one piece of shape d onto every board below one branch at depth i. After placing rules, each board has some uncovered cells: that is its *column*.
2. **Doubling.** Going one level deeper, every board is copied into two boards. The new rules at that depth are one piece of each shape, at most six pieces in all, because each modulus may be used only once. The uncovered area doubles, but only six new pieces arrive.
3. **Price tags.** Put a price on each shape, for example whole board 14, block 7, row 4, column 2, short row 2, single cell 1. The total for one of each is R = 30. For each board, compute the cheapest way to cover its uncovered cells with pieces (repeats allowed); call this its *cost*. Let Q be the sum of the costs of all boards.
4. **The inequality Q' ≥ 2Q - 30.** Copying doubles Q. Each new piece can lower the cost of the one board it lands on by at most its own price, so all the new pieces together lower Q by at most 30. On screen: Q = 30 → next level ≥ 2 × 30 - 30 = 30 → next ≥ 30 → ... The cost never reaches 0. A finished covering needs Q = 0, so once Q ≥ 30, the list can never be finished, however many levels you add.
5. **The computer's job.** Check every possible way of choosing the rules with moduli 6, 9, 10, 12, 15, 18, 20, 30, 36, 45, 60, 90, 180 (depth 2, so 4 boards). In every case, at least one of 11 price lists already gives Q ≥ R. The search cuts off a branch as soon as even the best possible remaining pieces could not bring Q below R. About half a million branches are checked in about a minute.

## 6. Exact objects for the screen

* The 9 × 5 board with the six piece shapes, each labelled with its modulus (1, 3, 5, 9, 15, 45) and its moduli in the problem (for example shape 15 ↔ moduli 15, 30, 60).
* The tree: root (mod 45 only) → 2 boards (mod 90) → 4 boards (mod 180).
* The inequality **Q' ≥ 2Q - R**, with R = 30 for the price list (14, 7, 4, 2, 2, 1).
* The 11 price lists (table in the paper). The first counts uncovered boards. The second counts uncovered cells weighted by 45/d: whole board 45, block 15, row 9, column 5, short row 3, cell 1.
* A real example at depth 2 that survives the first ten price lists but not the eleventh. Its four boards have 0, 17, 18 and 24 uncovered cells (59 in total). Draw rows v = 0..4 top to bottom and columns u = 0..8 left to right, with # for uncovered:

  ```text
  board 1 (0)          board 2 (17)         board 3 (18)         board 4 (24)
  . . . . . . . . .    . . # . . # . . #    . # # . # # . # #    . # # . # # . # #
  . . . . . . . . .    . . # . . # . . #    . # # . # # . # #    . # # . # # . # #
  . . . . . . . . .    . . . # . # . . #    . . . . . . . . .    . . . . . . . . .
  . . . . . . . . .    . . # # . # . . #    . # # . # # . # #    . # # . # # . # #
  . . . . . . . . .    . . # # . # . . #    . . . . . . . . .    . # # . # # . # #
  ```

  With prices (whole 14, block 7, row 4, column 2, short row 2, cell 1) the cheapest covers cost 0; 8 (four columns u = 2, 3, 5, 8); 12 (three rows); and 12 (six columns). The total is Q = 32, which is at least R = 30, so this branch is dead forever. Under the price list (5, 2, 2, 2, 1, 1) the same boards cost 0 + 4 + 4 + 4 = 12 < 13, so the choice of prices matters.
* A counter: "498,464 search branches, 0 survivors".

## 7. What is proved, what is computed, what is open

* **Proved by hand:** the doubling inequality and the fact that Q ≥ R means no finite covering can follow.
* **Computed (exactly, with integers, three independent programs):** every choice of the 13 small moduli gives Q ≥ R for one of the 11 price lists.
* **Together:** no covering exists for any a. This is a complete proof, but the computer part has not been formalised in a proof assistant.
* **Still open:** the paper's Problem 1 (smallest modulus 9 with moduli built from 2, 3 and 5, including infinite lists) and Problem 3 (smallest modulus 8).

## 8. Misconceptions to avoid

* "Covering just means the fractions 1/m add up to at least 1." No. Here the fractions add up to more than 1 (about 1.18), and coverings still do not exist. The obstruction is about how the pieces fit, not about total area.
* "Infinite coverings exist, so finite ones must too." No. An infinite list can shrink the uncovered set forever without ever emptying it, like 1/2 + 1/4 + 1/8 + ... never reaching 1 at any finite step. The proof is consistent with this: along the infinite covering, Q stays at least R too.
* "The computer checked a few values of a." No. The computer looks only at depth 2. The inequality then carries the conclusion to every depth.
* "One price list works for everything." Not as far as we know. A choice that is dead under one list can survive another, and the supplied family has 11 lists, of which the first is inert at this depth. The eleventh list closes the branches left by the first ten.

## Narration and accessibility handoff

Build each unfamiliar term from the concrete example before showing the formula. Read the key inequality or count aloud and leave it on screen long enough to follow. Use captions matching the spoken narration, and use labels/patterns as well as colour. Keep the proved/computed/open distinction visible in the final scene. Credit the named prior work where its result first appears. Root produces the narrated MP4 and editable video source; this brief does not claim that a video has been produced.
