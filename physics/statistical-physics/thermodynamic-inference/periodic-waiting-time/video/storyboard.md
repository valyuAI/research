# Storyboard: a machine that wastes nothing, but looks like it does

Running example throughout: the paper's three-state network. Square 1 to square 2 is
door a (blue), rate `a(t) = 1 + epsilon cos t`; square 2 to square 3 is door b (gold), rate
`b(t) = 1 + epsilon sin t`; square 1 to square 3 is the hidden line (grey, dashed once
hidden), rate 1. Pictures use `epsilon = 1/2`, the value in the paper's figure.

Colour meaning (from `vrvideo.style`): blue = door a and everything that starts through it
(curve f); gold = door b (curve g); grey = hidden line, muted notes; white = the counter;
yellow = the thing currently changing or being pointed at; red = the false positive and the
failed conjecture; green = zero waste; teal = the result that still stands.

| Scene | Narration summary | Visual | What the viewer now understands |
| --- | --- | --- | --- |
| 1 ArrowOfTime | A bouncing ball loses height (energy becomes heat). Backwards it gains height, which looks wrong: the arrow of time. Physicists measure waste by how wrong the backwards film looks. For tiny machines you only see jumps and waits. A paper proposed a waiting-time test for machines on a repeating schedule and conjectured it never overstates waste. We build a machine with zero waste where the test says otherwise. Pause. | Ball bouncing left to right with heat flickers at each impact; same motion reversed under a red "backwards" icon. Two short lines linking "how wrong backwards looks" to "energy wasted". A tape of jump ticks with a brace labelled "wait". "test $\le$ true waste" labelled conjecture, then "true waste = 0" (green) against "test says > 0" (red) and a yellow question mark. | The question: can waiting times measure waste? What a conjecture is. What the video will show. |
| 2 BoardGame | Three squares in a triangle, a counter. Tiny ticks; a die for every exit line; "go" means hop. A rate is average hops per unit time; bigger rate = wider door = more "go" faces. All rates one: the counter wanders. Long-run time fractions are one third each: probabilities. | Triangle board, counter on square 1. Two dice beside the exits roll "stay", "stay", "go"; counter hops. A strip of ten faces with one "go", then two "go" as line 1-2 thickens. Seeded random walk. Bar chart of time fractions converging to a dashed one-third line. | States, hops, rates, probabilities, all from a game. |
| 3 Balance | Traffic = probability times rate, e.g. one third times one. Traffic back is the same on every line: detailed balance, equilibrium. Backwards nothing looks wrong. Clockwise game: rate 2 one way round, 1 the other. Probabilities stay one third, but each line has twice the traffic clockwise: an arrow of time, energy burned. | Pairs of opposite arrows along each line with equal thickness and labels $\tfrac13\times1$. A rewind icon while the counter retraces hops. Arrows re-thicken: clockwise thick (label 2), anticlockwise thin (label 1); a yellow circular arrow; the counter mostly circulates clockwise. | Detailed balance versus a driven cycle; the arrow of time lives in unbalanced traffic. |
| 4 Entropy | Waste is the entropy production, sigma. Logarithm: log 1 = 0, positive above 1, negative below 1. Sigma adds traffic times log(this way over that way) over every line and direction. Clockwise game: log 2, about 0.7. Balanced: every log is 0, sigma = 0. Rule: balanced at every moment means no waste. | "entropy production = $\sigma$". Graph of log x with the point (1, 0) in yellow. The formula in words. Two worked rows: $3\times(\tfrac23\log2+\tfrac13\log\tfrac12)=\log2\approx0.69$ and "every $\log 1=0$, so $\sigma=0$". Green boxed rule. | What sigma is and why balanced traffic gives exactly zero. |
| 5 Hidden | Line 1-3 hidden; you see hops on the other two. Record pairs: a visible jump, the next one, and the wait (1 to 2, then 2 to 3). Backwards that is 3 to 2, then 2 to 1, same wait. No arrow of time means the same pattern of waits. Draw a waiting-time curve for each pair; in the balanced game they coincide. The test adds the mismatches into sigma hat. Whole film: backwards wrongness equals sigma; part of it: expect less. Hope: sigma hat never exceeds sigma. | Line 1-3 turns dashed grey with "hidden". A tape fills with coloured tick labels as the counter hops; a hidden hop leaves no tick. Yellow brace on the pair; the pair mirrors in time and its labels reverse. Histogram bars become the curve $e^{-2s}$; the reverse pair's curve lands exactly on it. A film strip whose frames mostly grey out; "$\hat\sigma\le\sigma$" in yellow, labelled "the hope". | How the waiting-time test works and why one expects it to underestimate. |
| 6 Schedule | Drive the machine: rates follow a repeating schedule, doors on a timer. Let t be a clock-hand angle. Door a = 1 + epsilon cos t, door b = 1 + epsilon sin t, hidden line 1. Epsilon between 0 and 1 sets the swing; use one half. a is widest at the start of a turn, b a quarter turn later. Maier and colleagues (2024) proposed the test for driven machines using only forward-schedule data and conjectured sigma hat never exceeds sigma. A true backwards film would also run the schedule backwards; this test does not. | Board with line thickness following the rates, a clock with a turning hand. Formulas in blue and gold. Plot of a(t) and b(t) over one turn with a moving yellow marker; dashed lines at 0.5 and 1.5; peak markers with a "quarter turn" brace. Citation card with the conjecture. Two rows contrasting "true backwards film: jumps and schedule reversed" with "the test: jumps reversed, schedule forwards". | The counterexample machine and the exact conjecture under test, including the forward-only subtlety. |
| 7 ZeroWaste | At every instant each door is equally wide both ways. With a third on each square, traffic in equals traffic out, so probabilities stay one third however the doors move. Every line balanced at every moment: sigma exactly 0. | Opposite arrows on each line that thicken and thin together with the doors; "1/3" labels fixed at each square; green boxed "$\sigma=0$". | The machine truly wastes nothing, by the rule from scene 4. |
| 8 TimeOrder | A hop through door a is most likely when a is wide (start of a turn); just then b is opening, so the chance of the next hop through b is rising. The reverse pair starts with a hop through b, likely a quarter turn in; then a is closing, so the chance of the next hop through a is falling. The test reports an arrow of time; there is one, but it is the schedule's (a before b), not waste. | Plot of a(t) and b(t). Blue dots along the time axis, denser where a is high; yellow tangent arrow on b at t = 0 pointing up. Gold dots, denser where b is high; yellow tangent arrow on a at a quarter turn pointing down. Caption "the schedule's arrow: a opens before b". | Intuition: event timing is biased by the schedule, so a pair and its reverse differ without any waste. |
| 9 Proof | Curves f (1 to 2, then 2 to 3) and g (3 to 2, then 2 to 1) both start at 1. Compare starting slopes; a prime = how fast a changes, angle brackets = average over a turn. Each slope has a shared "leave square 2" part that cancels. Left: average of a b' minus b a'. Insert the doors (slope of sine is cosine, of cosine is minus sine), multiply out. Pythagoras and averaging leave exactly epsilon squared. At epsilon one half: slopes -2.125 and -2.375, gap 1/4, so f starts above g. An exact fraction-based program confirms. | Numerically computed f and g at $\varepsilon=\tfrac12$ with tangent lines at 0. Equations transform term by term: $f'(0)=\langle ab'\rangle-\langle ab(a+b)\rangle$, $g'(0)=\langle ba'\rangle-\langle ab(a+b)\rangle$, the shared term highlighted then struck out, giving $\langle ab'-ba'\rangle$, then $\varepsilon\cos t+\varepsilon\sin t+\varepsilon^2(\cos^2t+\sin^2t)$, then $\varepsilon^2$. Cosine wave with equal positive and negative areas. Numbers, then the checker's PASS lines. | The decisive exact identity $(f-g)'(0)=\varepsilon^2>0$, seen as a cancellation. |
| 10 Verdict | f minus g at epsilon one half starts at 0 with slope 1/4; later g catches up and overtakes. Differences cannot cancel: a pair and its reverse are scored as (f - g) times log(f/g), positive either way. All four visible jumps are equally frequent, so this works for every pair; sigma hat = 4/3 times a standard mismatch measure that is zero only with no mismatch. Sigma hat positive and finite, sigma zero: the conjecture is false, for every epsilon in (0, 1), with smooth rates that never reach zero. | Plot of $f-g$ for $0\le s\le2.5$ with the tangent $\tfrac14 s$; the negative stretch after $s\approx1$ marked. Plot of $(f-g)\log(f/g)$ for $0\le s\le4.5$, never below the axis, with shaded area. Sign rows "$(+)\times(+)$", "$(-)\times(-)$". Green $\sigma=0$, red $\hat\sigma>0$, and the conjecture $\hat\sigma\le\sigma$ struck through. An epsilon slider sweeping (0, 1) with the readout "slope gap $\varepsilon^2>0$". | Why the whole estimate is positive, and that the bound fails generally, not at one lucky value. |
| 11 Scope | Kills one thing: the forward-only conjecture in its general form. The same paper's theorem using backwards-schedule data stands. Prior false alarms: Hartich and Godec; Harunari, Fiore and Barato used backwards-schedule data. New: an exact counterexample to this conjecture. No claim about the device turning the doors. Status: written proof, no simulation; exact computer check of the slope algebra; internal reviews of the probability steps; no formal machine proof or outside peer review. | One card at a time: red "disproved", teal "still stands", grey "known before", grey "not claimed". Then three status rows with check marks and one open mark. | Exactly what is and is not refuted, and how much to trust the result. |
| 12 Recap | Three takeaways; still unknown: a narrower safe version, and priority; end card. | Three numbered lines appear one by one. "Still unknown" with two lines. End card: paper title, "Valyu Research, 2026", folder path, "Narration uses a synthetic voice." | The whole story in three sentences, plus what is open. |

## First-time viewer review (GCSE level)

Read each clip in order, asking whether it relies on anything not yet shown.

- "Conjecture" is defined in the same sentence it first appears (scene 1).
- "Rate", "probability", "traffic", "detailed balance", "equilibrium", "entropy production",
  "logarithm", "waiting-time curve", "sigma hat" each get a picture first, then the name.
- Logarithms are beyond GCSE, so scene 4 gives only the three facts used later: log 1 = 0,
  positive above 1, negative below 1. Scene 10's no-cancellation argument uses exactly these.
- Gap found and fixed: `t` appeared in the door formulas before being defined. Scene 6 now says
  "let t be the angle of a clock hand" first.
- Gap found and fixed: a capital-sigma summation sign would clash with the lower-case sigma for
  entropy production, so formulas say "add up" in words instead.
- Derivatives: only "starting slope" and "how fast a rate is changing" (gradient intuition).
  The slopes of sine and cosine are stated, and can be seen on the plotted curves.
- Averages over a turn: shown as equal positive and negative areas of a cosine wave.
- Reverse pair: the mirror animation shows why 1-2 then 2-3 reverses to 3-2 then 2-1.
- The full KL statement is reduced to "a standard measure of mismatch that is zero only when
  nothing mismatches"; the pairwise argument before it carries the logic on its own.

## Claims and numbers ledger

All from the finding's `paper.tex`, `proof.md`, `README.md` and the replayed checker
(`python3 -B -O verification/check_short_lag.py`, six PASS lines, rerun 25 Oct 2026).

- Rates $a=1+\varepsilon\cos t$, $b=1+\varepsilon\sin t$, hidden 1, $0<\varepsilon<1$, period $2\pi$: paper Eq. (rates).
- Probabilities stay $1/3$; $\bar\sigma=0$: paper proof, first paragraph.
- Event rate $1/3$ for each visible directed jump; phase weighting by $a$ or $b$: paper proof.
- $f(0)=g(0)=1$; $f'(0)=-2-\varepsilon^2/2$; $g'(0)=-2-3\varepsilon^2/2$; $(f-g)'(0)=\varepsilon^2$: checker.
  At $\varepsilon=1/2$: $-2.125$, $-2.375$, gap $0.25$.
- $\hat\sigma=\tfrac43D_{\mathrm{KL}}(P\Vert Q)>0$ and finite: paper Eq. (kl) and finiteness paragraph.
- Pairwise form: a pair and its reverse contribute $\bar n\int(f-g)\log(f/g)\,ds\ge0$; self-reverse
  pairs contribute 0: `proof.md` ("reversal pairs contribute a positive multiple of (f-g)log(f/g)").
- Plot of $f-g$ at $\varepsilon=1/2$: periodic quadrature as in `plot_counterexample.py`
  (illustration only, as in the paper's figure). Computed here: maximum about 0.029 near
  $s\approx0.29$; sign changes near $s\approx0.96$ and $s\approx6.3$, so the narration says
  "g catches up, and overtakes" (an earlier draft's "briefly" was wrong and was removed). The
  pair score $(f-g)\log(f/g)$ peaks near $s\approx2.2$, so most of it comes from long waits;
  the score plot therefore runs to $s=4.5$ and is shown without a numerical total.
- Clockwise teaching game (rates 2 and 1): $\sigma=3\times(\tfrac23\log2+\tfrac13\log\tfrac12)=\log2\approx0.693$
  from the paper's Eq. (ep) definition. Illustrative, not from the paper.
- Balanced teaching game: $\Psi_{12\to23}(s)=\Psi_{32\to21}(s)=e^{-2s}$ (exit rate 2, one exit to the
  target). Illustrative.
- Scope: reversed-protocol theorem (published Eq. 16) unaffected; prior false positives by Hartich
  and Godec; reversed-protocol data by Harunari, Fiore and Barato; no claim about the controller's
  cost; no Lean formalization; no external peer review: paper Section 3, README, readiness.md.
- Background (not from the paper): with the whole trajectory observed, the forward/backward
  distinguishability equals the entropy production (with the protocol also reversed when driven),
  and partial observation can only lower it. Parrondo, Van den Broeck and Kawai, New J. Phys. 11,
  073008 (2009); Roldán and Parrondo, Phys. Rev. E 85, 031129 (2012), retrieved via Valyu search,
  25 Oct 2026.
