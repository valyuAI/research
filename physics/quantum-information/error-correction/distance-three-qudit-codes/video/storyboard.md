# Storyboard: how many qudits can one-error codes protect?

Audience: a bright 16-year-old after GCSE maths and physics. Running example: qutrits (q = 3)
with five questions (r = 5), where counting allows 30, the tables knew 28, and 29 was open.
Every number is recomputed by `data_prep.py` from `../verification/` and written to `data.json`.

Colour meaning (whole video): blue = codewords, qudits and their lines; yellow = the thing
currently changing; red = errors, collisions and contradictions; teal/green = success;
gold = holes; grey = all clear / background points.

| # | Scene | Narration summary | Visual | Viewer now understands |
|---|---|---|---|---|
| 1 | Hook | Send "1" over a noisy radio; static flips it. Say it three times, take a majority. What is the least redundancy that repairs one error? | Sender and receiver dots joined by a jagged static line; a 1 travels, turns red 0. Then 1 1 1 travels, middle flips, majority box gives green 1. "3 symbols for 1" | Errors flip symbols; repetition repairs them at a cost |
| 2 | Cube | Eight 3-bit messages on a cube; one flip = one edge. 000 and 111 are three edges apart: distance 3. Bubbles around them do not overlap | Cube with bit-string corners, yellow path 000-100-110-111, blue and teal bubbles | Distance 3 = non-overlapping one-error bubbles = one error repairable |
| 3 | Questions | Ask "do bits 1, 2 agree?" and "do bits 2, 3 agree?". Fingerprint table. Answers do not reveal the message | Three bit boxes with two arcs; table of error -> answers built row by row | Parity questions locate errors without reading data |
| 4 | Efficiency | r questions -> 2^r lists, one for all clear. 3 questions -> 7 positions: Hamming code. Fingerprints as points, all different | Eight 3-bit columns, one grey; 1 + n <= 2^r -> n <= 7; columns collapse to seven distinct dots | Counting bound; classical codes = distinct points |
| 5 | Quantum | Looking destroys quantum data; agreement questions do not. Two kinds of damage: shift and twist | A dial; "look" scrambles it red. Two dials with an "agree?" arc stay intact. Shift rotates needle, twist rotates an outer phase ring | Why quantum codes only use parity-like questions, and need to catch two kinds of error |
| 6 | Dials | Qutrit dial 0, 1, 2; clock arithmetic 2 + 2 = 1, 2 x 2 = 1. 3 x 3 grid of shift/twist amounts, 8 errors | Dial needle moves 2 then 2 more; grid with one grey cell and eight red | Qudits, clock arithmetic, 8 errors per qutrit |
| 7 | Sheets | Five questions. Real fingerprints of qutrit 14 of the [[28,23,3]]_3 code: shift (0,2,1,2,1), twist (1,0,1,1,1). Nine combinations form a sheet. Sheets may share only 00000 | Two columns, then a 3 x 3 grid of the nine real lists on a parallelogram "sheet" | Each qutrit owns a sheet of answers; repair = sheets overlap only at zero |
| 8 | Counting | 1 + 8n <= 243 -> n <= 30. Tables: 28 known, 29 unknown. Guess | Equation transforms; number line 26-31 with 28 green, 29 and 30 as "?" | The open question, concretely |
| 9 | Lines | Glue each list to its double -> 121 points; a sheet -> 4 points = a line; rule: lines never meet = skew | Real list and its double merge to one dot; the four real points of qutrit 14 as a bar in a 121-dot field; more bars appear, a collision flashes red | Code = set of skew lines |
| 10 | Bridge (3D) | Road under a bridge: skew lines in ordinary space | Two rods in 3D, slow camera turn | Skew lines need room |
| 11 | Fano | Smallest finite plane: 7 points, 7 lines, any two meet. Four questions: 40 points, 10 skew lines tile them | Fano plane with pairs of lines highlighted at their shared point; then 40 dots tiled by 10 coloured bars | Planes have no skew lines; with more room, lines can tile exactly |
| 12 | Holes | 29 lines -> 116 covered, 5 holes. Slice: 40 points; a line lies inside or crosses once; holes = 40 - 29 - 3x in {11, 8, 5, 2} >= 2. 121 x 2 = 242 > 5 x 40 = 200. Contradiction. Credit Beutelspacher 1975 | 121-dot field, 29 blue bars, 5 gold holes; a slice outline; equation with 11, 8, 5, 2; tally bars 242 vs 200 in red | Why 29 is impossible: the key proof step |
| 13 | Cheaters | Impure codes: two errors with same answers whose difference is harmless. One cheat -> at most 2 + 10 = 12 | Two error arrows to one answer, then squeeze into a smaller box, "2 + 10 = 12 < 28" | The bound covers all codes |
| 14 | Build | Slopes y = a x meet only at 0. L_a = {(x, y, a(x + y omega))}, 27 slopes from a 27-element number system; leftover plane holds one more line: 28 | Axes with slope lines through a hollow origin; formula; 27 teal bars + 1 yellow bar, 9 grey holes | The extremal code is explicit |
| 15 | Balance | Quantum compatibility: ten-number signatures must sum to 0; weights double signatures. Running total: 27 lines -> 0; extra line leaves a 1; three weights 2 leave a 2; 2 + 1 = 0 | Ten clock-digit boxes updated with the real running totals from data.json; slot 8 turns red, then green | The quantum condition is met; 28 is reached |
| 16 | Answer | Theorem for q >= 3 prime power: exists iff r >= 4 and n <= max skew lines. Even r: counting limit; odd r: q - 1 lower; r = 5: q^3 + 1 = 28, 65, 126 | Theorem card; bars "counting" vs "true" for q = 3, 4, 5 | The general result |
| 17 | Table | New [[59,54,3]]_4, [[61,56,3]]_4, [[62,57,3]]_4, [[65,60,3]]_4; no [[29,24,3]]_3 or [[66,61,3]]_4. 12 improve, 11 exact; Thas 1971 | Table: code, table said, now | Concrete impact |
| 18 | Status | Written proofs; 255 certificates pass an independent checker, 7 broken inputs rejected; CP-SAT could not close 28 vs 30; not Lean, not peer reviewed; stabilizer codes; Thas cited | Three cards: proved / computer-checked / not yet | What is proved vs checked vs assumed |
| 19 | Recap | Three points; open: distance 4, odd r, q = 3, r = 7: 16 known vs 29 bound. End card | Three numbered lines; number line 16 ... 29 gap; end card | Recap and what is still unknown |

## First-time-viewer review (fixes made)

- "Distance" is shown on the cube before it is named; "bubble" replaces "sphere".
- "Point" is introduced for classical fingerprints (scene 4) before it is reused for glued answer lists (scene 9), so "line" arrives with a picture.
- Qudits are introduced only after the "no looking" problem, so the viewer knows why questions matter.
- "Weight" is defined by its effect (relabelling twists doubles the signature) before it is used.
- The 27-element number system is named, not explained; the slope analogy carries the idea.
- Impure codes are compressed to one clip: the reduction is stated with its real number (12), not proved.
- Thas's 1971 theorem is mentioned only for what it supports (some table rows), not explained.
