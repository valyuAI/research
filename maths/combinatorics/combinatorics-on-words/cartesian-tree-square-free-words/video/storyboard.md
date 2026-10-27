# Storyboard: words that never repeat their shape

Running example: the binary rule `a -> 00101, b -> 00111, c -> 01100` applied to Dejean's word
`abcacbcabcbacbcacbabcabacabcac...`. Every number on screen is reproduced by `check_numbers.py`
or quoted from `../verification/` (`results_check_ct.json`, `results_ctproof.txt`).

Colour meaning: letters and digits in white; first half of a square blue, second half gold; yellow
for the thing currently being examined; red for squares, clashes and contradictions; green/teal for
success and matching letters; grey for "unknown" edge letters.

| Scene | Narration summary | Visual | What the viewer now understands |
|---|---|---|---|
| 1 Hook | banana contains "anan"; a square is a block followed by an exact copy; aa, abcabc; can an endless string avoid squares? | "banana" in big tiles, "an an" boxed red; two more examples; question | What a square in a word is |
| 2 TwoLetters | Try with a, b: a, ab, aba, then both fourth letters make a square | tiles added one by one; two branches end in red boxes | Two letters cannot avoid squares (longest is 3) |
| 3 Thue | Thue: three letters go forever; exponent of abcab is 5/3; Dejean: no block above 7/4; example bcacbca | 30-letter Dejean prefix; abcab with period bracket; 7/4 block boxed | Square-free ternary words exist; exponent; Dejean's word |
| 4 Shape | Numbers as columns; 31415 vs 20709 look alike; look-back rule; code 0 0 1 2 1 for both; name Cartesian tree | two column ranges; walking hops; code row filled in | What "same shape" means, via the code |
| 5 BinaryShape | 00, 01, 11 share code 0 1; 10 differs; 0110 -> 0 1 1 3; 0111 0011 is a shape square; ordinary squares are shape squares; only long ones are forbidden | binary words as low/high columns with codes | Shape squares; why a minimum half length is needed |
| 6 Table | The 2026 table; 29 and 9; question marks; two guesses fill the rest; result: all become infinity | 4 x 4 table; ? cells yellow, then ∞ in green | The open problem and what is new |
| 7 Rule | Replace letters of Dejean's word by 5-letter blocks; ternary rule with 6-letter blocks; short shape square 111 011 is allowed | letters drop into blocks; binary word grows; 111|011 boxed | The construction and the exact claim |
| 8 Window | 5-letter window is ambiguous (00111 vs 00001); 7-letter window: 23 codes, each with one middle letter | sliding yellow window; two windows side by side, middle letters compared | Shape of a 7-letter window determines its middle letter |
| 9 NearSquare | Suppose a long shape square with half length m; slide the window along both halves; halves are equal except 3 letters at each end | schematic cells; v moved under u; window slides; middle cells turn green, ends grey | Long shape square = ordinary square with fuzzy edges |
| 10 Upstairs | Blocks never straddle (00101 slid across 01100 00101); whole blocks align; read back as letters -> repetition in Dejean's word; exponent >= 2 - 14/m > 7/4 when m > 56 | sliding block with red crosses then green tick; block ticks; letters above blocks with arcs; inequality transforms; red "contradiction" | Why long shape squares are impossible |
| 11 Finite | Halves 4..56 fit in 24 base letters; 4,596 words checked, none; ternary 3,654 words, halves 3..64; two programs | bracket from 24 letters to binary strip; counter to 4,596 with green "0 found" | What the computer checked and why it is finite |
| 12 Status | Written argument + finite check = proof; computer assisted, not in Lean, not peer reviewed; modest; thresholds sharp by 29 and 9 | three-line status list with ticks and open circles; table cells 29 and 9 | How much to trust it and how big it is |
| 13 Ending | Recap in three points; open questions; end card | three short lines; two questions; end card | The whole story in their own words |

## First-time viewer review (GCSE level)

- "Square" is shown (banana) before it is named. "Exponent" is introduced with abcab before Dejean's
  7/4 is used, and 7/4 is said as "seven quarters" every time.
- "Shape" is introduced with ordinary numbers drawn as columns, where "taller" is visible, before
  binary digits; the rule is acted out column by column. The phrase "Cartesian tree" is only a name;
  nothing depends on knowing what the tree is.
- The table is introduced only after shape squares and the minimum half length are both explained.
- The decoding step shows a failure (5 letters) before the success (7 letters), so "7" is motivated.
- The long-square argument is schematic (a picture of 2 x 20 cells), and the narration does not claim
  the picture is to scale; the variable m is introduced by name in scene 9 before the inequality.
- The step "cutting the same piece from two blocks with equal codes gives equal codes" is stated,
  not proved (simplification of Lemma 3.3 of the paper).
- Fix applied: the 14 lost letters are explained as 3 + 3 + 4 + 4 on screen, so the inequality is not
  a jump.
