# Video brief: words that never repeat their shape

## The question in plain words

Write an endless string of letters, say from {a, b}. A *square* is two equal blocks side by side, like `abab` or `aabaab`. With two letters you cannot avoid squares for long. Now relax "equal": call two blocks the *same shape* if they rise and fall in the same way, in a precise sense described below. Can an endless binary string avoid two same-shaped blocks side by side, as long as each block has at least 4 letters? Can a three-letter string do it with blocks of at least 3 letters? A July 2026 paper by Shibata, Mieno, Köppl and Inenaga left exactly these two cases open and guessed "yes". We prove "yes" for both.

## Why anyone cares

Pattern matching on time series (stock prices, sensor data) often cares about shape, not exact values. "Cartesian-tree matching" is one standard notion of shape. Repetition-free words are the classic laboratory for understanding how much structure is forced in long sequences (Thue, 1906). This result completes a table of which kinds of repetitions can be avoided forever.

## The smallest concrete example

Shape code (parent distance): for each position, look left for the nearest letter that is not bigger, and write down how far back it is (0 if there is none).

- `banana` gets the code 0 0 1 2 1 2.
- Binary example with 0 < 1: `0110` gets 0 1 1 3: the last 0 looks back past `1` and `1` to the 0 three steps earlier.
- `00` and `01` and `11` all get the code 0 1, so they have the same shape.

So `0111` followed by `0011`? Codes: `0111` is 0 1 1 1, `0011` is 0 1 1 1. Same shape, so `01110011` is a shape-square with halves of length 4. Our binary word must never contain anything like that.

Known numbers (from the 2026 paper): with two letters and halves of length at least 3, the longest shape-square-free word has 29 letters. With halves of at least 4, the answer is "forever" (our result). With three letters and halves of at least 2 the limit is 9 letters; with halves at least 3 it is "forever" (our result).

## Prerequisite ideas, in order

1. Words, factors (contiguous blocks), squares.
2. Period and exponent: `abcab` has period 3 and length 5, exponent 5/3.
3. Dejean's theorem (1972): there is an endless word over {a, b, c} in which no block has exponent above 7/4. Show the Dejean substitution: a -> abcacbcabcbacbcacba, b -> bcabacabcacbacabacb, c -> cabcbabcabacbabcbac, and iterate it from `a`.
4. Substitution (morphism): replace every letter by a fixed block. Our binary rule: a -> 00101, b -> 00111, c -> 01100.
5. The shape code above.

## The key insight in five visual steps

1. **Start from a nearly repetition-free word** over {a, b, c} (Dejean). Animate its first 30 letters.
2. **Substitute blocks.** Each letter becomes a 5-letter binary block. Show the binary word growing: 00101 00111 01100 00101 ...
3. **Shape determines the middle letter.** Slide a window of 7 letters along the binary word; show that whenever two windows have the same shape code, their middle letters agree (there are only 23 possible codes; display a few). So if two long neighbouring blocks have the same shape, they are actually *letter-for-letter equal* except for 3 letters at each end.
4. **Equal long blocks force a repetition upstairs.** Because block boundaries can be recognised (the rule is "synchronizing"), a long equal stretch at distance m must line up with whole 5-letter blocks, so the original Dejean word would contain a block repeated with exponent close to 2, which is more than 7/4. Impossible. Draw the two copies with block boundaries aligned and the arrow back up to the Dejean word.
5. **Short cases by exhaustive check.** For halves of length 4 to 56, the computer checks every possible stretch: all 4,596 Dejean-type words of length 24. None contains a shape-square. Show a counter ticking to 4,596 with a green tick.

The ternary case is the same story with blocks 000101, 000221, 022211 and halves of length at least 3.

## What to put on screen

- The table from the 2026 paper with two question marks, which turn into infinity symbols at the end.
- The shape-code computation for `banana` and for `0110`.
- The two substitution rules.
- The inequality: exponent at least 2 - 14/m, which is greater than 7/4 once m > 56 (binary case); for the ternary case 2 - 16/m > 7/4 once m > 64.
- The numbers: 29 and 9 (finite limits), 4,596 and 3,654 (words checked), radius 3 windows of length 7.

## Proved versus computed versus open

- **Proved (with computer assistance):** both endless words exist; the explicit substitutions work for every Dejean-type starting word.
- **Computed:** the window-decoding property, the synchronization property and the absence of short shape-squares, each checked by two separate programs.
- **Not done:** no formal proof-assistant check; we do not know the smallest possible block length for other kinds of constructions; repetition thresholds for shapes (how close to a square one must get) remain open.

## Misconceptions to avoid

- "Same shape" is not "same letters": `00`, `01`, `11` all have the same shape.
- Avoiding shape-squares is harder than avoiding ordinary squares: every ordinary square is also a shape-square.
- The computer did not search forever. The infinite part is handled by the written argument in step 4; the computer only checks finitely many short cases.
- The thresholds 4 and 3 cannot be lowered: the paper's finite values 29 and 9 show that.
